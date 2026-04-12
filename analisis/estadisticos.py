"""
PROYECTO: Estadística para Ingeniería
MIEMBRO: RAFAEL RODRIGUEZ MENGUAL (Data Manager)
TAREA: Limpieza de datos y Estadísticos Descriptivos
"""
import pandas as pd
import numpy as np
import os

# NUEVO (Rafael): Diccionario para nombres legibles en la app
VAR_LABELS = {
    'salary_in_usd': 'Salario (USD)',
    'salary': 'Salario'
}

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

        # NUEVO (Rafael): Cálculo de estadísticos avanzados necesarios para la app
        n = df[col].count()
        minimo = df[col].min()
        maximo = df[col].max()
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        cv = (desviacion / media) * 100 if media != 0 else np.nan
        asimetria = df[col].skew()
        curtosis = df[col].kurtosis()

        stats = {
            'Variable': VAR_LABELS.get(col, col),
            'Media': media,
            'Mediana': mediana,
            'Moda': moda_val,
            'Rango': rango,
            'Desviación Típica': desviacion,
            'Varianza': varianza,

            # NUEVO (Rafael): Variables adicionales solicitadas
            'N': n,
            'Mínimo': minimo,
            'Máximo': maximo,
            'Q1': q1,
            'Q3': q3,
            'IQR': iqr,
            'CV%': cv,
            'Asimetría': asimetria,
            'Curtosis': curtosis
        }
        resultados.append(stats)
    
    return pd.DataFrame(resultados)


def calcular_estadisticos_por_categoria(df, columna_numerica, columna_categoria):
    """
    RAFAEL RODRIGUEZ MENGUAL - Estadísticos por categoría
    Agrupa por una variable categórica y calcula métricas descriptivas.
    """
    # NUEVO (Rafael): Agrupación por categoría usando groupby
    grouped = df.groupby(columna_categoria)[columna_numerica]

    resultado = grouped.agg([
        'count',
        'mean',
        'median',
        'std',
        'min',
        'max',
        lambda x: x.quantile(0.25),
        lambda x: x.quantile(0.75)
    ])

    # NUEVO (Rafael): Renombrar columnas para claridad
    resultado.columns = ['N', 'Media', 'Mediana', 'Desv. Típica', 'Mínimo', 'Máximo', 'Q1', 'Q3']

    # NUEVO (Rafael): Cálculo del IQR
    resultado['IQR'] = resultado['Q3'] - resultado['Q1']

    return resultado.reset_index()


def detectar_outliers_iqr(df, columna):
    """
    RAFAEL RODRIGUEZ MENGUAL - Detección de Outliers
    Detecta valores atípicos usando el método IQR.
    """
    # NUEVO (Rafael): Cálculo de Q1, Q3 e IQR
    q1 = df[columna].quantile(0.25)
    q3 = df[columna].quantile(0.75)
    iqr = q3 - q1

    # NUEVO (Rafael): Límites para detectar outliers
    limite_inf = q1 - 1.5 * iqr
    limite_sup = q3 + 1.5 * iqr

    # NUEVO (Rafael): Filtrado de outliers
    outliers = df[(df[columna] < limite_inf) | (df[columna] > limite_sup)]

    n_outliers = outliers.shape[0]
    total = df.shape[0]
    porcentaje = (n_outliers / total) * 100

    return pd.DataFrame([{
        'Variable': columna,
        'Q1': q1,
        'Q3': q3,
        'IQR': iqr,
        'Limite Inferior': limite_inf,
        'Limite Superior': limite_sup,
        'N Outliers': n_outliers,
        '% Outliers': porcentaje
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