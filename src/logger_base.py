import logging
import os
from datetime import datetime

def iniciar_logger():
    """
    Módulo centralizado para configurar los logs del proyecto ETL.
    Crea un archivo nuevo por ejecución con el formato exigido.
    """
    # 1. El GPS: Encontrar la ruta absoluta de la carpeta principal del proyecto
    directorio_actual = os.path.dirname(os.path.abspath(__file__)) # Esto es 'src'
    directorio_raiz = os.path.dirname(directorio_actual)           # Esto es 'etl_airbnb'
    
    # 2. Apuntar exactamente a la carpeta 'logs' y crearla si no existe
    carpeta_logs = os.path.join(directorio_raiz, 'logs')
    os.makedirs(carpeta_logs, exist_ok=True)

    # 3. Capturar el momento exacto para nombrar el archivo
    fecha_hora = datetime.now().strftime("%Y%m%d_%H%M")
    nombre_archivo = os.path.join(carpeta_logs, f"log_{fecha_hora}.txt")

    # 4. Configurar las reglas del Secretario General
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - [%(levelname)s] - %(message)s',
        handlers=[
            logging.FileHandler(nombre_archivo, encoding='utf-8'),
            logging.StreamHandler()
        ],
        force=True
    )
    
    return nombre_archivo