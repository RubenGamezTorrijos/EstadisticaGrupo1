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
    df = df.dropna(subset=['salary_in_usd', 'experience_level', 'work_year'])  
    df['work_year'] = df['work_year'].astype(int)                               
    df['salary_in_usd'] = df['salary_in_usd'].astype(float)                    
    os.makedirs('datos', exist_ok=True)                                         
    df.to_csv('datos/dataset_limpio.csv', index=False)                          
    
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
        if col not in df.columns:
            continue

        media = df[col].mean()
        mediana = df[col].median()
        moda = df[col].mode()
        moda_val = moda.iloc[0] if not moda.empty else np.nan
        rango = df[col].max() - df[col].min()
        desviacion = df[col].std()
        varianza = df[col].var()

        stats = {
            'Variable': col,
            'Media': media,
            'Mediana': mediana,
            'Moda': moda_val,
            'Rango': rango,
            'Desviación Típica': desviacion,
            'Varianza': varianza
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
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    df_stats.to_csv(ruta, index=False)
    pass
