import json

from core.models import Registro
from core.servicios import cupos_ocupados
from solucion import evaluar_admision

with open("datos.json", encoding="utf-8") as f:
    datos_viejos = json.load(f)

creados = 0
for r in datos_viejos:
    nombre = r.get("nombre", "Sin nombre")
    if Registro.objects.filter(nombre=nombre).exists():
        continue  

    peso = r.get("peso", 0)

    mascotas_ingresadas = cupos_ocupados()

    estado, motivo = evaluar_admision(mascotas_ingresadas, peso)

    Registro.objects.create(
        nombre=nombre,
        peso=peso,
        estado=estado,
        motivo=f"{motivo} (migrado desde datos.json)",
    )
    creados += 1

print(f"{creados} registro(s) migrado(s) desde datos.json.")