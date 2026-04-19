"""
PROYECTO: Estadística para Ingeniería
MIEMBRO: RAFAEL RODRIGUEZ MENGUAL (Data Manager)
TAREA: Limpieza de datos y Estadísticos Descriptivos Completos

INSTRUCCIONES PARA COMPLETAR:
================================
Debes implementar las funciones marcadas con '# TODO: COMPLETAR'
siguiendo las instrucciones en los docstrings.

Funciones que DEBES completar:
1. limpiar_datos()             - Limpieza del dataset (duplicados, nulos, tipos)
2. calcular_estadisticos()     - Estadísticos completos (media, mediana, moda, Q1, Q3, IQR, CV%, Asimetría, Curtosis)
3. calcular_estadisticos_por_categoria() - Estadísticos agrupados por categoría
4. detectar_outliers_iqr()     - Detección de valores atípicos por IQR

COLUMNAS DISPONIBLES EN EL DATASET:
- work_year (int): Año de trabajo
- experience_level (str): EN / MI / SE / EX  (Entry, Mid, Senior, Executive)
- job_category (str): categoría del puesto
- salary_in_usd (float): salario anual en USD ← VARIABLE PRINCIPAL
- salary (float): salario en moneda local
- work_setting (str): Remote / Hybrid / In-person
"""

import pandas as pd
import numpy as np
import os

# Índice de coste de vida aproximado (USA = 100)
COST_OF_LIVING_INDEX = {
    'United States': 100, 'United Kingdom': 85, 'Canada': 90, 
    'Spain': 70, 'Germany': 80, 'France': 80, 'Australia': 95, 
    'Portugal': 65, 'Netherlands': 85, 'Brazil': 50, 
    'Colombia': 40, 'Greece': 60, 'Italy': 75, 'Mexico': 45, 
    'Poland': 60, 'Estonia': 65, 'Nigeria': 35, 'Ireland': 90, 
    'India': 30, 'Russia': 40
}

# Mapeo de variables para etiquetas legibles
VAR_LABELS = {
    'work_year': 'Año de Trabajo',
    'experience_level': 'Nivel de Experiencia',
    'employment_type': 'Tipo de Empleo',
    'job_title': 'Título del Puesto',
    'salary': 'Salario (Original)',
    'salary_currency': 'Moneda',
    'salary_in_usd': 'Salario (USD)',
    'salary_in_eur': 'Salario (EUR)',
    'employee_residence': 'Residencia Empleado',
    'remote_ratio': 'Ratio Remoto',
    'company_location': 'Localización Empresa',
    'company_size': 'Tamaño Empresa',
    'job_category': 'Categoría de Puesto',
    'work_setting': 'Modalidad de Trabajo',
    'cost_of_living_index': 'Índice de Coste de Vida'
}

