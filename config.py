import json
import os
from metadata import registrar_archivo

CONFIG_PATH = ".cowfs/config.json"
USUARIOS_PATH = ".cowfs/usuarios.json"

# Crear la estructura de configuración si no existe
os.makedirs(".cowfs", exist_ok=True)
if not os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, "w") as f:
        json.dump({}, f)

if not os.path.exists(USUARIOS_PATH):
    with open(USUARIOS_PATH, "w") as f:
        json.dump({}, f)

def registrar_usuario(nombre):
    """Registra un nuevo usuario si no existe."""
    try:
        with open(USUARIOS_PATH, "r+") as f:
            try:
                usuarios = json.load(f)
            except json.JSONDecodeError:
                usuarios = {}

            if nombre in usuarios:
                print(f" El usuario '{nombre}' ya existe.")
                return

            usuarios[nombre] = {"archivos": []}
            f.seek(0)
            json.dump(usuarios, f, indent=4)
            f.truncate()

        print(f" Usuario '{nombre}' creado exitosamente.")
    except Exception as e:
        print(f"Error al registrar el usuario: {e}")

def crear_archivo(nombre_archivo):
    """Crea un archivo vacío y lo registra en el sistema."""
    ruta_archivo = os.path.join(".cowfs/archivos", nombre_archivo)
    if os.path.exists(ruta_archivo):
        print(f" El archivo '{nombre_archivo}' ya existe.")
        return

    try:
        with open(ruta_archivo, "w") as f:
            pass
        print(f"Archivo '{nombre_archivo}' creado exitosamente.")

        usuario_actual = obtener_usuario_actual()
        if usuario_actual:
            registrar_archivo(nombre_archivo, usuario_actual)
        else:
            print(" No hay un usuario actual. Usa 'cambiar_usuario' para establecer uno.")
    except Exception as e:
        print(f" Error al crear el archivo: {e}")

def cambiar_usuario(nombre):
    """Cambia el usuario activo."""
    with open(USUARIOS_PATH, "r") as f:
        usuarios = json.load(f)
    if nombre not in usuarios:
        print(f"El usuario '{nombre}' no existe. Usa 'crear_usuario <nombre>'.")
        return
    with open(CONFIG_PATH, "w") as f:
        json.dump({"usuario_actual": nombre}, f)
    print(f"Ahora estás trabajando como: {nombre}")

def obtener_usuario_actual():
    """Obtiene el usuario actual."""
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)
    return config.get("usuario_actual")