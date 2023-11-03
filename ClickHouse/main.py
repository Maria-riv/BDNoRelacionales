import pandas as pd
from clickhouse_driver import Client

data = {
    'fecha': ['2022-01-01'] * 5000 + ['2022-01-02'] * 5000 + ['2022-01-03'] * 5000,
    'producto': ['Producto A'] * 5000 + ['Producto B'] * 5000 + ['Producto C'] * 5000,
    'cantidad': [i for i in range(1, 15001)],
    'precio_por_unidad': [10] * 5000 + [15] * 5000 + [20] * 5000
}
df = pd.DataFrame(data)

# Conectarse a ClickHouse
client = Client(host='localhost')

# Tabla de ejemplo en ClickHouse
client.execute('''
    CREATE TABLE IF NOT EXISTS ventas (
        fecha Date,
        producto String,
        cantidad UInt32,
        precio_por_unidad UInt32
    ) ENGINE = MergeTree() ORDER BY fecha
''')

# Insertar datos del DataFrame a ClickHouse
client.execute('INSERT INTO ventas (fecha, producto, cantidad, precio_por_unidad) VALUES', df.to_dict('records'))

# Consultar datos de ClickHouse y cargar en un DataFrame
df2 = pd.DataFrame(client.execute('SELECT * FROM ventas'))

# Renombrar las columnas del DataFrame obtenido
df2.columns = ['fecha', 'producto', 'cantidad', 'precio_por_unidad']

# Muestra el DataFrame
print("DataFrame completo:")
print(df2)
print()

# Acceso a una columna específica
columna_producto = df2['producto']
print("Columna 'producto':")
print(columna_producto)
print()

# Acceso a múltiples columnas
columnas_seleccionadas = df2[['fecha', 'cantidad']]
print("Columnas 'fecha' y 'cantidad':")
print(columnas_seleccionadas)
print()

# Acceso a una fila específica basada en una condición
ventas_producto_a = df2[df2['producto'] == 'Producto A']
print("Ventas del Producto A:")
print(ventas_producto_a)
print()

# Acceso a múltiples columnas con una condición
ventas_producto_b_cantidad = df2[df2['producto'] == 'Producto B'][['producto', 'cantidad']]
print("Ventas del Producto B con columnas 'producto' y 'cantidad':")
print(ventas_producto_b_cantidad)
print()
