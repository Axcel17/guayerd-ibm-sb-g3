"""
Dashboard Interactivo de Análisis de Ventas
============================================
Sistema de reportería dinámica para análisis de clientes, productos y ventas
Creado con Streamlit
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from io import BytesIO
import warnings
warnings.filterwarnings('ignore')

# =============================
# CONFIGURACIÓN DE LA PÁGINA
# =============================
st.set_page_config(
    page_title="Dashboard de Ventas - Minimarket",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================
# FUNCIONES DE CARGA DE DATOS
# =============================
@st.cache_data
def cargar_datos():
    """Carga y prepara todos los datos necesarios para el dashboard"""
    try:
        # Cargar archivos base
        df_clientes = pd.read_csv(r"data/raw/clientes.csv")
        df_productos = pd.read_csv(r"data/raw/productos.csv")
        df_ventas = pd.read_csv(r"data/raw/ventas.csv")
        df_detalle = pd.read_csv(r"data/raw/detalle_ventas.csv")
        
        # Limpieza de datos
        df_clientes['fecha_alta'] = pd.to_datetime(df_clientes['fecha_alta'])
        df_clientes = df_clientes.drop_duplicates(subset=['id_cliente'], keep='first')
        
        df_ventas['fecha'] = pd.to_datetime(df_ventas['fecha'])
        df_ventas = df_ventas.drop_duplicates(subset=['id_venta'], keep='first')
        
        df_productos['precio_unitario'] = pd.to_numeric(df_productos['precio_unitario'], errors='coerce')
        df_productos = df_productos.drop_duplicates(subset=['id_producto'], keep='first')
        
        df_detalle['importe'] = pd.to_numeric(df_detalle['importe'], errors='coerce')
        df_detalle['cantidad'] = pd.to_numeric(df_detalle['cantidad'], errors='coerce')
        
        # Crear dataframe consolidado - evitar columnas duplicadas
        # Primero eliminar nombre_cliente de df_ventas si existe para evitar duplicados
        ventas_cols = [col for col in df_ventas.columns if col != 'nombre_cliente']
        df_ventas_limpio = df_ventas[ventas_cols]
        
        df_ventas_clientes = df_ventas_limpio.merge(df_clientes[['id_cliente', 'nombre_cliente', 'ciudad']], on='id_cliente', how='left')
        df_ventas_detalle = df_ventas_clientes.merge(df_detalle[['id_venta', 'id_producto', 'importe', 'cantidad']], on='id_venta', how='left')
        df_consolidado = df_ventas_detalle.merge(df_productos[['id_producto', 'nombre_producto', 'categoria', 'precio_unitario']], on='id_producto', how='left')
        
        # Calcular RFM
        snapshot_date = df_ventas['fecha'].max() + pd.Timedelta(days=1)
        df_rfm_base = df_ventas.merge(
            df_detalle.groupby('id_venta')['importe'].sum().reset_index().rename(columns={'importe': 'total_venta'}),
            on='id_venta'
        )
        
        df_rfm = df_rfm_base.groupby('id_cliente').agg(
            Recencia=('fecha', lambda x: (snapshot_date - x.max()).days),
            Frecuencia=('id_venta', 'count'),
            Monetario=('total_venta', 'sum')
        ).reset_index()
        
        # Agregar nombre del cliente al RFM
        df_rfm = df_rfm.merge(df_clientes[['id_cliente', 'nombre_cliente', 'ciudad']], on='id_cliente', how='left')
        
        return df_consolidado, df_rfm, df_clientes, df_productos, df_ventas, df_detalle
    
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")
        return None, None, None, None, None, None

# =============================
# FUNCIONES DE ANÁLISIS
# =============================
def calcular_metricas_principales(df_consolidado):
    """Calcula las métricas KPI principales basadas en datos filtrados"""
    ventas_totales = df_consolidado['importe'].sum()
    num_transacciones = df_consolidado['id_venta'].nunique()
    num_clientes_activos = df_consolidado['id_cliente'].nunique()
    ticket_promedio = ventas_totales / num_transacciones if num_transacciones > 0 else 0
    
    return ventas_totales, num_transacciones, num_clientes_activos, ticket_promedio

def ventas_por_periodo(df_consolidado, periodo='D'):
    """Agrupa ventas por período temporal"""
    df_temp = df_consolidado.copy()
    df_temp['fecha'] = pd.to_datetime(df_temp['fecha'])
    ventas_periodo = df_temp.groupby(pd.Grouper(key='fecha', freq=periodo))['importe'].sum().reset_index()
    return ventas_periodo

def top_productos(df_consolidado, n=10, metrica='importe'):
    """Obtiene los top N productos por métrica especificada"""
    if metrica == 'importe':
        top = df_consolidado.groupby('nombre_producto')['importe'].sum().nlargest(n).reset_index()
    else:
        top = df_consolidado.groupby('nombre_producto')['cantidad'].sum().nlargest(n).reset_index()
    return top

def analisis_por_ciudad(df_consolidado):
    """Análisis de ventas por ciudad"""
    ciudad_stats = df_consolidado.groupby('ciudad').agg({
        'importe': 'sum',
        'id_venta': 'count',
        'cantidad': 'sum'
    }).reset_index()
    ciudad_stats.columns = ['ciudad', 'ventas_totales', 'num_transacciones', 'unidades_vendidas']
    ciudad_stats = ciudad_stats.sort_values('ventas_totales', ascending=False)
    return ciudad_stats

def calcular_rfm_filtrado(df_consolidado_filtrado):
    """Calcula RFM basado en datos filtrados"""
    if len(df_consolidado_filtrado) == 0:
        return pd.DataFrame()
    
    # Verificar columnas necesarias
    columnas_necesarias = ['fecha', 'id_cliente', 'id_venta', 'importe']
    for col in columnas_necesarias:
        if col not in df_consolidado_filtrado.columns:
            st.error(f"Error: Columna '{col}' no encontrada. Columnas disponibles: {df_consolidado_filtrado.columns.tolist()}")
            return pd.DataFrame()
    
    # Verificar si existen nombre_cliente y ciudad
    if 'nombre_cliente' not in df_consolidado_filtrado.columns or 'ciudad' not in df_consolidado_filtrado.columns:
        st.warning("⚠️ Advertencia: Las columnas 'nombre_cliente' o 'ciudad' no están disponibles en los datos filtrados.")
        st.info(f"Columnas disponibles: {df_consolidado_filtrado.columns.tolist()}")
    
    # Calcular fecha snapshot basada en datos filtrados
    snapshot_date = df_consolidado_filtrado['fecha'].max() + pd.Timedelta(days=1)
    
    # Crear un DataFrame auxiliar con la información única por venta
    columnas_venta = ['id_venta', 'fecha', 'id_cliente']
    if 'nombre_cliente' in df_consolidado_filtrado.columns:
        columnas_venta.append('nombre_cliente')
    if 'ciudad' in df_consolidado_filtrado.columns:
        columnas_venta.append('ciudad')
    
    df_ventas_unicas = df_consolidado_filtrado[columnas_venta].drop_duplicates(subset=['id_venta'])
    
    # Calcular total por venta
    ventas_totales = df_consolidado_filtrado.groupby('id_venta')['importe'].sum().reset_index()
    ventas_totales.columns = ['id_venta', 'total_venta']
    
    # Unir con información de ventas
    ventas_completas = df_ventas_unicas.merge(ventas_totales, on='id_venta', how='left')
    
    # Preparar agregación para RFM - definir el orden explícitamente
    agg_dict = {
        'fecha': ('fecha', lambda x: (snapshot_date - x.max()).days),
        'id_venta': ('id_venta', 'count'),
        'total_venta': ('total_venta', 'sum')
    }
    
    # Agregar nombre_cliente y ciudad si están disponibles
    if 'nombre_cliente' in ventas_completas.columns:
        agg_dict['nombre_cliente'] = ('nombre_cliente', 'first')
    if 'ciudad' in ventas_completas.columns:
        agg_dict['ciudad'] = ('ciudad', 'first')
    
    # Calcular métricas RFM por cliente
    df_rfm = ventas_completas.groupby('id_cliente').agg(**agg_dict).reset_index()
    
    # Renombrar las columnas de métricas RFM
    rename_dict = {
        'fecha': 'Recencia',
        'id_venta': 'Frecuencia',
        'total_venta': 'Monetario'
    }
    df_rfm = df_rfm.rename(columns=rename_dict)
    
    return df_rfm

def segmentacion_rfm(df_rfm):
    """Segmenta clientes según RFM en categorías"""
    if len(df_rfm) == 0:
        return pd.DataFrame()
    
    df_seg = df_rfm.copy()
    
    # Calcular cuartiles para segmentación
    df_seg['R_Score'] = pd.qcut(df_seg['Recencia'], 4, labels=[4, 3, 2, 1], duplicates='drop')
    df_seg['F_Score'] = pd.qcut(df_seg['Frecuencia'].rank(method='first'), 4, labels=[1, 2, 3, 4], duplicates='drop')
    df_seg['M_Score'] = pd.qcut(df_seg['Monetario'].rank(method='first'), 4, labels=[1, 2, 3, 4], duplicates='drop')
    
    df_seg['RFM_Score'] = (df_seg['R_Score'].astype(int) + df_seg['F_Score'].astype(int) + df_seg['M_Score'].astype(int)) / 3
    
    # Definir segmentos
    def clasificar_cliente(row):
        score = row['RFM_Score']
        if score >= 3.5:
            return "Campeones"
        elif score >= 3.0:
            return "Leales"
        elif score >= 2.5:
            return "Potenciales"
        elif score >= 2.0:
            return "En Riesgo"
        else:
            return "Inactivos"
    
    df_seg['Segmento'] = df_seg.apply(clasificar_cliente, axis=1)
    return df_seg

# =============================
# ESTILOS CSS PERSONALIZADOS
# =============================
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 30px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .insight-box {
        background-color: #f0f8ff;
        border-left: 5px solid #1f77b4;
        padding: 20px;
        margin: 15px 0;
        border-radius: 8px;
        color: #1a1a1a;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }
    .insight-box strong {
        color: #0d47a1;
    }
</style>
""", unsafe_allow_html=True)

