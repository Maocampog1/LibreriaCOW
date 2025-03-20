import sys
from commands import ejecutar_comando

if len(sys.argv) < 2:
    print("⚠️ Debes proporcionar un comando.")
    sys.exit(1)

comando = sys.argv[1]
argumento1 = sys.argv[2] if len(sys.argv) > 2 else None
argumento2 = sys.argv[3] if len(sys.argv) > 3 else None

ejecutar_comando(comando, argumento1, argumento2)