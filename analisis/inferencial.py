"""
PROYECTO: Estadística para Ingeniería
ANÁLISIS INFERENCIAL Y PRUEBAS DE HIPÓTESIS
AUTORES: RUBEN GAMEZ TORRIJOS / RAFAEL RODRIGUEZ
ROL ASIGNADO (Lógica Estadística): Bryann Vallejo Luna
"""

import numpy as np
from scipy import stats
import pandas as pd

# =================================================================
# SECCIÓN: INFERENCIA POBLACIONAL (RESPONSABLE: BRYANN VALLEJO)
# =================================================================

def calcular_ic_95(data):
    """Calcula el intervalo de confianza al 95% para una serie de datos."""
    if len(data) < 2: return {'Media': 0, 'Inferior': 0, 'Superior': 0, 'Estado': 'ERROR'}
    
    media = np.mean(data)
    std_err = stats.sem(data)
    dof = len(data) - 1
    h = std_err * stats.t.ppf((1 + 0.95) / 2., dof)
    return {
        'Media': media, 
        'Inferior': media - h, 
        'Superior': media + h,
        'Error Estándar': std_err,
        'Estado': 'COMPLETO'
    }

def contraste_hipotesis(g1, g2, label1="G1", label2="G2"):
    """Realiza un contraste de hipótesis de dos muestras independientes."""
    if len(g1) < 2 or len(g2) < 2:
        return {'p_valor': 1.0, 't_statistic': 0.0, 'rechaza_h0': False, 'Estado': 'ERROR'}
        
    t_stat, p_valor = stats.ttest_ind(g1, g2, equal_var=False)
    return {
        'p_valor': p_valor, 
        't_statistic': t_stat,
        'rechaza_h0': p_valor < 0.05,
        'Conclusion': f"Diferencia Significativa" if p_valor < 0.05 else "Diferencia No Significativa",
        'Estado': 'COMPLETO'
    }

def verificar_supuestos(data):
    stat, p = stats.shapiro(data)
    return {"Shapiro-p": p, "Normal": p > 0.05, "Estado": "COMPLETO"}

# =================================================================
# SECCIÓN: UTILIDADES DE INTEGRACIÓN (RESPONSABLES: RUBEN / RAFAEL)
# =================================================================

# Nota: Las funciones de integración de reportes se gestionan en exportacion.py
# para mantener la arquitectura MVC limpia y desacoplada.