# =============================
# CARGA DE DATOS
# =============================
df_consolidado, df_rfm, df_clientes, df_productos, df_ventas, df_detalle = cargar_datos()

if df_consolidado is None:
    st.stop()

# =============================
# SIDEBAR - FILTROS
# =============================
st.sidebar.header("Filtros de Análisis")

# Filtro de fechas
fecha_min = df_consolidado['fecha'].min().date()
fecha_max = df_consolidado['fecha'].max().date()

fecha_inicio = st.sidebar.date_input("Fecha Inicio", fecha_min, min_value=fecha_min, max_value=fecha_max)
fecha_fin = st.sidebar.date_input("Fecha Fin", fecha_max, min_value=fecha_min, max_value=fecha_max)

# Filtro de ciudad
ciudades = ['Todas'] + sorted(df_consolidado['ciudad'].dropna().unique().tolist())
ciudad_seleccionada = st.sidebar.selectbox("Seleccionar Ciudad", ciudades)

# Filtro de categoría
categorias = ['Todas'] + sorted(df_consolidado['categoria'].dropna().unique().tolist())
categoria_seleccionada = st.sidebar.selectbox("Seleccionar Categoría", categorias)

# Aplicar filtros
df_filtrado = df_consolidado.copy()
df_filtrado = df_filtrado[(df_filtrado['fecha'].dt.date >= fecha_inicio) & (df_filtrado['fecha'].dt.date <= fecha_fin)]

if ciudad_seleccionada != 'Todas':
    df_filtrado = df_filtrado[df_filtrado['ciudad'] == ciudad_seleccionada]

if categoria_seleccionada != 'Todas':
    df_filtrado = df_filtrado[df_filtrado['categoria'] == categoria_seleccionada]

# =============================
# HEADER PRINCIPAL
# =============================
st.markdown('<h1 class="main-header">Dashboard de Análisis de Ventas - Minimarket</h1>', unsafe_allow_html=True)
st.markdown(f"**Período analizado:** {fecha_inicio.strftime('%d/%m/%Y')} - {fecha_fin.strftime('%d/%m/%Y')}")
st.markdown("---")

