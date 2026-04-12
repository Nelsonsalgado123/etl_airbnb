# 🏙️ Proceso ETL - Airbnb Buenos Aires

Este proyecto automatiza el proceso de Extracción, Transformación y Carga (ETL) de datos correspondientes a los alojamientos de Airbnb en la ciudad de Buenos Aires. Utiliza Python para el procesamiento de datos y MongoDB como motor de almacenamiento inicial.

## 📂 Estructura del Proyecto

El repositorio está organizado de la siguiente manera para separar la lógica, los datos y los registros:

```text
ETL_AIRBNB/
├── data/                 # ⚠️ Carpeta local para los datasets (.csv)
├── logs/                 # Registros automáticos de ejecución (.txt)
├── notebooks/            # Jupyter Notebooks de análisis previo
├── src/                  # Código fuente del pipeline
│   ├── logger_base.py    # Configuración de logs
│   ├── extraccion.py     # Script Fase 1 (MongoDB -> Pandas)
│   ├── transformacion.py # Script Fase 2 (Limpieza de datos)
│   └── carga.py          # Script Fase 3 (Carga a destino)
├── .gitignore            # Archivos excluidos del control de versiones
├── requirements.txt      # Dependencias del proyecto
└── README.md             # Documentación principal

```
## 🛠️ Instrucciones de Instalación y Ejecución

### 2.1 Configuración de la Base de Datos Local

1.  **Directorio de Datos:** Crea una carpeta llamada `data/` en la raíz del proyecto.
2.  **Descarga de Archivos:** Descarga y guarda en la carpeta `data/` los archivos comprimidos originales:
    * `listings.csv.gz`
    * `calendar.csv.gz`
    * `reviews.csv.gz`
3.  **Descompresión Automatizada:** No intentes descomprimir los archivos desde el explorador de archivos. Ejecuta el script especializado para procesar estos volúmenes de datos:
    ```bash
    python src/descomprimir.py
    ```
    *Esto generará los archivos `.csv` descomprimidos dentro de la misma carpeta `data/` de forma eficiente.*

4.  **Configuración de MongoDB:**
    * Abre MongoDB Compass y conéctate al servidor local (`mongodb://localhost:27017/`).
    * Crea una base de datos llamada `airbnb_ba`.
    * Crea 3 colecciones (`Listings`, `Reviews`, `Calendar`) e importa el archivo `.csv` correspondiente generado en el paso anterior.
    > ⚠️ **Nota:** La importación de la colección `Calendar` puede tomar varios minutos debido a que contiene más de 10 millones de registros.

### 2.2 Creación del Entorno Virtual e Instalación de Dependencias
Abre tu terminal y ejecuta los siguientes comandos para no afectar tu sistema base:

```bash
# 1. Crear el entorno virtual
python -m venv venv

# 2. Activar el entorno virtual (En Windows)
venv\Scripts\activate

# 3. Instalar las librerías necesarias
pip install -r requirements.txt
```

### 2.3. Ejecución del Pipeline ETL
Con el entorno activado y MongoDB corriendo con los datos cargados, el proceso debe ejecutarse en el siguiente orden estricto para mantener la integridad de los datos:

* **Fase 0: Análisis Exploratorio (Opcional)**
    Para revisar los hallazgos iniciales en el entorno interactivo:
    > `notebooks/exploracion_airbnb.ipynb`

* **Fase 1: Extracción**
    Establece la conexión con MongoDB, consulta las colecciones y las convierte en DataFrames estructurados.
    ```bash
    python src/extraccion.py
    ```

* **Fase 2: Transformación**
    Recibe los datos crudos, ejecuta la limpieza, maneja valores nulos y normaliza los formatos.
    ```bash
    python src/transformacion.py
    ```

* **Fase 3: Carga**
    Consolida la información limpia y la exporta al destino final (base de datos SQLite y reporte en Excel).
    ```bash
    python src/carga.py
    ```

💡 Sistema de Monitoreo: Cada ejecución del código genera automáticamente un archivo de registro detallado en la carpeta logs/, donde se documentan conexiones exitosas, posibles errores y la cantidad de registros procesados.

## 👥 Integrantes del Grupo y Responsabilidades
- **Nelson Livanier Salgado Tejada:** Arquitectura del repositorio, conexión a MongoDB y módulo de Extracción.
- **Juan David Osorio Zapata:** Análisis Exploratorio de Datos (EDA) y redacción del Informe Final.
- **Maria Camila:** Módulo de Transformación, limpieza de datos y Carga.
