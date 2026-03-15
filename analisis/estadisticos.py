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
    # TODO: ...

    # --- PASO 2: Eliminar nulos en columnas clave ---
    # TODO: ...

    # --- PASO 3: Asegurar tipos de datos ---
    # TODO: ...

    # --- PASO 4: Resetear índice ---
    # TODO: ...

    # --- PASO 5: Guardar dataset limpio ---
    # TODO: ...

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
    cols_num = ['salary_in_usd', 'salary']
    resultados = []

    for col in cols_num:
        if col not in df.columns:
            continue

        # ╔════════════════════════════════════════════════╗
        # ║  ¡IMPLEMENTA AQUÍ LOS ESTADÍSTICOS DEL LOOP!  ║
        # ╚════════════════════════════════════════════════╝

        data = df[col].dropna()

        # TODO: Calcular media, mediana, moda, min, max, rango, Q1, Q3, IQR, std, var, CV%, skew, kurtosis
        media = 0      # TODO: reemplazar
        mediana = 0    # TODO: reemplazar
        moda = 0       # TODO: reemplazar
        minimo = 0     # TODO: reemplazar
        maximo = 0     # TODO: reemplazar
        rango = 0      # TODO: reemplazar
        q1 = 0         # TODO: reemplazar
        q3 = 0         # TODO: reemplazar
        iqr = 0        # TODO: reemplazar
        desv = 0       # TODO: reemplazar
        varianza = 0   # TODO: reemplazar
        cv = 0         # TODO: reemplazar
        asimetria = 0  # TODO: reemplazar
        curtosis = 0   # TODO: reemplazar

        resultados.append({
            'Variable': col,
            'N': len(data),
            'Media': media,
            'Mediana': mediana,
            'Moda': moda,
            'Mínimo': minimo,
            'Máximo': maximo,
            'Rango': rango,
            'Q1': q1,
            'Q3': q3,
            'IQR': iqr,
            'Desviación Típica': desv,
            'Varianza': varianza,
            'CV%': round(cv, 2),
            'Asimetría': round(asimetria, 4),
            'Curtosis': round(curtosis, 4)
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
    # TODO: COMPLETAR

    # ╔══════════════════════════════════════════════════════╗
    # ║  ¡IMPLEMENTA AQUÍ LOS ESTADÍSTICOS POR CATEGORÍA!  ║
    # ╚══════════════════════════════════════════════════════╝

    # PISTA para lambda de cuartiles:
    # df.groupby(col_cat)[col_num].agg(['count','mean','median','std','min','max',
    #                                    lambda x: x.quantile(0.25),
    #                                    lambda x: x.quantile(0.75)]).round(2)

    return pd.DataFrame()  # TODO: reemplazar con tu implementación


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
    # TODO: COMPLETAR

    # ╔═════════════════════════════════════════════╗
    # ║  ¡IMPLEMENTA AQUÍ LA DETECCIÓN DE OUTLIERS! ║
    # ╚═════════════════════════════════════════════╝

    return pd.DataFrame()  # TODO: reemplazar con tu implementación


def exportar_tablas(df_stats, ruta):
    """
    RAFAEL RODRIGUEZ MENGUAL - Exportador de Tablas
    Guarda el DataFrame de estadísticos como CSV en la ruta indicada.
    (Esta función ya está implementada, no necesitas cambiarla)
    """
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    df_stats.to_csv(ruta, index=False, sep=';', encoding='utf-8')
