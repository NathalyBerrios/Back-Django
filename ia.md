# Uso de IA en la Evaluación

1. **Que herramienta use**
   Utilice IA para migrar el proyecto de la EV1 proyecto desde un archivo JSON a una base de datos SQLite, para implementar el sistema de roles y seguridad.

2. **Consulta que hice:**
   Cómo llevar mi proyecto de admisión veterinaria (JSON) a SQLite con Django, manteniendo mi regla de decisión de solucion.py sin reescribirla, y agregando login con 3 roles.

3. **Qué estaba mal y cómo lo corregí yo:**
   Revisé que la separación de evaluar_admision() mantuviera exactamente el mismo if/elif de mi ES1, sin reescribir la lógica.
   Implementar el script crear_usuarios.py usando decouple para extraer las contraseñas desde mi archivo .env, corrigiendo así el riesgo de dejar claves reales expuestas en el código fuente.