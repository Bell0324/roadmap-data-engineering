import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine 

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Sales Dashboard 2026", layout="wide")

# --- 2. CONEXIÓN Y LÓGICA DE DATOS (ETL) ---
engine = create_engine('sqlite:///mi_empresa.db')

@st.cache_data
def load_and_clean_data(_engine):
    query = """
    SELECT v.*, c.puesto, c.sucursal 
    FROM ventas v
    LEFT JOIN colaboradores c ON v.nombre_limpio = c.nombre
    WHERE v.monto > 0
    """
    data = pd.read_sql(query, _engine)
    
    # 💡 CORRECCIÓN CRÍTICA: Convertimos a datetime y luego a DATE puro
    # Esto asegura que el filtro de la línea 68 funcione correctamente.
    data["fecha"] = pd.to_datetime(data["fecha"], errors='coerce').dt.date
    
    # Eliminamos filas sin fecha si las hubiera
    data = data.dropna(subset=["fecha"])
    
    return data

# Cargamos los datos
df = load_and_clean_data(engine)

if df.empty:
    st.warning("⚠️ No se encontraron datos válidos.")
    st.stop()

# --- 3. BARRA LATERAL (Filtros y Formulario) ---
st.sidebar.title("🚀 Panel de Control")

vendedor = st.sidebar.multiselect(
    "Selecciona Colaborador:",
    options=df["nombre_limpio"].unique(),
    default=df["nombre_limpio"].unique()
)

start_date = st.sidebar.date_input("Fecha Inicio", df["fecha"].min())
end_date = st.sidebar.date_input("Fecha Fin", df["fecha"].max())

st.sidebar.markdown("---")
st.sidebar.header("➕ Registro de Nueva Venta")

with st.sidebar.form("nueva_venta_form", clear_on_submit=True):
    nuevo_vendedor = st.selectbox("Colaborador", options=df["nombre_limpio"].unique())
    nuevo_monto = st.number_input("Monto ($)", min_value=0.01, step=10.0)
    nueva_fecha = st.date_input("Fecha de Venta")
    submit_button = st.form_submit_button("Guardar en SQL")

if submit_button:
    nuevo_registro = pd.DataFrame({
        'nombre_limpio': [nuevo_vendedor],
        'monto': [nuevo_monto],
        'fecha': [pd.to_datetime(nueva_fecha)]
    })
    nuevo_registro.to_sql('ventas', con=engine, if_exists='append', index=False)
    
    # Limpiamos caché para actualizar gráficas
    st.cache_data.clear()
    
    st.sidebar.success(f"✅ Registro exitoso: {nuevo_vendedor}")
    st.rerun()

# --- 4. FILTRADO FINAL ---
# Ahora que df['fecha'] y start_date son del mismo tipo, esto funcionará:
df_selection = df.query(
    "nombre_limpio == @vendedor & fecha >= @start_date & fecha <= @end_date"
)

# --- 5. VISUALIZACIÓN DE MÉTRICAS (KPIs) ---
st.title("📊 Sales Intelligence Dashboard")
st.markdown("### Análisis de Desempeño y Auditoría Relacional")

m_col1, m_col2, m_col3 = st.columns(3)
with m_col1:
    st.metric("Ingresos Totales", f"${df_selection['monto'].sum():,.2f}")
with m_col2:
    st.metric("Transacciones", len(df_selection))
with m_col3:
    promedio = df_selection['monto'].mean() if not df_selection.empty else 0
    st.metric("Promedio de Venta", f"${promedio:,.2f}")

# --- 6. GRÁFICAS PRINCIPALES ---
st.markdown("---")
g_col1, g_col2 = st.columns(2)

with g_col1:
    st.subheader("Ventas por Colaborador")
    fig_bar = px.bar(
        df_selection, x='nombre_limpio', y='monto', color='monto',
        color_continuous_scale='Viridis', template='plotly_dark'
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with g_col2:
    st.subheader("Distribución por Sucursal")
    df_suc = df_selection.groupby("sucursal")["monto"].sum().reset_index()
    fig_pie = px.pie(df_suc, values='monto', names='sucursal', hole=0.4, template='plotly_dark')
    st.plotly_chart(fig_pie, use_container_width=True)

# --- 7. TENDENCIA Y AUDITORÍA ---
st.markdown("---")
st.subheader("📈 Tendencia Temporal")
df_trend = df_selection.groupby('fecha')['monto'].sum().reset_index()
fig_line = px.line(df_trend, x='fecha', y='monto', markers=True, template='plotly_dark')
st.plotly_chart(fig_line, use_container_width=True)

st.markdown("---")
with st.expander("🕵️ Ver Auditoría de los Últimos 5 Registros"):
    query_audit = "SELECT * FROM ventas ORDER BY rowid DESC LIMIT 5"
    st.table(pd.read_sql(query_audit, engine))

st.markdown("---")
st.caption(f"© 2026 Belén Abigail Acuña | Ingeniería de Sistemas | Pipeline AI-Ready")