# =============================
# SECCIÓN 1: MÉTRICAS PRINCIPALES (KPIs)
# =============================
st.header("Indicadores Clave de Rendimiento (KPIs)")

ventas_totales, num_transacciones, num_clientes_activos, ticket_promedio = calcular_metricas_principales(df_filtrado)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="💰 Ventas Totales (ARS)",
        value=f"${ventas_totales:,.2f}",
        delta=f"{(ventas_totales/1000):.1f}k"
    )

with col2:
    st.metric(
        label="🛒 Transacciones",
        value=f"{num_transacciones:,}",
        delta=f"{num_transacciones} ventas"
    )

with col3:
    st.metric(
        label="👥 Clientes Activos",
        value=f"{num_clientes_activos}",
        delta=f"{(num_clientes_activos/df_clientes.shape[0]*100):.1f}% del total"
    )

with col4:
    st.metric(
        label="🎯 Ticket Promedio (ARS)",
        value=f"${ticket_promedio:,.2f}",
        delta=f"por transacción"
    )

st.markdown("---")

# =============================
# SECCIÓN 2: EVOLUCIÓN TEMPORAL
# =============================
st.header("Evolución de las ventas")

col1, col2 = st.columns([3, 1])

with col2:
    periodo = st.radio(
        "Agrupar por:",
        ["Día", "Semana", "Mes"],
        index=1
    )
    
    periodo_map = {"Día": "D", "Semana": "W", "Mes": "M"}
    freq = periodo_map[periodo]

ventas_tiempo = ventas_por_periodo(df_filtrado, freq)

with col1:
    fig_tiempo = go.Figure()
    
    fig_tiempo.add_trace(go.Scatter(
        x=ventas_tiempo['fecha'],
        y=ventas_tiempo['importe'],
        mode='lines+markers',
        name='Ventas',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=8),
        fill='tonexty',
        fillcolor='rgba(31, 119, 180, 0.2)'
    ))
    
    # Línea de promedio
    promedio = ventas_tiempo['importe'].mean()
    fig_tiempo.add_hline(
        y=promedio,
        line_dash="dash",
        line_color="orange",
        annotation_text=f"Promedio: ARS ${promedio:,.0f}",
        annotation_position="right"
    )
    
    fig_tiempo.update_layout(
        title=f"Evolución de Ventas por {periodo}",
        xaxis_title="Fecha",
        yaxis_title="Ventas (ARS)",
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_tiempo, use_container_width=True)

