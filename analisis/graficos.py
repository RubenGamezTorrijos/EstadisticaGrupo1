"""
PROYECTO: Estadística para Ingeniería
ANÁLISIS GRÁFICO Y VISUALIZACIÓN
COORDINADOR: RUBEN GAMEZ TORRIJOS
ROL ASIGNADO (Lógica Visual): Leslie Ross Aranibar Pozo
ESTADO: Códig (Rama DEV)
"""

import matplotlib.pyplot as plt
import seaborn as sns
import config.settings as cfg
import os


# =================================================================
# SECCIÓN: VISUALIZACIÓN DE DATOS (RESPONSABLE: LESLIE ROSS)
# =================================================================

def crear_histograma(df, x_col, titulo="Distribución Salarial"):
    """
    MODULO: Histogramas
    ROL ASIGNADO: Leslie Ross Aranibar Pozo
    """
    # CÓDIGO POR LESLIE
    fig, ax = plt.subplots(figsize=(10, 6))

    sns.histplot(data=df, x=x_col, kde=True, ax=ax)

    ax.set_title(titulo, fontsize=14, pad=15)
    ax.set_xlabel(obtener_label(x_col))
    ax.set_ylabel("Frecuencia")

    return fig

def crear_boxplot(df, y_col, x_col, titulo="Comparativa Salarial"):
    """
    MODULO: Boxplots
    ROL ASIGNADO: Leslie Ross Aranibar Pozo
    """
    # CÓDIGO POR LESLIE
    fig, ax = plt.subplots(figsize=(12, 7))

    sns.boxplot(data=df, x=x_col, y=y_col, ax=ax)

    ax.set_title(titulo, fontsize=14, pad=15)
    ax.set_xlabel(obtener_label(x_col))
    ax.set_ylabel(obtener_label(y_col))

    plt.xticks(rotation=45)

    return fig

def crear_violin_plot(df, x_col, y_col, titulo="Densidad Salarial"):
    """
    MODULO: Violin Plots
    ROL ASIGNADO: Leslie Ross Aranibar Pozo
    """
    # CÓDIGO POR LESLIE
    fig, ax = plt.subplots(figsize=(12, 7))

    sns.violinplot(data=df, x=x_col, y=y_col, ax=ax)

    ax.set_title(titulo, fontsize=14, pad=15)
    ax.set_xlabel(obtener_label(x_col))
    ax.set_ylabel(obtener_label(y_col))

    plt.xticks(rotation=45)

    return fig

def crear_bar_chart(df, col, titulo="Presencia en Mercado"):
    """
    MODULO: Bar Charts
    ROL ASIGNADO: Leslie Ross Aranibar Pozo
    """
    # CÓDIGO POR LESLIE
    fig, ax = plt.subplots(figsize=(12, 6))

    counts = df[col].value_counts().head(10)

    sns.barplot(x=counts.index, y=counts.values, ax=ax)

    ax.set_title(titulo, fontsize=14, pad=15)
    ax.set_xlabel(obtener_label(col))
    ax.set_ylabel("Frecuencia")

    plt.xticks(rotation=45)

    return fig

def crear_grafico_comparativo_ic(df, x_col, y_col, titulo="Evidencia Inferencial"):
    """
    MODULO: Gráficos de Error (IC)
    ROL ASIGNADO: Leslie Ross Aranibar Pozo
    """
    # CÓDIGO POR LESLIE
    fig, ax = plt.subplots(figsize=(12, 6))

    resumen = df.groupby(x_col)[y_col].agg(['mean', 'std']).reset_index()

    sns.barplot(data=resumen, x=x_col, y='mean', ax=ax)

    ax.errorbar(
        x=range(len(resumen)),
        y=resumen['mean'],
        yerr=resumen['std'],
        fmt='none',
        c='black',
        capsize=5
    )

    ax.set_title(titulo, fontsize=14, pad=15)
    ax.set_xlabel(obtener_label(x_col))
    ax.set_ylabel(obtener_label(y_col))

    plt.xticks(rotation=45)

    return fig

def crear_scatter_regresion(df, x_col, y_col, titulo="Relación Salario vs COLI"):
    """
    MODULO: Dispersión con Regresión
    ROL ASIGNADO: Leslie Ross Aranibar Pozo
    """
    # CÓDIGO POR LESLIE
    fig, ax = plt.subplots(figsize=(10, 6))

    sns.regplot(data=df, x=x_col, y=y_col, ax=ax, scatter_kws={'alpha': 0.6})

    corr = df[x_col].corr(df[y_col])
    r_cuadrado = corr ** 2

    pendiente = corr * (df[y_col].std() / df[x_col].std())
    intercepto = df[y_col].mean() - pendiente * df[x_col].mean()

    p_valor = None

    ax.set_title(titulo, fontsize=14, pad=15)
    ax.set_xlabel(obtener_label(x_col))
    ax.set_ylabel(obtener_label(y_col))

    resultados = {
        'r_cuadrado': r_cuadrado,
        'pendiente': pendiente,
        'intercepto': intercepto,
        'p_valor': p_valor
    }

    return fig, resultados

def obtener_label(col):
    """Devuelve una etiqueta legible para el gráfico desde la configuración central."""
    return cfg.VAR_LABELS.get(col, col)

def sanitize_pdf_text(text):
    """Limpia caracteres especiales para compatibilidad con FPDF (latin-1)."""
    if text is None: return ""
    replacements = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'ñ': 'n', 'Ñ': 'N', '€': 'EUR', '$': 'USD',
        '₀': '0', '₁': '1', '₂': '2', '₃': '3', '₄': '4',
        '²': '^2', '±': '+/-', '≥': '>=', '≤': '<=', '≠': '!='
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    try:
        return text.encode('latin-1', 'replace').decode('latin-1')
    except:
        return text

def guardar_grafico(fig, nombre, ruta='outputs/graficos/'):
    """
    Guarda un gráfico como PNG de forma segura para los informes.
    Módulo desarrollado por Rafael Rodriguez para consumo global.
    """
    if fig is None: return None
    os.makedirs(ruta, exist_ok=True)
    ruta_completa = os.path.join(ruta, nombre)
    fig.savefig(ruta_completa, bbox_inches='tight', dpi=150)
    plt.close(fig)
    return ruta_completa
