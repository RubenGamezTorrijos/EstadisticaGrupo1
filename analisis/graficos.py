"""
PROYECTO: Estadística para Ingeniería
INFRAESTRUCTURA Y VISUALIZACIÓN
AUTORES: RUBEN GAMEZ TORRIJOS (Coordinador) / RAFAEL RODRIGUEZ
ROL ASIGNADO (Lógica Gráfica): Leslie Ross Aranibar Pozo
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

# =================================================================
# SECCIÓN: VISUALIZACIONES DESCRIPTIVAS (RESPONSABLE: LESLIE ROSS)
# =================================================================

def crear_histograma(df, x_col, titulo="Distribución Salarial"):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df[x_col], ax=ax, kde=True, color='#0b84f4')
    ax.set_title(titulo)
    ax.set_xlabel(obtener_label(x_col))
    ax.set_ylabel("Frecuencia")
    return fig

def crear_boxplot(df, y_col, x_col, titulo="Comparativa Salarial"):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=df, x=x_col, y=y_col, ax=ax, palette="RdBu_r")
    ax.set_title(titulo)
    ax.set_ylabel(obtener_label(y_col))
    ax.set_xlabel(obtener_label(x_col))
    plt.xticks(rotation=45)
    return fig

def crear_violin_plot(df, x_col, y_col, titulo="Densidad Salarial"):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.violinplot(data=df, x=x_col, y=y_col, ax=ax, color='#1e3a8a')
    ax.set_title(titulo)
    ax.set_xlabel(obtener_label(x_col))
    ax.set_ylabel(obtener_label(y_col))
    return fig

def crear_bar_chart(df, col, titulo="Presencia en Mercado"):
    counts = df[col].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    counts.plot(kind='bar', ax=ax, color='#0b84f4')
    ax.set_title(titulo)
    ax.set_xlabel(obtener_label(col))
    ax.set_ylabel("Cantidad")
    return fig

def crear_grafico_comparativo_ic(df, x_col, y_col, titulo="Evidencia Inferencial"):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=df, x=x_col, y=y_col, ax=ax, errorbar=('ci', 95), palette="Blues")
    ax.set_title(titulo)
    ax.set_xlabel(obtener_label(x_col))
    ax.set_ylabel(obtener_label(y_col))
    return fig

def crear_scatter_regresion(df, x_col, y_col, titulo="Relación Salario vs COLI"):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.regplot(data=df, x=x_col, y=y_col, ax=ax, line_kws={'color':'red'})
    ax.set_title(titulo)
    ax.set_xlabel(obtener_label(x_col))
    ax.set_ylabel(obtener_label(y_col))
    # Estadísticos simplificados para el retorno
    stats = {'r_cuadrado': 0.0} # Placeholder para cálculo real en modelo_regresion
    return fig, stats

# =================================================================
# SECCIÓN: INFRAESTRUCTURA DE APOYO (RESPONSABLES: RUBEN / RAFAEL)
# =================================================================

# Diccionario de traducción de variables para etiquetas de gráficos
# Mantenido por RUBEN para asegurar consistencia en la UI
VAR_LABELS = {
    'salary_in_usd': 'Salario (USD)',
    'experience_level': 'Nivel de Experiencia',
    'employment_type': 'Tipo de Contrato',
    'job_title': 'Cargo',
    'job_category': 'Categoría de Empleo',
    'employee_residence': 'Residencia del Empleado',
    'work_setting': 'Modalidad de Trabajo',
    'company_location': 'Ubicación de la Empresa',
    'company_size': 'Tamaño de la Empresa',
    'cost_of_living_index': 'Índice del Coste de Vida (COLI)'
}

def sanitize_pdf_text(text):
    """
    DESARROLLADO POR RAFAEL: Limpia caracteres que rompen la fuente Helvetica en el PDF.
    Soporta símbolos estadísticos comunes.
    """
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
    """
    DESARROLLADO POR RUBEN: Retorna la etiqueta legible para una columna.
    Usa VAR_LABELS como base de datos.
    """
    return VAR_LABELS.get(col, col.replace('_', ' ').title())

def guardar_grafico(fig, nombre, ruta='outputs/graficos/'):
    """
    DESARROLLADO POR RAFAEL: Guarda un gráfico como PNG de forma segura.
    Esta utilidad es consumida por el generador de informes.
    """
    if fig is None: return None
    os.makedirs(ruta, exist_ok=True)
    ruta_completa = os.path.join(ruta, nombre)
    fig.savefig(ruta_completa, bbox_inches='tight', dpi=150)
    plt.close(fig)
    return ruta_completa
