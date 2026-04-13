from extraccion import Extraccion
from transformacion import Transformacion
from carga import Carga

"""
Archivo principal que orquesta todo el proceso ETL.

Fases del proceso:
1. Extracción: Obtiene los datos desde MongoDB
2. Transformación: Limpia y prepara los datos
3. Carga: Guarda los datos en SQLite y los exporta a Excel

Este archivo permite ejecutar todo el pipeline de forma automatizada.
"""

def ejecutar_etl():
    """
    Función principal que ejecuta el flujo completo del proceso ETL.
    """

    print(" Iniciando proceso ETL...\n")

    # =====================
    # FASE 1: EXTRACCIÓN
    # =====================
    # Se establece conexión con MongoDB y se extraen las colecciones
    etl = Extraccion()

    data = {
        "listings": etl.extraer_coleccion("Listings"),
        "reviews": etl.extraer_coleccion("Reviews"),

        # Se usa un límite en Calendar para evitar sobrecarga de memoria
        "calendar": etl.extraer_coleccion("Calendar", limite=5000)
    }

    print(" Extracción completada")

    # =====================
    # FASE 2: TRANSFORMACIÓN
    # =====================
    # Se limpian los datos, se normalizan formatos y se generan nuevas variables
    transformador = Transformacion()
    data_limpia = transformador.transformar(data)

    print(" Transformación completada")

    # =====================
    # FASE 3: CARGA
    # =====================
    # Se almacenan los datos en SQLite y se exportan a archivos Excel
    cargador = Carga()
    cargador.cargar_sqlite(data_limpia)
    cargador.exportar_excel(data_limpia)

    print(" Carga completada")
    print("\n Proceso ETL finalizado correctamente")


# =====================
# PUNTO DE ENTRADA
# =====================
# Permite ejecutar el script directamente desde la terminal
if __name__ == "__main__":
    ejecutar_etl()