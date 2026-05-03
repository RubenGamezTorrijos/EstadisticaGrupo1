"""
PROYECTO: Estadística para Ingeniería
MIEMBRO: RAFAEL RODRIGUEZ MENGUAL (Data Manager)
TAREA: Limpieza de datos y Estadísticos Descriptivos
"""
import pandas as pd
import numpy as np
import os
import config.settings as cfg

# Diccionario para nombres legibles en la app (Sincronizado con settings)
VAR_LABELS = cfg.VAR_LABELS

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
    df = df.copy()

    df = df.dropna(subset=['salary_in_usd', 'experience_level', 'work_year'])  

    df = df.drop_duplicates()

    df['work_year'] = df['work_year'].astype(int)                               
    df['salary_in_usd'] = df['salary_in_usd'].astype(float)                    

    os.makedirs('datos', exist_ok=True)                                         
    df.to_csv('datos/dataset_limpio.csv', index=False, sep=';', encoding='utf-8')                          

    df = df.reset_index(drop=True)
    
    return df


def calcular_estadisticos(df):
    """
    RAFAEL RODRIGUEZ MENGUAL - Estadísticos Descriptivos
    Adaptado para v.2.5.3 por Rubén Gámez (Arquitecto)
    """
    # Columnas dinámicas incluyendo las nuevas de COLI
    cols_num = [cfg.COL_SALARIO_USD, cfg.COL_SALARIO_EUR, cfg.COL_COLI, cfg.COL_SALARIO_AJUSTADO]
    resultados = []
    
    for col in cols_num:
        if col not in df.columns:
            continue

        series = df[col].dropna()
        if series.empty: continue

        media = series.mean()
        desviacion = series.std()
        
        stats = {
            'Variable': cfg.VAR_LABELS.get(col, col),
            'Media': media,
            'Mediana': series.median(),
            'Moda': series.mode().iloc[0] if not series.mode().empty else np.nan,
            'Rango': series.max() - series.min(),
            'Desviación Típica': desviacion,
            'Varianza': series.var(),
            'N': len(series),
            'Mínimo': series.min(),
            'Máximo': series.max(),
            'Q1': series.quantile(0.25),
            'Q3': series.quantile(0.75),
            'IQR': series.quantile(0.75) - series.quantile(0.25),
            'CV%': (desviacion / media * 100) if media != 0 else 0,
            'Asimetría': series.skew(),
            'Curtosis': series.kurtosis()
        }
        resultados.append(stats)
    
    return pd.DataFrame(resultados)


def calcular_estadisticos_por_categoria(df, columna_numerica, columna_categoria):
    """RAFAEL RODRIGUEZ MENGUAL - Agrupación profesional por categoría."""
    resultado = df.groupby(columna_categoria)[columna_numerica].agg([
        ('N', 'count'),
        ('Media', 'mean'),
        ('Mediana', 'median'),
        ('Desv. Típica', 'std'),
        ('Mínimo', 'min'),
        ('Máximo', 'max'),
        ('Q1', lambda x: x.quantile(0.25)),
        ('Q3', lambda x: x.quantile(0.75))
    ]).reset_index()
    
    resultado['IQR'] = resultado['Q3'] - resultado['Q1']
    return resultado.round(2)


def detectar_outliers_iqr(df, columna):
    """RAFAEL RODRIGUEZ MENGUAL - Detección de Outliers (v.2.5.3)"""
    q1 = df[columna].quantile(0.25)
    q3 = df[columna].quantile(0.75)
    iqr = q3 - q1
    limite_inf = q1 - 1.5 * iqr
    limite_sup = q3 + 1.5 * iqr

    n_outliers = df[(df[columna] < limite_inf) | (df[columna] > limite_sup)].shape[0]
    porcentaje = (n_outliers / len(df)) * 100 if len(df) > 0 else 0

    return pd.DataFrame([{
        'Variable': cfg.VAR_LABELS.get(columna, columna),
        'Q1': q1, 'Q3': q3, 'IQR': iqr,
        'Limite Inferior': limite_inf,
        'Limite Superior': limite_sup,
        'N Outliers': n_outliers,
        '% Outliers': np.round(porcentaje, 2)
    }])


def exportar_tablas(df_stats, ruta):
    """
    RAFAEL RODRIGUEZ MENGUAL - Exportador
    Guarda las tablas de estadísticos en CSV.
    """
    # TODO (Rafael): Asegura que el directorio exista (os.makedirs)
    # y guarda df_stats como CSV en 'ruta'
    
    # --- Tu código aquí (aprox. 2 líneas) ---
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    df_stats.to_csv(ruta, index=False, sep=';', encoding='utf-8')
    pass