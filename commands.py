from config import registrar_usuario, cambiar_usuario, obtener_usuario_actual, crear_archivo, abrir_archivo, cerrar_y_guardar
from metadata import guardar_version, registrar_archivo, listar_versiones, listar_archivos
import os

def ejecutar_comando(comando, *argumentos):
    if comando == "crear_usuario":
        if argumentos[0]:
            registrar_usuario(argumentos[0])
        else:
            print("⚠️ Debes especificar un nombre de usuario.")
    elif comando == "cambiar_usuario":
        if argumentos[0]:
            cambiar_usuario(argumentos[0])
        else:
            print("⚠️ Debes especificar un nombre de usuario.")
    elif comando == "guardar_version":
        if argumentos[0]:
            guardar_version(argumentos[0], obtener_usuario_actual())
        else:
            print("⚠️ Debes especificar un archivo para guardar su versión.")
    elif comando == "crear_archivo":
        if argumentos[0]:
            crear_archivo(argumentos[0])
        else:
            print("⚠️ Debes especificar un nombre para el archivo.")
    elif comando == "listar_archivos":
        listar_archivos()
    elif comando == "listar_versiones":
        if argumentos[0]:
            listar_versiones(argumentos[0])
        else:
            print("⚠️ Debes especificar un archivo para listar")
    elif comando == "abrir_archivo":
        if argumentos[0]:
            abrir_archivo(argumentos[0])
        else:
            print("⚠️ Debes especificar un archivo para abrir")
    elif comando == "cerrar_archivo":
        cerrar_y_guardar()
    else:
        print("⚠️ Comando no reconocido.")