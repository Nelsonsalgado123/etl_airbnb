import sqlite3
import logging
from datetime import datetime

class Carga:
    """
    Clase encargada de cargar los datos transformados en una base de datos SQLite
    y exportarlos a archivos Excel para su posterior análisis.

    Esta fase corresponde a la etapa final del proceso ETL.
    """

    def __init__(self, db_name="airbnb.db"):
        """
        Inicializa la clase con el nombre de la base de datos SQLite
        y configura el sistema de logs.
        """
        self.db_name = db_name
        self._configurar_logs()

    def _configurar_logs(self):
        """
        Configura el sistema de logs para registrar cada evento del proceso de carga.
        Se genera un archivo por ejecución con fecha y hora.
        """
        fecha = datetime.now().strftime("%Y%m%d_%H%M")

        logging.basicConfig(
            filename=f"logs/log_{fecha}.txt",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

        logging.info("Inicializando módulo de carga")

    def cargar_sqlite(self, data):
        """
        Inserta los DataFrames transformados en una base de datos SQLite.

        Parámetros:
        data (dict): Diccionario con DataFrames limpios (listings, calendar, reviews)

        Proceso:
        - Se establece conexión con SQLite
        - Se crea/reemplaza cada tabla
        - Se insertan los registros
        """
        try:
            # Establecer conexión con la base de datos SQLite
            conn = sqlite3.connect(self.db_name)

            for nombre, df in data.items():
                # Guardar cada DataFrame como una tabla en SQLite
                # if_exists='replace' permite sobrescribir datos anteriores
                df.to_sql(nombre, conn, if_exists='replace', index=False)

                logging.info(f"Tabla '{nombre}' cargada correctamente en SQLite")

            # Cerrar la conexión
            conn.close()

            logging.info("Carga a SQLite finalizada correctamente")

        except Exception as e:
            # Captura de errores durante el proceso de carga
            logging.error(f"Error al cargar datos en SQLite: {e}")

    def exportar_excel(self, data):
        """
        Exporta los DataFrames transformados a archivos Excel (.xlsx).

        Parámetros:
        data (dict): Diccionario con DataFrames limpios

        Proceso:
        - Se genera un archivo Excel por cada dataset
        - Se guardan en el directorio raíz del proyecto
        """
        try:
            for nombre, df in data.items():
                # Exportar cada DataFrame a un archivo Excel
                df.to_excel(f"{nombre}.xlsx", index=False)

                logging.info(f"Archivo '{nombre}.xlsx' exportado correctamente")

        except Exception as e:
            # Captura de errores durante la exportación
            logging.error(f"Error al exportar a Excel: {e}")
            