import pandas as pd

# 1. Cargamos los datos originales
df = pd.read_csv('ventas.csv')

print("--- 📋 Datos Originales (Sucios) ---")
print(df)

# 2. PROCESO DE LIMPIEZA
# .str.strip() -> Borra espacios invisibles al principio y al final
# .str.capitalize() -> Pone la primera letra en Mayúscula y el resto en minúscula
df['nombre_limpio'] = df['nombre_sucio'].str.strip().str.capitalize()

# 3. Seleccionamos solo lo que queremos en nuestro reporte final
df_final = df[['id_p', 'id_u', 'nombre_limpio', 'monto']]

print("\n--- ✨ Datos Transformados (Limpios) ---")
print(df_final)

# 4. Guardamos el resultado en un nuevo archivo para el siguiente paso
df_final.to_csv('ventas_limpias.csv', index=False)
print("\n✅ ¡Archivo 'ventas_limpias.csv' generado con éxito!")