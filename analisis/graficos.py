import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

def crear_histograma(df, x_col, titulo="Distribución Salarial"):
    """
    MODULO: Visualizaciones Descriptivas
    ROL ASIGNADO: Leslie Ross Aranibar Pozo
    
    # 💡 PISTA DE IMPLEMENTACIÓN (REFERENCIA MAIN):
    # ==========================================
    # sns.histplot(df[x_col], ax=ax, kde=True, color='#0b84f4')
    # ax.set_xlabel("Salario (USD)")
    """
    
    fig, ax = plt.subplots(figsize=(10, 6))
    # Plantilla básica: implementar estilo v.2.1.4 aquí
    sns.histplot(df[x_col], ax=ax, color='#0b84f4')
    ax.set_title(f"{titulo} [Leslie: Pendiente Refinar]")
    return fig

def crear_boxplot(df, y_col, x_col, titulo="Comparativa Salarial"):
    """
    MODULO: Visualizaciones Descriptivas
    ROL ASIGNADO: Leslie Ross Aranibar Pozo
    
    # 💡 PISTA DE IMPLEMENTACIÓN (REFERENCIA MAIN):
    # ==========================================
    # sns.boxplot(data=df, x=x_col, y=y_col, ax=ax, palette="RdBu_r")
    """
    
    fig, ax = plt.subplots(figsize=(10, 6))
    # Plantilla básica
    sns.boxplot(data=df, x=x_col, y=y_col, ax=ax, palette="Blues")
    ax.set_title(f"{titulo} [Leslie: Pendiente Refinar]")
    plt.xticks(rotation=45)
    return fig

def crear_violin_plot(df, x_col, y_col, titulo="Densidad Salarial"):
    """
    MODULO: Visualizaciones Descriptivas
    ROL ASIGNADO: Leslie Ross Aranibar Pozo
    
    TODO: Implementar Violin Plot para mostrar densidad de probabilidad.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    # Plantilla básica
    sns.violinplot(data=df, x=x_col, y=y_col, ax=ax, color='#1e3a8a')
    ax.set_title(f"{titulo} [Leslie: Pendiente Refinar]")
    return fig

def crear_bar_chart(df, col, titulo="Presencia en Mercado"):
    """
    MODULO: Visualizaciones Descriptivas
    ROL ASIGNADO: Leslie Ross Aranibar Pozo
    
    TODO: Implementar gráfico de barras para variables categóricas (Top 10).
    """
    counts = df[col].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    # Plantilla básica
    counts.plot(kind='bar', ax=ax, color='#0b84f4')
    ax.set_title(f"{titulo} [Leslie: Pendiente Refinar]")
    plt.xticks(rotation=45)
    return fig

def crear_grafico_comparativo_ic(df, x_col, y_col, titulo="Evidencia Inferencial"):
    """
    MODULO: Evidencia Inferencial
    ROL ASIGNADO: Leslie Ross Aranibar Pozo (En colaboración con Bryann)
    
    TODO: Implementar gráfico de barras de error (Barplot con errorbars=95).
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    # Plantilla básica
    if not df.empty:
        sns.barplot(data=df, x=x_col, y=y_col, ax=ax, errorbar=('ci', 95), palette="Blues")
    ax.set_title(f"{titulo} [Leslie: Pendiente Refinar]")
    return fig

def crear_scatter_regresion(df, x_col, y_col, titulo="Relación Salario vs COLI"):
    """
    MODULO: Regresión Lineal
    ROL ASIGNADO: Leslie Ross Aranibar Pozo
    """
    
    # 💡 PISTA DE IMPLEMENTACIÓN (REFERENCIA MAIN):
    # ==========================================
    # sns.regplot(data=df, x=x_col, y=y_col, ax=ax, 
    #             scatter_kws={'alpha':0.5, 'color':'#0b84f4'},
    #             line_kws={'color':'#ff4b4b', 'lw':3})
    
    fig, ax = plt.subplots(figsize=(10, 6))
    # Plantilla básica
    sns.regplot(data=df, x=x_col, y=y_col, ax=ax, line_kws={'color': 'red'})
    ax.set_title(f"{titulo} [Leslie: Pendiente Refinar]")
    
    # Placeholder de estadísticas (Sincronizado con app.py)
    stats = {
        'correlacion': 0.0,
        'r_cuadrado': 0.0,
        'pendiente': 0.0,
        'intercepto': 0.0
    }
    return fig, stats

# --- UTILIDADES DE INFRAESTRUCTURA (RESTAURADAS DE MAIN) ---
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
