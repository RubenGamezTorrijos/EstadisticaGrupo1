"""
PROYECTO: Estadística para Ingeniería
MIEMBRO: LESLIE ROSS ARANIBAR POZO (Analista Descriptivo)
TAREA: Visualizaciones estadísticas y Análisis de Regresión
"""
import matplotlib.pyplot as plt
import seaborn as sns
import os
from matplotlib.ticker import FuncFormatter

# Configuración estética Leslie
sns.set_theme(style="darkgrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

def fmt_es(x, pos):
    """Formato español: punto para miles, coma para decimales"""
    return f"{x:,.0f}".replace(",", "@").replace(".", ",").replace("@", ".")

formatter = FuncFormatter(fmt_es)

def guardar_grafico(fig, nombre):
    """LESLIE ROSS ARANIBAR POZO - Guardar PNG"""
    ruta = os.path.join('outputs', 'graficos', nombre)
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    fig.savefig(ruta, bbox_inches='tight')
    plt.close(fig)

def crear_histograma(df, columna):
    """LESLIE ROSS ARANIBAR POZO - Histograma con KDE"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # TODO (Leslie): Generar histograma con Seaborn
    # 1. Usa sns.histplot(data=df, x=columna, kde=True, ax=ax, color='#00d1b2')
    # 2. Aplica el formatedor al eje X: ax.xaxis.set_major_formatter(formatter)
    # 3. Añade etiquetas de eje X e Y
    
    # --- Tu código aquí ---
    
    ax.set_title(f'Distribución de {columna}', fontsize=14, pad=15)
    guardar_grafico(fig, f'histograma_{columna}.png')
    return fig

def crear_boxplot(df, num, cat):
    """LESLIE ROSS ARANIBAR POZO - Boxplot por categoría"""
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # TODO (Leslie): Generar boxplot con Seaborn
    # 1. Usa sns.boxplot para relacionar la variable categórica (cat) con la numérica (num)
    # 2. Aplica formatter al eje Y si aplica (ax.yaxis.set_major_formatter)
    
    # --- Tu código aquí ---
    
    ax.set_title(f'{num} por {cat}', fontsize=14, pad=15)
    plt.xticks(rotation=45)
    guardar_grafico(fig, f'boxplot_{num}_{cat}.png')
    return fig

def crear_scatter_regresion(df, x_col, y_col):
    """LESLIE ROSS ARANIBAR POZO - Dispersión + Regresión"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # TODO (Leslie): Generar dispersión con línea de regresión (sns.regplot)
    # 1. Calcula la correlación de Pearson y guárdala en una variable `corr`
    # 2. Aplica el formatter al eje Y
    
    # --- Tu código aquí ---
    corr = 0.0  # Modifica esto por el cálculo real
    
    ax.set_title(f'Regresión: {y_col} vs {x_col} (r={corr:.2f})', fontsize=14, pad=15)
    guardar_grafico(fig, f'scatter_regresion_{x_col}_{y_col}.png')
    return fig

def crear_bar_chart(df, cat):
    """LESLIE ROSS ARANIBAR POZO - Diagrama de barras"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # TODO (Leslie): Obtener conteo de categorías y graficar con sns.barplot
    # Ejemplo: counts = df[cat].value_counts().head(10)
    
    # --- Tu código aquí ---
    
    ax.set_title(f'Top 10: {cat}', fontsize=14, pad=15)
    plt.xticks(rotation=45)
    guardar_grafico(fig, f'barras_{cat}.png')
    return fig
