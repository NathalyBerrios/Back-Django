# Sistema de admisión veterinaria municipal

Aplicación Django con dos interfaces sobre los mismos modelos y la misma base de datos (SQLite):

- **Pantallas HTML (ES2):** listado, crear, editar y eliminar, con login por sesión y 3 roles.
- **API REST (ES3):** bajo `/api/`, con autenticación JWT y permisos por rol.

## Instrucciones de instalación

1. Clonar el repositorio: https://github.com/NathalyBerrios/Back-Django.git
2. Crear y activar el entorno virtual:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate      # Windows
   source .venv/bin/activate   # Linux / macOS
   ```
3. Instalar dependencias: `pip install -r requirements.txt`
4. Entrar a la carpeta del proyecto: `cd miproyecto`
5. Renombrar `.env.example` a `.env` y rellenar **todas** las contraseñas (`PASS_ADMIN`, `PASS_NORMAL`, `PASS_VIEWER`).
6. Ejecutar migraciones: `python manage.py migrate`
7. Levantar el servidor: `python manage.py runserver`

## Carga de datos y usuarios

Los scripts iniciales se corren inyectándolos en el shell de Django:

- Usuarios y roles: `python manage.py shell < crear_usuarios.py` (PowerShell: `cat crear_usuarios.py | python manage.py shell`)
- Datos antiguos: `python manage.py shell < cargar_datos.py` (PowerShell: `cat cargar_datos.py | python manage.py shell`)

Los registros migrados desde `datos.json` no traen peso, así que entran con peso `0` y quedan como **Dato Inválido**: no consumen cupo.

## Reglas de negocio

- Peso ≤ 0 → `Dato Inválido`. Peso > 15 kg → `Rechazado`. Sin cupos → `Rechazado`. En otro caso → `Aceptado`.
- Hay 10 cupos **por día**: solo cuentan los `Aceptado` de hoy que no estén eliminados.
- Zona horaria del proyecto: `America/Santiago` (afecta qué cuenta como "hoy").
- El borrado es lógico (`eliminado=True`): la fila no se borra, tanto en las pantallas como en la API.

---

# API REST (ES3)

## Autenticación (JWT)

1. Pedir un token con un usuario de la EV2:

   ```bash
   curl -X POST -H "Content-Type: application/json" \
        -d '{"username": "admin1", "password": "TU_CLAVE"}' \
        http://127.0.0.1:8000/api/token/
   # {"refresh": "eyJhbGci...", "access": "eyJhbGci..."}
   ```

2. Mandar el `access` en la cabecera `Authorization` de toda otra petición:

   ```bash
   curl -H "Authorization: Bearer eyJhbGci..." http://127.0.0.1:8000/api/registros/
   ```

3. El `access` dura 15 minutos. Para renovarlo sin volver a mandar la contraseña: `POST /api/token/refresh/` con `{"refresh": "..."}` (el `refresh` dura 1 día).

> En Windows PowerShell usar `curl.exe` (no `curl`, que es otro comando), o probar con Postman / Thunder Client.

## Endpoints

| Método | URL | Qué hace | Quién puede | Código de éxito |
|---|---|---|---|---|
| POST | `/api/token/` | Entrega `access` y `refresh` | cualquier usuario válido | 200 |
| POST | `/api/token/refresh/` | Entrega un `access` nuevo | quien tenga un `refresh` válido | 200 |
| GET | `/api/registros/` | Lista registros (paginada, 10 por página, `?page=2`) | viewer, normal, admin | 200 |
| POST | `/api/registros/` | Crea un registro; el estado lo decide la regla de negocio | normal, admin | 201 |
| GET | `/api/registros/{id}/` | Muestra un registro | viewer, normal, admin | 200 |
| PUT | `/api/registros/{id}/` | Reemplaza nombre y peso, recalcula estado | admin | 200 |
| PATCH | `/api/registros/{id}/` | Cambia un campo suelto, recalcula estado | admin | 200 |
| DELETE | `/api/registros/{id}/` | Borrado lógico | admin | 204 |
| GET | `/api/registros/cupos/` | Cupos totales, ocupados hoy y disponibles | viewer, normal, admin | 200 |

Documentación interactiva (Swagger): inicia sesión en `/login/` y abre **`/api/docs/`**. Dentro, botón **Authorize** y pegar el `access`.

## Códigos de error

| Código | Cuándo ocurre | Ejemplo de respuesta |
|---|---|---|
| 400 | JSON mal formado o datos inválidos (nombre en blanco, peso que no es número entero) | `{"nombre": ["El nombre no puede quedar en blanco."]}` |
| 401 | No se envió token, o el token es inválido o expiró | `{"detail": "Authentication credentials were not provided."}` |
| 403 | El token es válido, pero el rol no permite esa acción (ej. un `viewer` creando un registro) | `{"detail": "You do not have permission to perform this action."}` |
| 404 | El `id` no existe, o el registro fue eliminado | `{"detail": "No Registro matches the given query."}` |

## Justificación de la configuración

- **JWT y no sesión ni token simple de DRF:** quien consume la API es un programa sin navegador, así que la cookie de sesión de la ES2 no sirve. Se usó JWT (`djangorestframework-simplejwt`) en vez del token simple porque el token simple nunca expira; con JWT el `access` caduca a los 15 minutos (si se filtra, sirve poco tiempo) y el `refresh` permite renovarlo sin volver a mandar la contraseña.
- **`DEFAULT_PERMISSION_CLASSES = IsAuthenticated`:** el default seguro del proyecto es que todo endpoint pida autenticación; nunca se usa `AllowAny`.
- **Permisos por rol (`core/permissions.py`):** se reutilizan los grupos de la ES2 (viewer lee; normal lee y crea; admin puede todo), en vez de `is_staff`, porque los tres usuarios de `crear_usuarios.py` tienen `is_staff=True` para entrar a `/admin/`, así que ese campo no distinguiría entre roles.
- **`PAGE_SIZE = 10`:** coincide con los 10 cupos diarios del negocio, así que un día completo de admisiones cabe en una sola página de la lista.
- **Serializer con campos enumerados (nunca `"__all__"`):** `estado`, `motivo` y `fecha` son de solo lectura porque los calcula la regla de decisión, no el cliente; `eliminado` no se expone.
- **Un solo estilo de vistas:** solo `ModelViewSet` + router (no se mezclan `APIView` ni `generics`), para mantener el código uniforme y explicable en la defensa.
- **Peso ≤ 0 no es un 400:** en la regla de negocio (ES1) es un resultado válido, `Dato Inválido`, y se guarda igual que en las pantallas HTML. El 400 se reserva para datos mal formados (nombre en blanco, peso no numérico).

## Pruebas

- **Automáticas:** `python manage.py test` (incluye `core/test_api.py`, con casos de autenticación, permisos, CRUD, errores y paginación).
- **En cliente HTTP:** capturas en `pruebas/`, descritas en `pruebas/pruebas.txt`. Cubren 401 (sin token), 200 (token y lectura), 201 (crear), 204 (borrar), 400 (datos inválidos), 403 (rol sin permiso), 404 (id inexistente) y paginación.
