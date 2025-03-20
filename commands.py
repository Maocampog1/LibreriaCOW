from config import registrar_usuario, cambiar_usuario, obtener_usuario_actual, crear_archivo
from metadata import guardar_version, registrar_archivo, listar_versiones, listar_archivos
from memory import asignar_memoria, liberar_memoria, ajustar_memoria
import sys
import os

def ejecutar_comando(comando, *argumentos):
    print(f"Comando recibido: {comando}")
    print(f"Argumentos recibidos: {argumentos}")
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
    elif comando == "asignar_memoria":
            if len(argumentos) == 2 and argumentos[1].isdigit():
                asignar_memoria(argumentos[0], int(argumentos[1]))
            else:
                print("⚠️ Debes especificar un archivo y la cantidad de bloques a asignar.")
    elif comando == "liberar_memoria":
        if argumentos and len(argumentos) >= 1 and argumentos[0]:  # Verifica que argumentos[0] no sea None o vacío
            liberar_memoria(argumentos[0])
        else:
            print("⚠️ Debes especificar un archivo para liberar su memoria.")

    else:
        print(f"⚠️ Comando no reconocido: {comando}")