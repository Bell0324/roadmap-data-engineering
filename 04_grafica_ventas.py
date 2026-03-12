import pandas as pd
import plotly.express as px

# 1. Cargamos los datos que ya limpiaste con éxito
df = pd.read_csv('ventas_limpias.csv')

# 2. Creamos una gráfica de barras interactiva
fig_bar = px.bar(
        df,  # Cambiado de df_selection a df
        x='nombre_limpio',
        y='monto',
        color='nombre_limpio', 
        color_discrete_sequence=px.colors.qualitative.Pastel, 
        template='plotly_dark',
        title="<b>Sales Distribution by Team Member</b>",
        labels={'nombre_limpio': 'Collaborator', 'monto': 'Total Revenue ($)'}
    )

# Esto quita la leyend de la derecha para que la gráfica tenga más espacio
fig_bar.update_layout(showlegend=False)

# 3. Guardamos la gráfica como una web interactiva
# Cambiado de fig a fig_bar
fig_bar.write_html("mi_reporte.html")

print("¡Gráfica generada con éxito! Revisa tu carpeta y abre 'mi_reporte.html'")

# Mostramos la gráfica
fig_bar.show()