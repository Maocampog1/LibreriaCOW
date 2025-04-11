# Sistemas de Archivos Copy-on-Write (CoW)

Este proyecto implementa un sistema de archivos basado en Copy-on-Write (CoW), que permite la gestión eficiente de archivos y versiones en un entorno multiusuario.

## Índice

1. [Introducción](#introducción)  
2. [Estructuras Principales](#estructuras-principales)  
3. [Funciones Clave](#funciones-clave)  
4. [Flujo de Ejecución](#flujo-de-ejecución)  
5. [Pruebas y Ejemplo de Uso](#pruebas-y-ejemplo-de-uso)  
6. [Cómo Ejecutar el Código](#cómo-ejecutar-el-código)  
7. [Conclusión](#conclusión)

---

## Introducción

El sistema de archivos CoW permite:

- **Control de versiones**: Cada vez que un archivo es modificado, se crea una nueva versión en lugar de sobrescribir la existente.  
- **Multiusuario**: Diferentes usuarios pueden interactuar con los mismos archivos, y sus cambios se reflejan en un historial acumulativo.  
- **Gestión eficiente de bloques**: Los bloques de datos son reutilizados o copiados según sea necesario, optimizando el uso del almacenamiento.

El sistema implementa muchas validaciones para evitar errores comunes como intentar leer o escribir en archivos cerrados.

---

## Estructuras Principales

### 1. FileVersion 
Representa una versión de un archivo.

```cpp
struct FileVersion {
    int version;                     // Número de versión
    std::vector<int> blocks;         // Bloques asociados a esta versión
    int size;                        // Tamaño de la versión en bytes
    int parent;                      // Versión padre (si aplica)
    std::string author;              // Autor de la versión
    std::string timestamp;           // Marca de tiempo de creación
};
```

### 2. Inodo
Representa la metadata básica de un archivo.

```cpp
struct Inode {
    char filename[config::MAX_FILENAME_LENGTH]; // Nombre del archivo
    size_t first_block;                         // Primer bloque de datos
    size_t size;                                // Tamaño total del archivo
    size_t version_count;                       // Número de versiones
    bool is_used;                               // Si el archivo está en uso
    std::vector<FileVersion> version;           // Historial de versiones
    std::string creation_time;                  // Fecha de creación
    std::string author;                         // Autor original
};

```

### 3. MetadataManager
Gestiona la metadata de los archivos, incluyendo:
- Las versiones de cada archivo
- Los bloques libres disponibles
- La información de estructura del sistema de archivos

### 4. StorageManager
Responsable de:
- La lectura de bloques del almacenamiento físico
- La escritura de bloques en el almacenamiento físico  
- La gestión del espacio en disco
- La asignación y liberación de bloques

### 5. FileHandler
Funciona como interfaz entre el usuario y el sistema, permitiendo:
- Operaciones de lectura de archivos
- Operaciones de escritura de archivos
- Cierre seguro de archivos
- Gestión de permisos y acceso concurrente

### 6. CoWFileSystem
Componente central que:
- Coordina todas las operaciones del sistema
- Implementa la lógica Copy-on-Write
- Gestiona la concurrencia y consistencia
- Proporciona la API pública del sistema de archivos

