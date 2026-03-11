"""
PROYECTO: Estadística para Ingeniería
MIEMBRO: RAFAEL RODRIGUEZ MENGUAL (Data Manager)
TAREA: Limpieza de datos y Estadísticos Descriptivos
"""
import pandas as pd
import numpy as np
import os

def limpiar_datos(df):
    """
    RAFAEL RODRIGUEZ MENGUAL - Data Manager
    Limpia el DataFrame eliminando nulos y verificando formatos.
    """
    # TODO (Rafael): Implementar limpieza de datos.
    # 1. Elimina filas con nulos en 'salary_in_usd', 'experience_level', 'work_year'
    # 2. Asegura que 'work_year' sea int, y 'salary_in_usd' float
    # 3. Guarda el dataset en 'datos/dataset_limpio.csv'
    
    # --- Tu código aquí (aprox. 5 líneas) ---
    
    return df

def calcular_estadisticos(df):
    """
    RAFAEL RODRIGUEZ MENGUAL - Estadísticos Descriptivos
    Calcula media, mediana, moda, rango, desviación y varianza.
    """
    cols_num = ['salary_in_usd', 'salary']
    resultados = []
    
    for col in cols_num:
        # TODO (Rafael): Calcula los estadísticos utilizando pandas
        # Ejemplo: df[col].mean() para la Media
        
        # --- Modifica los ceros por tus cálculos ---
        stats = {
            'Variable': col,
            'Media': 0.0,
            'Mediana': 0.0,
            'Moda': 0.0,
            'Rango': 0.0,
            'Desviación Típica': 0.0,
            'Varianza': 0.0
        }
        resultados.append(stats)
    
    return pd.DataFrame(resultados)

def exportar_tablas(df_stats, ruta):
    """
    RAFAEL RODRIGUEZ MENGUAL - Exportador
    Guarda las tablas de estadísticos en CSV.
    """
    # TODO (Rafael): Asegura que el directorio exista (os.makedirs)
    # y guarda df_stats como CSV en 'ruta'
    
    # --- Tu código aquí (aprox. 2 líneas) ---
    pass
