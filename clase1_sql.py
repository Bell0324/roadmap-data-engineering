import sqlite3

# 1. Establecemos la conexión (la base de datos vive en la memoria RAM)
conn = sqlite3.connect(':memory:')

# 2. CREAMOS EL CURSOR (Este era el paso que faltaba o estaba en el lugar equivocado)
cursor = conn.cursor()

# 3. Ahora sí podemos usarlo para crear las tablas
cursor.execute('CREATE TABLE usuarios (id INTEGER, nombre TEXT, ciudad TEXT)')
cursor.execute('CREATE TABLE pedidos (id_p INTEGER, id_u INTEGER, monto REAL)')

# 4. Insertamos los datos
cursor.execute("INSERT INTO usuarios VALUES (1, 'Bell', 'Ciudad de México'), (2, 'Alex', 'Bogotá')")
cursor.execute("INSERT INTO pedidos VALUES (100, 1, 250.50)")

# 5. El Query con LEFT JOIN
query = '''
SELECT u.nombre, u.ciudad, COALESCE(p.monto, 0.0)
FROM usuarios u
LEFT JOIN pedidos p ON u.id = p.id_u
'''

print("--- Reporte de Ventas ---")
for row in cursor.execute(query):
    print(row)