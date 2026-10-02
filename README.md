# Sistema de admisión veterinaria municipal
Aplicación Django con dos interfaces sobre los mismos modelos y la misma base de datos (SQLite):

- **Pantallas HTML:** listado, crear, editar y eliminar, con login por sesión y 3 roles.
- **API REST:** bajo `/api/`, con autenticación JWT y permisos por rol.
## Instrucciones de instalación
1. Clonar el repositorio.
2. Crear y activar el entorno virtual: `python -m venv .venv` y `.venv\Scripts\activate`
3. Instalar dependencias: `pip install -r requirements.txt`
4. Renombrar el archivo `.env.example` a `.env` y rellenar TODAS las contraseñas (`PASS_ADMIN`, `PASS_NORMAL`, `PASS_VIEWER`).
5. Ejecutar migraciones: `python manage.py migrate`.
6. Ejecutar migraciones: `python manage.py migrate`.
7. Levantar el servidor: `python manage.py runserver`.

## Carga de datos y usuarios
Los scripts iniciales se deben correr inyectándolos en el shell de Django:
* Para cargar usuarios y roles: `python manage.py shell < crear_usuarios.py` (En PowerShell usar: `cat crear_usuarios.py | python manage.py shell`)
* Para migrar datos antiguos: `python manage.py shell < cargar_datos.py` (En PowerShell usar: `cat cargar_datos.py | python manage.py shell`)

# API de Sistema de Admisión Veterinaria - Evaluación 3

Esta es una API RESTful desarrollada con Django y Django Rest Framework para gestionar el registro y la admisión de mascotas en una clínica veterinaria. Incluye autenticación mediante tokens JWT, control de permisos por roles y documentación automática con Swagger.

## Características Principales y Lógica de Negocio
* **CRUD de Registros:** Permite listar, crear, modificar y eliminar registros de mascotas (`api_views.py`).
* **Regla de Negocio (Admisión Automática):** Al crear o actualizar un registro, la API evalúa automáticamente el peso de la mascota. Si el peso es menor o igual a 15 kilos, el estado es "Aceptado". Si excede los 15 kilos, el estado cambia a "Rechazado" y se genera automáticamente un motivo detallando el exceso de peso.
* **Autenticación:** Implementación de `djangorestframework-simplejwt` para proteger los endpoints. Se requiere un token Bearer válido para acceder a las rutas.
* **Seguridad y Variables de Entorno:** Uso de `python-decouple` para proteger credenciales y el `SECRET_KEY` en el archivo `.env`.

## Roles de Usuario y Permisos (`PermisoPorRol`)
El sistema utiliza un permiso personalizado para restringir acciones según el grupo del usuario:
* **Admin (`grupo_admin`):** Acceso total. Puede ver, crear, modificar y eliminar registros.
* **Normal (`grupo_normal`):** Acceso intermedio. Puede ver y crear registros, pero no puede modificarlos ni eliminarlos.
* **Viewer (`grupo_viewer`):** Acceso de solo lectura. Únicamente puede listar o ver los registros.

## Endpoints Principales

### Autenticación
* `POST /api/token/` - Genera el token de acceso (`access`) y de refresco enviando usuario y contraseña.
* `POST /api/token/refresh/` - Renueva el token de acceso caducado.

### API de Registros (Requieren Token Bearer)
* `GET /api/registros/` - Lista todos los registros paginados.
* `POST /api/registros/` - Crea un nuevo registro evaluando la regla de negocio.
* `GET /api/registros/<id>/` - Muestra el detalle de un registro específico.
* `PUT/PATCH /api/registros/<id>/` - Actualiza un registro existente.
* `DELETE /api/registros/<id>/` - Elimina un registro (solo Admin).

### Documentación
* `GET /api/schema/swagger-ui/` - Interfaz gráfica de Swagger generada con `drf-spectacular` para explorar y probar la API desde el navegador.

## Requisitos Previos e Instalación

1. **Clonar el proyecto** y abrir la carpeta en la terminal.
2. **Crear y activar el entorno virtual:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # En Windows