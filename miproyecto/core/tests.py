from django.contrib.auth.models import Group, User
from django.test import TestCase

from solucion import evaluar_admision
from .models import Registro


class EvaluarAdmisionTests(TestCase):
    
    def test_peso_cero_o_negativo_es_dato_invalido(self):
        estado, motivo = evaluar_admision(mascotas_ingresadas=0, peso=0)
        self.assertEqual(estado, "Dato Inválido")

    def test_peso_mayor_a_15_es_rechazado(self):
        estado, motivo = evaluar_admision(mascotas_ingresadas=0, peso=20)
        self.assertEqual(estado, "Rechazado")
        self.assertIn("15 kilos", motivo)

    def test_sin_cupos_es_rechazado(self):
        # CUPOS_TOTALES es 10: si ya entraron 10, no debe quedar cupo
        estado, motivo = evaluar_admision(mascotas_ingresadas=10, peso=5)
        self.assertEqual(estado, "Rechazado")
        self.assertIn("cupos", motivo)

    def test_peso_valido_y_con_cupo_es_aceptado(self):
        estado, motivo = evaluar_admision(mascotas_ingresadas=0, peso=5)
        self.assertEqual(estado, "Aceptado")


class RegistroModelTests(TestCase):
    def test_soft_delete_no_borra_la_fila(self):
        reg = Registro.objects.create(
            nombre="Firulais", peso=5, estado="Aceptado", motivo="Ingresado con éxito a la jornada."
        )
        reg.soft_delete()
        # Sigue existiendo en la base, solo queda marcado como eliminado
        self.assertTrue(Registro.objects.filter(pk=reg.pk).exists())
        reg.refresh_from_db()
        self.assertTrue(reg.eliminado)
        self.assertIsNotNone(reg.fecha_eliminacion)


class PermisosVistasTests(TestCase):
    """
    Formaliza lo mismo que se probó a mano escribiendo las URLs en el
    navegador: cada rol solo puede llegar a donde le corresponde, aunque
    escriba la dirección directamente.
    """

    @classmethod
    def setUpTestData(cls):
        grupo_admin = Group.objects.create(name="admin")
        grupo_normal = Group.objects.create(name="normal")
        grupo_viewer = Group.objects.create(name="viewer")

        cls.admin_user = User.objects.create_user("test_admin", password="clave123")
        cls.admin_user.groups.add(grupo_admin)

        cls.normal_user = User.objects.create_user("test_normal", password="clave123")
        cls.normal_user.groups.add(grupo_normal)

        cls.viewer_user = User.objects.create_user("test_viewer", password="clave123")
        cls.viewer_user.groups.add(grupo_viewer)

        cls.registro = Registro.objects.create(
            nombre="Firulais", peso=5, estado="Aceptado", motivo="Ingresado con éxito a la jornada."
        )

    def test_anonimo_es_redirigido_a_login(self):
        respuesta = self.client.get("/")
        self.assertRedirects(respuesta, "/login/?next=/")

    def test_viewer_no_puede_crear(self):
        self.client.login(username="test_viewer", password="clave123")
        respuesta = self.client.get("/registros/crear/")
        self.assertRedirects(respuesta, "/")

    def test_viewer_no_puede_editar_escribiendo_la_url_a_mano(self):
        self.client.login(username="test_viewer", password="clave123")
        respuesta = self.client.get(f"/registros/{self.registro.pk}/editar/")
        self.assertRedirects(respuesta, "/")

    def test_viewer_no_puede_eliminar_escribiendo_la_url_a_mano(self):
        self.client.login(username="test_viewer", password="clave123")
        respuesta = self.client.get(f"/registros/{self.registro.pk}/eliminar/")
        self.assertRedirects(respuesta, "/")

    def test_normal_puede_crear(self):
        self.client.login(username="test_normal", password="clave123")
        respuesta = self.client.get("/registros/crear/")
        self.assertEqual(respuesta.status_code, 200)

    def test_normal_no_puede_editar_escribiendo_la_url_a_mano(self):
        self.client.login(username="test_normal", password="clave123")
        respuesta = self.client.get(f"/registros/{self.registro.pk}/editar/")
        self.assertRedirects(respuesta, "/")

    def test_admin_puede_editar(self):
        self.client.login(username="test_admin", password="clave123")
        respuesta = self.client.get(f"/registros/{self.registro.pk}/editar/")
        self.assertEqual(respuesta.status_code, 200)

    def test_admin_puede_eliminar(self):
        self.client.login(username="test_admin", password="clave123")
        respuesta = self.client.post(f"/registros/{self.registro.pk}/eliminar/")
        self.registro.refresh_from_db()
        self.assertTrue(self.registro.eliminado)


class CrudFormularioTests(TestCase):
    """Valida que crear/editar reaccionen bien a datos buenos y malos."""

    @classmethod
    def setUpTestData(cls):
        grupo_admin = Group.objects.create(name="admin")
        cls.admin_user = User.objects.create_user("test_admin2", password="clave123")
        cls.admin_user.groups.add(grupo_admin)

    def setUp(self):
        self.client.login(username="test_admin2", password="clave123")

    def test_crear_con_peso_valido_guarda_el_registro(self):
        respuesta = self.client.post(
            "/registros/crear/", {"nombre": "Michi", "peso": "4"}
        )
        self.assertRedirects(respuesta, "/")
        self.assertTrue(Registro.objects.filter(nombre="Michi").exists())

    def test_crear_con_peso_no_numerico_no_guarda_y_muestra_error(self):
        respuesta = self.client.post(
            "/registros/crear/", {"nombre": "Michi", "peso": "no-es-numero"}
        )
        self.assertEqual(respuesta.status_code, 200)  # se queda en el formulario
        self.assertFalse(Registro.objects.filter(nombre="Michi").exists())
        self.assertContains(respuesta, "número entero")

    def test_crear_con_nombre_vacio_no_guarda(self):
        respuesta = self.client.post("/registros/crear/", {"nombre": "  ", "peso": "4"})
        self.assertEqual(respuesta.status_code, 200)
        self.assertFalse(Registro.objects.filter(peso=4, nombre="").exists())

    def test_editar_recalcula_estado_si_cambia_el_peso(self):
        reg = Registro.objects.create(
            nombre="Toby", peso=5, estado="Aceptado", motivo="Ingresado con éxito a la jornada."
        )
        respuesta = self.client.post(
            f"/registros/{reg.pk}/editar/", {"nombre": "Toby", "peso": "20"}
        )
        self.assertRedirects(respuesta, "/")
        reg.refresh_from_db()
        self.assertEqual(reg.estado, "Rechazado")  # 20 kilos supera el máximo
