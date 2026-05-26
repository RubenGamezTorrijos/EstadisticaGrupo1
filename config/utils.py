"""
config/utils.py
================
Utilidades transversales para formateo de datos, localización y validaciones.
"""

import pandas as pd
import numpy as np

def formatear_moneda(valor, divisa="USD"):
    """
    Formatea números según el estándar solicitado:
    - EUR: Miles con punto, decimales con coma (€243,6K)
    - USD: Miles con coma, decimales con punto ($243.6K)
    - Miles: 1 decimal (€243,6K)
    - Millones: 2 decimales (€1,24M)
    """
    if valor is None or pd.isna(valor) or np.isinf(valor):
        return "N/A"

    simbolo = "€" if "EUR" in divisa.upper() or divisa == "€" else "$"
    es_euro = "EUR" in divisa.upper() or divisa == "€"
    
    # Lógica de escala (K para miles, M para millones)
    abs_val = abs(valor)
    suffix = ""
    scaled_val = valor
    
    if abs_val >= 1_000_000:
        scaled_val = valor / 1_000_000
        suffix = "M"
        precision = 2
    elif abs_val >= 1_000:
        scaled_val = valor / 1_000
        suffix = "K"
        precision = 1
    else:
        scaled_val = valor
        suffix = ""
        precision = 0 # Para montos pequeños, sin decimales según ejemplo
    
    if es_euro:
        # Europa: 1.234,56
        s = f"{scaled_val:,.{precision}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    else:
        # USA: 1,234.56
        s = f"{scaled_val:,.{precision}f}"
    
    return f"{simbolo}{s}{suffix}"

def formatear_numero_entero(valor):
    """Formatea años y otros enteros sin separadores (2025, no 2.025)."""
    if valor is None or pd.isna(valor):
        return "N/A"
    try:
        # Forzamos a entero y luego a string para evitar decimales o comas
        return str(int(float(valor)))
    except:
        return str(valor)

def formatear_porcentaje(valor, es_euro=True):
    """Formatea valores como porcentaje (ej: 85.5 -> 85,50%)."""
    if valor is None or pd.isna(valor) or np.isinf(valor):
        return "N/A"
    
    if es_euro:
        # Europa: 85,50%
        return f"{valor:,.2f}%".replace(",", "X").replace(".", ",").replace("X", ".")
    else:
        # USA: 85.50%
        return f"{valor:,.2f}%"

def validar_datos_insuficientes(df, min_filas=2):
    """Verifica si hay suficientes datos para realizar cálculos."""
    return df is not None and len(df) >= min_filas
