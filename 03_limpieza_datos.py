import pandas as pd

# 1. Cargamos los datos originales (Asegúrate que ventas.csv tenga una columna 'fecha')
df = pd.read_csv('ventas.csv')

# 2. PROCESO DE LIMPIEZA
df['nombre_limpio'] = df['nombre_sucio'].str.strip().str.capitalize()

# 3. SELECCIÓN: ¡Aquí agregamos 'fecha'!
# Asegúrate de escribirlo exactamente como aparece en tu ventas.csv (ej: 'fecha' o 'Fecha')
df_final = df[['id_p', 'id_u', 'nombre_limpio', 'monto', 'fecha']] 

# 4. Guardamos
# ... después de limpiar el nombre ...
df_final = df[['id_p', 'id_u', 'nombre_limpio', 'monto', 'fecha']]
df_final.to_csv('ventas_limpias.csv', index=False)