def limpiar_datos(df):
    """
    RAFAEL RODRIGUEZ MENGUAL - Limpieza del Dataset

    Pasos que debes implementar:
    1. Eliminar filas duplicadas               → df.drop_duplicates()
    2. Eliminar nulos en columnas clave:       → df.dropna(subset=['salary_in_usd','experience_level','job_category'])
    3. Asegurar tipos:
       - 'work_year' → int
       - 'salary_in_usd' → float
    4. Resetear el índice                      → df.reset_index(drop=True)
    5. Guardar en 'datos/dataset_limpio.csv'

    PISTA: Usa df.copy() al inicio para no modificar el DataFrame original.

    Args:
        df: DataFrame original (crudo)

    Returns:
        DataFrame limpio y procesado
    """
    # TODO: COMPLETAR - Elimina duplicados, nulos en columnas clave y asegura tipos

    # ╔══════════════════════════════════════════════════════╗
    # ║  ¡IMPLEMENTA AQUÍ TU LÓGICA DE LIMPIEZA DE DATOS!  ║
    # ╚══════════════════════════════════════════════════════╝

    df_limpio = df.copy()

    # --- PASO 1: Eliminar duplicados ---
    df_limpio = df_limpio.drop_duplicates()

    # --- PASO 2: Eliminar nulos en columnas clave ---
    df_limpio = df_limpio.dropna(subset=['salary_in_usd', 'experience_level', 'job_category'])

    # --- PASO 3: Asegurar tipos de datos ---
    df_limpio['work_year'] = df_limpio['work_year'].astype(int)
    df_limpio['salary_in_usd'] = df_limpio['salary_in_usd'].astype(float)
    
    # --- PASO 4: Multidivisa (EUR) ---
    # Usamos un cambio base de 0.92 si no existe la columna
    if 'salary_in_eur' not in df_limpio.columns:
        df_limpio['salary_in_eur'] = df_limpio['salary_in_usd'] * 0.92
    df_limpio['salary_in_eur'] = df_limpio['salary_in_eur'].astype(float)

    # --- PASO 5: Nueva Variable de Coste de Vida (Mejora 2) ---
    # Asignamos 70 (media estimada global) a los países que no estén en el Top 20
    if 'company_location' in df_limpio.columns:
        df_limpio['cost_of_living_index'] = df_limpio['company_location'].map(COST_OF_LIVING_INDEX).fillna(70)

    # --- PASO 5: Resetear índice ---
    df_limpio = df_limpio.reset_index(drop=True)

    # --- PASO 5: Guardar dataset limpio ---
    # os.makedirs('datos', exist_ok=True)
    # df_limpio.to_csv('datos/dataset_limpio.csv', index=False)

    return df_limpio


def calcular_estadisticos(df):
    """
    RAFAEL RODRIGUEZ MENGUAL - Estadísticos Descriptivos Completos

    Debes calcular para las columnas 'salary_in_usd' y 'salary' todos los
    siguientes estadísticos y devolverlos en un DataFrame:

    ESTADÍSTICOS REQUERIDOS:
    ┌─────────────────────┬─────────────────────────────────────────┐
    │ Variable            │ Nombre de la columna en el retorno      │
    ├─────────────────────┼─────────────────────────────────────────┤
    │ Nombre columna      │ 'Variable'                              │
    │ Nº observaciones    │ 'N'                                     │
    │ Media aritmética    │ 'Media'          → data.mean()          │
    │ Mediana (Q2)        │ 'Mediana'        → data.median()        │
    │ Moda                │ 'Moda'           → data.mode().iloc[0]  │
    │ Mínimo              │ 'Mínimo'         → data.min()           │
    │ Máximo              │ 'Máximo'         → data.max()           │
    │ Rango               │ 'Rango'          = Máximo - Mínimo      │
    │ Cuartil 1 (25%)     │ 'Q1'             → data.quantile(0.25)  │
    │ Cuartil 3 (75%)     │ 'Q3'             → data.quantile(0.75)  │
    │ Rango Intercuart.   │ 'IQR'            = Q3 - Q1              │
    │ Desviación Típica   │ 'Desviación Típica' → data.std()        │
    │ Varianza            │ 'Varianza'       → data.var()           │
    │ Coef. Variación (%) │ 'CV%'            = (std/media)*100      │
    │ Asimetría           │ 'Asimetría'      → data.skew()          │
    │ Curtosis            │ 'Curtosis'       → data.kurtosis()      │
    └─────────────────────┴─────────────────────────────────────────┘

    Args:
        df: DataFrame limpio

    Returns:
        pd.DataFrame con una fila por variable analizada
    """
    # TODO: COMPLETAR
    cols_num = ['salary_in_usd', 'salary_in_eur', 'work_year', 'cost_of_living_index']
    resultados = []

    for col in cols_num:
        if col not in df.columns:
            continue

        series = df[col].dropna()
        if series.empty: continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        media = series.mean()
        desv = series.std()

        resultados.append({
            'ID_Variable': col,
            'Variable': VAR_LABELS.get(col, col),
            'N': len(series),
            'Media': media,
            'Mediana': series.median(),
            'Moda': series.mode().iloc[0] if not series.mode().empty else np.nan,
            'Mínimo': series.min(),
            'Máximo': series.max(),
            'Rango': series.max() - series.min(),
            'Q1': q1,
            'Q3': q3,
            'IQR': iqr,
            'Desviación Típica': desv,
            'Varianza': series.var(),
            'CV%': (desv / media * 100) if media != 0 else 0,
            'Asimetría': series.skew(),
            'Curtosis': series.kurtosis()
        })

    return pd.DataFrame(resultados)


