"""
PROYECTO: Estadística para Ingeniería
ANÁLISIS INFERENCIAL Y PRUEBAS DE HIPÓTESIS
AUTORES: RUBEN GAMEZ TORRIJOS / RAFAEL RODRIGUEZ
ROL ASIGNADO (Lógica Estadística): Bryann Vallejo Luna
ESTADO: ✅ INTEGRADO (Lógica de Bryann verificada)
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
    """
    n = len(data)
    if n < 2:
        return {'Media': 0, 'Inferior': 0, 'Superior': 0, 'Error Estándar': 0, 'Estado': 'ERROR_N_BAJO'}

    media = np.mean(data)
    # Cálculo del intervalo usando distribución T de Student (apropiado para muestras pequeñas/grandes)
    intervalo = stats.t.interval(
        0.95, 
        df=n-1, 
        loc=media, 
        scale=stats.sem(data)
    )

    return {
        'Media': media,
        'Inferior': intervalo[0],
        'Superior': intervalo[1],
        'Error Estándar': stats.sem(data),
        'Estado': 'COMPLETO'
    }

def contraste_hipotesis(g1, g2, label1="G1", label2="G2"):
    """
    MODULO: Contrastes de Hipótesis (T-Test Welch)
    ROL ASIGNADO: Bryann Vallejo Luna
    """
    # Welch's T-test: no asume varianzas iguales (equal_var=False)
    t_stat, p_valor = stats.ttest_ind(g1, g2, equal_var=False)

    if p_valor < 0.05:
        decision = 'Se rechaza H0'
        conclusion = f'Diferencias significativas entre {label1} y {label2}.'
    else:
        decision = 'No se rechaza H0'
        conclusion = f'Sin evidencia de diferencias significativas entre {label1} y {label2}.'

    return {
        'p_valor': p_valor,
        't_statistic': t_stat,
        'rechaza_h0': p_valor < 0.05,
        'Conclusion': conclusion,
        'Decisión': decision,
        'Estado': 'COMPLETO'
    }

def verificar_supuestos(data):
    """
    MODULO: Verificación de Supuestos (Normalidad)
    ROL ASIGNADO: Bryann Vallejo Luna
    """
    n = len(data)
    # Selección dinámica de prueba según tamaño de muestra
    if n <= 5000:
        stat, p = stats.shapiro(data)
        prueba = "Shapiro-Wilk"
    else:
        # Estandarización para Kolmogorov-Smirnov
        data_std = (data - data.mean()) / data.std()
        stat, p = stats.kstest(data_std, 'norm')
        prueba = "Kolmogorov-Smirnov"

    return {
        'Prueba': prueba,
        'P-Valor': p,
        'Normal': p > 0.05,
        'Estado': 'COMPLETO'
    }
