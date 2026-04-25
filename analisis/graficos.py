"""
PROYECTO: Estadística para Ingeniería
ANÁLISIS GRÁFICO Y VISUALIZACIÓN
COORDINADOR: RUBEN GAMEZ TORRIJOS
ROL ASIGNADO (Lógica Visual): Leslie Ross Aranibar Pozo
ESTADO: PENDIENTE (Rama DEV)
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
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
    # PENDIENTE POR LESLIE
    return None

def crear_boxplot(df, y_col, x_col, titulo="Comparativa Salarial"):
    """
    MODULO: Boxplots
    ROL ASIGNADO: Leslie Ross Aranibar Pozo
    """
    # PENDIENTE POR LESLIE
    return None

def crear_violin_plot(df, x_col, y_col, titulo="Densidad Salarial"):
    """
    MODULO: Violin Plots
    ROL ASIGNADO: Leslie Ross Aranibar Pozo
    """
    # PENDIENTE POR LESLIE
    return None

def crear_bar_chart(df, col, titulo="Presencia en Mercado"):
    """
    MODULO: Bar Charts
    ROL ASIGNADO: Leslie Ross Aranibar Pozo
    """
    # PENDIENTE POR LESLIE
    return None

def crear_grafico_comparativo_ic(df, x_col, y_col, titulo="Evidencia Inferencial"):
    """
    MODULO: Gráficos de Error (IC)
    ROL ASIGNADO: Leslie Ross Aranibar Pozo
    """
    # PENDIENTE POR LESLIE
    return None

def crear_scatter_regresion(df, x_col, y_col, titulo="Relación Salario vs COLI"):
    """
    MODULO: Dispersión con Regresión
    ROL ASIGNADO: Leslie Ross Aranibar Pozo
    """
    # PENDIENTE POR LESLIE
    return None, {'r_cuadrado': 0.0, 'pendiente': 0.0, 'intercepto': 0.0, 'p_valor': 0.0}

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
