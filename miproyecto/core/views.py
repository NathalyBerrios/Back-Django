import json, os
from django.shortcuts import render

def resumen(request):
    registros = []
    # Evita que la página se caiga si el JSON aún no existe
    if os.path.exists("datos.json"):
        with open("datos.json") as f:
            registros = json.load(f)
            
    return render(request, "resumen.html", {"registros": registros})