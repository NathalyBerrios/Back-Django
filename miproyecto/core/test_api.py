
from django.contrib.auth.models import Group, User
from rest_framework.test import APITestCase

from .models import Registro

URL = "/api/registros/"


class ApiBase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Los mismos tres roles de la ES2
        cls.usuarios = {}
        for rol in ("admin", "normal", "viewer"):
            grupo = Group.objects.create(name=rol)
            usuario = User.objects.create_user(f"u_{rol}", password="clave123")
            usuario.groups.add(grupo)
            cls.usuarios[rol] = usuario

    def como(self, rol):
        """Entra a la API con el JWT real (pidiéndolo a /api/token/)."""
        respuesta = self.client.post(
            "/api/token/", {"username": f"u_{rol}", "password": "clave123"}
        )
        self.assertEqual(respuesta.status_code, 200)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {respuesta.data['access']}"
        )


class AutenticacionTests(ApiBase):
    def test_sin_token_responde_401(self):
        self.assertEqual(self.client.get(URL).status_code, 401)

    def test_token_invalido_responde_401(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer falso")
        self.assertEqual(self.client.get(URL).status_code, 401)

    def test_credenciales_malas_no_entregan_token(self):
        r = self.client.post("/api/token/", {"username": "u_admin", "password": "mala"})
        self.assertEqual(r.status_code, 401)

    def test_refresh_entrega_un_access_nuevo(self):
        r = self.client.post("/api/token/", {"username": "u_admin", "password": "clave123"})
        r2 = self.client.post("/api/token/refresh/", {"refresh": r.data["refresh"]})
        self.assertEqual(r2.status_code, 200)
        self.assertIn("access", r2.data)

    def test_documentacion_exige_sesion(self):
        self.assertIn(self.client.get("/api/docs/").status_code, (401, 403))
        self.client.login(username="u_viewer", password="clave123")
        self.assertEqual(self.client.get("/api/docs/").status_code, 200)


class PermisosPorRolTests(ApiBase):
    def test_viewer_puede_leer(self):
        self.como("viewer")
        self.assertEqual(self.client.get(URL).status_code, 200)

    def test_viewer_no_puede_crear_403(self):
        self.como("viewer")
        r = self.client.post(URL, {"nombre": "Ana", "peso": 5}, format="json")
        self.assertEqual(r.status_code, 403)

    def test_normal_puede_crear_pero_no_borrar(self):
        self.como("normal")
        r = self.client.post(URL, {"nombre": "Ana", "peso": 5}, format="json")
        self.assertEqual(r.status_code, 201)
        r = self.client.delete(f"{URL}{r.data['id']}/")
        self.assertEqual(r.status_code, 403)

    def test_normal_no_puede_editar_403(self):
        reg = Registro.objects.create(nombre="A", peso=5, estado="Aceptado", motivo="x")
        self.como("normal")
        r = self.client.patch(f"{URL}{reg.pk}/", {"peso": 6}, format="json")
        self.assertEqual(r.status_code, 403)

    def test_admin_puede_todo(self):
        self.como("admin")
        r = self.client.post(URL, {"nombre": "Ana", "peso": 5}, format="json")
        self.assertEqual(r.status_code, 201)
        pk = r.data["id"]
        self.assertEqual(self.client.put(f"{URL}{pk}/", {"nombre": "Ana2", "peso": 6}, format="json").status_code, 200)
        self.assertEqual(self.client.patch(f"{URL}{pk}/", {"peso": 7}, format="json").status_code, 200)
        self.assertEqual(self.client.delete(f"{URL}{pk}/").status_code, 204)


class CrudYReglaTests(ApiBase):
    def setUp(self):
        self.como("admin")

    def test_crear_aplica_la_regla_de_decision(self):
        r = self.client.post(URL, {"nombre": "Firu", "peso": 5}, format="json")
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.data["estado"], "Aceptado")

    def test_peso_mayor_a_15_queda_rechazado(self):
        r = self.client.post(URL, {"nombre": "Grande", "peso": 30}, format="json")
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.data["estado"], "Rechazado")

    def test_peso_cero_queda_dato_invalido(self):
        r = self.client.post(URL, {"nombre": "Cero", "peso": 0}, format="json")
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.data["estado"], "Dato Inválido")

    def test_cliente_no_puede_imponer_el_estado(self):
        r = self.client.post(
            URL, {"nombre": "Grande", "peso": 30, "estado": "Aceptado"}, format="json"
        )
        self.assertEqual(r.data["estado"], "Rechazado")

    def test_no_expone_campos_internos(self):
        r = self.client.post(URL, {"nombre": "Ana", "peso": 5}, format="json")
        self.assertNotIn("eliminado", r.data)
        self.assertNotIn("fecha_eliminacion", r.data)

    def test_se_acaban_los_cupos_del_dia(self):
        for i in range(10):
            self.assertEqual(
                self.client.post(URL, {"nombre": f"m{i}", "peso": 5}, format="json").data["estado"],
                "Aceptado",
            )
        r = self.client.post(URL, {"nombre": "once", "peso": 5}, format="json")
        self.assertEqual(r.data["estado"], "Rechazado")
        self.assertIn("cupos", r.data["motivo"])

    def test_aceptados_de_dias_anteriores_no_bloquean_hoy(self):
        from datetime import timedelta
        from django.utils import timezone

        ayer = timezone.now() - timedelta(days=2)
        for i in range(12):
            Registro.objects.create(nombre=f"v{i}", peso=5, estado="Aceptado", motivo="x", fecha=ayer)
        r = self.client.post(URL, {"nombre": "hoy", "peso": 5}, format="json")
        self.assertEqual(r.data["estado"], "Aceptado")

    def test_patch_recalcula_estado(self):
        pk = self.client.post(URL, {"nombre": "Ana", "peso": 5}, format="json").data["id"]
        r = self.client.patch(f"{URL}{pk}/", {"peso": 40}, format="json")
        self.assertEqual(r.data["estado"], "Rechazado")

    def test_patch_sin_peso_conserva_el_peso(self):
        pk = self.client.post(URL, {"nombre": "Ana", "peso": 5}, format="json").data["id"]
        r = self.client.patch(f"{URL}{pk}/", {"nombre": "Ana B"}, format="json")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["peso"], 5)
        self.assertEqual(r.data["estado"], "Aceptado")

    def test_delete_es_logico_y_devuelve_204(self):
        pk = self.client.post(URL, {"nombre": "Ana", "peso": 5}, format="json").data["id"]
        self.assertEqual(self.client.delete(f"{URL}{pk}/").status_code, 204)
        self.assertTrue(Registro.objects.filter(pk=pk, eliminado=True).exists())
        self.assertEqual(self.client.get(f"{URL}{pk}/").status_code, 404)
        self.assertEqual(self.client.get(URL).data["count"], 0)

    def test_endpoint_cupos(self):
        self.client.post(URL, {"nombre": "Ana", "peso": 5}, format="json")
        r = self.client.get(f"{URL}cupos/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data, {"cupos_totales": 10, "ocupados_hoy": 1, "disponibles": 9})


class ErroresTests(ApiBase):
    def setUp(self):
        self.como("admin")

    def test_nombre_en_blanco_400_con_mensaje(self):
        r = self.client.post(URL, {"nombre": "   ", "peso": 5}, format="json")
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.data["nombre"][0], "El nombre no puede quedar en blanco.")

    def test_peso_no_numerico_400(self):
        r = self.client.post(URL, {"nombre": "Ana", "peso": "abc"}, format="json")
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.data["peso"][0], "El peso debe ser un número entero.")

    def test_falta_el_peso_400(self):
        r = self.client.post(URL, {"nombre": "Ana"}, format="json")
        self.assertEqual(r.status_code, 400)

    def test_id_inexistente_404(self):
        self.assertEqual(self.client.get(f"{URL}9999/").status_code, 404)
        self.assertEqual(self.client.delete(f"{URL}9999/").status_code, 404)


class PaginacionTests(ApiBase):
    def test_lista_paginada_de_a_10(self):
        for i in range(12):
            Registro.objects.create(nombre=f"r{i}", peso=5, estado="Rechazado", motivo="x")
        self.como("viewer")
        r = self.client.get(URL)
        self.assertEqual(r.data["count"], 12)
        self.assertEqual(len(r.data["results"]), 10)
        self.assertIsNotNone(r.data["next"])
        self.assertEqual(len(self.client.get(URL + "?page=2").data["results"]), 2)
