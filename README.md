# 🏙️ Proceso ETL - Airbnb Buenos Aires

Este proyecto automatiza el proceso de Extracción, Transformación y Carga (ETL) de datos correspondientes a los alojamientos de Airbnb en la ciudad de Buenos Aires. Utiliza Python para el procesamiento de datos y MongoDB como motor de almacenamiento inicial.

---

## 📂 1. Estructura del Proyecto

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

## 🛠️ Instrucciones de Instalación y Ejecución

### 2. Configuración de la Base de Datos Local
Debido a restricciones de tamaño de alojamiento y buenas prácticas de versionado, los archivos CSV originales no se incluyen en este repositorio. Para ejecutar este proyecto localmente, es necesario replicar la base de datos siguiendo estos pasos:

Directorio de Datos: Crea una carpeta llamada data/ en la raíz del proyecto y descarga los archivos listings.csv, reviews.csv y calendar.csv en su interior.

Motor de Base de Datos: Abre MongoDB Compass y conéctate al servidor local (mongodb://localhost:27017/).

Creación de la Base de Datos: Crea una base de datos llamada exactamente airbnb_ba.

Importación de Colecciones: Crea 3 colecciones (Listings, Reviews, Calendar) e importa su archivo CSV correspondiente a cada una.
(Nota: El archivo Calendar tiene un volumen superior a los 10 millones de registros, por lo que la importación puede tomar varios minutos).

### 3. Creación del Entorno Virtual e Instalación de Dependencias
Abre tu terminal y ejecuta los siguientes comandos para no afectar tu sistema base:

# 1. Crear el entorno virtual
python -m venv venv

# 2. Activar el entorno virtual (En Windows)
venv\Scripts\activate

# 3. Instalar las librerías necesarias
pip install -r requirements.txt

### 3. Ejecución del Pipeline ETL
Con el entorno activado y MongoDB corriendo con los datos cargados, el proceso debe ejecutarse en el siguiente orden estricto para mantener la integridad de los datos:
Fase 0: Análisis Exploratorio (Opcional)
Para revisar los hallazgos iniciales en el entorno interactivo:
notebooks/exploracion_airbnb.ipynb
Fase 1: Extracción
Establece la conexión con MongoDB, consulta las colecciones y las convierte en DataFrames estructurados. python src/extraccion.py
Fase 2: Transformación
Recibe los datos crudos, ejecuta la limpieza, maneja valores nulos y normaliza los formatos. python src/transformacion.py
Fase 3: Carga
Consolida la información limpia y la exporta al destino final (base de datos SQLite y reporte en Excel). python src/carga.py

💡 Sistema de Monitoreo: Cada ejecución del código genera automáticamente un archivo de registro detallado en la carpeta logs/, donde se documentan conexiones exitosas, posibles errores y la cantidad de registros procesados.

## 👥 Integrantes del Grupo y Responsabilidades
- **Nelson Livanier Salgado Tejada:** Arquitectura del repositorio, conexión a MongoDB y módulo de Extracción.
- **Juan David:** Análisis Exploratorio de Datos (EDA) y redacción del Informe Final.
- **Maria Camila:** Módulo de Transformación, limpieza de datos y Carga.