# Insights automáticos
if len(ventas_tiempo) > 0:
    mejor_periodo = ventas_tiempo.loc[ventas_tiempo['importe'].idxmax()]
    peor_periodo = ventas_tiempo.loc[ventas_tiempo['importe'].idxmin()]

    st.markdown(f"""
    <div class="insight-box">
        <strong>💡 Insights:</strong><br>
        • Mejor {periodo.lower()}: {mejor_periodo['fecha'].strftime('%d/%m/%Y')} con ARS ${mejor_periodo['importe']:,.2f}<br>
        • Menor {periodo.lower()}: {peor_periodo['fecha'].strftime('%d/%m/%Y')} con ARS ${peor_periodo['importe']:,.2f}<br>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# =============================
# SECCIÓN 3: ANÁLISIS POR CIUDAD
# =============================
col_header1, col_header2 = st.columns([10, 1])
with col_header1:
    st.header("Análisis por Ciudad")
with col_header2:
    st.markdown("")  # Espaciado
    with st.popover("ℹ️"):
        st.markdown("""
        **Análisis por ciudad**
        
        Compara el rendimiento de ventas entre ciudades:
        - **Ventas Totales**: Ingresos por ubicación
        - **Transacciones**: Número de compras
        - **Ticket Promedio**: Gasto promedio por compra
        
        Identifica:
        - Ciudades con mejor desempeño
        - Oportunidades de crecimiento
        - Diferencias en comportamiento de compra
        """)

ciudad_stats = analisis_por_ciudad(df_filtrado)

col1, col2 = st.columns(2)

with col1:
    fig_ciudad_ventas = px.bar(
        ciudad_stats,
        x='ciudad',
        y='ventas_totales',
        title='Ventas Totales por Ciudad (ARS)',
        labels={'ventas_totales': 'Ventas (ARS)', 'ciudad': 'Ciudad'},
        color='ventas_totales',
        color_continuous_scale='Blues',
        text='ventas_totales'
    )
    fig_ciudad_ventas.update_traces(texttemplate='$%{text:,.0f}', textposition='inside')
    fig_ciudad_ventas.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_ciudad_ventas, use_container_width=True)

with col2:
    fig_ciudad_trans = px.pie(
        ciudad_stats,
        values='num_transacciones',
        names='ciudad',
        title='Distribución de Transacciones por Ciudad',
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_ciudad_trans.update_traces(textposition='inside', textinfo='percent+label')
    fig_ciudad_trans.update_layout(height=400)
    st.plotly_chart(fig_ciudad_trans, use_container_width=True)

# Tabla resumen
ciudad_stats_display = ciudad_stats.copy()
ciudad_stats_display['ventas_totales'] = ciudad_stats_display['ventas_totales'].apply(lambda x: f"ARS ${x:,.2f}")
ciudad_stats_display['ticket_promedio'] = (ciudad_stats['ventas_totales'] / ciudad_stats['num_transacciones']).apply(lambda x: f"ARS ${x:,.2f}")
ciudad_stats_display.columns = ['Ciudad', 'Ventas Totales', 'Transacciones', 'Unidades Vendidas', 'Ticket Promedio']
st.dataframe(ciudad_stats_display, use_container_width=True, hide_index=True)

st.markdown("---")

# =============================
# SECCIÓN 4: ANÁLISIS DE PRODUCTOS
# =============================
st.header("Análisis de Productos")

col1, col2 = st.columns(2)

with col1:
    n_productos = st.slider("Top N Productos:", 5, 20, 10)

with col2:
    metrica_prod = st.selectbox("Ordenar por:", ["Ingresos", "Cantidad Vendida"])

metrica = 'importe' if metrica_prod == "Ingresos" else 'cantidad'
top_prods = top_productos(df_filtrado, n=n_productos, metrica=metrica)

# Mostrar gráficos de productos en dos columnas
col1, col2 = st.columns(2)

with col1:
    fig_productos = px.bar(
        top_prods,
        y='nombre_producto',
        x=metrica,
        orientation='h',
        title=f'Top {n_productos} Productos por {metrica_prod}',
        labels={metrica: metrica_prod, 'nombre_producto': 'Producto'},
        color=metrica,
        color_continuous_scale='Viridis',
        text=metrica
    )

    if metrica == 'importe':
        fig_productos.update_traces(texttemplate='$%{text:,.0f}', textposition='inside')
    else:
        fig_productos.update_traces(texttemplate='%{text:,.0f} unid.', textposition='inside')

    fig_productos.update_layout(height=500, showlegend=False, yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_productos, use_container_width=True)

with col2:
    # Distribución por categoría con información detallada en hover
    categoria_stats = df_filtrado.groupby('categoria').agg({
        'importe': 'sum',
        'id_venta': 'nunique'
    }).reset_index()
    categoria_stats.columns = ['categoria', 'ventas_totales', 'num_transacciones']
    categoria_stats = categoria_stats.sort_values('ventas_totales', ascending=False)
    
    # Calcular métricas adicionales para el hover
    categoria_stats['ticket_promedio'] = categoria_stats['ventas_totales'] / categoria_stats['num_transacciones']
    categoria_stats['porcentaje'] = (categoria_stats['ventas_totales'] / categoria_stats['ventas_totales'].sum() * 100)
    
    # Crear texto de hover personalizado
    hover_text = []
    for _, row in categoria_stats.iterrows():
        text = (f"<b>{row['categoria']}</b><br><br>"
                f"<b>Ventas Totales:</b> ARS ${row['ventas_totales']:,.2f}<br>"
                f"<b>Porcentaje:</b> {row['porcentaje']:.1f}%<br>"
                f"<b>Transacciones:</b> {row['num_transacciones']:,.0f}<br>"
                f"<b>Ticket Promedio:</b> ARS ${row['ticket_promedio']:,.2f}")
        hover_text.append(text)
    
    # Usar go.Pie para mejor control
    fig_cat_pie = go.Figure(data=[go.Pie(
        labels=categoria_stats['categoria'],
        values=categoria_stats['ventas_totales'],
        hovertext=hover_text,
        hoverinfo='text',
        textposition='inside',
        textinfo='label+percent',
        marker=dict(colors=px.colors.qualitative.Set2)
    )])
    
    fig_cat_pie.update_layout(
        title='Distribución de Ventas por Categoría',
        height=500
    )
    st.plotly_chart(fig_cat_pie, use_container_width=True)

st.markdown("---")

# =============================
# SECCIÓN 5: ANÁLISIS DE MÉTODOS DE PAGO
# =============================
st.header("Análisis de Métodos de Pago")

df_ventas_filtradas = df_ventas[
    (df_ventas['fecha'].dt.date >= fecha_inicio) & 
    (df_ventas['fecha'].dt.date <= fecha_fin)
]

metodo_pago_stats = df_ventas_filtradas['medio_pago'].value_counts().reset_index()
metodo_pago_stats.columns = ['medio_pago', 'cantidad']

col1, col2 = st.columns(2)

with col1:
    fig_pago = px.bar(
        metodo_pago_stats,
        x='medio_pago',
        y='cantidad',
        title='Frecuencia de Métodos de Pago',
        labels={'cantidad': 'Número de Transacciones', 'medio_pago': 'Método de Pago'},
        color='cantidad',
        color_continuous_scale='Teal',
        text='cantidad'
    )
    fig_pago.update_traces(textposition='inside')
    fig_pago.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_pago, use_container_width=True)

with col2:
    # Método de pago por ciudad (top 3 ciudades)
    top_3_ciudades = ciudad_stats.head(3)['ciudad'].tolist()
    df_pago_ciudad = df_filtrado[df_filtrado['ciudad'].isin(top_3_ciudades)]
    
    pago_ciudad_stats = df_pago_ciudad.groupby(['ciudad', 'medio_pago']).size().reset_index(name='count')
    
    fig_pago_ciudad = px.bar(
        pago_ciudad_stats,
        x='ciudad',
        y='count',
        color='medio_pago',
        title='Métodos de Pago por Ciudad (Top 3)',
        labels={'count': 'Cantidad', 'ciudad': 'Ciudad', 'medio_pago': 'Método de Pago'},
        barmode='group'
    )
    fig_pago_ciudad.update_layout(height=400)
    st.plotly_chart(fig_pago_ciudad, use_container_width=True)

st.markdown("---")

# =============================
# SECCIÓN 6: SEGMENTACIÓN RFM
# =============================
col_header1, col_header2 = st.columns([10, 1])
with col_header1:
    st.header("Análisis RFM")
with col_header2:
    st.markdown("")  # Espaciado
    with st.popover("ℹ️"):
        st.markdown("""
        **¿Qué es RFM?**
        
        **Recency (Recencia)**: Días desde la última compra
        - ✅ Menor = Mejor (compró recientemente)
        - ❌ Mayor = Peor (hace tiempo que no compra)
        
        **Frequency (Frecuencia)**: Número de compras
        - ✅ Mayor = Mejor (cliente frecuente)
        - ❌ Menor = Peor (compra poco)
        
        **Monetary (Monetario)**: Gasto total
        - ✅ Mayor = Mejor (cliente valioso)
        - ❌ Menor = Peor (gasta poco)
        
        **Segmentos de clientes:**
        - **Campeones**: Los mejores clientes
        - **Leales**: Clientes constantes
        - **Potenciales**: Pueden mejorar
        - **En Riesgo**: Requieren atención
        - **Inactivos**: No compran hace tiempo
        """)

# Calcular RFM basado en datos filtrados
df_rfm_filtrado = calcular_rfm_filtrado(df_filtrado)

# Validar que hay datos
if len(df_rfm_filtrado) == 0:
    st.warning("⚠️ No hay datos suficientes para calcular el análisis RFM con los filtros aplicados.")
else:
    df_rfm_seg = segmentacion_rfm(df_rfm_filtrado)
    
    # KPIs RFM
    st.subheader("Métricas generales")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="🕐 Recencia Promedio",
            value=f"{df_rfm_filtrado['Recencia'].mean():.0f} días",
            delta=f"Min: {df_rfm_filtrado['Recencia'].min()} días",
            delta_color="inverse"  # Menor es mejor
        )

    with col2:
        st.metric(
            label="🔄 Frecuencia Promedio",
            value=f"{df_rfm_filtrado['Frecuencia'].mean():.1f} compras",
            delta=f"Max: {df_rfm_filtrado['Frecuencia'].max()} compras"
        )

    with col3:
        st.metric(
            label="💰 Gasto Promedio",
            value=f"ARS ${df_rfm_filtrado['Monetario'].mean():,.2f}",
            delta=f"Total: ARS ${df_rfm_filtrado['Monetario'].sum():,.0f}"
        )

    
    # Calcular métricas por segmento
    segmento_metricas = df_rfm_seg.groupby('Segmento').agg({
        'Recencia': 'mean',
        'Frecuencia': 'mean',
        'Monetario': 'mean',
        'id_cliente': 'count'
    }).reset_index()
    segmento_metricas.columns = ['Segmento', 'Recencia Promedio', 'Frecuencia Promedio', 'Gasto Promedio', 'Cantidad Clientes']
    
    # Calcular porcentaje
    total_clientes = segmento_metricas['Cantidad Clientes'].sum()
    segmento_metricas['Porcentaje'] = (segmento_metricas['Cantidad Clientes'] / total_clientes * 100)
    
    # Crear texto de hover personalizado
    hover_text = []
    for _, row in segmento_metricas.iterrows():
        text = (f"<b>{row['Segmento']}</b><br><br>"
                f"<b>Cantidad de Clientes:</b> {row['Cantidad Clientes']:,.0f}<br>"
                f"<b>Porcentaje:</b> {row['Porcentaje']:.1f}%<br><br>"
                f"<b>Recencia Promedio:</b> {row['Recencia Promedio']:.0f} días<br>"
                f"<b>Frecuencia Promedio:</b> {row['Frecuencia Promedio']:.1f} compras<br>"
                f"<b>Gasto Promedio:</b> ARS ${row['Gasto Promedio']:,.2f}")
        hover_text.append(text)
    
    # Gráfico de pie con información completa
    fig_seg_pie = go.Figure(data=[go.Pie(
        labels=segmento_metricas['Segmento'],
        values=segmento_metricas['Cantidad Clientes'],
        hovertext=hover_text,
        hoverinfo='text',
        textposition='inside',
        textinfo='label+percent',
        marker=dict(colors=px.colors.qualitative.Bold),
        hole=0.4
    )])
    
    fig_seg_pie.update_layout(
        title='Distribución de Segmentos de Clientes',
        height=450
    )
    st.plotly_chart(fig_seg_pie, use_container_width=True)
    
    # Tabla detallada de segmentos
    segmento_metricas_display = segmento_metricas.copy()
    segmento_metricas_display['Recencia Promedio'] = segmento_metricas_display['Recencia Promedio'].apply(lambda x: f"{x:.0f} días")
    segmento_metricas_display['Frecuencia Promedio'] = segmento_metricas_display['Frecuencia Promedio'].apply(lambda x: f"{x:.1f} compras")
    segmento_metricas_display['Gasto Promedio'] = segmento_metricas_display['Gasto Promedio'].apply(lambda x: f"ARS ${x:,.2f}")
    segmento_metricas_display['Porcentaje'] = segmento_metricas_display['Porcentaje'].apply(lambda x: f"{x:.1f}%")
    segmento_metricas_display = segmento_metricas_display[['Segmento', 'Cantidad Clientes', 'Porcentaje', 'Recencia Promedio', 'Frecuencia Promedio', 'Gasto Promedio']]
    st.dataframe(segmento_metricas_display, use_container_width=True, hide_index=True)

    # Gráficos de distribución RFM - Box plots con violin para mejor visualización
    col_header1, col_header2 = st.columns([10, 1])
    with col_header1:
        st.subheader("Distribuciones de métricas RFM por Segmento")
    with col_header2:
        st.markdown("")  # Espaciado
        with st.popover("ℹ️"):
            st.markdown("""
            **¿Cómo leer estos gráficos?**
            
            Cada figura combina dos visualizaciones:
            
            **Forma de violín:**
            - Muestra la distribución completa de los datos
            - La parte más ancha indica mayor concentración de clientes
            - Te permite ver la "forma" de tus datos
            
            **Box plot interno (caja):**
            - La línea central es la **mediana** (50% de los datos)
            - Los bordes de la caja son **Q1 y Q3** (25% y 75%)
            - Los bigotes muestran el rango de datos
            - Los puntos son **outliers** (valores atípicos)
            
            Pasa el mouse sobre el gráfico para ver estadísticos detallados.
            """)

    col1, col2, col3 = st.columns(3)

    with col1:
        fig_rec = go.Figure()
        for segmento in df_rfm_seg['Segmento'].unique():
            df_seg = df_rfm_seg[df_rfm_seg['Segmento'] == segmento]
            
            fig_rec.add_trace(go.Violin(
                y=df_seg['Recencia'],
                name=segmento,
                box_visible=True,
                meanline_visible=False,
                points='outliers',
                pointpos=0,
                hoverinfo='y'
            ))
        
        fig_rec.update_layout(
            title='Distribución de Recencia',
            xaxis_title='Segmento',
            yaxis_title='Días desde última compra',
            height=450,
            showlegend=False,
            xaxis={'tickangle': 0}
        )
        st.plotly_chart(fig_rec, use_container_width=True)

    with col2:
        fig_freq = go.Figure()
        for segmento in df_rfm_seg['Segmento'].unique():
            df_seg = df_rfm_seg[df_rfm_seg['Segmento'] == segmento]
            
            fig_freq.add_trace(go.Violin(
                y=df_seg['Frecuencia'],
                name=segmento,
                box_visible=True,
                meanline_visible=False,
                points='outliers',
                pointpos=0,
                hoverinfo='y'
            ))
        
        fig_freq.update_layout(
            title='Distribución de Frecuencia',
            xaxis_title='Segmento',
            yaxis_title='Número de compras',
            height=450,
            showlegend=False,
            xaxis={'tickangle': 0}
        )
        st.plotly_chart(fig_freq, use_container_width=True)

    with col3:
        fig_mon = go.Figure()
        for segmento in df_rfm_seg['Segmento'].unique():
            df_seg = df_rfm_seg[df_rfm_seg['Segmento'] == segmento]
            
            fig_mon.add_trace(go.Violin(
                y=df_seg['Monetario'],
                name=segmento,
                box_visible=True,
                meanline_visible=False,
                points='outliers',
                pointpos=0,
                hoverinfo='y'
            ))
        
        fig_mon.update_layout(
            title='Distribución de Gasto',
            xaxis_title='Segmento',
            yaxis_title='Gasto Total (ARS)',
            height=450,
            showlegend=False,
            xaxis={'tickangle': 0}
        )
        st.plotly_chart(fig_mon, use_container_width=True)

    # Scatter plots RFM mejorados
    st.subheader("Análisis de Relaciones entre Métricas RFM")

    tab1, tab2, tab3 = st.tabs(["Frecuencia vs Monetario", "Recencia vs Monetario", "Recencia vs Frecuencia"])

    # Preparar hover_data - incluir nombre_cliente y ciudad si existen
    hover_base = []
    if 'nombre_cliente' in df_rfm_seg.columns:
        hover_base.append('nombre_cliente')
    if 'ciudad' in df_rfm_seg.columns:
        hover_base.append('ciudad')

    with tab1:
        hover_data_tab1 = hover_base + ['Recencia']
        fig_scatter1 = px.scatter(
            df_rfm_seg,
            x='Frecuencia',
            y='Monetario',
            color='Segmento',
            size='Recencia',
            hover_data=hover_data_tab1 if hover_data_tab1 else None,
            title='Frecuencia vs Gasto Total (tamaño del punto = días desde última compra)',
            labels={'Frecuencia': 'Número de Compras', 'Monetario': 'Gasto Total (ARS)'},
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig_scatter1.update_layout(height=500)
        st.plotly_chart(fig_scatter1, use_container_width=True)
        st.info("💡 **Insight:** Los mejores clientes están en la esquina superior derecha (alta frecuencia + alto gasto)")

    with tab2:
        hover_data_tab2 = hover_base + ['Frecuencia']
        fig_scatter2 = px.scatter(
            df_rfm_seg,
            x='Recencia',
            y='Monetario',
            color='Segmento',
            size='Frecuencia',
            hover_data=hover_data_tab2 if hover_data_tab2 else None,
            title='Recencia vs Gasto Total (tamaño del punto = número de compras)',
            labels={'Recencia': 'Días desde última compra', 'Monetario': 'Gasto Total (ARS)'},
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig_scatter2.update_layout(height=500)
        st.plotly_chart(fig_scatter2, use_container_width=True)
        st.info("💡 **Insight:** Los mejores clientes están en la esquina superior izquierda (compra reciente + alto gasto)")

    with tab3:
        hover_data_tab3 = hover_base + ['Monetario']
        fig_scatter3 = px.scatter(
            df_rfm_seg,
            x='Recencia',
            y='Frecuencia',
            color='Segmento',
            size='Monetario',
            hover_data=hover_data_tab3 if hover_data_tab3 else None,
            title='Recencia vs Frecuencia (tamaño del punto = gasto total)',
            labels={'Recencia': 'Días desde última compra', 'Frecuencia': 'Número de Compras'},
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig_scatter3.update_layout(height=500)
        st.plotly_chart(fig_scatter3, use_container_width=True)
        st.info("💡 **Insight:** Los mejores clientes están en la esquina superior izquierda (compra reciente + alta frecuencia)")

    # Top clientes
    st.subheader("Top 15 Mejores Clientes")
    
    # Seleccionar solo columnas que existen
    columnas_top = ['Recencia', 'Frecuencia', 'Monetario', 'Segmento']
    if 'nombre_cliente' in df_rfm_seg.columns:
        columnas_top.insert(0, 'nombre_cliente')
    if 'ciudad' in df_rfm_seg.columns:
        columnas_top.insert(1, 'ciudad')
    
    top_clientes = df_rfm_seg.nlargest(15, 'Monetario')[columnas_top]
    top_clientes_display = top_clientes.copy()
    top_clientes_display['Recencia'] = top_clientes_display['Recencia'].apply(lambda x: f"{x} días")
    top_clientes_display['Frecuencia'] = top_clientes_display['Frecuencia'].apply(lambda x: f"{x} compras")
    top_clientes_display['Monetario'] = top_clientes_display['Monetario'].apply(lambda x: f"ARS ${x:,.2f}")
    
    # Renombrar columnas dinámicamente
    nuevos_nombres = {}
    if 'nombre_cliente' in top_clientes_display.columns:
        nuevos_nombres['nombre_cliente'] = 'Cliente'
    if 'ciudad' in top_clientes_display.columns:
        nuevos_nombres['ciudad'] = 'Ciudad'
    nuevos_nombres.update({
        'Recencia': 'Última Compra',
        'Frecuencia': 'Total Compras',
        'Monetario': 'Gasto Total',
        'Segmento': 'Segmento'
    })
    top_clientes_display = top_clientes_display.rename(columns=nuevos_nombres)
    
    st.dataframe(top_clientes_display, use_container_width=True, hide_index=True)

st.markdown("---")

# =============================
# SECCIÓN 7: CORRELACIONES RFM
# =============================
col_header1, col_header2 = st.columns([10, 1])
with col_header1:
    st.header("Matriz de Correlación RFM")
with col_header2:
    st.markdown("")  # Espaciado
    with st.popover("ℹ️"):
        st.markdown("""
        **¿Qué nos dice la correlación?**
        - **Positiva (+)**: Cuando una métrica aumenta, la otra también
        - **Negativa (-)**: Cuando una métrica aumenta, la otra disminuye
        - **Cercana a 0**: No hay relación entre las métricas
        
        **Valores de referencia:**
        - **0.7 a 1.0**: Correlación fuerte
        - **0.3 a 0.7**: Correlación moderada
        - **0.0 a 0.3**: Correlación débil
        """)

# Calcular correlaciones solo si hay datos RFM filtrados
if len(df_rfm_filtrado) > 0:
    corr_matrix = df_rfm_filtrado[['Recencia', 'Frecuencia', 'Monetario']].corr()

    col1, col2 = st.columns([2, 1])

    with col1:
        fig_corr = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmid=0,
            text=corr_matrix.values,
            texttemplate='%{text:.3f}',
            textfont={"size": 16, "color": "white"},
            colorbar=dict(title="Correlación")
        ))
        
        fig_corr.update_layout(
            title='Correlación entre Métricas RFM',
            height=450,
            xaxis_title="",
            yaxis_title=""
        )
        
        st.plotly_chart(fig_corr, use_container_width=True)

    with col2:
        # Interpretación automática
        freq_mon_corr = corr_matrix.loc['Frecuencia', 'Monetario']
        rec_freq_corr = corr_matrix.loc['Recencia', 'Frecuencia']
        rec_mon_corr = corr_matrix.loc['Recencia', 'Monetario']
        
        st.markdown(f"""
        **Frecuencia ↔ Monetario**  
        Correlación: `{freq_mon_corr:.3f}`
        """)
        if freq_mon_corr > 0.5:
            st.success("✅ Positiva: Clientes frecuentes gastan más")
        elif freq_mon_corr > 0.3:
            st.info("⚠️ Moderada: Cierta conexión entre frecuencia y gasto")
        else:
            st.warning("❌ Débil: Frecuencia no implica mayor gasto")
        
        st.markdown(f"""
        **Recencia ↔ Frecuencia**  
        Correlación: `{rec_freq_corr:.3f}`
        """)
        if rec_freq_corr < -0.3:
            st.success("✅ Negativa: Clientes recientes son más frecuentes")
        else:
            st.info("⚠️ Relación débil entre recencia y frecuencia")
        
        st.markdown(f"""
        **Recencia ↔ Monetario**  
        Correlación: `{rec_mon_corr:.3f}`
        """)
        if rec_mon_corr < -0.3:
            st.success("✅ Negativa: Clientes recientes gastan más")
        else:
            st.info("⚠️ Relación débil entre recencia y gasto")
else:
    st.warning("⚠️ No hay datos suficientes para calcular correlaciones RFM con los filtros aplicados.")

st.markdown("---")

# =============================
# SECCIÓN 8: ANÁLISIS TEMPORAL
# =============================
col_header1, col_header2 = st.columns([10, 1])
with col_header1:
    st.header("Análisis Temporal")
with col_header2:
    st.markdown("")  # Espaciado
    with st.popover("ℹ️"):
        st.markdown("""
        **Análisis Temporal**
        
        Esta sección te ayuda a identificar:
        - **Tendencias**: ¿Qué categorías crecen o decrecen?
        - **Estacionalidad**: ¿Hay días/meses con más ventas?
        - **Patrones**: ¿Cuándo venden más tus productos?
        
        Usa estos insights para:
        - Planificar inventario
        - Ajustar campañas de marketing
        - Optimizar recursos según demanda
        """)

tab1, tab2, tab3 = st.tabs(["Tendencias por Categoría", "Estacionalidad", "Exportar Datos"])

with tab1:
    # Ventas por mes y categoría
    df_tiempo_cat = df_filtrado.copy()
    df_tiempo_cat['mes'] = df_tiempo_cat['fecha'].dt.to_period('M').astype(str)
    
    ventas_mes_cat = df_tiempo_cat.groupby(['mes', 'categoria'])['importe'].sum().reset_index()
    
    fig_trend = px.line(
        ventas_mes_cat,
        x='mes',
        y='importe',
        color='categoria',
        title='Evolución de Ventas por Categoría (ARS)',
        labels={'importe': 'Ventas (ARS)', 'mes': 'Mes', 'categoria': 'Categoría'},
        markers=True
    )
    fig_trend.update_layout(height=450, hovermode='x unified')
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # Identificar categoría con mayor crecimiento
    if len(ventas_mes_cat) > 0:
        primera_mitad = ventas_mes_cat.groupby('categoria')['importe'].apply(lambda x: x.iloc[:len(x)//2].sum() if len(x) > 1 else x.sum())
        segunda_mitad = ventas_mes_cat.groupby('categoria')['importe'].apply(lambda x: x.iloc[len(x)//2:].sum() if len(x) > 1 else 0)
        crecimiento = ((segunda_mitad - primera_mitad) / primera_mitad * 100).sort_values(ascending=False)
        
        if len(crecimiento) > 0:
            mejor_categoria = crecimiento.idxmax()
            peor_categoria = crecimiento.idxmin()
            
            st.markdown(f"""
            <div class="insight-box">
                <strong>💡 Insights de Tendencias:</strong><br>
                • <strong>Categoría en crecimiento:</strong> {mejor_categoria} ({crecimiento[mejor_categoria]:.1f}% de aumento)<br>
                • <strong>Categoría en descenso:</strong> {peor_categoria} ({crecimiento[peor_categoria]:.1f}% de cambio)
            </div>
            """, unsafe_allow_html=True)

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        # Análisis por día de la semana
        df_estacional = df_filtrado.copy()
        df_estacional['dia_semana'] = df_estacional['fecha'].dt.day_name()
        
        dias_esp = {
            'Monday': 'Lunes',
            'Tuesday': 'Martes', 
            'Wednesday': 'Miércoles',
            'Thursday': 'Jueves',
            'Friday': 'Viernes',
            'Saturday': 'Sábado',
            'Sunday': 'Domingo'
        }
        
        orden_dias = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        ventas_dia = df_estacional.groupby('dia_semana')['importe'].sum().reindex(orden_dias).reset_index()
        ventas_dia['dia_semana_esp'] = ventas_dia['dia_semana'].map(dias_esp)
        
        fig_estacional = px.bar(
            ventas_dia,
            x='dia_semana_esp',
            y='importe',
            title='Ventas por Día de la Semana',
            labels={'importe': 'Ventas (ARS)', 'dia_semana_esp': 'Día'},
            color='importe',
            color_continuous_scale='Turbo',
            text='importe'
        )
        fig_estacional.update_traces(texttemplate='$%{text:,.0f}', textposition='inside')
        fig_estacional.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_estacional, use_container_width=True)
        
        mejor_dia = ventas_dia.loc[ventas_dia['importe'].idxmax(), 'dia_semana_esp']
        peor_dia = ventas_dia.loc[ventas_dia['importe'].idxmin(), 'dia_semana_esp']
        st.info(f"📅 **Mejor día:** {mejor_dia} | **Menor día:** {peor_dia}")
    
    with col2:
        # Análisis por hora (si hay datos de hora)
        df_mes = df_filtrado.copy()
        df_mes['mes_num'] = df_mes['fecha'].dt.month
        
        meses_esp = {
            1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
            5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
            9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
        }
        
        ventas_mes = df_mes.groupby('mes_num')['importe'].sum().reset_index()
        ventas_mes['mes_nombre'] = ventas_mes['mes_num'].map(meses_esp)
        
        fig_mes = px.bar(
            ventas_mes,
            x='mes_nombre',
            y='importe',
            title='Ventas por Mes',
            labels={'importe': 'Ventas (ARS)', 'mes_nombre': 'Mes'},
            color='importe',
            color_continuous_scale='Viridis',
            text='importe'
        )
        fig_mes.update_traces(texttemplate='$%{text:,.0f}', textposition='inside')
        fig_mes.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_mes, use_container_width=True)
        
        mejor_mes = ventas_mes.loc[ventas_mes['importe'].idxmax(), 'mes_nombre']
        peor_mes = ventas_mes.loc[ventas_mes['importe'].idxmin(), 'mes_nombre']
        st.info(f"📆 **Mejor mes:** {mejor_mes} | **Menor mes:** {peor_mes}")
    
    # Heatmap de ventas por día y mes
    df_heatmap = df_filtrado.copy()
    df_heatmap['mes'] = df_heatmap['fecha'].dt.month
    df_heatmap['dia'] = df_heatmap['fecha'].dt.day
    
    ventas_heatmap = df_heatmap.groupby(['mes', 'dia'])['importe'].sum().reset_index()
    ventas_pivot = ventas_heatmap.pivot(index='mes', columns='dia', values='importe').fillna(0)
    
    fig_heat = go.Figure(data=go.Heatmap(
        z=ventas_pivot.values,
        x=ventas_pivot.columns,
        y=[meses_esp.get(i, i) for i in ventas_pivot.index],
        colorscale='YlOrRd',
        colorbar=dict(title="Ventas (ARS)")
    ))
    
    fig_heat.update_layout(
        title='Mapa de Calor: Ventas por Mes y Día',
        xaxis_title='Día del Mes',
        yaxis_title='Mes',
        height=400
    )
    st.plotly_chart(fig_heat, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box">
        <strong>🔍 Cómo interpretar el mapa de calor:</strong><br>
        • <strong>Colores más intensos (rojo):</strong> Días con mayores ventas<br>
        • <strong>Colores más claros (amarillo):</strong> Días con menores ventas<br>
        • Identifica patrones: ¿hay días del mes que siempre venden más?
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.markdown("**Descarga los datos procesados para análisis adicional en Excel, Power BI, u otras herramientas**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        tabla_seleccion = st.selectbox(
            "Seleccionar conjunto de datos:",
            ["Datos Consolidados (Filtrados)", "RFM Segmentado", "Clientes", "Productos", "Ventas", "Detalle Ventas"]
        )
    
    with col2:
        formato = st.radio("Formato:", ["CSV", "Excel"], horizontal=True)
    
    # Mostrar preview
    if tabla_seleccion == "Datos Consolidados (Filtrados)":
        data_to_export = df_filtrado
        st.markdown(f"**Preview** (primeras 100 filas de {len(df_filtrado):,} totales)")
        st.dataframe(df_filtrado.head(100), use_container_width=True)
    elif tabla_seleccion == "RFM Segmentado":
        data_to_export = df_rfm_seg
        st.markdown(f"**Preview** ({len(df_rfm_seg):,} clientes)")
        st.dataframe(df_rfm_seg, use_container_width=True)
    elif tabla_seleccion == "Clientes":
        data_to_export = df_clientes
        st.markdown(f"**Preview** ({len(df_clientes):,} clientes)")
        st.dataframe(df_clientes, use_container_width=True)
    elif tabla_seleccion == "Productos":
        data_to_export = df_productos
        st.markdown(f"**Preview** ({len(df_productos):,} productos)")
        st.dataframe(df_productos, use_container_width=True)
    elif tabla_seleccion == "Ventas":
        data_to_export = df_ventas
        st.markdown(f"**Preview** (primeras 100 filas de {len(df_ventas):,} totales)")
        st.dataframe(df_ventas.head(100), use_container_width=True)
    else:
        data_to_export = df_detalle
        st.markdown(f"**Preview** (primeras 100 filas de {len(df_detalle):,} totales)")
        st.dataframe(df_detalle.head(100), use_container_width=True)
    
    # Botones de descarga
    if formato == "CSV":
        st.download_button(
            label="📥 Descargar CSV",
            data=data_to_export.to_csv(index=False).encode('utf-8'),
            file_name=f'{tabla_seleccion.lower().replace(" ", "_")}.csv',
            mime='text/csv',
            use_container_width=True
        )
    else:
        # Para Excel necesitamos usar BytesIO
        from io import BytesIO
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            data_to_export.to_excel(writer, index=False, sheet_name='Datos')
        excel_data = output.getvalue()
        
        st.download_button(
            label="📥 Descargar Excel",
            data=excel_data,
            file_name=f'{tabla_seleccion.lower().replace(" ", "_")}.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            use_container_width=True
        )
    
    st.success("✅ Datos listos para descargar. Click en el botón de arriba para iniciar la descarga.")

st.markdown("---")

# =============================
# FOOTER
# =============================
st.markdown("""
<div style='text-align: center; color: gray; padding: 20px;'>
    <p>📊 Dashboard de Análisis de Ventas | Minimarket | Desarrollado con Streamlit & Plotly</p>
    <p>Datos actualizados al: {}</p>
</div>
""".format(datetime.now().strftime('%d/%m/%Y %H:%M')), unsafe_allow_html=True)
