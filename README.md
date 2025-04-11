# Biblioteca de Gestión de Archivos Basados en Copy-on-Write (CoW) 

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

El sistema de archivos **CoW** permite:

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

---

## Funciones Clave

### 1. CoWFileSystem::create
Crea un nuevo archivo en el sistema:
```cpp
void CoWFileSystem::create(const std::string& filename, const std::string& author);
```
**Flujo:**
- Verifica si el archivo ya existe.
- Asigna bloques libres para el archivo.
- Registra la primera versión del archivo en los metadatos.

### 2. CoWFileSystem::open
Abre un archivo para un usuario específico.
```cpp
std::shared_ptr<FileHandler> CoWFileSystem::open(const std::string& filename, const std::string& author);
```
**Flujo**:
- Verifica si el archivo existe.
- Crea un FileHandler para gestionar las operaciones del archivo.

### 3. CoWFileSystem::read
Lee el contenido acumulado de todas las versiones de un archivo.
```cpp
std::vector<uint8_t> CoWFileSystem::read(const std::string& filename, const std::string& author);
```
**Flujo**:
- Recupera todas las versiones del archivo.
- Junta los bloques de todas las versiones para devolver el contenido completo.

### 4. CoWFileSystem::write
Escribe datos en un archivo, creando una nueva versión.
```cpp
void CoWFileSystem::write(const std::string& filename, const std::vector<uint8_t>& data, const std::string& author);
```
**Flujo**:
- Realiza una operación Copy-on-Write si los bloques actuales están compartidos.
- Escribe los datos en nuevos bloques si es necesario.
- Registra la nueva versión en los metadatos.

### 5. CoWFileSystem::close
Cierra un archivo abierto.
```cpp
void CoWFileSystem::close(const std::string& filename);
```
**Flujo**:
- Marca el archivo como cerrado en el FileHandler.
- Elimina el archivo del mapa de archivos abiertos.


### 6. MetadataManager::get_all_versions
Obtiene todas las versiones de un archivo.
```cpp
std::vector<FileVersion> MetadataManager::get_all_versions(const std::string& filename) const;
```
**Flujo**:
- Busca el archivo en los metadatos.
- Devuelve una lista de todas las versiones registradas.

---

## Flujo de Ejecución

### 1. Creación de un archivo
- **Acción del usuario**: Llama a `create()`
- **Procesos del sistema**:
  - Asigna bloques libres para el nuevo archivo
  - Registra la primera versión en los metadatos
  - Establece los atributos iniciales (autor, timestamp)

### 2. Apertura de un archivo
- **Acción del usuario**: Llama a `open()`
- **Procesos del sistema**:
  - Verifica permisos y existencia del archivo
  - Crea un objeto `FileHandler` para manejar las operaciones
  - Actualiza el estado del archivo a "abierto"

### 3. Escritura en un archivo
- **Acción del usuario**: Llama a `write()`
- **Procesos del sistema**:
  - Verifica si los bloques actuales están compartidos (Copy-on-Write)
  - Si es necesario:
    - Asigna nuevos bloques
    - Copia los datos existentes
  - Escribe los nuevos datos
  - Registra una nueva versión con:
    - Referencia a los bloques modificados
    - Nueva marca de tiempo
    - Identificación del autor

### 4. Lectura de un archivo
- **Acción del usuario**: Llama a `read()`
- **Procesos del sistema**:
  - Recupera todas las versiones disponibles
  - Reconstruye el contenido completo concatenando:
    - Bloques de la versión original
    - Bloques modificados en versiones posteriores
  - Devuelve el contenido unificado al usuario

### 5. Cierre de un archivo
- **Acción del usuario**: Llama a `close()`
- **Procesos del sistema**:
  - Libera el `FileHandler` asociado
  - Actualiza el estado del archivo a "cerrado"
  - Elimina la entrada del mapa de archivos abiertos
  - Persiste cualquier cambio pendiente en disco

---

##  Pruebas y Ejemplo de Uso
El archivo ```main.cpp``` incluye pruebas que demuestran cómo interactuar con el sistema.

**Ejemplo:**
```cpp
CoW paula("Paula");
paula.create("diario.txt");
paula.open("diario.txt");
paula.write("Querido diario, hoy fue un buen día.");
paula.read(); // Lee: "Querido diario, hoy fue un buen día."
paula.close();

CoW carlos("Carlos");
carlos.open("diario.txt");
carlos.write("Carlos estuvo aquí también.");
carlos.read(); // Lee: "Querido diario, hoy fue un buen día.Carlos estuvo aquí también."
carlos.close();
```

---

## Cómo Ejecutar el Código
**Compilación:**
- Usa un compilador compatible con C++17 o superior.
- Comando de compilación (ejemplo con g++):
```cpp
g++ -std=c++17 -o cowfs main.cpp CoW.cpp cow_filesystem.cpp file_handler.cpp metadata_manager.cpp storage_manager.cpp version_manager.cpp -I.
```
**Ejecución:**
- Ejecuta el binario generado
```cpp
./cow
```
## Conclusión
Este sistema permite una gestión avanzada de archivos con control de versiones, escritura segura, y soporte para múltiples usuarios. Gracias a la estrategia Copy-on-Write, se optimiza el uso del almacenamiento y se garantiza la integridad de los datos.
