# MEMORIA TÉCNICA: DASHBOARD DE ANÁLISIS ESTADÍSTICO PARA INGENIERÍA
**Versión:** 2.5.3-final  
**Coordinador del Proyecto:** Rubén Gámez Torrijos  
**Fecha:** 4 de mayo de 2026

## 1. Resumen Ejecutivo y Objetivo
Este proyecto consiste en el desarrollo de una plataforma analítica avanzada integrada en la web, diseñada para el procesamiento y modelado estadístico de datos en contextos de ingeniería. El objetivo es proporcionar una herramienta robusta que permita pasar de la ingesta de datos brutos a la toma de decisiones basada en evidencia científica, garantizando la trazabilidad matemática y la excelencia visual.

## 2. Arquitectura y Tecnologías
La aplicación adopta una arquitectura **MVC (Modelo-Vista-Controlador)** desacoplada para maximizar la escalabilidad:

*   **Lenguaje:** Python 3.10+
*   **Frontend & Orquestación:** Streamlit (v1.31.0+).
*   **Procesamiento de Datos:** Pandas (v2.1.0) y NumPy (v1.26.0).
*   **Cálculo Científico e Inferencial:** SciPy (v1.12.0) y Scikit-Learn (v1.4.0).
*   **Visualización:** Seaborn, Matplotlib y Plotly.

### Estructura de Directorios:
```text
/proyecto_estadistica
├── app.py                # Punto de entrada
├── controllers/          # Lógica de flujo (MVC)
├── models/               # Carga y transformación de datos
├── analisis/             # Núcleo de cálculo estadístico (CRÍTICO)
│   ├── estadisticos.py   # Descriptiva y limpieza
│   ├── inferencial.py    # Tests de hipótesis e IC
│   └── modelo_regresion.py # Modelado predictivo
├── views/                # Capa de presentación y estilos CSS
├── config/               # Parámetros y constantes globales
└── datos/                # Repositorio de datasets (local)
```

## 3. Desglose de Módulos Críticos

### 3.1. Módulo de Análisis Estadístico (`analisis/estadisticos.py`)
*   **Propósito:** Cálculo de métricas de tendencia central, dispersión y forma.
*   **Entrada:** `pandas.DataFrame`.
*   **Salida:** `pandas.DataFrame` con métricas resumidas.
*   **Dependencias:** `pandas`, `numpy`.

### 3.2. Módulo Inferencial (`analisis/inferencial.py`)
*   **Propósito:** Ejecución de contrastes de hipótesis y estimación por intervalos.
*   **Entrada:** Series numéricas y variables categóricas.
*   **Salida:** Diccionarios de resultados con p-values y estadísticos.
*   **Dependencia Crítica:** `scipy.stats`.

## 4. Cálculos Estadísticos Detallados (Rigor Científico)

### 4.1. Estadísticos Descriptivos
*   **Media ($\mu$):** Implementación vía `pandas.Series.mean()`.
*   **Desviación Típica ($s$):** Implementación vía `pandas.Series.std()`, utilizando la **corrección de Bessel** ($n-1$) por defecto para estimaciones insesgadas.
*   **Forma:** Asimetría (`skew()`) y Curtosis (`kurtosis()`) calculadas mediante momentos centrales.

### 4.2. Detección de Valores Atípicos (Outliers)
*   **Método:** Rango Intercuartílico (IQR).
*   **Fórmula:** $[Q_1 - 1.5 \cdot IQR, Q_3 + 1.5 \cdot IQR]$.
*   **Implementación:** Cálculo de percentiles 25 y 75 mediante `pandas.Series.quantile()`.

### 4.3. Tests de Normalidad (Validación de Supuestos)
El sistema selecciona el test según el tamaño de muestra $n$:
1.  **Si $n \leq 5000$:** **Test de Shapiro-Wilk**. Librería: `scipy.stats.shapiro`.
2.  **Si $n > 5000$:** **Test de Kolmogorov-Smirnov** (con datos estandarizados). Librería: `scipy.stats.kstest`.

### 4.4. Contrastes de Hipótesis (Comparación de Medias)
*   **Para 2 Grupos:** **Test T de Student para muestras independientes**. 
    *   *Nota:* Se implementa como **Test de Welch** (`equal_var=False` en `scipy.stats.ttest_ind`) para no asumir homocedasticidad.
