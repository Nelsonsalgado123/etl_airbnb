import pandas as pd
from pymongo import MongoClient
import logging
from logger_base import iniciar_logger

class Extraccion:
    """
    Clase para establecer conexión con MongoDB, extraer colecciones 
    y cargarlas en DataFrames de Pandas.
    """
    
    def __init__(self, db_name='airbnb_ba', uri='mongodb://localhost:27017/'):
        # 1. Configurar el sistema de logs (La libreta de apuntes)
        iniciar_logger()
        
        # 2. Establecer la conexión con la base de datos
        try:
            self.client = MongoClient(uri)
            self.db = self.client[db_name]
            logging.info(f"✅ Conexión exitosa a la base de datos: '{db_name}'")
        except Exception as e:
            logging.error(f"❌ Error al conectar con la base de datos: {e}")
            self.client = None

    def extraer_coleccion(self, nombre_coleccion, limite=None):
        """
        Consulta una colección en la base de datos, la carga en un DataFrame 
        y registra la cantidad de registros extraídos en el log.
        """
        if not self.client:
            logging.error("No hay conexión activa a la base de datos.")
            return None

        try:
            # Seleccionar el cajón (colección)
            coleccion = self.db[nombre_coleccion]
            
            # Consultar los datos (con límite de seguridad opcional)
            if limite:
                datos = list(coleccion.find().limit(limite))
            else:
                datos = list(coleccion.find())
            
            # Cargar los datos en un DataFrame de pandas
            df = pd.DataFrame(datos)
            
            # Registrar en el log la cantidad de registros extraídos
            logging.info(f"📦 Se extrajeron {len(df)} registros de la colección '{nombre_coleccion}'.")
            
            return df
            
        except Exception as e:
            logging.error(f"❌ Error al extraer la colección '{nombre_coleccion}': {e}")
            return None

# ==========================================
# ZONA DE EJECUCIÓN (Para probar que funciona)
# ==========================================
if __name__ == "__main__":
    print("Iniciando el proceso de extracción...\n")
    
    # 1. Instanciar la clase (Crear la conexión)
    extractor = Extraccion()
    
    # 2. Consultar y cargar cada colección en DataFrames
    df_listings = extractor.extraer_coleccion('Listings')
    df_reviews  = extractor.extraer_coleccion('Reviews')
    
    # ⚠️ SALVAVIDAS PARA LA RAM:
    # El archivo Calendar tiene 10 millones de filas. Si Python intenta poner 
    # todo eso en la RAM al mismo tiempo, tu computador se puede congelar.
    # Usamos el parámetro 'limite=5000' para probar que la conexión funciona perfecto 
    df_calendar = extractor.extraer_coleccion('Calendar', limite=5000)
    
    print("\n¡Extracción finalizada con éxito!")