import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Sales Dashboard 2026", layout="wide")

# --- 2. CONEXIÓN Y LÓGICA DE DATOS (ETL) ---
# Creamos el motor de conexión al inicio
engine = create_engine('sqlite:///mi_empresa.db')

@st.cache_data
def load_and_clean_data(_engine):
    # 1. Traemos los datos de ventas
    query = "SELECT * FROM ventas"
    data = pd.read_sql(query, _engine)
    
    # 2. LIMPIEZA DE FECHAS (La clave del éxito)
    # Cortamos el texto para quitar los ceros sobrantes antes de convertir
    data['fecha'] = data['fecha'].astype(str).str.split(" ").str[0]
    data['fecha'] = pd.to_datetime(data['fecha'], errors='coerce').dt.date
    
    # 3. SEGURIDAD PARA 'SUCURSAL'
    # Si la columna no existe (porque es un SELECT * de ventas), la creamos vacía
    if 'sucursal' not in data.columns:
        data['sucursal'] = 'General'
    
    # 4. Limpieza de nombres y montos
    data['nombre_limpio'] = data['nombre_limpio'].astype(str).str.strip()
    data['monto'] = pd.to_numeric(data['monto'], errors='coerce').fillna(0)
    
    # 5. Quitamos filas sin fecha
    data = data.dropna(subset=['fecha'])
    
    return data

# Ejecutamos la carga inicial
df = load_and_clean_data(engine)

if df.empty:
    st.warning("⚠️ No se encontraron datos válidos en la base de datos.")
    st.stop()

# --- 3. BARRA LATERAL (Filtros y Formulario) ---
st.sidebar.title("🚀 Panel de Control")

# Diagnóstico rápido en la barra lateral (solo para ti)
st.sidebar.info(f"Registros totales en DB: {len(df)}")

vendedor = st.sidebar.multiselect(
    "Selecciona Colaborador:",
    options=sorted(df["nombre_limpio"].unique()),
    default=df["nombre_limpio"].unique()
)

# Rango de fechas basado en los datos reales
start_date = st.sidebar.date_input("Fecha Inicio", df["fecha"].min())
end_date = st.sidebar.date_input("Fecha Fin", df["fecha"].max())

st.sidebar.markdown("---")
st.sidebar.header("➕ Registro de Nueva Venta")

with st.sidebar.form("nueva_venta_form", clear_on_submit=True):
    nuevo_vendedor = st.selectbox("Colaborador", options=sorted(df["nombre_limpio"].unique()))
    nuevo_monto = st.number_input("Monto ($)", min_value=0.01, step=10.0)
    nueva_fecha = st.date_input("Fecha de Venta")
    submit_button = st.form_submit_button("Guardar en SQL")

if submit_button:
    # Preparamos el nuevo registro
    nuevo_registro = pd.DataFrame({
        'nombre_limpio': [nuevo_vendedor],
        'monto': [nuevo_monto],
        # Guardamos como objeto date puro para que coincida con el resto
        'fecha': [pd.to_datetime(nueva_fecha).date()] 
    })
    
    # Insertamos en la tabla 'ventas'
    nuevo_registro.to_sql('ventas', con=engine, if_exists='append', index=False)
    
    # 🔥 CRÍTICO: Limpiamos la caché para que el Dashboard lea los nuevos datos
    st.cache_data.clear()
    st.sidebar.success(f"✅ ¡Venta de {nuevo_vendedor} guardada!")
    st.rerun()

# --- 4. FILTRADO DE DATOS (Lógica de Negocio) ---
# Usamos una máscara booleana, que es más estable que .query() para fechas
mask = (
    df["nombre_limpio"].isin(vendedor) & 
    (df["fecha"] >= start_date) & 
    (df["fecha"] <= end_date)
)
df_selection = df.loc[mask]

# --- 5. VISUALIZACIÓN DE MÉTRICAS (KPIs) ---
st.title("📊 Sales Intelligence Dashboard")
st.markdown("### Análisis de Desempeño y Auditoría Relacional")

if not df_selection.empty:
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.metric("Ingresos Totales", f"${df_selection['monto'].sum():,.2f}")
    with m_col2:
        st.metric("Transacciones", len(df_selection))
    with m_col3:
        st.metric("Promedio de Venta", f"${df_selection['monto'].mean():,.2f}")

    # --- 6. GRÁFICAS PRINCIPALES ---
    st.markdown("---")
    g_col1, g_col2 = st.columns(2)

    with g_col1:
        st.subheader("Ventas por Colaborador")
        fig_bar = px.bar(
            df_selection, x='nombre_limpio', y='monto', 
            color='monto', color_continuous_scale='Viridis',
            template='plotly_dark'
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with g_col2:
        st.subheader("Distribución por Sucursal")
        # Rellenamos sucursales vacías para que la gráfica no falle
        df_selection["sucursal"] = df_selection["sucursal"].fillna("Sin Asignar")
        df_suc = df_selection.groupby("sucursal")["monto"].sum().reset_index()
        fig_pie = px.pie(
            df_suc, values='monto', names='sucursal', 
            hole=0.4, template='plotly_dark'
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # Gráfica de tendencia
    st.markdown("---")
    st.subheader("📈 Tendencia Temporal de Ventas")
    df_trend = df_selection.groupby('fecha')['monto'].sum().reset_index()
    fig_line = px.line(
        df_trend, x='fecha', y='monto', 
        markers=True, template='plotly_dark'
    )
    st.plotly_chart(fig_line, use_container_width=True)

else:
    st.error("🚫 No hay datos para los filtros seleccionados. Prueba ampliando el rango de fechas.")

# --- 7. AUDITORÍA FINAL ---
st.markdown("---")
with st.expander("🕵️ Ver Auditoría de los Últimos 5 Registros Reales"):
    # Leemos directo de la base de datos sin filtros para verificar ingresos
    query_audit = "SELECT * FROM ventas ORDER BY rowid DESC LIMIT 5"
    st.table(pd.read_sql(query_audit, engine))

st.caption("© 2026 Belén Abigail Acuña | Ingeniería de Sistemas | Pipeline AI-Ready")