"""
PROYECTO: Estadística para Ingeniería
MIEMBRO: BRYANN VALLEJO LUNA (Analista Inferencial)
TAREA: Intervalos de Confianza y Contrastes de Hipótesis
"""
import pandas as pd
import numpy as np
from scipy import stats
import config.settings as cfg

def realizar_test_hipotesis(df, variable_num, variable_cat):
    """
    BRYANN SKEITH LOZA CACERES - Estadística Inferencial
    Realiza un test T o ANOVA según el número de categorías.
    """
    grupos = df[variable_cat].unique()
    datos_grupos = [df[df[variable_cat] == g][variable_num].dropna() for g in grupos]
    
    # Filtrar grupos con muy pocos datos
    datos_grupos = [g for g in datos_grupos if len(g) > 5]
    
    if len(datos_grupos) < 2:
        return {"error": "No hay suficientes grupos con datos (mínimo 5 registros por grupo) para realizar el test de hipótesis."}

    if len(datos_grupos) == 2:
        # Test de Student
        stat, p_val = stats.ttest_ind(datos_grupos[0], datos_grupos[1], equal_var=False)
        test_nombre = "Test T de Student (2 grupos)"
    else:
        # ANOVA
        stat, p_val = stats.f_oneway(*datos_grupos)
        test_nombre = "ANOVA (múltiples grupos)"

    return {
        "Test": test_nombre,
        "Variable Numérica": cfg.VAR_LABELS.get(variable_num, variable_num),
        "Variable Categórica": cfg.VAR_LABELS.get(variable_cat, variable_cat),
        "Estadístico": float(stat),
        "P-Valor": float(p_val),
        "Significativo (5%)": "Sí" if p_val < 0.05 else "No"
    }

def calcular_intervalos_confianza(df, columna, confianza=0.95):
    """BRYANN SKEITH LOZA CACERES - Intervalos de Confianza"""
    data = df[columna].dropna()
    if data is None or len(data) < 3:
        return {
            'Prueba': 'N/A', 'Stat': 0, 'P-Valor': 0, 'Estado': 'ERROR',
            'error': 'Se requieren al menos 3 registros para validar normalidad.'
        }
    n = len(data)
    if n < 2:
        return {
            "Variable": cfg.VAR_LABELS.get(columna, columna),
            "Media": 0, "Error Estándar": 0, "Límite Inferior": 0, "Límite Superior": 0,
            "error": "Datos insuficientes"
        }
    media = np.mean(data)
    sem = stats.sem(data)
    intervalo = sem * stats.t.ppf((1 + confianza) / 2., n-1)
    
    return {
        "Variable": cfg.VAR_LABELS.get(columna, columna),
        "Media": media,
        "Error Estándar": sem,
        "Límite Inferior": media - intervalo,
        "Límite Superior": media + intervalo
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

    if data is None or len(data) < 3:
        return {
            'Prueba': 'N/A', 'Stat': 0, 'P-Valor': 0, 'Estado': 'ERROR',
            'error': 'Se requieren al menos 3 registros para validar normalidad.'
        }
    if len(data) < 3:
        return {
            'Prueba': 'N/A',
            'Stat': 0,
            'P-Valor': 1.0,
            'Estado': 'ERROR',
            'error': 'Datos insuficientes (n < 3)'
        }
        
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
