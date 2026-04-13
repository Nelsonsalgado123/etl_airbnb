import pandas as pd
import logging
from datetime import datetime

class Transformacion:
    """
    Clase encargada de transformar los datos extraídos desde MongoDB.
    Se realizan procesos de limpieza, normalización y generación de nuevas variables
    para dejar los datos listos para análisis y carga.
    """

    def __init__(self):
        self._configurar_logs()

    def _configurar_logs(self):
        """
        Configura el sistema de logs para registrar todas las transformaciones realizadas.
        Se genera un archivo por ejecución con fecha y hora.
        """
        fecha = datetime.now().strftime("%Y%m%d_%H%M")
        logging.basicConfig(
            filename=f"logs/log_{fecha}.txt",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
        logging.info("Inicializando módulo de transformación")

    def limpiar_nulos_duplicados(self, df, nombre):
        """
        Elimina registros duplicados y valores nulos para mejorar la calidad de los datos.
        """
        before = len(df)
        # Convertir columnas tipo lista a string (clave para evitar error)
        for col in df.columns:
            df[col] = df[col].apply(
                lambda x: str(x) if isinstance(x, (list, dict)) else x
            )

        # Eliminación de duplicados
        df = df.drop_duplicates()

        # Eliminación de valores nulos
        df = df.dropna()

        after = len(df)

        logging.info(f"{nombre}: {before} -> {after} registros después de limpieza")
        return df

    def normalizar_precio(self, df):
        """
        Convierte el campo 'price' a formato numérico eliminando símbolos como '$' y ','.
        Esto permite realizar análisis matemáticos sobre el precio.
        """
        if 'price' in df.columns:
            df['price'] = (
                df['price']
                .astype(str)
                .str.replace('$', '', regex=False)
                .str.replace(',', '', regex=False)
                .astype(float)
            )
            logging.info("Precios normalizados correctamente")
        return df

    def transformar_fechas(self, df):
        """
        Convierte la columna 'date' a formato datetime y genera nuevas variables
        temporales como año, mes, día y trimestre.
        """
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')

            # Creación de variables derivadas
            df['year'] = df['date'].dt.year
            df['month'] = df['date'].dt.month
            df['day'] = df['date'].dt.day
            df['quarter'] = df['date'].dt.quarter

            logging.info("Fechas transformadas correctamente")
        return df

    def categorizar_precios(self, df):
        """
        Clasifica los precios en categorías para facilitar el análisis:
        Bajo, Medio, Alto, Premium y Lujo.
        """
        if 'price' in df.columns:
            bins = [0, 50, 100, 200, 500, float('inf')]
            labels = ['Bajo', 'Medio', 'Alto', 'Premium', 'Lujo']

            df['price_category'] = pd.cut(df['price'], bins=bins, labels=labels)

            logging.info("Precios categorizados")
        return df

    def convertir_tipos_sqlite(self, df):
        """
        Convierte todos los valores complejos a string para compatibilidad con SQLite.
        """
        for col in df.columns:
            df[col] = df[col].apply(
                lambda x: str(x) if not isinstance(x, (int, float, str, bool, type(None))) else x
            )
        return df

    def transformar(self, data):
        """
        Aplica todas las transformaciones necesarias a cada colección.
        Retorna los DataFrames limpios y listos para la carga.
        """

        # =====================
        # TRANSFORMACIÓN LISTINGS
        # =====================
        listings = self.limpiar_nulos_duplicados(data["listings"], "Listings")
        listings = self.normalizar_precio(listings)
        listings = self.categorizar_precios(listings)

        # =====================
        # TRANSFORMACIÓN CALENDAR
        # =====================
        calendar = self.limpiar_nulos_duplicados(data["calendar"], "Calendar")
        calendar = self.normalizar_precio(calendar)
        calendar = self.transformar_fechas(calendar)

        # =====================
        # TRANSFORMACIÓN REVIEWS
        # =====================
        reviews = self.limpiar_nulos_duplicados(data["reviews"], "Reviews")
        reviews = self.transformar_fechas(reviews)
        
        # =====================
        # AJUSTE FINAL PARA SQLITE
        # =====================
        listings = self.convertir_tipos_sqlite(listings)
        calendar = self.convertir_tipos_sqlite(calendar)
        reviews = self.convertir_tipos_sqlite(reviews)


        return {
            "listings": listings,
            "calendar": calendar,
            "reviews": reviews
        }