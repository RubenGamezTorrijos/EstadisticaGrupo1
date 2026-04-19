import numpy as np
from scipy import stats
import pandas as pd

def calcular_ic_95(data):
    """
    MODULO: Inferencia Poblacional
    ROL ASIGNADO: Bryann Vallejo Luna
    
    TODO: Implementar cálculo de Intervalo de Confianza (T-Student) al 95%.
    Debe devolver un diccionario con: Media, Inferior, Superior.
    """
    if len(data) < 2:
        return {"Error": "Datos insuficientes"}
        
    media = np.mean(data)
    # Plantilla de cálculo: Bryann debe implementar SE y Margen de Error
    std_err = stats.sem(data)
    dof = len(data) - 1
    h = std_err * stats.t.ppf((1 + 0.95) / 2., dof)
    
    return {
        'Media': media,
        'Inferior': media - h,
        'Superior': media + h,
        'N': len(data),
        'Margen Error': h,
        'Estado': '[Bryann: Pendiente Validar Fórmulas]'
    }

def contraste_hipotesis(g1, g2, label1="G1", label2="G2"):
    """
    MODULO: Contrastes de Hipótesis
    ROL ASIGNADO: Bryann Vallejo Luna
    
    TODO: Implementar T-test de muestras independientes y Cohen's d.
    """
    # Plantilla básica de T-test
    # TODO: Bryann debe decidir si usar Welch (equal_var=False) o Student.
    t_stat, p_valor = stats.ttest_ind(g1, g2, equal_var=False)
    rechaza = p_valor < 0.05
    
    return {
        'p_valor': p_valor,
        't_statistic': t_stat,
        'rechaza_h0': rechaza,
        'Conclusión': "[Bryann: Pendiente desarrollar análisis crítico]",
        'Media G1': np.mean(g1),
        'Media G2': np.mean(g2)
    }

def verificar_supuestos(data):
    """
    TODO: Bryann debe implementar verificación de normalidad (Shapiro-Wilk).
    """
    stat, p = stats.shapiro(data)
    return {"Shapiro-p": p, "Normal": p > 0.05}
