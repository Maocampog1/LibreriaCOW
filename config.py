import json
import os
from metadata import VERSIONES_DIR, guardar_version, registrar_archivo, ARCHIVOS_DIR
from tkinter import Tk, Text, Button, END
#import tkinter as tk

CONFIG_PATH = ".cowfs/config.json"
USUARIOS_PATH = ".cowfs/usuarios.json"
ventana = None
archivo_abierto = None

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
                print(f"⚠️ El usuario '{nombre}' ya existe.")
                return

            usuarios[nombre] = {"archivos": []}
            f.seek(0)
            json.dump(usuarios, f, indent=4)
            f.truncate()

        print(f"✅ Usuario '{nombre}' creado exitosamente.")
    except Exception as e:
        print(f"❌ Error al registrar el usuario: {e}")

def crear_archivo(nombre_archivo):
    """Crea un archivo vacío y lo registra en el sistema."""
    ruta_archivo = os.path.join(".cowfs/archivos", nombre_archivo)
    if os.path.exists(ruta_archivo):
        print(f"⚠️ El archivo '{nombre_archivo}' ya existe.")
        return

    try:
        with open(ruta_archivo, "w") as f:
            pass
        print(f"✅ Archivo '{nombre_archivo}' creado exitosamente.")

        usuario_actual = obtener_usuario_actual()
        if usuario_actual:
            registrar_archivo(nombre_archivo, usuario_actual)
        else:
            print("⚠️ No hay un usuario actual. Usa 'cambiar_usuario' para establecer uno.")

        abrir_archivo(nombre_archivo) # Abre el archivo recién creado

    except Exception as e:
        print(f"⚠️ Error al crear el archivo: {e}")

def cambiar_usuario(nombre):
    """Cambia el usuario activo."""
    with open(USUARIOS_PATH, "r") as f:
        usuarios = json.load(f)
    if nombre not in usuarios:
        print(f"⚠️ El usuario '{nombre}' no existe. Usa 'crear_usuario <nombre>'.")
        return
    with open(CONFIG_PATH, "w") as f:
        json.dump({"usuario_actual": nombre}, f)
    print(f"✅ Ahora estás trabajando como: {nombre}")

def obtener_usuario_actual():
    """Obtiene el usuario actual."""
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)
    return config.get("usuario_actual")

def abrir_archivo(nombre):
    """Abre una ventana para editar el contenido de un archivo."""
    global ventana, archivo_abierto

    ruta_archivo = os.path.join(ARCHIVOS_DIR, nombre)
    if not os.path.exists(ruta_archivo):
        print(f"⚠️ El archivo '{nombre}' no existe.")
        return

    archivo_abierto = ruta_archivo

    # Crear la ventana de edición
    ventana = Tk()
    ventana.title(f"Editando: {nombre}")

    # Crear un cuadro de texto para mostrar y editar el contenido
    texto = Text(ventana, wrap="word", width=80, height=20)
    texto.pack(expand=True, fill="both")

    # Cargar el contenido del archivo en el cuadro de texto
    with open(ruta_archivo, "r") as f:
        contenido = f.read()
        texto.insert(END, contenido)

    # Botón para cerrar y guardar
    boton_guardar = Button(ventana, text="Cerrar y Guardar", command=lambda: cerrar_y_guardar(texto))
    boton_guardar.pack()

    ventana.mainloop()


def cerrar_y_guardar(texto_widget):
    """Cierra la ventana y guarda los cambios en el archivo, creando una nueva versión."""
    global ventana, archivo_abierto

    if archivo_abierto:
        nombre_archivo = os.path.basename(archivo_abierto)  # Obtener solo el nombre
        usuario_actual = obtener_usuario_actual()  # Obtener el usuario actual

        # Obtener el contenido del cuadro de texto
        nuevo_contenido = texto_widget.get("1.0", END).strip()

        # Guardar el contenido en el archivo original
        with open(archivo_abierto, "w") as f:
            f.write(nuevo_contenido)

        print(f"✅ Cambios guardados en '{archivo_abierto}'.")

        if usuario_actual:
            # Guardar la versión ANTES de sobrescribir el archivo original
            guardar_version(nombre_archivo, usuario_actual)

    # Cerrar la ventana
    if ventana:
        ventana.destroy()
        ventana = None
        archivo_abierto = None
        