*   **Para >2 Grupos:** **ANOVA de un factor**. Librería: `scipy.stats.f_oneway`.

### 4.5. Intervalos de Confianza (IC 95%)
*   **Modelo:** Distribución t-Student.
*   **Librería:** `scipy.stats.sem` (Error estándar) y `scipy.stats.t.ppf` (Valor crítico).
*   **Fórmula:** $\bar{x} \pm t_{\alpha/2, n-1} \cdot \frac{s}{\sqrt{n}}$.

### 4.6. Modelo de Regresión Lineal
*   **Método:** Mínimos Cuadrados Ordinarios (OLS).
*   **Librería:** `sklearn.linear_model.LinearRegression`.
*   **Métrica de Ajuste:** Coeficiente de determinación $R^2$ vía `sklearn.metrics.r2_score`.

> [!IMPORTANT]
> **Observaciones Críticas:**
> 1.  **Heterocedasticidad:** El uso sistemático del Test de Welch en comparaciones de dos grupos es una práctica excelente para evitar errores de Tipo I cuando las varianzas son distintas.
> 2.  **Supuestos de Regresión:** La implementación actual de regresión vía `sklearn` no valida automáticamente la linealidad ni la normalidad de los residuos antes del ajuste. Se recomienda al usuario interpretar el $R^2$ con precaución en distribuciones no normales.
### 5. Flujo de la Aplicación Streamlit
La aplicación gestiona el estado y la navegación mediante un controlador centralizado:
*   **Gestión de Estado:** Se utiliza `st.session_state` para persistir el dataset filtrado entre diferentes vistas, evitando recargas innecesarias.
*   **Optimización:** Uso de `@st.cache_data` en `models/data_loader.py` para cachear la lectura de archivos CSV/Excel, mejorando la latencia significativamente tras la primera carga.
*   **Navegación:** Implementada en `views/sidebar.py`, permitiendo al usuario conmutar entre:
    1.  📊 Análisis Descriptivo (Tablas y métricas).
    2.  📈 Visualización Avanzada (Distribuciones y Boxplots).
    3.  🧪 Inferencia Estadística (Tests e Intervalos).
    4.  🤖 Modelado (Regresión Lineal).

### 6. Pipeline de Datos
1.  **Ingesta:** Lectura multiformato vía `pandas.read_csv` y `pandas.read_excel`.
2.  **Limpieza (`limpiar_datos`):** 
    *   Eliminación de registros con valores nulos en variables críticas.
    *   Eliminación de duplicados exactos para evitar sesgos en el cálculo de la media.
3.  **Transformación:** Conversión dinámica de divisas y cálculo de índices para normalizar el análisis económico.

### 7. Entorno y Dependencias
El archivo `requirements.txt` define el ecosistema crítico:
*   **statsmodels (v0.14.0+):** CRÍTICO. Requerido por la función `crear_scatter_regresion_interactivo` de Plotly Express para el cálculo de líneas de tendencia mediante OLS.
*   **xlsxwriter:** Motor necesario para la exportación de reportes Excel (.xlsx).
*   **Versiones:** Se recomienda Python 3.12 para compatibilidad total.

### 8. Limitaciones y Observaciones Críticas
*   **Sesgo de Selección:** El análisis es descriptivo del dataset cargado; las inferencias (ANOVA) asumen que los datos son una muestra representativa de la población de ingenieros.
*   **Asunciones de Regresión:** El modelo de regresión lineal no valida actualmente la independencia de los errores (Durbin-Watson). Se recomienda su uso como herramienta exploratoria.
*   **P-Hacking:** El sistema permite realizar múltiples tests de hipótesis. Se advierte al usuario que realizar múltiples comparaciones aumenta la probabilidad de falsos positivos si no se aplica una corrección de nivel de significación.

### 9. Instrucciones de Ejecución
*   **Local:** 
    1. Instalar dependencias: `pip install -r requirements.txt`
    2. Ejecutar: `streamlit run app.py`
*   **Nube (Streamlit Cloud):** 
    1. Vincular repositorio de GitHub.
    2. El servidor detectará automáticamente `requirements.txt`. 
    3. **Nota:** La falta de `statsmodels` en el repositorio remoto causará un error en el módulo de regresión interactiva.

---
*Fin de la Memoria Técnica v2.5.3*
