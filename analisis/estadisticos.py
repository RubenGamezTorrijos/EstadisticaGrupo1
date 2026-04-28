import pandas as pd
import numpy as np
import os
from config.settings import VAR_LABELS, COL_SALARIO_USD, COL_SALARIO_EUR, COL_SALARIO_DINAMICO, COL_COLI


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
    # Lista de columnas a analizar (usando constantes centralizadas)
    cols_num = [COL_SALARIO_USD, COL_SALARIO_EUR, COL_SALARIO_DINAMICO, COL_COLI, 'work_year']
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
