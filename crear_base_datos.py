import pandas as pd
from sqlalchemy import create_engine

# 1. Agarro el archivo limpio que hice en el paso anterior (ventas_limpias.csv)
# "Traigo los datos que ya están purificados"
df = pd.read_csv('ventas_limpias.csv')

# 2. Creo la conexión a mi base de datos (se va a llamar 'mi_empresa.db')
# SQLite es mejor por ahora porque es un archivo que vive en mi carpeta, no ocupa internet
engine = create_engine('sqlite:///mi_empresa.db')

# 3. Meto los datos en una tabla llamada 'ventas'
# Si la tabla ya existe, que la reemplace con los datos nuevos (replace)
df.to_sql('ventas', con=engine, if_exists='replace', index=False)

print("¡Listo! todo guardado en la base de datos")