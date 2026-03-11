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
    media = 0.0
    intervalo = (0.0, 0.0)
    
    return {
        'Media': media,
        'Inferior': intervalo[0],
        'Superior': intervalo[1],
        'Margen Error': (intervalo[1] - intervalo[0]) / 2 if intervalo[1] else 0.0
    }

def contraste_hipotesis(grupo1, grupo2, label1="G1", label2="G2"):
    """
    BRYANN VALLEJO LUNA - Contraste de Hipótesis (Welch T-test)
    Compara dos medias independientes sin asumir varianzas iguales.
    """
    # TODO (Bryann): Realiza una prueba Welch's T-Test usando scipy.stats.ttest_ind
    # Extrae el t_stat y el p_valor, y genera una conclusión en función del p_valor.
    
    # --- Tu código aquí ---
    t_stat, p_valor = (0.0, 1.0)
    decision = "Pendiente de ejecutar"
    conclusion = "No definido"
    
    return {
        'Comparación': f"{label1} vs {label2}",
        'T-Stat': t_stat,
        'P-Valor': p_valor,
        'Decisión': decision,
        'Conclusión': conclusion
    }

def verificar_supuestos(data):
    """
    BRYANN VALLEJO LUNA - Prueba de Normalidad (Shapiro-Wilk o K-S)
    """
    # TODO (Bryann): Aplica el test correcto (K-S si n > 5000, Shapiro si no)
    
    # --- Tu código aquí ---
    stat, p = 0.0, 1.0
    prueba = "En desarrollo"
        
    return {'Prueba': prueba, 'Stat': stat, 'P-Valor': p}

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
