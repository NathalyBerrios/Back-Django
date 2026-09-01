# Uso de IA en la Evaluación

1. **Que herramienta use**
   Utilicé Gemini para entender los requerimientos de la evaluación, estructurar el proyecto en Django y guiarme en la sintaxis de Python.
   También utilice la IA para corregir los comentarios entregados en la retroalimentación convertir solucion.py en una función reutilizable, agregar el peso y motivo al JSON, y dejar la ruta principal en /.

2. **Consulta que hice:**
   Evaluar la lógica del codigo que me entregó un código donde el orden de las variables no era tan eficiente. 
   Pregunte como debia quedar la estructura del codigo para estos cambios y obtuve la estructura de cómo debía verse una función en solucion.py, cómo importarla en views.py, y cómo ajustar el archivo urls.py.

3. **Qué estaba mal y cómo lo corregí yo:**
   La estructura inicial propuesta por la IA leía todas las caracteristicas del caso antes de revisar si había cupos disponibles, lo cual era poco eficiente para la vida real. Corregí esto indicándole a la IA que cambiara el orden de los input iniciales para validar la capacidad del recinto primero. 
   El script original usaba input() para pedir los datos por consola. Al integrarlo con Django, elimine esos input() directos y encapsular todo en la función procesar_admision. Verifiqué que la ruta en urls.py quedara exactamente como path path('', resumen, name='resumen').