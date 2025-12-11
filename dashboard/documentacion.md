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

### 6. **Segmentación RFM (Por Reglas)**
- Clasificación automática de clientes:
  - ⭐ Campeones (mejores clientes)
  - 💎 Clientes Leales
  - 📈 Potenciales
  - ⚠️ En Riesgo
  - 😴 Inactivos
- Visualización interactiva
- Top clientes identificados

### 7. **🎯 Análisis de Clustering Avanzado** ⭐ NUEVO
Segmentación avanzada mediante Machine Learning (K-Means con 9 clusters optimizados):

#### 7.1. Métricas de Calidad del Modelo
- Silhouette Score (0.357) - Buena separación entre clusters
- Calinski-Harabasz Index (308.83) - Clusters bien definidos
- Davies-Bouldin Index (0.916) - Baja similitud entre clusters
- Explicación detallada de validación del modelo

#### 7.2. Distribución de Clientes por Segmento
- Gráfico de torta: % de clientes por segmento
- Gráfico de torta: % de ventas por segmento
- Tabla resumen con métricas cuantitativas

#### 7.3. Visualizaciones 3D Interactivas
- **Vista PCA 3D**: Componentes principales (47.72% varianza explicada)
- **Vista RFM 3D**: Dimensiones originales con escalas logarítmicas
- Rotación 360°, zoom, y hover interactivo

#### 7.4. Visualización 2D
- Scatter plot con PCA 2D (~37% varianza explicada)
- Identificación visual de separación de clusters

#### 7.5. Perfiles Detallados por Segmento
- Selector interactivo de segmento
- Métricas clave: Clientes, Recency, Frequency, Monetary
- Distribución de preferencias por categoría
- Top 10 clientes del segmento

#### 7.6. Comparación Entre Segmentos
- Heatmap normalizado de todas las variables
- Gráfico de barras agrupadas con métricas RFM
- Análisis comparativo visual

#### 7.7. Recomendaciones Estratégicas
- Estrategias personalizadas para cada segmento:
  - 👑 **VIP Premium Activo** (61 clientes): Programa exclusivo, eventos especiales
  - ⭐ **VIP Moderado** (286 clientes): Incentivos para aumentar frecuencia
  - 🔄 **Habitual Moderado** (920 clientes): Engagement y upselling
  - 💤 **Inactivos por Categoría** (264 clientes): Campañas de reactivación específicas

#### 7.8. Segmentos Identificados
1. **VIP Premium Activo** - 499 compras promedio, $3.5M valor
2. **VIP Moderado** - 188 compras promedio, $1.3M valor
3. **Habitual Moderado** - Base estable, mayor volumen
4. **Ocasionales Inactivos** - 6 micro-segmentos por categoría preferida

### 8. **Análisis Avanzado**
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
├── requirements.txt                    # Dependencias
├── 2_feature_engineering.ipynb         # Notebook de clustering
└── dashboard/
    ├── dashboard_ventas.py             # Dashboard principal
    └── documentacion.md                # Esta documentación
└── data/
    ├── raw/
    │   ├── clientes.csv
    │   ├── productos.csv
    │   ├── ventas.csv
    │   └── detalle_ventas.csv
    └── clean/                          # Archivos generados por clustering
        ├── clustering_features.csv
        ├── clustering_profiles.csv
        ├── clustering_metrics.json
        ├── clustering_viz_2d.csv
        └── clustering_viz_3d.csv
```

### Paso 3: Generar archivos de clustering (IMPORTANTE)

Para habilitar la sección de clustering avanzado, ejecuta el notebook hasta la última celda:

```powershell
# Desde VS Code, abrir el notebook y ejecutar todas las celdas
# O desde Jupyter:
jupyter notebook 2_feature_engineering.ipynb
```

Esto generará los 5 archivos necesarios en `data/clean/` para el análisis de clustering.

## ▶️ Ejecución

Desde PowerShell, en la carpeta `dashboard/`:

```powershell
cd dashboard
streamlit run dashboard_ventas.py
```

El dashboard se abrirá automáticamente en tu navegador en `http://localhost:8501`

> **Nota**: Si la sección de clustering no aparece, verifica que los archivos en `data/clean/` hayan sido generados ejecutando el notebook `2_feature_engineering.ipynb`.

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

### 6. Segmentación RFM (Por Reglas)
- Distribución de segmentos
- Métricas por segmento
- Scatter plot interactivo
- Top 10 mejores clientes

### 7. Clustering Avanzado (Machine Learning) ⭐
- **Métricas de Calidad**: Silhouette, Calinski-Harabasz, Davies-Bouldin
- **Visualizaciones 3D/2D**: Interactivas con PCA y RFM original
- **Perfiles Detallados**: Análisis por segmento con selector
- **Comparación**: Heatmap y gráficos comparativos
- **Recomendaciones**: Estrategias personalizadas por segmento
- **9 Segmentos Optimizados**: VIP Premium, VIP Moderado, Habitual, Inactivos por categoría