def calcular_estadisticos_por_categoria(df, columna_numerica, columna_categoria):
    """
    RAFAEL RODRIGUEZ MENGUAL - Estadísticos por Categoría

    Agrupa el DataFrame por 'columna_categoria' y para cada grupo calcula:
    count, mean, median, std, min, max, Q1 (quantile 0.25) y Q3 (quantile 0.75)
    Añade IQR = Q3 - Q1

    EJEMPLO DE USO:
    calcular_estadisticos_por_categoria(df, 'salary_in_usd', 'experience_level')
    → Devuelve una tabla con las métricas por: Entry-level, Mid-level, Senior, Executive

    PISTA: Usa df.groupby(columna_categoria)[columna_numerica].agg([...]).round(2)

    Columnas del retorno:
    [columna_categoria, 'N', 'Media', 'Mediana', 'Desv. Típica', 'Mínimo', 'Máximo', 'Q1', 'Q3', 'IQR']

    Args:
        df: DataFrame limpio
        columna_numerica: nombre de la columna numérica (ej: 'salary_in_usd')
        columna_categoria: nombre de la columna categórica (ej: 'experience_level')

    Returns:
        pd.DataFrame con estadísticos por cada categoría
    """
    stats = df.groupby(columna_categoria)[columna_numerica].agg([
        ('N', 'count'),
        ('Media', 'mean'),
        ('Mediana', 'median'),
        ('Desv. Típica', 'std'),
        ('Mínimo', 'min'),
        ('Máximo', 'max'),
        ('Q1', lambda x: x.quantile(0.25)),
        ('Q3', lambda x: x.quantile(0.75))
    ])
    stats['IQR'] = stats['Q3'] - stats['Q1']
    return stats.reset_index().round(2)


def detectar_outliers_iqr(df, columna):
    """
    RAFAEL RODRIGUEZ MENGUAL - Detección de Outliers (Método IQR)

    Un outlier es un valor FUERA del rango [Q1 - 1.5*IQR, Q3 + 1.5*IQR].

    Fórmulas:
    ─────────
    Q1 = df[columna].quantile(0.25)
    Q3 = df[columna].quantile(0.75)
    IQR = Q3 - Q1
    Límite Inferior = Q1 - 1.5 * IQR
    Límite Superior = Q3 + 1.5 * IQR
    Outliers = registros donde valor < Límite Inferior  OR  valor > Límite Superior

    Columnas del DataFrame de retorno:
    ['Variable', 'Q1', 'Q3', 'IQR', 'Límite Inferior', 'Límite Superior', 'N Outliers', '% Outliers']

    Args:
        df: DataFrame limpio
        columna: nombre de la columna a analizar

    Returns:
        pd.DataFrame con una sola fila que resume los outliers encontrados
    """
    q1 = df[columna].quantile(0.25)
    q3 = df[columna].quantile(0.75)
    iqr = q3 - q1
    lim_inf = q1 - 1.5 * iqr
    lim_sup = q3 + 1.5 * iqr
    
    outliers = df[(df[columna] < lim_inf) | (df[columna] > lim_sup)]
    n_out = len(outliers)
    pct_out = (n_out / len(df)) * 100 if len(df) > 0 else 0
    
    return pd.DataFrame([{
        'Variable': columna,
        'Q1': q1,
        'Q3': q3,
        'IQR': iqr,
        'Límite Inferior': lim_inf,
        'Límite Superior': lim_sup,
        'N Outliers': n_out,
        '% Outliers': np.round(float(pct_out), 2)
    }])


def exportar_tablas(df_stats, ruta):
    """
    RAFAEL RODRIGUEZ MENGUAL - Exportador de Tablas
    Guarda el DataFrame de estadísticos como CSV en la ruta indicada.
    (Esta función ya está implementada, no necesitas cambiarla)
    """
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    df_stats.to_csv(ruta, index=False, sep=';', encoding='utf-8')
