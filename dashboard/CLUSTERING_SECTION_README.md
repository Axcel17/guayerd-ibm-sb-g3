# 🎯 Sección de Análisis de Clustering Avanzado

## 📋 Resumen de Implementación

Se ha agregado una sección completa de análisis de clustering al dashboard, ubicada **antes del footer** y **después de la sección de exportación de datos**.

## 🎨 Componentes Implementados

### 1. **Métricas de Calidad del Modelo** 📊
- Silhouette Score (0.357)
- Calinski-Harabasz Index (308.83)
- Davies-Bouldin Index (0.916)
- Número de clusters (9)
- Explicación detallada de por qué estos indicadores validan el modelo

### 2. **Distribución de Clientes** 👥
- Gráfico de torta: % de clientes por segmento
- Gráfico de torta: % de ventas por segmento
- Tabla resumen con métricas cuantitativas

### 3. **Visualizaciones 3D Interactivas** 🎨
- **Tab 1: Vista PCA 3D** - Componentes principales (47.72% varianza)
- **Tab 2: Vista RFM 3D** - Dimensiones originales (Recency, Frequency, Monetary)
- Totalmente interactivas (rotar, zoom, hover)

### 4. **Visualización 2D** 📊
- Scatter plot con PCA 2D
- Varianza explicada: ~37%
- Hover data con información del cliente

### 5. **Perfiles Detallados por Segmento** 🔍
- Selector interactivo de segmento
- Métricas clave: Clientes, Recency, Frequency, Monetary
- Distribución de preferencias por categoría (gráfico de barras)
- Top 10 clientes del segmento seleccionado

### 6. **Comparación Entre Segmentos** ⚖️
- Heatmap normalizado de todas las variables
- Gráfico de barras agrupadas con métricas RFM
- Comparación visual de perfiles

### 7. **Recomendaciones Estratégicas** 💡
- Estrategias personalizadas para cada segmento:
  - VIP Premium Activo: Programa exclusivo, comunicación VIP
  - VIP Moderado: Incentivos para aumentar frecuencia
  - Habitual Moderado: Engagement y upselling
  - Inactivos: Campañas de reactivación por categoría

## 📁 Archivos Generados

Desde el notebook `2_feature_engineering.ipynb`:

1. **clustering_features.csv** - Features + asignación de cluster por cliente
2. **clustering_profiles.csv** - Perfiles agregados de cada cluster
3. **clustering_metrics.json** - Métricas de calidad del modelo
4. **clustering_viz_2d.csv** - Datos para visualización 2D
5. **clustering_viz_3d.csv** - Datos para visualización 3D

## 🚀 Cómo Usar

### Paso 1: Generar los archivos
```bash
# Ejecutar el notebook hasta la última celda
jupyter notebook 2_feature_engineering.ipynb
# O ejecutar solo la última celda desde VS Code
```

### Paso 2: Ejecutar el dashboard
```bash
cd dashboard
streamlit run dashboard_ventas.py
```

### Paso 3: Navegar a la sección
Scroll hasta el final del dashboard (antes del footer) para ver la nueva sección:
**"🎯 Análisis de Clustering Avanzado"**

## 🎯 Diferencias con Segmentación RFM

| Característica | RFM por Reglas | Clustering Avanzado |
|---------------|----------------|---------------------|
| Variables usadas | 3 (R, F, M) | 14 (RFM + categorías + diversidad) |
| Método | Reglas fijas | K-Means optimizado |
| Flexibilidad | Baja | Alta |
| Detección de patrones | Simple | Compleja |
| Segmentos | 5 fijos | 9 optimizados |
| Validación | Subjetiva | Métricas estadísticas |

## 📊 Insights Clave

### Segmentos Principales:
1. **VIP Premium Activo** (61 clientes) - 499 compras promedio, $3.5M
2. **VIP Moderado** (286 clientes) - 188 compras promedio, $1.3M
3. **Habitual Moderado** (920 clientes) - Mayor volumen, base estable
4. **Ocasionales Inactivos** (264 clientes) - 6 micro-segmentos por categoría

### Validación del Modelo:
- ✅ Silhouette > 0.3 → Buena separación
- ✅ Calinski-Harabasz alto → Clusters bien definidos
- ✅ Davies-Bouldin < 1 → Baja similitud entre clusters

## 🛠️ Tecnologías Utilizadas

- **Streamlit** - Framework del dashboard
- **Plotly** - Visualizaciones 3D/2D interactivas
- **Pandas** - Manipulación de datos
- **Scikit-learn** - Normalización y scaling
- **JSON** - Almacenamiento de métricas

## 📝 Notas Técnicas

- Los gráficos 3D son completamente interactivos (usar mouse para rotar)
- Las escalas logarítmicas en RFM 3D mejoran la visualización
- El heatmap usa normalización Z-score para comparabilidad
- Los colores son consistentes entre visualizaciones

## 🔄 Actualizaciones Futuras Sugeridas

- [ ] Exportar perfiles de cluster a PDF
- [ ] Dashboard de seguimiento temporal de clusters
- [ ] Predicción de migración entre clusters
- [ ] A/B testing de estrategias por segmento
- [ ] Integración con CRM para ejecución automática

---

**Desarrollado por:** IBM Guayerd Analytics Team  
**Fecha:** Diciembre 2025  
**Versión:** 1.0
