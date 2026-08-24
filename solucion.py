import json
import os
from tabulate import tabulate

print("--- Sistema de Admisión Veterinaria ---")

# Límite máximo de atenciones para el día
CUPOS_TOTALES = 10 

# Cupos
mascotas_ingresadas = int(input("¿Cuántas mascotas ya han entrado hoy?: "))
cupos = CUPOS_TOTALES - mascotas_ingresadas 

# Datos de la mascota
nombre = input("Nombre de la mascota: ")
peso = int(input("Peso de la mascota (kilos): ")) 

# Regla de decisión con if y elif
if peso <= 0:
    print(f"Error: El peso ingresado para {nombre} es inválido. Debe ser mayor a 0.")
elif cupos <= 0:
    print(f"Rechazado: Lo sentimos, ya no quedan cupos para atender a {nombre} hoy.")
elif peso > 15:
    print(f"Rechazado: {nombre} excede el peso máximo permitido de 15 kilos para los caniles.")
elif peso <= 15 and cupos > 0:
    print(f"Aceptado: {nombre} ha sido ingresado con éxito a la jornada.")
    
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