Evaluación Parcial N°2 - Telepresencia

Integrantes: Ignacio Antifil / Mauricio Chacano  
Asignatura: Telepresencia

Descripción del Proyecto:

Este repositorio contiene las soluciones desarrolladas para la Evaluación Parcial N°2:

1. **`agregar_50_libros.py`**: Script de automatización de API REST para la gestión de catálogo de libros. Realiza peticiones HTTP con manejo de paginación para recuperar el catálogo completo e interactuar con servicios de biblioteca local.
2. **`geolocalizacion.py`**: Aplicación de navegación y cálculo de rutas conectada a la API REST de Graphhopper. Incluye localización en español, métricas con formateo a dos decimales, narración paso a paso de las instrucciones del viaje y opción de salida del sistema.

---
Requisitos Previos
- Python 3.x
- Biblioteca `requests` de Python
- Clave API activa de Graphhopper
---
Instrucciones de Ejecución

1. Script de Automatización de Libros (`agregar_50_libros.py`)

Para ejecutar la consulta e interacción con la API de la biblioteca local:
```bash
 python3 agregar_50_libros.py
```
2. Script de Geolocalización (geolocalizacion.py)

Como Ejecutar el script desde la terminal:
   ```bash
   python3 geolocalizacion.py
```
Allí le pedirán lo siguiente:
- Ingrese la ciudad de origen (ej. Santiago, Chile).
- Ingrese la ciudad de destino (ej. Valparaíso, Chile).
- El código le calculara la ruta a tomar
- Para finalizar el programa, escriba s o salir.
