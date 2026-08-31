import json
import os
from tabulate import tabulate

CUPOS_TOTALES = 10 

# 1. TODO SE ENCAPSULA EN ESTA FUNCIÓN
def procesar_admision(mascotas_ingresadas, nombre, peso):
    cupos = CUPOS_TOTALES - mascotas_ingresadas 

    estado = ""
    motivo = "" # Creamos la variable motivo para guardarla en el JSON

    # Asignamos estado y motivo de forma separada
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

    # --- FASE 2: GUARDAR EN JSON ---
    registros = []

    if os.path.exists("datos.json"):
        with open("datos.json", "r", encoding="utf-8") as f:
            try:
                registros = json.load(f)
            except json.JSONDecodeError:
                # Por si el archivo existe pero está vacío o corrupto
                registros = []

    # 2. EL JSON AHORA GUARDA LAS 4 VARIABLES (Nombre, Estado, Peso y Motivo)
    nuevo_registro = {
        "nombre": nombre, 
        "estado": estado,
        "peso": peso,
        "motivo": motivo
    }
    
    registros.append(nuevo_registro)

    with open("datos.json", "w", encoding="utf-8") as f:
        json.dump(registros, f, indent=2)

    # La función debe retornar el registro para que Django lo reciba en views.py
    return nuevo_registro


# Bloque de prueba para la consola (Django ignorará esto y solo usará la función)
if __name__ == "__main__":
    print("--- Sistema de Admisión Veterinaria ---")
    
    masc_ingresadas = int(input("¿Cuántas mascotas ya han entrado hoy?: "))
    nom = input("Nombre de la mascota: ")
    p = int(input("Peso de la mascota (kilos): "))
    
    # Llamamos a la función
    resultado = procesar_admision(masc_ingresadas, nom, p)
    
    print(f"\n[{resultado['estado']}] {resultado['nombre']} - {resultado['motivo']}")
    
    # Mostramos la tabla leyendo el archivo recién actualizado
    if os.path.exists("datos.json"):
        with open("datos.json", "r", encoding="utf-8") as f:
            datos_guardados = json.load(f)
            print("\n--- Resumen de Registros ---")
            print(tabulate(datos_guardados, headers="keys"))