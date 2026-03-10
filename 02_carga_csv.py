import sqlite3
import pandas as pd
import os

# 1. Verificamos si existe el archivo de datos
if not os.path.exists('ventas.csv'):
    print("❌ Error: No encuentro el archivo 'ventas.csv'. Créalo primero.")
else:
    # 2. Conexión y preparación de base de datos
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE usuarios (id INTEGER, nombre TEXT)')
    cursor.execute("INSERT INTO usuarios VALUES (1, 'Bell'), (2, 'Alex'), (3, 'Charlie')")

    # 3. EXTRACCIÓN: Leemos el CSV
    df_ventas = pd.read_csv('ventas.csv')

    # 4. CARGA: Pasamos los datos a SQL
    df_ventas.to_sql('pedidos', conn, index=False, if_exists='replace')

    # 5. TRANSFORMACIÓN: Reporte final
    query = '''
    SELECT u.nombre, SUM(p.monto) as total
    FROM usuarios u
    JOIN pedidos p ON u.id = p.id_u
    GROUP BY u.nombre
    '''

    print("--- 🚀 Reporte Automatizado desde CSV ---")
    for row in cursor.execute(query):
        print(row)