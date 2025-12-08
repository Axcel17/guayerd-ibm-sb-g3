# 📊 Dashboard de Análisis de Ventas - Minimarket

Dashboard interactivo desarrollado con **Streamlit** y **Plotly** para análisis en tiempo real de ventas, clientes y productos.

## 🚀 Características Principales

### 1. **KPIs Principales**
- 💰 Ventas Totales
- 🛒 Número de Transacciones
- 👥 Clientes Activos
- 🎯 Ticket Promedio

### 2. **Análisis Temporal**
- Evolución de ventas por día, semana o mes
- Identificación de picos de venta
- Tendencias y estacionalidad
- Análisis por día de la semana

### 3. **Análisis Geográfico**
- Ventas por ciudad
- Distribución de transacciones
- Comparativa entre ciudades
- Productos top por ciudad

### 4. **Análisis de Productos**
- Top N productos por ingresos o cantidad
- Ventas por categoría
- Productos más vendidos por ciudad
- Distribución de categorías

### 5. **Métodos de Pago**
- Frecuencia de uso
- Distribución por ciudad
- Análisis comparativo

### 6. **Segmentación RFM**
- Clasificación automática de clientes:
  - ⭐ Campeones (mejores clientes)
  - 💎 Clientes Leales
  - 📈 Potenciales
  - ⚠️ En Riesgo
  - 😴 Inactivos
- Visualización interactiva
- Top clientes identificados

### 7. **Análisis Avanzado**
- Matriz de correlación RFM
- Tendencias por categoría
- Exportación de datos

## 📦 Instalación

### Paso 1: Instalar dependencias

```powershell
pip install -r requirements.txt
```

### Paso 2: Verificar estructura de archivos

Asegúrate de tener la siguiente estructura:

```
guayerd-ibm-sb-g3/
├── requirements.txt            # Dependencias
└── dashboard
    ├── dashboard_ventas.py     # Dashboard principal
└── data/raw/
    ├── clientes.csv
    ├── productos.csv
    ├── ventas.csv
    └── detalle_ventas.csv
```

## ▶️ Ejecución

Desde PowerShell, en la carpeta del proyecto:

```powershell
streamlit run dashboard_ventas.py
```

El dashboard se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 🎛️ Filtros Disponibles

### Sidebar (Panel Lateral)
- **Rango de Fechas**: Filtra datos por período específico
- **Ciudad**: Analiza datos de una ciudad particular
- **Categoría**: Enfócate en categorías de productos específicas

Todos los gráficos se actualizan dinámicamente según los filtros aplicados.

## 📊 Secciones del Dashboard

### 1. Indicadores Clave (KPIs)
Muestra métricas principales en tarjetas destacadas con valores actualizados según filtros.

### 2. Evolución Temporal
- Gráfico de líneas interactivo
- Selector de granularidad (Día/Semana/Mes)
- Línea de promedio
- Insights automáticos sobre mejores y peores períodos

### 3. Análisis por Ciudad
- Gráfico de barras de ventas totales
- Pie chart de distribución de transacciones
- Tabla resumen detallada

### 4. Análisis de Productos
- Top N productos (slider ajustable)
- Ordenamiento por ingresos o cantidad
- Ventas por categoría
- Gráficos de barras y pie charts

### 5. Métodos de Pago
- Frecuencia de cada método
- Comparativa entre ciudades top
- Gráficos de barras agrupadas

### 6. Segmentación RFM
- Distribución de segmentos
- Métricas por segmento
- Scatter plot interactivo
- Top 10 mejores clientes

### 7. Productos por Ciudad
- Análisis detallado ciudad por ciudad
- Top 10 productos locales
- Distribución de categorías

### 8. Análisis Avanzado (Tabs)
- **Correlaciones**: Heatmap de correlación RFM
- **Tendencias**: Evolución por categoría y día de semana
- **Datos Crudos**: Explorador de tablas con descarga CSV

## 💡 Insights Automáticos

El dashboard genera insights automáticos como:
- Mejores y peores períodos de venta
- Variación porcentual entre períodos
- Correlaciones entre métricas RFM
- Segmentos de clientes identificados
