import sqlite3
import logging
from datetime import datetime
import re

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
                # limpiar antes de exportar
                df = self.limpiar_texto_excel(df)
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
        Exporta los DataFrames a Excel.

        - Si el dataset es muy grande (ej: reviews), exporta solo una muestra
        - Limpia caracteres inválidos antes de exportar
        """
        try:
            for nombre, df in data.items():

                # Limpiar texto para evitar errores en Excel
                df = self.limpiar_texto_excel(df)

                # CASO ESPECIAL: REVIEWS (muy grande)
                if nombre == "reviews":
                    df = df.head(50000)  # muestra de 50k registros
                    df.to_excel(f"{nombre}.xlsx", index=False)

                    logging.warning(
                        "Se exportó solo una muestra de reviews (50k registros) por tamaño del dataset"
                    )

                #  OTROS DATASETS (normales)
                else:
                    df.to_excel(f"{nombre}.xlsx", index=False)
                    logging.info(f"{nombre}.xlsx exportado correctamente")

        except Exception as e:
            logging.error(f"Error al exportar a Excel: {e}")

    def limpiar_texto_excel(self, df):
        """
        Limpia caracteres inválidos para Excel.
        """
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].astype(str).apply(
                lambda x: re.sub(r'[^\x00-\x7F]+', '', x)  # elimina caracteres raros
            )
        return df