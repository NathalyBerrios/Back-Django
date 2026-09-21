import json

from django.utils import timezone

from core.models import Registro
from solucion import evaluar_admision

with open("datos.json", encoding="utf-8") as f:
    datos_viejos = json.load(f)

creados = 0
for r in datos_viejos:
    nombre = r.get("nombre", "Sin nombre")
    if Registro.objects.filter(nombre=nombre).exists():
        continue  # evita duplicar si el script se corre dos veces

    peso = r.get("peso", 10)

    mascotas_ingresadas = Registro.objects.filter(
        estado="Aceptado",
        eliminado=False,
        fecha__date=timezone.localdate(),
    ).count()

    estado, motivo = evaluar_admision(mascotas_ingresadas, peso)

    Registro.objects.create(
        nombre=nombre,
        peso=peso,
        estado=estado,
        motivo=f"{motivo} (migrado desde datos.json)",
    )
    creados += 1

print(f"{creados} registro(s) migrado(s) desde datos.json.")