### 8. Productos por Ciudad
- Análisis detallado ciudad por ciudad
- Top 10 productos locales
- Distribución de categorías

### 9. Análisis Temporal Avanzado
- Tendencias por categoría
- Análisis por día de semana
- Patrones estacionales

### 10. Exportación de Datos
- Descarga en CSV o Excel
- Selección de tablas específicas
- Exportación de análisis completos

## 💡 Insights Automáticos

El dashboard genera insights automáticos como:
- Mejores y peores períodos de venta
- Variación porcentual entre períodos
- Correlaciones entre métricas RFM
- Segmentos de clientes identificados automáticamente
- Patrones de comportamiento por cluster
- Recomendaciones estratégicas personalizadas

## 🎯 Diferencias: RFM vs Clustering Avanzado

| Característica | RFM por Reglas | Clustering K-Means |
|---------------|----------------|---------------------|
| **Variables** | 3 (Recency, Frequency, Monetary) | 14 (RFM + categorías + diversidad) |
| **Método** | Reglas fijas predefinidas | Machine Learning optimizado |
| **Flexibilidad** | Baja - segmentos fijos | Alta - adapta a patrones reales |
| **Detección** | Patrones simples | Patrones complejos multidimensionales |
| **N° Segmentos** | 5 predefinidos | 9 optimizados por métricas |
| **Validación** | Subjetiva | Métricas estadísticas objetivas |
| **Uso** | Clasificación rápida estándar | Análisis profundo y estratégico |

## 📊 Métricas de Validación del Clustering

### ✅ Silhouette Score = 0.357
- **Rango**: [-1, 1] | **Óptimo**: > 0.3
- **Interpretación**: Buena separación entre clusters
- Los clientes dentro de cada grupo son más similares entre sí que con otros grupos

### ✅ Calinski-Harabasz = 308.83
- **Rango**: [0, ∞] | **Óptimo**: Alto
- **Interpretación**: Clusters bien definidos y compactos
- Alta varianza entre clusters vs varianza interna

### ✅ Davies-Bouldin = 0.916
- **Rango**: [0, ∞] | **Óptimo**: < 1
- **Interpretación**: Baja similitud entre clusters
- Cada cluster es único y bien diferenciado

## 🛠️ Tecnologías Utilizadas

- **Streamlit** - Framework del dashboard interactivo
- **Plotly** - Visualizaciones 3D/2D interactivas
- **Pandas** - Manipulación y análisis de datos
- **Scikit-learn** - Algoritmos de Machine Learning y normalización
- **NumPy** - Computación numérica
- **JSON** - Almacenamiento de métricas

## 📁 Archivos de Clustering Generados

Los siguientes archivos son generados automáticamente por el notebook:

1. **clustering_features.csv** - Features + asignación de cluster por cliente (1,531 registros)
2. **clustering_profiles.csv** - Perfiles agregados de cada cluster (9 clusters)
3. **clustering_metrics.json** - Métricas de calidad del modelo
4. **clustering_viz_2d.csv** - Datos pre-procesados para visualización 2D PCA
5. **clustering_viz_3d.csv** - Datos pre-procesados para visualización 3D PCA

## 🎨 Paleta de Colores

El dashboard utiliza una paleta consistente:
- **VIP Premium**: Dorado (#FFD700)
- **VIP Moderado**: Azul cielo (#87CEEB)
- **Habitual**: Verde (#90EE90)
- **Inactivos**: Rosa claro (#FFB6C1)

## 🚀 Recomendaciones de Uso

### Para Análisis Rápido
→ Usa la **Segmentación RFM por Reglas** (Sección 6)

### Para Estrategia Profunda
→ Usa el **Clustering Avanzado** (Sección 7)

### Para Exploración Visual
→ Visualizaciones 3D interactivas en Clustering

### Para Reportes Ejecutivos
→ Exporta datos desde Sección 10 + Screenshots de gráficos

## 🔄 Actualizaciones Futuras Sugeridas

- [ ] Exportar perfiles de cluster a PDF
- [ ] Dashboard de seguimiento temporal de clusters
- [ ] Predicción de migración entre clusters
- [ ] A/B testing de estrategias por segmento
- [ ] Integración con CRM para ejecución automática
- [ ] API REST para consultas programáticas
- [ ] Alertas automáticas de cambios en segmentos

---

**Desarrollado por:** IBM Guayerd Analytics Team  
**Versión:** 2.0 - Con Clustering Avanzado  
**Fecha:** Diciembre 2025  
**Contacto:** [Tu correo o equipo]
