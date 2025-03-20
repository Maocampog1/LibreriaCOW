import json
import os
import math

MEMORY_PATH = ".cowfs/memory.json"
BLOCK_SIZE = 1024  # Tamaño de cada bloque en bytes

# Crear el archivo de memoria si no existe
if not os.path.exists(MEMORY_PATH):
    with open(MEMORY_PATH, "w") as f:
        json.dump({"total_blocks": 100, "free_blocks": list(range(1, 101)), "allocated_blocks": {}}, f)

def cargar_memoria():
    """Carga el estado de la memoria desde el archivo."""
    with open(MEMORY_PATH, "r") as f:
        return json.load(f)

def guardar_memoria(memoria):
    """Guarda el estado de la memoria en el archivo."""
    with open(MEMORY_PATH, "w") as f:
        json.dump(memoria, f, indent=4)

def obtener_tamano_archivo(nombre_archivo):
    """Obtiene el tamaño del archivo en bytes."""
    if os.path.exists(nombre_archivo):
        return os.path.getsize(nombre_archivo)
    else:
        print(f"⚠️ El archivo '{nombre_archivo}' no existe.")
        return 0

def asignar_memoria(nombre_archivo, tamano_estimado=None):
    """Asigna bloques de memoria a un archivo en función de un tamaño estimado."""
    memoria = cargar_memoria()

    # Si no se especifica un tamaño estimado, asignar un bloque por defecto
    if tamano_estimado is None:
        tamano_estimado = BLOCK_SIZE

    # Calcular el número de bloques necesarios
    bloques_necesarios = math.ceil(tamano_estimado / BLOCK_SIZE)

    if len(memoria["free_blocks"]) < bloques_necesarios:
        print(f"⚠️ No hay suficientes bloques libres para asignar a '{nombre_archivo}'.")
        return

    # Asignar bloques
    bloques_asignados = memoria["free_blocks"][:bloques_necesarios]
    memoria["free_blocks"] = memoria["free_blocks"][bloques_necesarios:]
    memoria["allocated_blocks"][nombre_archivo] = {
        "blocks": bloques_asignados,
        "size": 0,  # El tamaño real del archivo comienza en 0
        "estimated_size": tamano_estimado
    }
    guardar_memoria(memoria)
    print(f"✅ {bloques_necesarios} bloques asignados a '{nombre_archivo}' (estimado: {tamano_estimado} bytes): {bloques_asignados}")

def liberar_memoria(nombre_archivo):
    """Libera los bloques de memoria asignados a un archivo."""
    memoria = cargar_memoria()
    print(f"Estado inicial de la memoria: {memoria}")

    if nombre_archivo not in memoria["allocated_blocks"]:
        print(f"⚠️ El archivo '{nombre_archivo}' no tiene bloques asignados.")
        return

    bloques_liberados = memoria["allocated_blocks"].pop(nombre_archivo)["blocks"]
    print(f"Bloques a liberar: {bloques_liberados}")

    memoria["free_blocks"].extend(bloques_liberados)
    memoria["free_blocks"].sort()
    print(f"Estado actualizado de los bloques libres: {memoria['free_blocks']}")

    guardar_memoria(memoria)
    print(f"✅ Bloques liberados para '{nombre_archivo}': {bloques_liberados}")

def ajustar_memoria(nombre_archivo, tamano_actual):
    """Ajusta la memoria asignada a un archivo si su tamaño actual excede el estimado."""
    memoria = cargar_memoria()

    if nombre_archivo not in memoria["allocated_blocks"]:
        print(f"⚠️ El archivo '{nombre_archivo}' no tiene bloques asignados.")
        return

    # Obtener información del archivo
    archivo_info = memoria["allocated_blocks"][nombre_archivo]
    tamano_estimado = archivo_info["estimated_size"]
    bloques_actuales = len(archivo_info["blocks"])

    # Calcular bloques necesarios según el tamaño actual
    bloques_necesarios = math.ceil(tamano_actual / BLOCK_SIZE)

    if bloques_necesarios > bloques_actuales:
        # Asignar bloques adicionales si hay espacio disponible
        bloques_adicionales = bloques_necesarios - bloques_actuales
        if len(memoria["free_blocks"]) < bloques_adicionales:
            print(f"⚠️ No hay suficientes bloques libres para ajustar '{nombre_archivo}'.")
            return

        nuevos_bloques = memoria["free_blocks"][:bloques_adicionales]
        memoria["free_blocks"] = memoria["free_blocks"][bloques_adicionales:]
        archivo_info["blocks"].extend(nuevos_bloques)
        archivo_info["estimated_size"] = tamano_actual
        guardar_memoria(memoria)
        print(f"✅ Memoria ajustada para '{nombre_archivo}'. Nuevos bloques asignados: {nuevos_bloques}")
    else:
        print(f"✅ No se requiere ajuste de memoria para '{nombre_archivo}'.")