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
    sns.histplot(df[x_col], ax=ax, kde=True, color='#2c3e50', edgecolor='white', alpha=0.7)
    ax.set_title(titulo, fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel(obtener_label(x_col), fontsize=12)
    ax.set_ylabel("Frecuencia", fontsize=12)
    sns.despine()
    return fig

def crear_boxplot(df, y_col, x_col, titulo="Comparativa Salarial"):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=df, x=x_col, y=y_col, ax=ax, palette="viridis", width=0.6)
    ax.set_title(titulo, fontsize=14, fontweight='bold', pad=15)
    ax.set_ylabel(obtener_label(y_col), fontsize=12)
    ax.set_xlabel(obtener_label(x_col), fontsize=12)
    plt.xticks(rotation=45)
    sns.despine()
    return fig

def crear_violin_plot(df, x_col, y_col, titulo="Densidad Salarial"):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.violinplot(data=df, x=x_col, y=y_col, ax=ax, palette="magma", inner="quartile")
    ax.set_title(titulo, fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel(obtener_label(x_col), fontsize=12)
    ax.set_ylabel(obtener_label(y_col), fontsize=12)
    sns.despine()
    return fig

def crear_bar_chart(df, col, titulo="Presencia en Mercado"):
    counts = df[col].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=counts.index, y=counts.values, ax=ax, palette="rocket")
    ax.set_title(titulo, fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel(obtener_label(col), fontsize=12)
    ax.set_ylabel("Cantidad", fontsize=12)
    plt.xticks(rotation=45)
    sns.despine()
    return fig

def crear_grafico_comparativo_ic(df, x_col, y_col, titulo="Evidencia Inferencial"):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=df, x=x_col, y=y_col, ax=ax, errorbar=('ci', 95), palette="coolwarm", capsize=.1)
    ax.set_title(titulo, fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel(obtener_label(x_col), fontsize=12)
    ax.set_ylabel(obtener_label(y_col), fontsize=12)
    sns.despine()
    return fig

def crear_scatter_regresion(df, x_col, y_col, titulo="Relación Salario vs COLI"):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.regplot(data=df, x=x_col, y=y_col, ax=ax, 
                scatter_kws={'color': '#3498db', 'alpha': 0.5}, 
                line_kws={'color': '#e74c3c', 'weight': 'bold'})
    ax.set_title(titulo, fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel(obtener_label(x_col), fontsize=12)
    ax.set_ylabel(obtener_label(y_col), fontsize=12)
    sns.despine()
    
    # Calcular R2 real para devolver
    from scipy import stats as scipy_stats
    slope, intercept, r_value, p_value, std_err = scipy_stats.linregress(df[x_col], df[y_col])
    stats_dict = {
        'r_cuadrado': round(r_value**2, 4),
        'pendiente': round(slope, 4),
        'intercepto': round(intercept, 4),
        'p_valor': round(p_value, 4)
    }
    return fig, stats_dict

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
