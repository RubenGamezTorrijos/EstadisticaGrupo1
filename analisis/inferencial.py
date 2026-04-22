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
    """
    MODULO: Inferencia Poblacional
    ROL ASIGNADO: Bryann Vallejo Luna
    
    # 💡 PISTA DE IMPLEMENTACIÓN (REFERENCIA MAIN):
    # ==========================================
    # media = np.mean(data)
    # std_err = stats.sem(data)
    # dof = len(data) - 1
    # h = std_err * stats.t.ppf((1 + 0.95) / 2., dof)
    # return {'Media': media, 'Inferior': media - h, 'Superior': media + h, 'Estado': 'COMPLETO'}
    """
    # IMPLEMENTACIÓN PENDIENTE POR BRYANN
    return {
        'Media': 0.0,
        'Inferior': 0.0,
        'Superior': 0.0,
        'Error Estándar': 0.0,
        'Estado': 'PENDIENTE'
    }

def contraste_hipotesis(g1, g2, label1="G1", label2="G2"):
    """
    MODULO: Contrastes de Hipótesis
    ROL ASIGNADO: Bryann Vallejo Luna
    """
    # IMPLEMENTACIÓN PENDIENTE POR BRYANN
    return {
        'p_valor': 1.0,
        't_statistic': 0.0,
        'rechaza_h0': False,
        'Conclusion': 'Pendiente',
        'Estado': 'PENDIENTE'
    }

def verificar_supuestos(data):
    """
    MODULO: Verificación de Supuestos
    ROL ASIGNADO: Bryann Vallejo Luna
    """
    # IMPLEMENTACIÓN PENDIENTE POR BRYANN
    return {"Shapiro-p": 0.0, "Normal": False, "Estado": "PENDIENTE"}
