import json

from core.models import Registro

with open("datos.json", encoding="utf-8") as f:
    datos_viejos = json.load(f)

creados = 0
for r in datos_viejos:
    nombre = r.get("nombre", "Sin nombre")
    if Registro.objects.filter(nombre=nombre).exists():
        continue  # evita duplicar si el script se corre dos veces
    Registro.objects.create(
        nombre=nombre,
        peso=r.get("peso", 10),
        estado=r.get("estado", "Aceptado"),
        motivo=r.get("motivo", "Migrado desde datos.json (registro antiguo, sin motivo)."),
    )
    creados += 1

print(f"{creados} registro(s) migrado(s) desde datos.json.")