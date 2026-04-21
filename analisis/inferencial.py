"""
PROYECTO: Estadística para Ingeniería
MIEMBRO: BRYANN VALLEJO LUNA (Analista Inferencial)
TAREA: Intervalos de Confianza y Contrastes de Hipótesis
"""
import pandas as pd
import numpy as np
from scipy import stats
import os

def calcular_ic_95(data):
    """
    BRYANN VALLEJO LUNA - Intervalo de Confianza 95%
    Calcula el IC para una serie de datos.
    """
    n = len(data)
    
    # TODO (Bryann): Calcular media, error estándar y el intervalo IC al 95%.
    # 1. Usa np.mean(data)
    # 2. Usa stats.sem(data)
    # 3. Usa stats.t.interval(0.95, n-1, ...)
    
    # --- Tu código aquí ---
    media = np.mean(data)

    # Intervalo de confianza directamente
    intervalo = stats.t.interval(
        0.95, 
        df=len(data)-1, 
        loc=media, 
        scale=stats.sem(data)
    )

    return {
        'Media': media,
        'Inferior': intervalo[0],
        'Superior': intervalo[1],
        'Margen Error': (intervalo[1] - intervalo[0]) / 2 if intervalo[1] else 0.0
    }

def contraste_hipotesis(g1, g2, label1="G1", label2="G2"):
    """
    BRYANN VALLEJO LUNA - Contraste de Hipótesis (Welch T-test)
    Compara dos medias independientes sin asumir varianzas iguales.
    """
    # TODO (Bryann): Realiza una prueba Welch's T-Test usando scipy.stats.ttest_ind
    # Extrae el t_stat y el p_valor, y genera una conclusión en función del p_valor.
    
    # --- Tu código aquí ---
    # Control básico

    t_stat, p_valor = stats.ttest_ind(g1, g2, equal_var=False)

    if p_valor < 0.05:
        decision = 'Se rechaza H0'
        conclusion = f'Hay diferencias estadísticamente significativas entre {label1} y {label2}.'
    else:
        decision = 'No se rechaza H0'
        conclusion = f'No hay evidencia suficiente para afirmar diferencias significativas entre {label1} y {label2}.'

    return {
        'P-Valor': p_valor,
        't_statistic': t_stat,
        'Decisión': decision,
        'Conclusión': conclusion,
        'Estado': 'OK'
    }


def verificar_supuestos(data):
    """
    BRYANN VALLEJO LUNA - Prueba de Normalidad (Shapiro-Wilk o K-S)
    """
    # TODO (Bryann): Aplica el test correcto (K-S si n > 5000, Shapiro si no)
    
    # --- Tu código aquí ---

    n = len(data)

    # Selección de prueba
    if n <= 5000:
        stat, p = stats.shapiro(data)
        prueba = "Shapiro-Wilk"
    else:
        # K-S necesita datos estandarizados
        data_std = (data - data.mean()) / data.std()
        stat, p = stats.kstest(data_std, 'norm')
        prueba = "Kolmogorov-Smirnov"

    return {
        'Prueba': prueba,
        'Stat': stat,
        'P-Valor': p,
        'Estado': 'OK'
    }

def generar_reporte_inferencial(df):
    """Procesa los análisis inferenciales clave"""
    
    # TODO (Bryann): Manda llamar a calcular_ic_95() y contraste_hipotesis(),
    # y guarda el resultado en outputs/tablas/inferencial.csv.
    
    # --- Tu código aquí ---
    # ic_salario = ...
    # test_exp = ...
    # Guardar en CSV...
    
    # Valores por defecto para que no falle app.py 
    ic_salario = {'Inferior': 0, 'Superior': 0, 'Media': 0, 'Margen Error': 0}
    test_exp = {'P-Valor': 1.0, 'Decisión': '-', 'Conclusión': '-'}
    
    return ic_salario, test_exp
