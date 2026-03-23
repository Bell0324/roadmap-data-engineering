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

# Traemos los datos (SELECT inicial)
query = "SELECT * FROM ventas WHERE monto > 10"
df = pd.read_sql(query, engine)

# --- ESCUDO CONTRA ERRORES (NaT) ---
df["fecha"] = pd.to_datetime(df["fecha"], errors='coerce')
df = df.dropna(subset=["fecha"])

if df.empty:
    st.warning("⚠️ No hay datos que coincidan con los filtros de SQL.")
    st.stop()

# --- 4. BARRA LATERAL (Filtros y Formulario) ---
st.sidebar.header("Opciones de Filtro")

# Filtro de Vendedor e Intervalo de Fecha
vendedor = st.sidebar.multiselect(
    "Selecciona Colaborador:",
    options=df["nombre_limpio"].unique(),
    default=df["nombre_limpio"].unique()
)

start_date = st.sidebar.date_input("Fecha Inicio", df["fecha"].min())
end_date = st.sidebar.date_input("Fecha Fin", df["fecha"].max())

# --- FORMULARIO PARA AGREGAR VENTAS (Escritura) ---
st.sidebar.markdown("---")
st.sidebar.header("➕ Añadir Nueva Venta")

with st.sidebar.form("nueva_venta_form", clear_on_submit=True):
    nuevo_vendedor = st.selectbox("Colaborador", options=df["nombre_limpio"].unique())
    nuevo_monto = st.number_input("Monto ($)", min_value=0.0, step=10.0)
    nueva_fecha = st.date_input("Fecha de Venta")
    
    submit_button = st.form_submit_button("Guardar Venta")

if submit_button:
    # Lógica para INSERTAR en SQL
    nuevo_registro = pd.DataFrame({
        'nombre_limpio': [nuevo_vendedor],
        'monto': [nuevo_monto],
        'fecha': [pd.to_datetime(nueva_fecha)]
    })
    # Guardamos en la BD
    nuevo_registro.to_sql('ventas', con=engine, if_exists='append', index=False)
    st.sidebar.success(f"✅ ¡Venta de {nuevo_vendedor} guardada!")
    st.rerun() # Recargamos para que se vea en las gráficas y auditoría

# --- 5. LÓGICA DE FILTRADO (Para las gráficas) ---
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

# --- 9. AUDITORÍA: ÚLTIMAS VENTAS REGISTRADAS ---
st.markdown("---")
st.subheader("🕵️ Auditoría: Últimos Registros en Base de Datos")

query_audit = "SELECT * FROM ventas ORDER BY rowid DESC LIMIT 5"
df_audit = pd.read_sql(query_audit, engine)

if not df_audit.empty:
    st.table(df_audit)
else:
    st.write("Aún no hay registros recientes.")

# --- CIERRE ---
st.markdown("---")
st.write("Sistema desarrollado por **Belén Abigail Acuña** | Ingeniería de Datos 2026")