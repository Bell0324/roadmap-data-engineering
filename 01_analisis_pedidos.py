import sqlite3

# Creamos una base de datos en la memoria de tu PC
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# 1. Creamos la tabla de Usuarios (Dimension)
cursor.execute('''
CREATE TABLE usuarios (
    id_usuario INTEGER PRIMARY KEY,
    nombre TEXT,
    ciudad TEXT
)
''')

# 2. Creamos la tabla de Pedidos (Fact)
cursor.execute('''
CREATE TABLE pedidos (
    id_pedido INTEGER PRIMARY KEY,
    id_usuario INTEGER,
    monto DECIMAL,
    FOREIGN KEY (id_usuario) REFERENCES usuarios (id_usuario)
)
''')

# Insertamos datos de prueba
cursor.execute("INSERT INTO usuarios VALUES (1, 'Bell', 'Ciudad de México')")
cursor.execute("INSERT INTO pedidos VALUES (1001, 1, 250.50)")
cursor.execute("INSERT INTO pedidos VALUES (1002, 1, 100.00)")

# ESTA ES LA CONSULTA QUE TRAE LOS DATOS
query = '''
SELECT u.nombre, p.id_pedido, p.monto
FROM usuarios u
JOIN pedidos p ON u.id_usuario = p.id_usuario
'''

for row in cursor.execute(query):
    print(row)