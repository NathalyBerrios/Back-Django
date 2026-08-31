import json
import os
from django.shortcuts import render

# 1. Importamos la regla de negocio que encapsulamos en solucion.py
from solucion import procesar_admision 

def resumen(request):
    # 2. Evaluamos si llegan datos a la vista (por ejemplo, al enviar un formulario web)
    if request.method == "POST":
        # Capturamos los datos del formulario de forma segura
        nombre = request.POST.get("nombre", "Sin nombre")
        peso = int(request.POST.get("peso", 0))
        mascotas_ingresadas = int(request.POST.get("mascotas_ingresadas", 0))
        
        # 3. ¡AQUÍ ESTÁ LA MAGIA! Reutilizamos tu regla pasándole los datos
        procesar_admision(mascotas_ingresadas, nombre, peso)

    # 4. Leemos los registros para enviarlos a la plantilla (como ya lo hacías)
    registros = []
    
    if os.path.exists("datos.json"):
        with open("datos.json", "r", encoding="utf-8") as f:
            try:
                registros = json.load(f)
            except json.JSONDecodeError:
                # Evita que se caiga si el archivo existe pero está vacío
                registros = []
                
    return render(request, "resumen.html", {"registros": registros})