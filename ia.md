# Uso de IA en la Evaluación

1. **Que herramienta use**
   Utilice IA para migrar el proyecto de la EV1 proyecto desde un archivo JSON a una base de datos SQLite, para implementar el sistema de roles y seguridad. Para esto me ayude de gemini y claude.

2. **Consulta que hice:**
   Cómo llevar mi proyecto de admisión veterinaria (JSON) a SQLite con Django, manteniendo mi regla de decisión de solucion.py sin reescribirla, y agregando login con 3 roles.
   Cómo protejo mis vistas para que solo ciertos usuarios puedan entrar, pero sin usar solo if en el html.
   Cómo cambiar el historial en github por la exposición del secret_key.

3. **Qué estaba mal y cómo lo corregí yo:**
   Revisé que la separación de evaluar_admision() mantuviera exactamente el mismo if/elif de mi ES1, sin reescribir la lógica.
   Implementar el script crear_usuarios.py usando decouple para extraer las contraseñas desde mi archivo .env, corrigiendo así el riesgo de dejar claves reales expuestas en el código fuente.
   La IA me indicó que la seguridad en la plantilla no es suficiente y me propuso crear un archivo `decorators.py` con una función `@requiere_rol` para validar los permisos a nivel de servidor.
   Entendí el error y cual es el proceso y cambie en el archivo .env el valor de la clave para que no quede expuesto en el historial.