# Uso de Inteligencia Artificial (Evaluación 2)

## 1. Herramientas utilizadas
Utilicé Google Gemini y Claude para asistir en la migración de JSON a SQLite, la implementación de vistas CRUD y el sistema de roles de seguridad.
Para la EVA3 utilicé Claude para adaptar el ejemplo de la pauta a mi modelo de registro y generar el código de la API.

## 2. Detalle de Consultas, Respuestas y Mis Correcciones

Consulta: "Necesito el código para el archivo views.py para hacer un CRUD con mi modelo Registro usando Django. Tengo que asegurar que mi regla de negocio en solucion.py no se vuelva a escribir."
Respuesta de la IA: Me entregó la estructura de las 4 vistas web e incluyó la importación `from solucion import evaluar_admision`, aplicándola directamente en las vistas `crear` y `editar`.
Mi corrección: Revisé que esta separación mantuviera exactamente el mismo bloque if/elif de mi entrega anterior (ES1), comprobando que la IA no alterara ni reescribiera mi lógica original.

Consulta: "Cómo protejo mis vistas para que solo ciertos usuarios puedan entrar, pero sin usar solo if en el html."
Respuesta de la IA: Me indicó que la seguridad ocultando botones en la plantilla no es suficiente y me propuso crear un archivo `decorators.py` con una función `@requiere_rol`.
Mi corrección: Entendí la diferencia entre interfaz visual y seguridad real. Implementé el decorador para validar los permisos a nivel de servidor y rechazar las peticiones no autorizadas directamente en el backend.

Consulta: "¿Cómo creo los roles y usuarios automáticamente sin guardar las contraseñas en mi código fuente?"
Respuesta de la IA: Me recomendó utilizar un archivo `.env` para aislar los datos sensibles.
Mi corrección: Implementé el script `crear_usuarios.py` usando la librería `decouple` para extraer las contraseñas desde el `.env`, eliminando así el riesgo de exponer las claves reales en el código.

Consulta: "Cómo cambiar el historial en github por la exposición del secret_key."
Respuesta de la IA: Me explicó que alterar el historial de Git es riesgoso y que el estándar de la industria es invalidar la clave expuesta rotándola por una nueva localmente.
Mi corrección: Entendí el proceso y procedí a cambiar el valor de la clave secreta directamente en mi archivo `.env` local para que la antigua quedara inutilizada.

Consulta: "Necesito revisar mi repositorio de la ES2 contra los comentarios del profesor"
Respuesta de la IA: Confirmó que el filtro por fecha en los cupos ya estaba aplicado y encontró que cargar_datos.py asignaba peso 10 por defecto a los registros sin peso, en vez de 0.
Mi corrección: Cambié el peso por defecto a 0 para que queden como Dato Inválido, moví el conteo de cupos a core/servicios.py (un solo lugar) y cambié la zona horaria a America/Santiago.

Consulta: "Necesito ayuda para convertir mi proyecto de la ES2 en una API con Django REST Framework, cumpliendo la pauta de la ES3"
Respuesta de la IA: Me entregó serializers.py, api_views.py, permissions.py, la configuración de settings y las rutas. 
Mi corrección: Adapté los nombres a mi modelo y armé los permisos con mis grupos admin/normal/viewer. Comprobé con pruebas que un viewer recibe 403 al crear y un normal recibe 403 al borrar.

Consulta de seguridad: "¿Cómo autentico la API y qué permisos dejo por defecto?"
Respuesta de la IA: Propuso JWT con SimpleJWT y IsAuthenticated como permiso por defecto.
Mi corrección: Verifiqué que GET sin token responde 401 y que mandar "estado": "Aceptado" en el JSON no cambia el resultado (ver pruebas/salida_pruebas.txt).