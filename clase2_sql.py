import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('sqlite:///mi_empresa.db')

# 1. Creamos los datos de los colaboradores, una nueva tabla
# Imaginndo que Bell y Charlie ahora tienen "puestos" y "sucursales"
data_colaboradores = {
    'id_vendedor': [1, 2, 3],
    'nombre': ['Bell', 'Alex', 'Charlie'],
    'puesto': ['Data Engineer Senior', 'Sales Specialist', 'Junior Developer'],
    'sucursal': ['Heredia', 'San José', 'Alajuela']
}

df_colab = pd.DataFrame(data_colaboradores)

# 2. Guardamos esta nueva tabla en la base de datos
df_colab.to_sql('colaboradores', con=engine, if_exists='replace', index=False)

print("✅ Tabla 'colaboradores' creada con éxito.")