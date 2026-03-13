import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración
st.set_page_config(page_title="Sales Performance Dashboard", layout="wide")

# 2. Encabezado
st.title("📊 Interactive Sales Performance Dashboard")
st.markdown("### Data Visualization for Process Optimization")

# 3. Carga de datos
df = pd.read_csv('ventas_limpias.csv')

# --- NOTA: Asegúrate de que 'fecha' existe en tu CSV ---
if 'fecha' in df.columns:
    df["fecha"] = pd.to_datetime(df["fecha"])
else:
    # Si no existe, creamos una fecha falsa para que no falle
    df["fecha"] = pd.to_datetime("2026-03-12")

# 4. SIDEBAR (Definimos los filtros PRIMERO)
st.sidebar.header("Filter Options")

# Filtro de Vendedor
vendedor = st.sidebar.multiselect(
    "Select Collaborator:",
    options=df["nombre_limpio"].unique(),
    default=df["nombre_limpio"].unique()
)

# Filtro de Fecha
start_date = st.sidebar.date_input("Start Date", df["fecha"].min())
end_date = st.sidebar.date_input("End Date", df["fecha"].max())

# 5. LÓGICA DE FILTRADO (Ahora que ya tenemos las variables)
df_selection = df.query(
    "nombre_limpio == @vendedor & fecha >= @start_date & fecha <= @end_date"
)

# 6. Métricas (KPIs)
st.subheader("Key Performance Indicators")
col1, col2 = st.columns(2)
total_sales = df_selection["monto"].sum()
total_transactions = len(df_selection)

with col1:
    st.metric(label="Total Sales Revenue ($)", value=f"${total_sales:,.2f}")
with col2:
    st.metric(label="Number of Transactions", value=total_transactions)

# 7. Visualizaciones
left_column, right_column = st.columns(2)

with left_column:
    st.subheader("Sales by Collaborator")
    fig_bar = px.bar(
        df_selection, x='nombre_limpio', y='monto', color='monto',
        color_continuous_scale='Viridis', template='plotly_dark'
    )
    st.plotly_chart(fig_bar, width="stretch")

with right_column:
    st.subheader("Data Preview")
    st.dataframe(df_selection, width="stretch")

# 8. Gráfica de Tendencia Temporal
st.subheader("Sales Trend Over Time")

# Agrupamos las ventas por fecha para que la línea no se vea quebrada
df_trend = df_selection.groupby('fecha')['monto'].sum().reset_index()

fig_line = px.line(
    df_trend,
    x='fecha',
    y='monto',
    title="<b>Daily Revenue Trend</b>",
    markers=True, # Pone puntitos en cada venta
    template='plotly_dark',
    line_shape='spline', # Hace la línea curva y elegante
    color_discrete_sequence=['#00CC96'] # Un color verde neón profesional
)

st.plotly_chart(fig_line, width="stretch")

st.markdown("---")
st.write("Built by **Belén Abigail Acuña**")