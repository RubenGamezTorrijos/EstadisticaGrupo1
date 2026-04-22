# 📘 MANUAL DE DESARROLLO — Estadística para Ingeniería v.2.2.1
> **Proyecto**: Análisis de Salarios en Ciencia de Datos (2020–2023)
> **Equipo Grupo 1**: Rubén Gámez · Rafael Rodriguez · Leslie Ross · Bryann Vallejo
> **Documento interno** — Uso exclusivo del equipo.

---

## 📋 Tabla de Contenidos

1. [Arquitectura del Proyecto](#1-arquitectura-del-proyecto)
2. [Verificación de Requisitos de la Práctica](#2-verificación-de-requisitos)
3. [Tareas por Rol](#3-tareas-por-rol)
   - [Rafael Rodriguez — Data Manager](#31-rafael-rodriguez--data-manager)
   - [Leslie Ross — Analista Descriptivo](#32-leslie-ross--analista-descriptivo)
   - [Bryann Vallejo — Analista Inferencial](#33-bryann-vallejo--analista-inferencial)
4. [Guía de Librerías](#4-guía-de-librerías)
5. [Guía de Git para el Equipo](#5-guía-de-git-para-el-equipo)

---

## 1. Arquitectura del Proyecto

```
proyecto_estadistica/
│
├── app.py                    ← RUBÉN: Aplicación principal
├── setup_data.py             ← RUBÉN: Script para inicializar y generar el dataset dummy temporal
├── requirements.txt          ← RUBÉN: Dependencias Python
├── README.md                 ← RUBÉN: Documentación pública
├── MANUAL_DESARROLLO.md      ← RUBÉN: Este archivo
│
├── analisis/                 ← Módulos de análisis (cada uno tiene su dueño)
│   ├── estadisticos.py       ← RAFAEL: Limpieza y estadísticos descriptivos
│   ├── graficos.py           ← LESLIE: Visualizaciones (histogramas, boxplots, etc.)
│   ├── inferencial.py        ← BRYANN: Intervalos de confianza y contrastes
│   ├── modelo_regresion.py   ← LESLIE + RAFAEL: Regresión lineal y scatter
│   └── exportacion.py        ← RUBÉN: Generador de PDF
│
├── datos/
│   ├── jobs_in_data.csv       ← Dataset original (NO MODIFICAR)
│   ├── cost_of_living_index.csv ← NUEVO: Datos reales Numbeo 2023
│   └── dataset_enriquecido.csv  ← Dataset FINAL generado por script
│
├── scripts/
│   └── preprocesar_coli.py    ← RUBÉN: Script de integración COLI (Merge)
│
├── informes/
│   ├── enunciado_practica.md ← Requisitos oficiales del profesor
│   ├── informe_descriptivo.md
│   └── informe_inferencial.md
│
└── outputs/                  ← Carpeta auto-generada (ignorar en Git)
    ├── graficos/
    └── tablas/
```

### ¿Cómo fluyen los datos?

```
jobs_in_data.csv + cost_of_living_index.csv
      ↓
  preprocesar_coli.py     [Rubén — scripts/] -> dataset_enriquecido.csv
      ↓
  limpiar_datos()         [Rafael — estadisticos.py]
      ↓
calcular_estadisticos()   [Rafael — estadisticos.py]
      ↓
  crear_histograma()      [Leslie — graficos.py]
  crear_boxplot()         [Leslie — graficos.py]
      ↓
  calcular_ic_95()        [Bryann — inferencial.py]
  contraste_hipotesis()   [Bryann — inferencial.py]
      ↓
  generar_pdf()           [Rubén — exportacion.py]
```

---

## 2. Verificación de Requisitos

Esta tabla confirma que el proyecto cumple **todos los requisitos mínimos** del enunciado del profesor:

### ✅ Dataset (Sección 1 del Enunciado)

| Requisito | Estado | Detalle |
| :--- | :---: | :--- |
| Muestra mínima 100 datos | ✅ | +3.500 registros en `ds_salaries.csv` |
| ≥ 2 variables numéricas continuas | ✅ | `salary_in_usd`/`salary_in_eur` y `cost_of_living_index` |
| 1 variable discreta | ✅ | `work_year` (2020–2023) |
| 1 variable categórica | ✅ | `experience_level`, `job_category`, `work_setting` |
| No es serie temporal | ✅ | Datos de corte transversal por año |

### ✅ Análisis Descriptivo (Sección 2 del Enunciado)

| Requisito | Estado | Archivo | Función |
| :--- | :---: | :--- | :--- |
| Media, mediana, moda, rango, desv. típica, varianza | ✅ | `estadisticos.py` | `calcular_estadisticos()` |
| Histogramas | ✅ | `graficos.py` | `crear_histograma()` |
| Diagramas de barra | ✅ | `graficos.py` | `crear_bar_chart()` |
| Caja y bigotes (boxplot) | ✅ | `graficos.py` | `crear_boxplot()` |
| Análisis de regresión + scatter + coef. correlación | ✅ | `graficos.py` | `crear_scatter_regresion()` |
| Boxplot por variable categórica | ✅ | `graficos.py` | `crear_boxplot(df, 'salary_in_usd' / 'salary_in_eur', 'experience_level')` |
| Discusión crítica de resultados | ⚠️ | `informes/informe_descriptivo.md` | Redactar en equipo |

### ✅ Análisis Inferencial (Sección 3 del Enunciado)

| Requisito | Estado | Archivo | Función |
| :--- | :---: | :--- | :--- |
| IC para variable continua 1 (`salary_in_usd`) | ✅ | `inferencial.py` | `calcular_ic_95()` |
| IC para variable continua 2 (`cost_of_living_index`) | ✅ | `inferencial.py` | `calcular_ic_95()` |
| Contraste de hipótesis var. 1 | ✅ | `inferencial.py` | `contraste_hipotesis_1_muestra()` |
| Contraste de hipótesis var. 2 (entre grupos) | ✅ | `inferencial.py` | `contraste_hipotesis()` |
| Justificación y explicación de resultados | ⚠️ | `informes/informe_inferencial.md` | Redactar Bryann |

### ✅ Mejora Propia — Variable `cost_of_living_index` (PROFESIONAL)

> **Pregunta de investigación**: *¿Suben los salarios en países con mayor coste de vida?*

- **Fuente**: Datos reales extraídos de **NUMBEO 2023 Mid-Year** (`cost_of_living_index.csv`)
- **Proceso de Integración**: Se utiliza el script `scripts/preprocesar_coli.py` para realizar un merge entre el dataset de salarios y el índice de coste de vida por país (`company_location`).
- **Nuevas Variables**: 
    - `cost_of_living_index`: Índice real del país.
    - `salary_adjusted_coli`: Salario real ajustado por poder adquisitivo.
- **Análisis**: Scatter plot `cost_of_living_index` vs `salary_in_usd` + regresión lineal.
- **Cobertura**: 100% de los países integrados (70 países).

| País | Índice COLI |
|:---|:---:|
| EE.UU. (referencia) | 100 |
| Australia | 95 |
| Canadá | 90 |
| Irlanda | 90 |
| Reino Unido | 85 |
| Alemania / Francia | 80 |
| España / Estonia | 70/65 |
| México / Colombia | 45/40 |
| India | 30 |

---

## 3. Tareas por Rol

---

### 3.1 Rafael Rodriguez — Data Manager

**Archivo**: `analisis/estadisticos.py`

#### Tarea R-01: `limpiar_datos(df)` ✅ ACTUALIZADA

Elimina duplicados, nulos y estandariza tipos. Carga el `dataset_enriquecido.csv` generado por el script de preprocesamiento.

```python
# Rafael ahora consume el dataset ya enriquecido con COLI real
def cargar_datos_maestros():
    # Carga el dataset que ya contiene el COLI real y el salario ajustado
    df = pd.read_csv('datos/dataset_enriquecido.csv')
    return limpiar_datos(df)

# Cómo funciona internamente:
df_limpio = df.copy()                             # No modificar el original
df_limpio = df_limpio.drop_duplicates()           # Paso 1: Eliminar filas iguales
df_limpio = df_limpio.dropna(                     # Paso 2: Eliminar nulos en columnas clave
    subset=['salary_in_usd', 'experience_level', 'job_category']
)
df_limpio['work_year'] = df_limpio['work_year'].astype(int)      # Paso 3: Tipo correcto
df_limpio['salary_in_usd'] = df_limpio['salary_in_usd'].astype(float)

# Paso extra: Crear salary_in_eur (si no existe) con tipo de cambio base 0.92
if 'salary_in_eur' not in df_limpio.columns:
    df_limpio['salary_in_eur'] = df_limpio['salary_in_usd'] * 0.92

# Paso extra: Crear cost_of_living_index usando company_location
df_limpio['cost_of_living_index'] = df_limpio['company_location'].map(COST_OF_LIVING_INDEX).fillna(70)
```

#### Tarea R-02: `calcular_estadisticos(df)` ✅ IMPLEMENTADA

Calcula: N, Media, Mediana, Moda, Mínimo, Máximo, Rango, Q1, Q3, IQR, Desv. Típica, Varianza, CV%, Asimetría, Curtosis para `salary_in_usd`, `salary_in_eur`, `work_year` y `cost_of_living_index`.

> 📌 **Verificar**: Asegúrate de que el DataFrame retornado tiene exactamente estas columnas:
> `['Variable', 'N', 'Media', 'Mediana', 'Moda', 'Mínimo', 'Máximo', 'Rango', 'Q1', 'Q3', 'IQR', 'Desviación Típica', 'Varianza', 'CV%', 'Asimetría', 'Curtosis']`

#### Tarea R-03: `calcular_estadisticos_por_categoria(df, col_num, col_cat)` ✅ IMPLEMENTADA

Calcula estadísticos agrupados. Ejemplo de uso:
```python
# Estadísticos de salario por nivel de experiencia:
tabla = calcular_estadisticos_por_categoria(df, 'salary_in_usd', 'experience_level')
```

#### Tarea R-04: `detectar_outliers_iqr(df, columna)` ✅ IMPLEMENTADA

Detecta outliers usando el criterio IQR. Retorna una fila con los límites y el nº de valores atípicos.
```python
outliers = detectar_outliers_iqr(df, 'salary_in_usd')
# Resultado: Q1, Q3, IQR, Límite Inferior, Límite Superior, N Outliers, % Outliers
```

> ✅ **Tarea de Rafael completada**. Documentar resultados en `informes/informe_descriptivo.md`.

---

### 3.2 Leslie Ross — Analista Descriptivo

**Archivo principal**: `analisis/graficos.py`

#### Tarea L-01: `crear_histograma(df, columna)` 🛠️ PENDIENTE

**¿Qué hace?** Dibuja la distribución de frecuencias con curva de densidad (KDE) y marca Media, Mediana, Q1 y Q3 con líneas verticales.

```python
# TEMPLATE COMPLETO — Copia esto dentro del bloque TODO
configurar_estilo()
fig, ax = plt.subplots(figsize=(14, 8))

# --- Calcular estadísticos ---
media   = df[columna].mean()
mediana = df[columna].median()
q1      = df[columna].quantile(0.25)
q3      = df[columna].quantile(0.75)

sym = "$" if "usd" in columna.lower() else "€"

# --- Histograma con KDE ---
sns.histplot(data=df, x=columna, bins=bins, kde=True, ax=ax,
             color='skyblue', edgecolor='white')

# --- Líneas de estadísticos ---
ax.axvline(media,   color='red',    linestyle='--', linewidth=2.5,
           label=f'Media: {media:,.0f} {sym}')
ax.axvline(mediana, color='green',  linestyle='--', linewidth=2.5,
           label=f'Mediana: {mediana:,.0f} {sym}')
ax.axvline(q1,      color='orange', linestyle=':',  linewidth=2,
           label=f'Q1 (25%): {q1:,.0f} {sym}')
ax.axvline(q3,      color='orange', linestyle=':',  linewidth=2,
           label=f'Q3 (75%): {q3:,.0f} {sym}')

# --- Etiquetas y formato ---
ax.set_title(sanitize_pdf_text(titulo), fontsize=18, fontweight='bold', pad=20)
ax.set_xlabel(obtener_label(columna), fontsize=14)
ax.set_ylabel('Frecuencia', fontsize=14)
ax.xaxis.set_major_formatter(formatter)   # Formato español: 1.234.567
ax.legend(fontsize=12, frameon=True, shadow=True)
plt.tight_layout()

return fig
```

#### Tarea L-02: `crear_boxplot(df, num, cat)` 🛠️ PENDIENTE

**¿Qué hace?** Muestra la distribución de una variable numérica agrupada por categoría, mostrando outliers.

```python
# TEMPLATE COMPLETO
configurar_estilo()
fig, ax = plt.subplots(figsize=(14, 8))

# El parámetro hue=cat evita deprecation warnings en seaborn moderno
sns.boxplot(data=df, x=cat, y=num, ax=ax, palette='Set2',
            hue=cat, legend=False, showfliers=True)

ax.set_title(sanitize_pdf_text(titulo), fontsize=18, fontweight='bold', pad=20)
ax.set_xlabel(obtener_label(cat), fontsize=14)
ax.set_ylabel(obtener_label(num), fontsize=14)
plt.xticks(rotation=45)
ax.yaxis.set_major_formatter(formatter)
plt.tight_layout()

return fig
```

#### Tarea L-03: `crear_violin_plot(df, x, y)` 🛠️ PENDIENTE

**¿Qué hace?** Combina boxplot + curva de densidad. Muestra CÓMO se distribuyen los datos dentro de cada grupo (no solo los cuartiles).

```python
# TEMPLATE COMPLETO
configurar_estilo()
fig, ax = plt.subplots(figsize=(14, 8))

# inner='quartile' muestra Q1, Q2, Q3 dentro del violín
sns.violinplot(data=df, x=x, y=y, ax=ax, palette='muted',
               inner='quartile', hue=x, legend=False)

ax.set_title(sanitize_pdf_text(titulo), fontsize=18, fontweight='bold', pad=20)
ax.set_xlabel(obtener_label(x), fontsize=14)
ax.set_ylabel(obtener_label(y), fontsize=14)
plt.xticks(rotation=45)
ax.yaxis.set_major_formatter(formatter)
plt.tight_layout()

return fig
```

#### Tarea L-04: `crear_grafico_interactivo(df, x, y, color, tipo)` 🛠️ PENDIENTE

**¿Qué hace?** Genera gráficos interactivos con Plotly (el usuario puede hacer zoom, filtrar, etc.).

```python
# TEMPLATE COMPLETO
if not PLOTLY_AVAILABLE:
    return None   # Si Plotly no está instalado, devolver None

tipos = {
    'scatter':   px.scatter(df, x=x, y=y, color=color,
                            hover_data=df.columns, template='plotly_white'),
    'bar':       px.bar(df, x=x, y=y, color=color, template='plotly_white'),
    'box':       px.box(df, x=x, y=y, color=color, template='plotly_white'),
    'histogram': px.histogram(df, x=x, nbins=50, template='plotly_white'),
    'violin':    px.violin(df, x=x, y=y, color=color, box=True,
                           points='all', template='plotly_white'),
}

if tipo not in tipos:
    return None

fig = tipos[tipo]
fig.update_layout(title=f"Gráfico Interactivo ({tipo})",
                  margin=dict(l=20, r=20, t=50, b=20))
return fig
```

---

### 3.3 Bryann Vallejo — Analista Inferencial

**Archivo principal**: `analisis/inferencial.py`

#### Tarea B-01: `calcular_ic_95(data, confianza=0.95)` 🛠️ PENDIENTE

**¿Qué hace?** Calcula el Intervalo de Confianza para la media usando la distribución **T de Student** (no la Normal, porque la varianza poblacional es desconocida).

**Concepto clave**:
```
IC = media ± t_critico * (desv_tipica / √n)
```

```python
# TEMPLATE COMPLETO
data = data.dropna()
n = len(data)
if n < 2:
    return {}  # No se puede calcular con menos de 2 datos

media        = data.mean()
std          = data.std()
se           = std / np.sqrt(n)                      # Error Estándar
t_critico    = t.ppf((1 + confianza) / 2, df=n - 1) # Valor crítico T
margen_error = t_critico * se
ic_inferior  = media - margen_error
ic_superior  = media + margen_error

return {
    # Versión legible para mostrar en la UI:
    'Media': media, 'Inferior': ic_inferior, 'Superior': ic_superior,
    'Margen Error': margen_error,
    # Versión para funciones internas:
    'media': media, 'ic_inferior': ic_inferior, 'ic_superior': ic_superior,
    'margen_error': margen_error, 'n': n, 'se': se, 't_critico': t_critico
}
```

#### Tarea B-02: `contraste_hipotesis_1_muestra(data, mu0, alfa=0.05)` 🛠️ PENDIENTE

**¿Qué hace?** Contrasta H₀: μ = mu0 con un **T-test de una muestra**. Ejemplo: ¿Es la media salarial igual a 100.000 $?

```python
# TEMPLATE COMPLETO
data = data.dropna()
media = data.mean()
std   = data.std()

t_stat, p_valor = ttest_1samp(data, mu0, alternative=alternativa)
rechaza_h0 = p_valor < alfa
cohen_d    = (media - mu0) / std if std != 0 else 0  # Tamaño del efecto

return {
    'Hipótesis Nula':  f'mu = {mu0:,.0f}',
    'Media Muestral':  media,
    'mu0':             mu0,
    'T-Stat':          float(t_stat),
    'P-Valor':         float(p_valor),
    'Decisión':        'Rechazar H0' if rechaza_h0 else 'No Rechazar H0',
    'Conclusión':      f'La media ES diferente de {mu0:,.0f}' if rechaza_h0
                       else f'La media NO es diferente de {mu0:,.0f}',
    'Cohen d':         np.round(float(cohen_d), 4),
    'rechaza_h0':      bool(rechaza_h0),
    'p_valor':         float(p_valor),
    't_statistic':     float(t_stat)
}
```

#### Tarea B-03: `contraste_hipotesis(grupo1, grupo2, label1, label2)` 🛠️ PENDIENTE

**¿Qué hace?** Compara dos grupos con el **Welch T-test** (no asume varianzas iguales). Ejemplo: ¿Es el salario de "Senior" mayor que "Mid-level"?

```python
# TEMPLATE COMPLETO
grupo1, grupo2 = grupo1.dropna(), grupo2.dropna()
n1, n2         = len(grupo1), len(grupo2)
media1, media2 = grupo1.mean(), grupo2.mean()
std1, std2     = grupo1.std(), grupo2.std()

# Welch T-test: equal_var=False porque no asumimos varianzas iguales
t_stat, p_valor  = ttest_ind(grupo1, grupo2, equal_var=False)
diferencia       = media1 - media2

# Cohen's d — mide la magnitud del efecto
pooled_std = np.sqrt(((n1-1)*std1**2 + (n2-1)*std2**2) / (n1+n2-2))
cohen_d    = diferencia / pooled_std if pooled_std != 0 else 0
rechaza_h0 = p_valor < alfa

return {
    'Comparación':       f'{label1} vs {label2}',
    'Media G1':          media1,  'Media G2': media2,
    'Diferencia Medias': diferencia,
    'T-Stat':            float(t_stat), 'P-Valor': float(p_valor),
    'Decisión':          'Rechazar H0' if rechaza_h0 else 'No Rechazar H0',
    'Conclusión':        f'Diferencia significativa entre {label1} y {label2}' if rechaza_h0
                         else f'Sin diferencia significativa',
    'Cohen d':           np.round(float(cohen_d), 4),
    'rechaza_h0':        bool(rechaza_h0), 'p_valor': float(p_valor),
    't_statistic':       float(t_stat)
}
```

#### Tarea B-04: `anova_one_way(df, col_num, col_grupo)` 🛠️ PENDIENTE

**¿Qué hace?** Compara más de 2 grupos a la vez con el **F-test** (ANOVA). Ejemplo: ¿Hay diferencias de salario entre los 4 niveles de experiencia?

```python
# TEMPLATE COMPLETO
grupos = [grupo[columna_numerica].dropna()
          for _, grupo in df.groupby(columna_grupo)]
if len(grupos) < 2:
    return {}

f_stat, p_valor = f_oneway(*grupos)   # * desempaqueta la lista de grupos
rechaza_h0 = p_valor < alfa

estadisticos_grupos = df.groupby(columna_grupo)[columna_numerica].agg(
    ['count', 'mean', 'std', 'min', 'max']
).round(2)

return {
    'Hipótesis Nula':       'Todas las medias son iguales',
    'F-Stat':               float(f_stat),
    'P-Valor':              float(p_valor),
    'Decisión':             'Rechazar H0' if rechaza_h0 else 'No Rechazar H0',
    'Conclusión':           'Diferencias significativas' if rechaza_h0
                            else 'Sin diferencias significativas',
    'Estadísticos por Grupo': estadisticos_grupos,
    'f_statistic':          float(f_stat),
    'p_valor':              float(p_valor),
    'rechaza_h0':           bool(rechaza_h0)
}
```

#### Tarea B-05: `verificar_supuestos_normalidad(data)` 🛠️ PENDIENTE

**¿Qué hace?** Verifica si los datos siguen una distribución normal. Usa Shapiro-Wilk para n ≤ 5000 y Kolmogorov-Smirnov para n > 5000.

```python
# TEMPLATE COMPLETO
data = data.dropna()
n = len(data)

if n <= 5000:
    stat, p_valor = shapiro(data)
    prueba = 'Shapiro-Wilk'
else:
    stat, p_valor = stats.kstest(data, 'norm', args=(data.mean(), data.std()))
    prueba = 'Kolmogorov-Smirnov'

es_normal = p_valor > 0.05  # Si p > 0.05, NO rechazamos normalidad

return {
    'Prueba': prueba, 'Estadístico': stat, 'P-Valor': p_valor,
    'Es Normal': es_normal,
    'Conclusión': 'Datos normales' if es_normal else 'Datos NO normales',
    'estadistico': float(stat), 'p_valor': float(p_valor),
    'es_normal': bool(es_normal),
    'conclusion': 'Distribución normal' if es_normal else 'Sin normalidad'
}
```

#### Tarea B-06: `verificar_homocedasticidad(grupo1, grupo2)` 🛠️ PENDIENTE

**¿Qué hace?** Comprueba si dos grupos tienen varianzas similares (Levene test).

```python
# TEMPLATE COMPLETO
stat, p_valor     = levene(grupo1.dropna(), grupo2.dropna())
varianzas_iguales = p_valor > 0.05

return {
    'Prueba': 'Levene', 'Estadístico': stat, 'P-Valor': p_valor,
    'Varianzas Iguales': varianzas_iguales,
    'Conclusión': 'Homocedasticidad' if varianzas_iguales else 'Heterocedasticidad',
    'estadistico': float(stat), 'p_valor': float(p_valor),
    'varianzas_iguales': bool(varianzas_iguales),
    'conclusion': 'Varianzas iguales' if varianzas_iguales else 'Varianzas diferentes'
}
```

---

## 4. Guía de Librerías

### 🐼 Pandas — Manipulación de datos

```python
import pandas as pd

df = pd.read_csv('datos/ds_salaries.csv')   # Leer CSV
df.head()                                    # Ver primeras 5 filas
df.info()                                    # Ver tipos y nulos
df.describe()                                # Estadísticos rápidos
df['salary_in_usd'].mean()                   # Media de una columna
df['salary_in_usd'].median()                 # Mediana
df.groupby('experience_level')['salary_in_usd'].mean()  # Media por grupo
df.dropna(subset=['salary_in_usd'])          # Eliminar nulos en columna
df.drop_duplicates()                         # Eliminar duplicados
df.astype({'work_year': int})                # Cambiar tipo
```

### 🔢 NumPy — Cálculos numéricos

```python
import numpy as np

np.sqrt(n)        # Raíz cuadrada (para error estándar)
np.mean([1,2,3])  # Media
np.std([1,2,3])   # Desviación típica
np.round(3.14159, 4)  # Redondear a 4 decimales
```

### 📊 Seaborn + Matplotlib — Gráficos estáticos (Leslie)

```python
import seaborn as sns
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(14, 8))  # Crear figura y ejes

sns.histplot(data=df, x='salary_in_usd', bins=30, kde=True, ax=ax)
ax.set_title('Mi Título', fontsize=16)
ax.set_xlabel('Salario USD', fontsize=12)
ax.set_ylabel('Frecuencia', fontsize=12)
plt.tight_layout()   # Ajustar márgenes
plt.show()           # Mostrar (solo en notebook/scripts)
# En Streamlit: st.pyplot(fig)
```

### 📈 Plotly — Gráficos interactivos (Leslie)

```python
import plotly.express as px

fig = px.scatter(df, x='cost_of_living_index', y='salary_in_usd',
                 color='experience_level', template='plotly_white')
fig.show()
# En Streamlit: st.plotly_chart(fig)
```

### 🔬 SciPy — Tests estadísticos (Bryann)

```python
from scipy.stats import t, ttest_1samp, ttest_ind, f_oneway, shapiro, levene

# T de Student valor crítico (95%):
t_critico = t.ppf((1 + 0.95) / 2, df=n-1)

# T-test 1 muestra:
t_stat, p_valor = ttest_1samp(data, mu0=100000)

# T-test 2 muestras (Welch):
t_stat, p_valor = ttest_ind(grupo1, grupo2, equal_var=False)

# ANOVA F-test:
f_stat, p_valor = f_oneway(grupo1, grupo2, grupo3, grupo4)

# Shapiro-Wilk (normalidad):
stat, p_valor = shapiro(data)

# Levene (homocedasticidad):
stat, p_valor = levene(grupo1, grupo2)

# Regla: si p_valor < 0.05 → Rechazar H0
```

---

## 5. Guía de Git para el Equipo

### Configuración inicial (solo una vez)

```bash
# Verificar que Git está instalado
git --version

# Configurar usuario (cada uno con sus datos)
git config --global user.name "Tu Nombre"
git config --global user.email "tu.email@universidad.es"

# Clonar el repositorio (si no lo tienes ya)
git clone https://github.com/ruben-mg-dev/estadisticagrupo1.git
cd estadisticagrupo1
```

### Flujo de trabajo diario

```bash
# 1. SIEMPRE empezar actualizando tu copia local
git checkout dev           # Asegúrate de estar en la rama dev
git pull origin dev        # Descarga los cambios del equipo

# 2. Trabajar en tu archivo asignado
#    (editar estadisticos.py, graficos.py o inferencial.py)

# 3. Ver qué has cambiado
git status
git diff analisis/graficos.py  # Ver los cambios de un archivo específico

# 4. Guardar tus cambios (commit)
git add analisis/graficos.py                         # Solo tu archivo
git commit -m "feat(graficos): Implementa crear_histograma con KDE y estadísticos"

# 5. Subir tus cambios a GitHub
git push origin dev

# 6. Avisa al equipo en grupos WhatsApp/Teams que has subido cambios
```

### Convención de mensajes de commit

```
feat(archivo): descripción breve
fix(archivo): descripción del error corregido
docs(archivo): cambio en documentación
```

**Ejemplos reales para cada uno**:
```bash
# Rafael:
git commit -m "feat(estadisticos): Implementa limpiar_datos con COLI index"

# Leslie:
git commit -m "feat(graficos): Implementa crear_histograma con líneas Media y Q3"
git commit -m "feat(graficos): Implementa crear_boxplot y violin_plot"

# Bryann:
git commit -m "feat(inferencial): Implementa calcular_ic_95 con T de Student"
git commit -m "feat(inferencial): Implementa ANOVA y tests de normalidad"
```

### ⚠️ Reglas de seguridad del repositorio

```
✅ Sube SOLO los archivos que te corresponden.
✅ NO uses: git add .   (esto añade TODO y puede sobrescribir el trabajo de otros)
✅ Haz commits pequeños y frecuentes (mejor que uno grande al final).
❌ NO modifiques: app.py, exportacion.py, __init__.py (son de Rubén)
❌ NO hagas merge a main sin permiso de Rubén.
```

### Si algo sale mal (recuperar errores)

```bash
# Deshacer el último commit (mantiene los cambios en el archivo):
git reset --soft HEAD~1

# Descartar los cambios de un archivo (¡cuidado! no recuperable):
git checkout -- analisis/graficos.py

# Ver el historial de commits:
git log --oneline -10
```

---

## Resumen de Estado del Proyecto

| Miembro | Rol | Archivos | Estado |
| :--- | :--- | :--- | :---: |
| **Rubén Gámez** | Arquitecto / Coordinador | `app.py`, `exportacion.py`, `__init__.py` | ✅ FINALIZADO |
| **Rafael Rodriguez** | Data Manager | `estadisticos.py` | ✅ FINALIZADO |
| **Leslie Ross** | Analista Descriptivo | `graficos.py` | 🛠️ PENDIENTE |
| **Bryann Vallejo** | Analista Inferencial | `inferencial.py` | 🛠️ PENDIENTE |

---

*Documento generado para el equipo de Estadística para Ingeniería — Grupo 1*
*Arquitecto del sistema: Rubén Torrijos*
