import json
import os
from datetime import datetime

METADATA_PATH = ".cowfs/metadata.json"
ARCHIVOS_DIR = ".cowfs/archivos/"
VERSIONES_DIR = ".cowfs/versiones/"
USUARIOS_PATH = ".cowfs/usuarios.json"

# Asegurar directorios
os.makedirs(ARCHIVOS_DIR, exist_ok=True)
os.makedirs(VERSIONES_DIR, exist_ok=True)

def cargar_usuarios():
    """Carga el archivo de usuarios o retorna un diccionario vacío."""
    if not os.path.exists(USUARIOS_PATH):
        return {}

    try:
        with open(USUARIOS_PATH, "r") as f:
            contenido = f.read().strip()
            return json.loads(contenido) if contenido else {}
    except json.JSONDecodeError:
        print("⚠️ Error: Archivo de usuarios corrupto, se usará un archivo vacío.")
        return {}


def guardar_usuarios(usuarios):
    """Guarda los datos de usuarios en el archivo JSON."""
    with open(USUARIOS_PATH, "w") as f:
        json.dump(usuarios, f, indent=4)

def cargar_metadata():
    """Carga el archivo de metadata o retorna un diccionario vacío."""
    if not os.path.exists(METADATA_PATH):
        return {}

    try:
        with open(METADATA_PATH, "r") as f:
            contenido = f.read().strip()
            return json.loads(contenido) if contenido else {}
    except json.JSONDecodeError:
        print("Error: Metadata corrupta, se usará un archivo vacío.")
        return {}

def guardar_metadata(metadata):
    """Guarda la metadata en el archivo JSON."""
    with open(METADATA_PATH, "w") as f:
        json.dump(metadata, f, indent=4)

# ...existing code...

def registrar_archivo(nombre, usuario):
    """Registra un archivo existente en el sistema y lo asocia al usuario."""
    metadata = cargar_metadata()
    usuarios = cargar_usuarios()
    ruta = os.path.join(ARCHIVOS_DIR, nombre)

    if not os.path.exists(ruta):
        print(f"El archivo '{nombre}' no existe en {ARCHIVOS_DIR}. Debes crearlo antes.")
        return

    if nombre in metadata:
        print(f" El archivo '{nombre}' ya está registrado.")
        return

    # Registrar el archivo en metadata
    metadata[nombre] = {
        "usuario_creador": usuario,
        "fecha_creacion": datetime.now().isoformat(),
        "ruta": ruta,
        "versiones": {},  # Cambiado a un diccionario para soportar DAG
        "ultima_version": None  # Referencia a la última versión
    }
    guardar_metadata(metadata)

    # Registrar el archivo en usuarios
    if usuario not in usuarios:
        usuarios[usuario] = {"archivos": []}
    usuarios[usuario]["archivos"].append(nombre)
    guardar_usuarios(usuarios)

    print(f" Archivo '{nombre}' registrado por {usuario}.")
    

def guardar_version(nombre, usuario, padre=None):
    """Guarda una nueva versión del archivo."""
    metadata = cargar_metadata()
    if nombre not in metadata:
        print(f"El archivo '{nombre}' no está registrado.")
        return

    ruta_original = metadata[nombre]["ruta"]
    if not os.path.exists(ruta_original):
        print(f" No se encontró el archivo original '{nombre}'.")
        return

    # Generar un identificador único para la nueva versión
    id_version = f"v{len(metadata[nombre]['versiones']) + 1}"
    ruta_version = os.path.join(VERSIONES_DIR, f"{nombre}_{id_version}.txt")

    # Determinar el padre automáticamente
    if padre is None:
        if len(metadata[nombre]["versiones"]) == 0:
            padre = "archivo_original"  # La primera versión tiene como padre el archivo original
        else:
            padre = metadata[nombre]["ultima_version"]  # Las siguientes versiones tienen como padre la última versión

    try:
        with open(ruta_original, "r") as original, open(ruta_version, "w") as version:
            version.write(original.read())

        metadata[nombre]["versiones"][id_version] = {
            "id": id_version,
            "usuario": usuario,
            "fecha": datetime.now().isoformat(),
            "ruta": ruta_version,
            "padre": padre  # Referencia al padre
        }
        metadata[nombre]["ultima_version"] = id_version  # Actualizar la última versión
        guardar_metadata(metadata)
        print(f"Versión {id_version} de '{nombre}' guardada.")
    except Exception as e:
        print(f"Error al guardar la versión: {e}")

def listar_archivos():
    """Lista los archivos registrados en el sistema."""
    metadata = cargar_metadata()
    if not metadata:
        print(" No hay archivos registrados.")
        return

    print("Archivos registrados:")
    for archivo, datos in metadata.items():
        print(f"- {archivo} (Creado por: {datos['usuario_creador']})")

def listar_versiones(nombre):
    """Lista las versiones de un archivo y sus relaciones."""
    metadata = cargar_metadata()
    if nombre not in metadata:
        print(f"El archivo '{nombre}' no está registrado.")
        return

    versiones = metadata[nombre]["versiones"]
    if not versiones:
        print(f"No hay versiones registradas para '{nombre}'.")
        return

    print(f"Versiones de '{nombre}':")
    for id_version, datos in versiones.items():
        padre = datos["padre"] if datos["padre"] else "None"
        print(f"- {id_version} (Creado por: {datos['usuario']}, Padre: {padre})")

# ...existing code...

def crear_rama(nombre, id_version_base, usuario):
    """Crea una nueva rama a partir de una versión existente."""
    metadata = cargar_metadata()
    if nombre not in metadata:
        print(f" El archivo '{nombre}' no está registrado.")
        return

    if id_version_base not in metadata[nombre]["versiones"]:
        print(f" La versión base '{id_version_base}' no existe.")
        return

    nueva_rama = f"{id_version_base}_branch"
    metadata[nombre]["versiones"][nueva_rama] = {
        "id": nueva_rama,
        "usuario": usuario,
        "fecha": datetime.now().isoformat(),
        "ruta": None,  # La nueva rama no tiene contenido inicial
        "padre": id_version_base
    }
    guardar_metadata(metadata)
    print(f" Nueva rama '{nueva_rama}' creada a partir de '{id_version_base}'.")