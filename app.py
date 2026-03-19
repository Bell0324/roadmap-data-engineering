import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine 

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Sales Dashboard 2026", layout="wide")

# --- 2. ENCABEZADO ---
st.title("🚀 Sales Performance Dashboard")
st.markdown("### Conexión Directa a Base de Datos SQL")

# --- 3. CONEXIÓN A SQL ---
engine = create_engine('sqlite:///mi_empresa.db')

# Filtramos desde la base para ser más eficientes
query = "SELECT * FROM ventas WHERE monto > 10"
df = pd.read_sql(query, engine)

# --- ESCUDO CONTRA ERRORES (NaT) ---
# 1. Convertimos a fecha, si algo falla lo marcamos como NaT (vacío)
df["fecha"] = pd.to_datetime(df["fecha"], errors='coerce')

# 2. Borramos las filas que tengan la fecha vacía para que el calendario no falle
df = df.dropna(subset=["fecha"])

# 3. Si por alguna razón la tabla quedó vacía tras la limpieza, avisamos
if df.empty:
    st.warning("⚠️ No hay datos que coincidan con los filtros de SQL.")
    st.stop()

# --- 4. BARRA LATERAL ---
st.sidebar.header("Opciones de Filtro")

# Filtro de Vendedor
vendedor = st.sidebar.multiselect(
    "Selecciona Colaborador:",
    options=df["nombre_limpio"].unique(),
    default=df["nombre_limpio"].unique()
)

# Filtro de Fecha (Ahora seguro porque ya no hay NaT)
start_date = st.sidebar.date_input("Fecha Inicio", df["fecha"].min())
end_date = st.sidebar.date_input("Fecha Fin", df["fecha"].max())

# --- 5. LÓGICA DE FILTRADO ---
df_selection = df.query(
    "nombre_limpio == @vendedor & fecha >= @start_date & fecha <= @end_date"
)

# --- 6. MÉTRICAS (KPIs) ---
st.subheader("Indicadores Clave")
col1, col2 = st.columns(2)

total_sales = df_selection["monto"].sum()
total_transactions = len(df_selection)

with col1:
    st.metric(label="Ingresos Totales", value=f"${total_sales:,.2f}")
with col2:
    st.metric(label="Total de Transacciones", value=total_transactions)

# --- 7. GRÁFICAS Y TABLA ---
left_column, right_column = st.columns(2)

with left_column:
    st.subheader("Ventas por Colaborador")
    fig_bar = px.bar(
        df_selection, x='nombre_limpio', y='monto', color='monto',
        color_continuous_scale='Viridis', template='plotly_dark'
    )
    st.plotly_chart(fig_bar)

with right_column:
    st.subheader("Vista Previa de Datos")
    st.dataframe(df_selection)

# --- 8. TENDENCIA TEMPORAL ---
st.subheader("Tendencia de Ventas en el Tiempo")
df_trend = df_selection.groupby('fecha')['monto'].sum().reset_index()

fig_line = px.line(
    df_trend, x='fecha', y='monto',
    title="<b>Ingresos Diarios</b>",
    markers=True, template='plotly_dark',
    line_shape='spline',
    color_discrete_sequence=['#00CC96']
)
st.plotly_chart(fig_line)

# --- CIERRE ---
st.markdown("---")
st.write("Sistema desarrollado por **Belén Abigail Acuña** | Ingeniería de Datos 2026")