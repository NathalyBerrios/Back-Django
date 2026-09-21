# Sistema de admisión veterinaria municipal

## Instrucciones de instalación
1. Clonar el repositorio.
2. Crear y activar el entorno virtual: `python -m venv .venv` y `.venv\Scripts\activate`
3. Instalar dependencias: `pip install -r requirements.txt`
4. Renombrar el archivo `.env.example` a `.env` y rellenar TODAS las contraseñas (`PASS_ADMIN`, `PASS_NORMAL`, `PASS_VIEWER`).
5. Ejecutar migraciones: `python manage.py migrate`

## Carga de datos y usuarios
Los scripts iniciales se deben correr inyectándolos en el shell de Django:
* Para cargar usuarios y roles: `python manage.py shell < crear_usuarios.py` (En PowerShell usar: `cat crear_usuarios.py | python manage.py shell`)
* Para migrar datos antiguos: `python manage.py shell < cargar_datos.py` (En PowerShell usar: `cat cargar_datos.py | python manage.py shell`)
