
import json
import os
from tabulate import tabulate

print("--- Sistema de Admisión Veterinaria ---")

CUPOS_TOTALES = 10 

mascotas_ingresadas = int(input("¿Cuántas mascotas ya han entrado hoy?: "))
cupos = CUPOS_TOTALES - mascotas_ingresadas 

nombre = input("Nombre de la mascota: ")
peso = int(input("Peso de la mascota (kilos): "))

# Variable para guardar el resultado final
estado = ""

if peso <= 0:
    estado = "Dato Inválido"
    print(f"Error: El peso ingresado para {nombre} es inválido. Debe ser mayor a 0.")
elif peso > 15:
    estado = "Rechazo: Excede peso"
    print(f"Rechazado: {nombre} excede el peso máximo permitido de 15 kilos para los caniles.")
elif cupos <= 0:
    estado = "Rechazo: Sin cupos"
    print(f"Rechazado: Lo sentimos, ya no quedan cupos para atender a {nombre} hoy.")
elif peso <= 15 and cupos > 0:
    estado = "Aceptado"
    print(f"Aceptado: {nombre} ha sido ingresado con éxito a la jornada.")

# --- FASE 2: GUARDAR EN JSON Y MOSTRAR TABLA ---

registros = []

# Revisamos si el archivo ya existe para no borrar los registros anteriores
if os.path.exists("datos.json"):
    with open("datos.json", "r") as f:
        registros = json.load(f)

# Agregamos el nuevo registro a la lista
registros.append({"nombre": nombre, "estado": estado})

# Escribimos la lista actualizada en el archivo datos.json
with open("datos.json", "w") as f:
    json.dump(registros, f, indent=2)

# Mostramos la tabla en la consola
print("\n--- Resumen de Registros ---")
print(tabulate(registros, headers="keys"))
