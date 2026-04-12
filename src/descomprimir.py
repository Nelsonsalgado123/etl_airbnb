import gzip
import shutil
import os

print("Iniciando descompresión masiva de los datasets de Airbnb...")

# Lista de los nombres de los archivos
archivos = ['calendar', 'listings', 'reviews']

for nombre in archivos:
    archivo_comprimido = f'data/{nombre}.csv.gz'
    archivo_descomprimido = f'data/{nombre}.csv'
    
    print(f"Descomprimiendo {nombre}...")
    
    try:
        with gzip.open(archivo_comprimido, 'rb') as f_in:
            with open(archivo_descomprimido, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        print(f"✅ {nombre}.csv extraído con éxito.")
        
    except FileNotFoundError:
        print(f"❌ Error: No encuentro el archivo {archivo_comprimido}. Revisa la carpeta 'data'.")

print("\n¡Proceso terminado! Revisa tu carpeta 'data'.")