
# Sistema de Gestión de Versiones con Copy-on-Write (COW)

Este proyecto implementa un sistema de gestión de versiones de archivos utilizando el concepto de **Copy-on-Write (COW)** y estructuras de datos como **árboles dirigidos acíclicos (DAG)**. El sistema permite crear, modificar y versionar archivos de manera eficiente, optimizando el uso de memoria y almacenamiento.

---

## Integrantes del Grupo

- **Paula Inés Llanos**
- **Luis Ángel Nerio**
- **Maria Alejandra Ocampo**

---

## Requisitos del Sistema

- **Sistema Operativo**: Windows 11 (Versión 23H2) o superior.
- **Lenguaje de Programación**: Python 3.12.
- **Herramientas**:
  - **IDE**: Visual Studio Code (VSCode).
  - **Control de Versiones**: Git y GitHub.

---

## Comandos Disponibles

El sistema soporta los siguientes comandos:

### 1. Crear Usuario
Registra un nuevo usuario en el sistema.

```bash
python cowfs.py crear_usuario <nombre_usuario>
```

**Ejemplo**:
```bash
python cowfs.py crear_usuario luis
```

---

### 2. Cambiar Usuario
Cambia el usuario activo en el sistema.

```bash
python cowfs.py cambiar_usuario <nombre_usuario>
```

**Ejemplo**:
```bash
python cowfs.py cambiar_usuario maria
```

---

### 3. Crear Archivo
Crea un nuevo archivo en el sistema.

```bash
python cowfs.py crear_archivo <nombre_archivo>
```

**Ejemplo**:
```bash
python cowfs.py crear_archivo archivo1.txt
```

---

### 4. Guardar Versión
Guarda una nueva versión de un archivo utilizando el mecanismo de **Copy-on-Write (COW)**.

```bash
python cowfs.py guardar_version <nombre_archivo>
```

**Ejemplo**:
```bash
python cowfs.py guardar_version archivo1.txt
```

---

### 5. Listar Archivos
Muestra una lista de todos los archivos registrados en el sistema.

```bash
python cowfs.py listar_archivos
```

---

### 6. Asignar Memoria
Asigna bloques de memoria a un archivo.

```bash
python cowfs.py asignar_memoria <nombre_archivo> <num_bloques>
```

**Ejemplo**:
```bash
python cowfs.py asignar_memoria archivo1.txt 10
```

---

### 7. Liberar Memoria
Libera la memoria asignada a un archivo.

```bash
python cowfs.py liberar_memoria <nombre_archivo>
```

**Ejemplo**:
```bash
python cowfs.py liberar_memoria archivo1.txt
```

---

## Instrucciones para Ejecutar el Proyecto

1. **Clonar el Repositorio**:
   ```bash
   git clone https://github.com/ssramirezr/assignment1-compi.git
   ```

2. **Navegar al Directorio del Proyecto**:
   ```bash
   cd assignment1-compi
   ```

3. **Instalar Python**:
   - Asegúrate de tener Python 3.12 instalado. Puedes descargarlo desde [aquí](https://www.python.org/downloads/).

4. **Ejecutar el Sistema**:
   - Usa los comandos mencionados anteriormente para interactuar con el sistema.
   - Ejemplo:
     ```bash
     python cowfs.py crear_usuario luis
     python cowfs.py crear_archivo archivo1.txt
     python cowfs.py guardar_version archivo1.txt
     ```

---

## Estructura del Proyecto

```
cow_fs/
    cow_fs/
        __init__.py
        _pycache_/
        .cowfs/
    archivos/
        versions.py
    config.json
    metadata.json
    usuarios.json
    commands.py
    config.py
    cowfs.py
    metadata.py
    memoria.py
```

---

## Detalles Técnicos

### Copy-on-Write (COW)
- **COW** es una técnica que evita la duplicación de datos hasta que sea necesario. Cuando se modifica un archivo, se crea una nueva versión en lugar de sobrescribir la existente.
- Esto permite un versionado eficiente y un uso optimizado de la memoria.

### Árboles Dirigidos Acíclicos (DAG)
- Cada archivo tiene un **DAG** que representa su historial de versiones.
- Cada nodo del DAG es una versión del archivo, y los nodos están conectados para representar las relaciones entre versiones.

### Gestión de Memoria
- El sistema permite asignar y liberar bloques de memoria para cada archivo, lo que facilita la gestión de recursos.

