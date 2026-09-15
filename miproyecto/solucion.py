import json
import os
from tabulate import tabulate

CUPOS_TOTALES = 10

# 1. LA REGLA DE DECISIÓN, TAL CUAL LA ES1 — NO SE TOCA
# Se saca a su propia función para poder importarla desde Django sin
# arrastrar el guardado en JSON.
def evaluar_admision(mascotas_ingresadas, peso):
    cupos = CUPOS_TOTALES - mascotas_ingresadas

    estado = ""
    motivo = ""

    if peso <= 0:
        estado = "Dato Inválido"
        motivo = "El peso debe ser mayor a 0."
    elif peso > 15:
        estado = "Rechazado"
        motivo = "Excede el peso máximo permitido de 15 kilos."
    elif cupos <= 0:
        estado = "Rechazado"
        motivo = "No quedan cupos disponibles para hoy."
    else:
        estado = "Aceptado"
        motivo = "Ingresado con éxito a la jornada."

    return estado, motivo


# Sigue usando datos.json porque es la que se corre por consola con
# "python solucion.py". Django ya no la llama: Django llama a
# evaluar_admision() directamente y guarda en la base de datos.
def procesar_admision(mascotas_ingresadas, nombre, peso):
    estado, motivo = evaluar_admision(mascotas_ingresadas, peso)

    # --- GUARDAR EN JSON (solo para el modo consola) ---
    registros = []

    if os.path.exists("datos.json"):
        with open("datos.json", "r", encoding="utf-8") as f:
            try:
                registros = json.load(f)
            except json.JSONDecodeError:
                registros = []

    nuevo_registro = {
        "nombre": nombre,
        "estado": estado,
        "peso": peso,
        "motivo": motivo
    }

    registros.append(nuevo_registro)

    with open("datos.json", "w", encoding="utf-8") as f:
        json.dump(registros, f, indent=2)

    return nuevo_registro


if __name__ == "__main__":
    print("--- Sistema de Admisión Veterinaria ---")

    masc_ingresadas = int(input("¿Cuántas mascotas ya han entrado hoy?: "))
    nom = input("Nombre de la mascota: ")
    p = int(input("Peso de la mascota (kilos): "))

    resultado = procesar_admision(masc_ingresadas, nom, p)

    print(f"\n[{resultado['estado']}] {resultado['nombre']} - {resultado['motivo']}")

    if os.path.exists("datos.json"):
        with open("datos.json", "r", encoding="utf-8") as f:
            datos_guardados = json.load(f)
            print("\n--- Resumen de Registros ---")
            print(tabulate(datos_guardados, headers="keys"))