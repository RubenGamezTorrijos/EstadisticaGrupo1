"""
PROYECTO: Estadística para Ingeniería
MIEMBRO: BRYANN VALLEJO LUNA (Analista Inferencial)
TAREA: Intervalos de Confianza, Contrastes de Hipótesis y Verificación de Supuestos

INSTRUCCIONES PARA COMPLETAR:
================================
Debes implementar las funciones marcadas con '# TODO: COMPLETAR'
siguiendo las instrucciones en los docstrings.

Funciones que DEBES completar:
1. calcular_ic_95()                  - Intervalo de Confianza (T de Student)
2. contraste_hipotesis_1_muestra()   - T-test para 1 muestra (H0: μ = mu0)
3. contraste_hipotesis()             - T-test Welch para 2 muestras independientes
4. anova_one_way()                   - ANOVA de una vía (F-test)
5. verificar_supuestos_normalidad()  - Test de normalidad (Shapiro-Wilk / K-S)
6. verificar_homocedasticidad()      - Test de varianza (Levene)

MÓDULOS SCIPY DISPONIBLES:
from scipy.stats import t            → t.ppf(), distribución T Student
from scipy.stats import ttest_1samp → T-test 1 muestra
from scipy.stats import ttest_ind   → T-test 2 muestras independientes
from scipy.stats import f_oneway    → ANOVA F-test
from scipy.stats import shapiro     → Test de normalidad Shapiro-Wilk
from scipy.stats import levene      → Test de homocedasticidad de Levene
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import t, shapiro, levene, ttest_1samp, ttest_ind, f_oneway
import os


def calcular_ic_95(data, confianza=0.95):
    """
    BRYANN VALLEJO LUNA - Intervalo de Confianza para la Media

    Usa la distribución T de Student (no la normal) porque la varianza
    poblacional es desconocida.

    FÓRMULAS:
    ─────────
    n         = len(data)
    media     = data.mean()
    std       = data.std()
    se        = std / sqrt(n)          ← Error Estándar
    t_critico = t.ppf((1+confianza)/2, df=n-1)
    margen    = t_critico * se
    IC = [media - margen, media + margen]

    CLAVES REQUERIDAS EN EL DICT DE RETORNO:
    'Media', 'Inferior', 'Superior', 'Margen Error',
    'media', 'ic_inferior', 'ic_superior', 'margen_error',
    'n', 'se', 't_critico'

    (Mantener las dos variantes de clave es necesario para compatibilidad
    con app.py y las funciones de exportación)

    Args:
        data: pd.Series de datos numéricos
        confianza: nivel de confianza (por defecto 0.95)

    Returns:
        dict con todos los resultados del IC
    """
    # TODO: COMPLETAR

    # ╔═══════════════════════════════════════════════════════╗
    # ║  ¡IMPLEMENTA AQUÍ EL CÁLCULO DEL IC 95%!             ║
    # ╚═══════════════════════════════════════════════════════╝

    data = data.dropna()
    n     = len(data)
    media = data.mean()

    # TODO: Calcular std, se, t_critico, margen_error, ic_inferior, ic_superior
    std          = 0  # TODO: reemplazar
    se           = 0  # TODO: reemplazar
    t_critico    = 0  # TODO: reemplazar
    margen_error = 0  # TODO: reemplazar
    ic_inferior  = 0  # TODO: reemplazar
    ic_superior  = 0  # TODO: reemplazar

    return {
        # Keys para app.py (formato con mayúsculas)
        'Media': media,
        'Inferior': ic_inferior,
        'Superior': ic_superior,
        'Margen Error': margen_error,
        # Keys compatibilidad qwen3 (minúsculas)
        'media': media,
        'ic_inferior': ic_inferior,
        'ic_superior': ic_superior,
        'margen_error': margen_error,
        'n': n,
        'se': se,
        't_critico': t_critico
    }


def contraste_hipotesis_1_muestra(data, mu0, alternativa='two-sided', alfa=0.05):
    """
    BRYANN VALLEJO LUNA - Contraste de Hipótesis (1 Muestra, T-test)

    H₀: μ = mu0   (la media poblacional es igual a mu0)
    H₁: μ ≠ mu0   (dos colas)

    FÓRMULAS / FUNCIONES:
    ─────────────────────
    t_stat, p_valor = ttest_1samp(data, mu0)   ← de scipy.stats
    rechaza_h0      = p_valor < alfa
    cohen_d         = (media - mu0) / std       ← d de Cohen (tamaño del efecto)

    USO DESDE app.py:
    contraste_hipotesis_1_muestra(df['salary_in_usd'], mu0=100000)

    CLAVES REQUERIDAS EN EL DICT DE RETORNO:
    'Hipótesis Nula', 'Media Muestral', 'mu0', 'T-Stat', 'P-Valor',
    'Decisión', 'Conclusión', 'Cohen d', 'rechaza_h0', 'p_valor', 't_statistic'

    Args:
        data: pd.Series de datos numéricos
        mu0: valor hipotético de la media bajo H₀ (ej: 100000)
        alternativa: 'two-sided' (default)
        alfa: nivel de significancia (default 0.05)

    Returns:
        dict con resultados del contraste
    """
    # TODO: COMPLETAR

    # ╔══════════════════════════════════════════════════════╗
    # ║  ¡IMPLEMENTA AQUÍ EL T-TEST 1 MUESTRA!              ║
    # ╚══════════════════════════════════════════════════════╝

    data  = data.dropna()
    media = data.mean()
    std   = data.std()
    n     = len(data)

    # TODO: Llamar a ttest_1samp y calcular rechaza_h0 y cohen_d
    t_stat     = 0  # TODO: reemplazar
    p_valor    = 1  # TODO: reemplazar
    rechaza_h0 = False  # TODO: reemplazar
    cohen_d    = 0  # TODO: reemplazar

    return {
        'Hipótesis Nula': f'μ = {mu0:,.0f}',
        'Media Muestral': media,
        'mu0': mu0,
        'T-Stat': t_stat,
        'P-Valor': p_valor,
        'Decisión': 'Rechazar H₀' if rechaza_h0 else 'No Rechazar H₀',
        'Conclusión': f'La media ES significativamente diferente de ${mu0:,.0f}' if rechaza_h0 else f'La media NO es diferente de ${mu0:,.0f}',
        'Cohen d': round(cohen_d, 4),
        'rechaza_h0': rechaza_h0,
        'p_valor': p_valor,
        't_statistic': t_stat
    }


def contraste_hipotesis(grupo1, grupo2, label1="G1", label2="G2", alfa=0.05):
    """
    BRYANN VALLEJO LUNA - Contraste de Hipótesis (2 Muestras, Welch T-test)

    H₀: μ₁ = μ₂   (las medias de ambos grupos son iguales)
    H₁: μ₁ ≠ μ₂

    Usa Welch T-test (equal_var=False) porque NO asume que las
    varianzas sean iguales.

    FÓRMULAS / FUNCIONES:
    ─────────────────────
    t_stat, p_valor  = ttest_ind(grupo1, grupo2, equal_var=False)
    diferencia       = media1 - media2
    pooled_std       = sqrt(((n1-1)*std1² + (n2-1)*std2²) / (n1+n2-2))
    cohen_d          = diferencia / pooled_std   ← d de Cohen

    USO DESDE app.py:
    contraste_hipotesis(df[df['experience_level']=='Senior']['salary_in_usd'],
                        df[df['experience_level']=='Mid-level']['salary_in_usd'],
                        "Senior", "Mid-level")

    CLAVES REQUERIDAS EN EL DICT DE RETORNO:
    'Comparación', 'Media G1', 'Media G2', 'Diferencia Medias',
    'T-Stat', 'P-Valor', 'Decisión', 'Conclusión', 'Cohen d',
    'media_grupo1', 'media_grupo2', 'diferencia_medias',
    'rechaza_h0', 'p_valor', 't_statistic'

    Args:
        grupo1, grupo2: pd.Series (las dos muestras a comparar)
        label1, label2: etiquetas para los grupos
        alfa: nivel de significancia (default 0.05)

    Returns:
        dict con resultados del contraste
    """
    # TODO: COMPLETAR

    # ╔══════════════════════════════════════════════════════╗
    # ║  ¡IMPLEMENTA AQUÍ EL WELCH T-TEST 2 MUESTRAS!       ║
    # ╚══════════════════════════════════════════════════════╝

    grupo1 = grupo1.dropna()
    grupo2 = grupo2.dropna()

    n1, n2         = len(grupo1), len(grupo2)
    media1, media2 = grupo1.mean(), grupo2.mean()
    std1, std2     = grupo1.std(), grupo2.std()

    # TODO: Calcular t_stat, p_valor, diferencia, cohen_d, rechaza_h0
    t_stat     = 0    # TODO: reemplazar
    p_valor    = 1    # TODO: reemplazar
    diferencia = 0    # TODO: reemplazar
    cohen_d    = 0    # TODO: reemplazar
    rechaza_h0 = False  # TODO: reemplazar

    return {
        'Comparación': f'{label1} vs {label2}',
        'Media G1': media1,
        'Media G2': media2,
        'Diferencia Medias': diferencia,
        'T-Stat': t_stat,
        'P-Valor': p_valor,
        'Decisión': 'Rechazar H₀' if rechaza_h0 else 'No Rechazar H₀',
        'Conclusión': f'Hay diferencia significativa entre {label1} y {label2}' if rechaza_h0 else f'No hay diferencia significativa entre {label1} y {label2}',
        'Cohen d': round(cohen_d, 4),
        'media_grupo1': media1,
        'media_grupo2': media2,
        'diferencia_medias': diferencia,
        'rechaza_h0': rechaza_h0,
        'p_valor': p_valor,
        't_statistic': t_stat
    }


def contraste_hipotesis_2_muestras(grupo1, grupo2, alternativa='two-sided', alfa=0.05, equal_var=False):
    """Alias de contraste_hipotesis para compatibilidad."""
    return contraste_hipotesis(grupo1, grupo2, alfa=alfa)


def anova_one_way(df, columna_numerica, columna_grupo, alfa=0.05):
    """
    BRYANN VALLEJO LUNA - ANOVA de Una Vía (F-test)

    Compara las medias de TODOS los grupos al mismo tiempo.

    H₀: μ₁ = μ₂ = μ₃ = ... (todas las medias son iguales)
    H₁: Al menos una media es diferente

    FÓRMULAS / FUNCIONES:
    ─────────────────────
    grupos   = [grupo[col_num].dropna() for _, grupo in df.groupby(col_grupo)]
    f_stat, p_valor = f_oneway(*grupos)   ← de scipy.stats
    rechaza_h0      = p_valor < alfa

    ESTADÍSTICOS POR GRUPO:
    df.groupby(columna_grupo)[columna_numerica].agg(['count','mean','std','min','max'])

    CLAVES REQUERIDAS EN EL DICT DE RETORNO:
    'Hipótesis Nula', 'F-Stat', 'P-Valor', 'Decisión', 'Conclusión',
    'Estadísticos por Grupo', 'f_statistic', 'p_valor', 'rechaza_h0', 'conclusion'

    Args:
        df: DataFrame limpio
        columna_numerica: columna a comparar (ej: 'salary_in_usd')
        columna_grupo: columna de agrupación (ej: 'experience_level')
        alfa: nivel de significancia

    Returns:
        dict con resultados del ANOVA
    """
    # TODO: COMPLETAR

    # ╔════════════════════════════════════════╗
    # ║  ¡IMPLEMENTA AQUÍ EL ANOVA F-TEST!    ║
    # ╚════════════════════════════════════════╝

    f_stat     = 0    # TODO: reemplazar
    p_valor    = 1    # TODO: reemplazar
    rechaza_h0 = False  # TODO: reemplazar

    estadisticos_grupos = df.groupby(columna_grupo)[columna_numerica].agg(
        ['count', 'mean', 'std', 'min', 'max']
    ).round(2)

    return {
        'Hipótesis Nula': 'Todas las medias son iguales',
        'F-Stat': f_stat,
        'P-Valor': p_valor,
        'Decisión': 'Rechazar H₀' if rechaza_h0 else 'No Rechazar H₀',
        'Conclusión': 'Hay diferencias significativas entre grupos' if rechaza_h0 else 'No hay diferencias significativas entre grupos',
        'Estadísticos por Grupo': estadisticos_grupos,
        'f_statistic': f_stat,
        'p_valor': p_valor,
        'rechaza_h0': rechaza_h0,
        'conclusion': 'Rechazar H₀' if rechaza_h0 else 'No Rechazar H₀'
    }


def verificar_supuestos_normalidad(data):
    """
    BRYANN VALLEJO LUNA - Test de Normalidad (Shapiro-Wilk / Kolmogorov-Smirnov)

    IMPORTANTE: Shapiro-Wilk solo funciona para n ≤ 5000.
    Para n > 5000, usar Kolmogorov-Smirnov (kstest).

    FÓRMULAS:
    ─────────
    Si len(data) <= 5000:
        stat, p_valor = shapiro(data)
        prueba = 'Shapiro-Wilk'
    Si len(data) > 5000:
        stat, p_valor = stats.kstest(data, 'norm', args=(data.mean(), data.std()))
        prueba = 'Kolmogorov-Smirnov'

    es_normal = p_valor > 0.05

    CLAVES REQUERIDAS:
    'Prueba', 'Estadístico', 'P-Valor', 'Es Normal', 'Conclusión',
    'estadistico', 'p_valor', 'es_normal', 'conclusion'

    Args:
        data: pd.Series de datos

    Returns:
        dict con resultados del test
    """
    # TODO: COMPLETAR

    # ╔══════════════════════════════════════════════════╗
    # ║  ¡IMPLEMENTA AQUÍ EL TEST DE NORMALIDAD!         ║
    # ╚══════════════════════════════════════════════════╝

    data = data.dropna()
    prueba    = 'Shapiro-Wilk'  # TODO: determinar qué prueba usar según n
    stat      = 0  # TODO: reemplazar
    p_valor   = 1  # TODO: reemplazar
    es_normal = p_valor > 0.05

    return {
        'Prueba': prueba,
        'Estadístico': stat,
        'P-Valor': p_valor,
        'Es Normal': es_normal,
        'Conclusión': 'Los datos siguen una distribución normal' if es_normal else 'Los datos NO siguen una distribución normal',
        'estadistico': stat,
        'p_valor': p_valor,
        'es_normal': es_normal,
        'conclusion': 'Los datos siguen distribución normal' if es_normal else 'Los datos NO siguen distribución normal'
    }


def verificar_homocedasticidad(grupo1, grupo2):
    """
    BRYANN VALLEJO LUNA - Test de Homocedasticidad (Levene)

    Comprueba si las varianzas de dos grupos son iguales.

    FÓRMULA:
    ─────────
    stat, p_valor = levene(grupo1, grupo2)   ← de scipy.stats
    varianzas_iguales = p_valor > 0.05

    CLAVES REQUERIDAS:
    'Prueba', 'Estadístico', 'P-Valor', 'Varianzas Iguales', 'Conclusión',
    'estadistico', 'p_valor', 'varianzas_iguales', 'conclusion'

    Args:
        grupo1, grupo2: pd.Series (las dos muestras)

    Returns:
        dict con resultados del test
    """
    # TODO: COMPLETAR

    # ╔══════════════════════════════════════════════════╗
    # ║  ¡IMPLEMENTA AQUÍ EL TEST DE HOMOCEDASTICIDAD!   ║
    # ╚══════════════════════════════════════════════════╝

    stat              = 0  # TODO: reemplazar
    p_valor           = 1  # TODO: reemplazar
    varianzas_iguales = p_valor > 0.05

    return {
        'Prueba': 'Levene',
        'Estadístico': stat,
        'P-Valor': p_valor,
        'Varianzas Iguales': varianzas_iguales,
        'Conclusión': 'Varianzas iguales (homocedasticidad cumplida)' if varianzas_iguales else 'Varianzas diferentes (heterocedasticidad)',
        'estadistico': stat,
        'p_valor': p_valor,
        'varianzas_iguales': varianzas_iguales,
        'conclusion': 'Varianzas iguales' if varianzas_iguales else 'Varianzas diferentes'
    }


def verificar_supuestos(data):
    """Alias de verificar_supuestos_normalidad para compatibilidad con versión anterior."""
    return verificar_supuestos_normalidad(data)


def generar_reporte_inferencial(df):
    """
    Genera un resumen de los análisis inferenciales.
    (Esta función se completa automáticamente con las anteriores)
    """
    ic_salario = calcular_ic_95(df['salary_in_usd'])
    senior = df[df['experience_level'] == 'Senior']['salary_in_usd']
    mid    = df[df['experience_level'] == 'Mid-level']['salary_in_usd']
    test_exp = contraste_hipotesis(senior, mid, 'Senior', 'Mid-level')

    os.makedirs('outputs/tablas', exist_ok=True)
    df_reporte = pd.DataFrame([{
        'IC_Inferior': ic_salario['Inferior'],
        'IC_Superior': ic_salario['Superior'],
        'Media': ic_salario['Media'],
        'P-Valor_Senior_vs_Mid': test_exp['P-Valor'],
        'Decisión': test_exp['Decisión']
    }])
    df_reporte.to_csv('outputs/tablas/inferencial.csv', index=False, sep=';')
    return ic_salario, test_exp
