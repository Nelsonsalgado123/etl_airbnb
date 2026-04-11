# 🏙️ Proceso ETL - Airbnb Buenos Aires

## 🎯 Descripción y Objetivo del Proyecto
Este proyecto implementa un proceso automatizado de Extracción, Transformación y Carga (ETL) utilizando Python. El objetivo es tomar los datasets de Airbnb de la Ciudad Autónoma de Buenos Aires (Listings, Reviews y Calendar) almacenados en una base de datos MongoDB local, limpiarlos, normalizarlos y cargarlos en una base de datos analítica SQLite y archivos Excel para su posterior análisis.

## 🛠️ Instrucciones de Instalación y Ejecución

### 1. Requisitos Previos
- Python 3.8 o superior instalado.
- MongoDB instalado y corriendo localmente con los datasets cargados.

### 2. Creación del Entorno Virtual e Instalación de Dependencias
Abre tu terminal y ejecuta los siguientes comandos para no afectar tu sistema base:

**Crear y activar el entorno virtual (Windows):**
python -m venv venv
venv\Scripts\activate

**Instalar las librerías necesarias:**
pip install -r requirements.txt

### 3. Ejecución del Proyecto
Para correr el proceso ETL, ejecuta los scripts en el siguiente orden:
1. **Análisis Exploratorio:** Revisar el notebook en `notebooks/exploracion_airbnb.ipynb`.
2. **Extracción:** `python src/extraccion.py` (Conecta a MongoDB y extrae).
3. **Transformación:** `python src/transformacion.py` (Limpia y normaliza).
4. **Carga:** `python src/carga.py` (Carga a SQLite y exporta a .xlsx).

*Nota: Los registros de cada paso (logs) se guardarán automáticamente en la carpeta `logs/`.*

## 👥 Integrantes del Grupo y Responsabilidades
- **[Tu Nombre]:** Arquitectura del repositorio, conexión a MongoDB y módulo de Extracción.
- **[Nombre Compañero 1]:** Análisis Exploratorio de Datos (EDA) y redacción del Informe Final.
- **[Nombre Compañero 2]:** Módulo de Transformación, limpieza de datos y Carga.
