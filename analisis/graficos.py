"""
PROYECTO: Estadística para Ingeniería
MIEMBRO: LESLIE ROSS ARANIBAR POZO (Analista Descriptivo)
TAREA: Visualizaciones estadísticas, Violin Plot, Regresión y Gráficos Interactivos

INSTRUCCIONES PARA COMPLETAR:
================================
Debes implementar las funciones marcadas con '# TODO: COMPLETAR'
siguiendo las instrucciones en los docstrings.

Funciones que DEBES completar:
1. crear_histograma()          - Histograma con KDE y líneas de Media, Mediana, Q1 y Q3
2. crear_boxplot()             - Boxplot agrupado por categoría
3. crear_violin_plot()         - Violin Plot por categoría (distribución completa)
4. crear_scatter_regresion()   - Scatter Plot con línea de regresión y R², r en el gráfico
5. crear_grafico_interactivo() - Gráficos interactivos via Plotly

LIBRERÍAS DISPONIBLES:
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.ticker import FuncFormatter

# Plotly (opcional pero recomendado):
import plotly.express as px
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

from matplotlib.ticker import FuncFormatter


# Formateador de números en español (ya implementado - no tocar)
def fmt_es(x, pos):
    """Formato español: 1.234.567"""
    return f"{x:,.0f}".replace(",", "@").replace(".", ",").replace("@", ".")


formatter = FuncFormatter(fmt_es)


def configurar_estilo():
    """Configura el estilo base de los gráficos."""
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (12, 6)
    plt.rcParams['font.size'] = 12


# Mapeo de variables para etiquetas legibles
VAR_LABELS = {
    'work_year': 'Año de Trabajo',
    'experience_level': 'Nivel de Experiencia',
    'employment_type': 'Tipo de Empleo',
    'job_title': 'Titulo de Empleo',
    'salary': 'Salario (EUR)',
    'salary_currency': 'Moneda',
    'salary_in_usd': 'Salario (USD)',
    'employee_residence': 'Residencia Empleado',
    'remote_ratio': 'Ratio Remoto',
    'company_location': 'Ubicacion Empresa',
    'company_size': 'Tamaño Empresa',
    'job_category': 'Categoria de Puesto',
    'work_setting': 'Modalidad de Trabajo'
}

def sanitize_pdf_text(text):
    """Limpia caracteres que rompen la fuente Helvetica estándar de FPDF"""
    if not isinstance(text, str):
        text = str(text)
    replacements = {
        '₀': '0', '₁': '1', '₂': '2', '₃': '3', '₄': '4',
        'µ': 'mu', 'μ': 'mu', 'σ': 'sigma', 'π': 'pi',
        '²': '^2', '±': '+/-', '≥': '>=', '≤': '<=', '≠': '!='
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    try:
        return text.encode('latin-1', 'replace').decode('latin-1')
    except:
        return text

def obtener_label(col):
    """Retorna la etiqueta legible para una columna."""
    return VAR_LABELS.get(col, col.replace('_', ' ').title())

def guardar_grafico(fig, nombre, ruta='outputs/graficos/'):
    """
    LESLIE ROSS - Guarda un gráfico como PNG.
    (Esta función ya está implementada, no la modifiques)
    """
    os.makedirs(ruta, exist_ok=True)
    ruta_completa = os.path.join(ruta, nombre)
    fig.savefig(ruta_completa, bbox_inches='tight', dpi=150)
    plt.close(fig)
    return ruta_completa


def crear_histograma(df, columna, titulo='Histograma', bins=30,
                     guardar=False, ruta_guardado='outputs/graficos/'):
    """
    LESLIE ROSS ARANIBAR POZO - Histograma con KDE y Líneas de Estadísticos

    El histograma DEBE incluir:
    ✅ Barras del histograma + curva KDE suavizada (usa sns.histplot con kde=True)
    ✅ Línea vertical ROJA:   Media del dataset   → ax.axvline(media, color='red', linestyle='--')
    ✅ Línea vertical VERDE:  Mediana             → ax.axvline(mediana, color='green', linestyle='--')
    ✅ Línea vertical NARANJA:Q1 (percentil 25%)  → ax.axvline(q1, color='orange', linestyle=':')
    ✅ Línea vertical NARANJA:Q3 (percentil 75%)  → ax.axvline(q3, color='orange', linestyle=':')
    ✅ Leyenda que muestre el valor de cada estadístico : label=f'Media: ${media:,.0f}'
    ✅ Títulos de ejes y del gráfico
    ✅ Formatear el eje X con el formatter español (eje X: formatter)

    PISTA PARA LAS LÍNEAS DE ESTADÍSTICOS:
        media   = df[columna].mean()
        mediana = df[columna].median()
        q1      = df[columna].quantile(0.25)
        q3      = df[columna].quantile(0.75)
        ax.axvline(media, color='red', linestyle='--', linewidth=2.5,
                   label=f'Media: ${media:,.0f}')
        ... (idem para mediana, q1, q3)

    Args:
        df: DataFrame con los datos
        columna: columna a graficar (ej: 'salary_in_usd')
        titulo: título del gráfico
        bins: número de barras del histograma (por defecto 30)
        guardar: Si True, guarda el gráfico como PNG
        ruta_guardado: directorio para guardar

    Returns:
        matplotlib.figure.Figure
    """
    # TODO: COMPLETAR

    # ╔═════════════════════════════════════════════════════╗
    # ║  ¡IMPLEMENTA AQUÍ EL HISTOGRAMA CON KDE Y LÍNEAS!  ║
    # ╚═════════════════════════════════════════════════════╝

    configurar_estilo()
    fig, ax = plt.subplots(figsize=(14, 8))

    media = df[columna].mean()
    mediana = df[columna].median()
    q1 = df[columna].quantile(0.25)
    q3 = df[columna].quantile(0.75)

    sns.histplot(data=df, x=columna, bins=bins, kde=True, ax=ax, color='skyblue', edgecolor='white')
    
    ax.axvline(media, color='red', linestyle='--', linewidth=2.5, label=f'Media: {media:,.2f}')
    ax.axvline(mediana, color='green', linestyle='--', linewidth=2.5, label=f'Mediana: {mediana:,.2f}')
    ax.axvline(q1, color='orange', linestyle=':', linewidth=2, label=f'Q1 (25%): {q1:,.2f}')
    ax.axvline(q3, color='orange', linestyle=':', linewidth=2, label=f'Q3 (75%): {q3:,.2f}')

    ax.set_title(sanitize_pdf_text(titulo), fontsize=18, fontweight='bold', pad=20)
    ax.set_xlabel(obtener_label(columna), fontsize=14)
    ax.set_ylabel('Frecuencia', fontsize=14)
    ax.xaxis.set_major_formatter(formatter)
    ax.legend(fontsize=12, frameon=True, shadow=True)

    plt.tight_layout()

    if guardar:
        guardar_grafico(fig, f'histograma_{columna}.png', ruta_guardado)

    return fig


def crear_boxplot(df, num, cat, titulo='Boxplot',
                  guardar=False, ruta_guardado='outputs/graficos/'):
    """
    LESLIE ROSS ARANIBAR POZO - Boxplot por Categoría

    Muestra la distribución de una variable numérica agrupada
    por una variable categórica, incluyendo outliers visibles.

    INSTRUCCIONES:
    ✅ Usa sns.boxplot(data=df, x=cat, y=num, palette='Set2', showfliers=True)
    ✅ Rota las etiquetas del eje X 45 grados para mejor legibilidad
    ✅ Añade título y labels en los ejes
    ✅ Formatea el eje Y con el formatter español

    PISTA:
        fig, ax = plt.subplots(figsize=(14, 8))
        sns.boxplot(data=df, x=cat, y=num, ax=ax, palette='Set2',
                    hue=cat, legend=False, showfliers=True)
        ax.yaxis.set_major_formatter(formatter)

    Args:
        df: DataFrame con los datos
        num: nombre de la columna numérica (ej: 'salary_in_usd')
        cat: nombre de la columna categórica (ej: 'experience_level')
        titulo: título del gráfico
        guardar: Si True, guarda el gráfico como PNG

    Returns:
        matplotlib.figure.Figure
    """
    # TODO: COMPLETAR

    # ╔═══════════════════════════════════════╗
    # ║  ¡IMPLEMENTA AQUÍ EL BOXPLOT!         ║
    # ╚═══════════════════════════════════════╝

    configurar_estilo()
    fig, ax = plt.subplots(figsize=(14, 8))

    sns.boxplot(data=df, x=cat, y=num, ax=ax, palette='Set2', hue=cat, legend=False, showfliers=True)
    
    ax.set_title(sanitize_pdf_text(titulo), fontsize=18, fontweight='bold', pad=20)
    ax.set_xlabel(obtener_label(cat), fontsize=14)
    ax.set_ylabel(obtener_label(num), fontsize=14)
    plt.xticks(rotation=45)
    ax.yaxis.set_major_formatter(formatter)

    plt.tight_layout()

    if guardar:
        guardar_grafico(fig, f'boxplot_{num}_{cat}.png', ruta_guardado)

    return fig


def crear_violin_plot(df, x, y, titulo='Violin Plot',
                      guardar=False, ruta_guardado='outputs/graficos/'):
    """
    LESLIE ROSS ARANIBAR POZO - Violin Plot por Categoría

    El Violin Plot combina un Boxplot con una curva de densidad (KDE),
    mostrando CÓMO se distribuyen los datos dentro de cada grupo,
    no solo sus cuartiles.

    INSTRUCCIONES:
    ✅ Usa sns.violinplot(data=df, x=x, y=y, palette='muted', inner='quartile')
       → inner='quartile' muestra Q1, Q2, Q3 dentro del violín
    ✅ Añade título formateado y labels en ambos ejes
    ✅ Formatea el eje Y con el formatter español

    PISTA:
        fig, ax = plt.subplots(figsize=(14, 8))
        sns.violinplot(data=df, x=x, y=y, ax=ax, palette='muted', inner='quartile')

    Args:
        df: DataFrame con los datos
        x: columna categórica (eje X, ej: 'experience_level')
        y: columna numérica (eje Y, ej: 'salary_in_usd')
        titulo: título del gráfico
        guardar: Si True, guarda el gráfico como PNG

    Returns:
        matplotlib.figure.Figure
    """
    # TODO: COMPLETAR

    # ╔═══════════════════════════════════════════╗
    # ║  ¡IMPLEMENTA AQUÍ EL VIOLIN PLOT!         ║
    # ╚═══════════════════════════════════════════╝

    configurar_estilo()
    fig, ax = plt.subplots(figsize=(14, 8))

    sns.violinplot(data=df, x=x, y=y, ax=ax, palette='muted', inner='quartile', hue=x, legend=False)
    
    ax.set_title(sanitize_pdf_text(titulo), fontsize=18, fontweight='bold', pad=20)
    ax.set_xlabel(obtener_label(x), fontsize=14)
    ax.set_ylabel(obtener_label(y), fontsize=14)
    plt.xticks(rotation=45)
    ax.yaxis.set_major_formatter(formatter)

    plt.tight_layout()

    if guardar:
        guardar_grafico(fig, f'violin_{x}_{y}.png', ruta_guardado)

    return fig


def crear_scatter_regresion(df, x_col, y_col, titulo='Dispersión y Regresión',
                            guardar=False, ruta_guardado='outputs/graficos/'):
    """
    LESLIE ROSS ARANIBAR POZO - Scatter Plot con Regresión Lineal

    DEBE mostrar:
    ✅ Puntos de dispersión (sns.scatterplot)
    ✅ Línea de regresión ROJA calculada manualmente con numpy:
        m, b = np.polyfit(df[x_col], df[y_col], 1)   ← pendiente e intercepto
        r    = np.corrcoef(df[x_col], df[y_col])[0,1] ← correlación de Pearson
        r_sq = r ** 2                                  ← coeficiente de determinación R²
    ✅ Anotación de texto en el gráfico con: r, R², pendiente
        ax.text(0.02, 0.98, f'r = {r:.4f}\\nR² = {r_sq:.4f}\\nPendiente = {m:.2f}',
                transform=ax.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    ✅ Leyenda con la ecuación de la recta

    RETORNO:
    ─────────
    Esta función debe retornar UNA TUPLA (figura, dict_estadisticos):
    return fig, {
        'pendiente': m,
        'intercepto': b,
        'correlacion': r,
        'r_cuadrado': r_sq
    }

    Args:
        df: DataFrame con los datos
        x_col: columna para el eje X (ej: 'work_year')
        y_col: columna para el eje Y (ej: 'salary_in_usd')
        titulo: título del gráfico
        guardar: Si True, guarda el gráfico como PNG

    Returns:
        Tupla: (matplotlib.figure.Figure, dict con r, r², pendiente, intercepto)
    """
    # TODO: COMPLETAR

    # ╔══════════════════════════════════════════════════════════╗
    # ║  ¡IMPLEMENTA AQUÍ EL SCATTER + REGRESIÓN + ESTADÍSTICOS! ║
    # ╚══════════════════════════════════════════════════════════╝

    configurar_estilo()
    fig, ax = plt.subplots(figsize=(14, 10))

    sns.scatterplot(data=df, x=x_col, y=y_col, ax=ax, alpha=0.6, color='steelblue')
    
    # Calcular regresión
    x_data = df[x_col].values
    y_data = df[y_col].values
    m, b = np.polyfit(x_data, y_data, 1)
    correlation_matrix = np.corrcoef(x_data, y_data)
    r = correlation_matrix[0, 1]
    r_sq = r ** 2
    
    # Dibujar línea
    ax.plot(x_data, m * x_data + b, color='red', linewidth=2.5, label=f'y = {m:.2f}x + {b:.2f}')
    
    # Anotación
    info_text = f'r = {r:.4f}\nR² = {r_sq:.4f}\nPendiente = {m:.2f}'
    ax.text(0.05, 0.95, info_text, transform=ax.transAxes, verticalalignment='top',
            bbox={'boxstyle': 'round', 'facecolor': 'white', 'alpha': 0.8, 'edgecolor': 'gray'}, fontsize=12)

    ax.set_title(sanitize_pdf_text(titulo), fontsize=18, fontweight='bold', pad=20)
    ax.set_xlabel(obtener_label(x_col), fontsize=14)
    ax.set_ylabel(obtener_label(y_col), fontsize=14)
    ax.yaxis.set_major_formatter(formatter)
    ax.legend(fontsize=12)

    plt.tight_layout()

    if guardar:
        guardar_grafico(fig, f'scatter_{x_col}_{y_col}.png', ruta_guardado)

    regresion_stats = {
        'pendiente': m,
        'intercepto': b,
        'correlacion': r,
        'r_cuadrado': r_sq
    }

    return fig, regresion_stats


def crear_bar_chart(df, cat, x=None, y=None, titulo='Diagrama de Barras',
                    orientacion='v', guardar=False, ruta_guardado='outputs/graficos/'):
    """
    LESLIE ROSS ARANIBAR POZO - Diagrama de Barras

    Soporta dos APIs:
    - API clásica: crear_bar_chart(df, 'job_category')     → usa cat
    - API nueva:   crear_bar_chart(df, None, x=..., y=...) → usa x, y

    INSTRUCCIONES:
    ✅ Usa sns.barplot con palette='magma'
    ✅ Soporta orientacion='h' (horizontal) y 'v' (vertical)
    ✅ Rota etiquetas eje X 45 grados si es vertical

    Args:
        df: DataFrame con los datos
        cat: columna categórica (API clásica)
        x, y: columnas X e Y (API nueva - prioridad si no son None)
        titulo: título
        orientacion: 'v' vertical o 'h' horizontal
        guardar: Si True, guarda PNG

    Returns:
        matplotlib.figure.Figure
    """
    # TODO: COMPLETAR (parcialmente)

    configurar_estilo()
    fig, ax = plt.subplots(figsize=(14, 8))

    # Soporte para ambas APIs
    if x is not None and y is not None:
        x_col, y_col = x, y
    else:
        x_col = cat
        counts = df[cat].value_counts().head(10)
        df = counts.reset_index()
        df.columns = [cat, 'count']
        x_col, y_col = cat, 'count'

    sns.barplot(data=df, x=x_col, y=y_col, ax=ax, palette='magma', orient=orientacion)

    if orientacion == 'v':
        ax.set_xlabel(x_col, fontsize=14)
        ax.set_ylabel(y_col, fontsize=14)
        plt.xticks(rotation=45)
        ax.yaxis.set_major_formatter(formatter)
    else:
        ax.set_xlabel(y_col, fontsize=14)
        ax.set_ylabel(x_col, fontsize=14)
        ax.xaxis.set_major_formatter(formatter)

    ax.set_title(titulo, fontsize=18, fontweight='bold', pad=20)
    plt.tight_layout()

    if guardar:
        guardar_grafico(fig, f'barras_{x_col}.png', ruta_guardado)

    return fig


def crear_grafico_interactivo(df, x, y, color=None, tipo='scatter'):
    """
    LESLIE ROSS ARANIBAR POZO - Gráfico Interactivo con Plotly

    Genera visualizaciones interactivas usando la librería Plotly.

    TIPOS DISPONIBLES:
    ─────────────────
    'scatter'   → px.scatter(df, x=x, y=y, color=color, hover_data=df.columns)
    'bar'       → px.bar(df, x=x, y=y, color=color)
    'box'       → px.box(df, x=x, y=y, color=color)
    'histogram' → px.histogram(df, x=x, nbins=50)
    'violin'    → px.violin(df, x=x, y=y, color=color)

    IMPORTANTE: Si PLOTLY_AVAILABLE es False, retornar None.

    Args:
        df: DataFrame con los datos
        x: columna eje X
        y: columna eje Y
        color: columna para colorear (opcional)
        tipo: tipo de gráfico

    Returns:
        plotly.graph_objects.Figure | None
    """
    # TODO: COMPLETAR

    if not PLOTLY_AVAILABLE:
        return None

    if tipo == 'scatter':
        fig = px.scatter(df, x=x, y=y, color=color, hover_data=df.columns, template='plotly_white')
    elif tipo == 'bar':
        fig = px.bar(df, x=x, y=y, color=color, template='plotly_white')
    elif tipo == 'box':
        fig = px.box(df, x=x, y=y, color=color, template='plotly_white')
    elif tipo == 'histogram':
        fig = px.histogram(df, x=x, nbins=50, template='plotly_white')
    elif tipo == 'violin':
        fig = px.violin(df, x=x, y=y, color=color, box=True, points='all', template='plotly_white')
    else:
        return None

    fig.update_layout(title=f"Gráfico Interactivo ({tipo})", margin=dict(l=20, r=20, t=50, b=20))
    return fig
