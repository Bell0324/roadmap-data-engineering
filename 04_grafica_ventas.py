import pandas as pd
import plotly.express as px

# 1. Cargamos los datos que ya limpiaste con éxito
df = pd.read_csv('ventas_limpias.csv')

# 2. Creamos una gráfica de barras interactiva
fig = px.bar(df, 
             x='nombre_limpio', 
             y='monto', 
             title='Visualización de Ventas: Reporte Diario',
             color='monto', 
             color_continuous_scale='Reds',
             labels={'nombre_limpio': 'Vendedor', 'monto': 'Total Vendido ($)'},
             template='plotly_dark')

# 3. Guardamos la gráfica como una web interactiva
fig.write_html("mi_reporte.html")

print("🚀 ¡Gráfica generada con éxito! Revisa tu carpeta y abre 'mi_reporte.html'")
fig.show()