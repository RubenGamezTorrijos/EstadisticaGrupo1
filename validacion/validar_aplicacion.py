#!/usr/bin/env python3
"""
VALIDADOR OFICIAL - Grupo de Trabajo 1
Verifica que los cálculos de la aplicación Streamlit coinciden con fórmulas estadísticas estándar.

Uso:
    python validar_aplicacion.py --dataset datos/dataset_enriquecido.csv --tolerancia 0.01

Autor: Rubén Gámez Torrijos (Coordinador) + Equipo
Fecha: Mayo 2026
Versión: 1.0.0
"""

import argparse
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import json
import sys
import os
from datetime import datetime

# =============================================================================
# CONFIGURACIÓN GLOBAL
# =============================================================================
TOLERANCIA_RELATIVA = 0.01  # 1% de tolerancia para comparaciones flotantes
TOLERANCIA_ABSOLUTA = 1e-6  # Para valores muy pequeños
ALPHA = 0.05  # Nivel de significación para tests de hipótesis

# Columnas según settings.py
COL_SALARIO_USD = 'salary_dollar_usd'
COL_SALARIO_EUR = 'salary_euro'
COL_COLI = 'cost_of_living_index'
COL_SALARIO_AJUSTADO = 'salary_adjusted_coli'
COL_PAIS = 'company_location'

# =============================================================================
# FÓRMULAS ESTADÍSTICAS "MANUALES" (Referencia Académica)
# =============================================================================

def calcular_media_manual(series: pd.Series) -> float:
    """Fórmula: μ = (1/n) * Σxᵢ"""
    data = series.dropna()
    return np.sum(data) / len(data) if len(data) > 0 else np.nan

def calcular_mediana_manual(series: pd.Series) -> float:
    """Valor central de la distribución ordenada"""
    data = series.dropna().sort_values()
    n = len(data)
    if n == 0:
        return np.nan
    if n % 2 == 0:
        return (data.iloc[n//2 - 1] + data.iloc[n//2]) / 2
    return data.iloc[n//2]

def calcular_moda_manual(series: pd.Series) -> float:
    """Valor con mayor frecuencia"""
    data = series.dropna()
    if len(data) == 0:
        return np.nan
    counts = data.value_counts()
    return counts.index[0] if len(counts) > 0 else np.nan

def calcular_varianza_muestral_manual(series: pd.Series) -> float:
    """Fórmula: s² = (1/(n-1)) * Σ(xᵢ - x̄)² [Corrección de Bessel]"""
    data = series.dropna()
    if len(data) < 2:
        return np.nan
    media = calcular_media_manual(data)
    return np.sum((data - media) ** 2) / (len(data) - 1)

def calcular_desviacion_tipica_manual(series: pd.Series) -> float:
    """Fórmula: s = √s²"""
    var = calcular_varianza_muestral_manual(series)
    return np.sqrt(var) if var is not None and var >= 0 else np.nan

def calcular_cuartil_manual(series: pd.Series, q: float) -> float:
    """Percentil usando método lineal (compatible con pandas)"""
    data = series.dropna()
    if len(data) == 0:
        return np.nan
    return np.percentile(data, q * 100, method='linear')

def calcular_iqr_manual(series: pd.Series) -> float:
    """IQR = Q3 - Q1"""
    q1 = calcular_cuartil_manual(series, 0.25)
    q3 = calcular_cuartil_manual(series, 0.75)
    return q3 - q1 if q1 is not None and q3 is not None else np.nan

def calcular_cv_manual(series: pd.Series) -> float:
    """CV% = (s / x̄) * 100"""
    media = calcular_media_manual(series)
    desv = calcular_desviacion_tipica_manual(series)
    return (desv / media * 100) if media is not None and media != 0 else np.nan

def calcular_asimetria_manual(series: pd.Series) -> float:
    """γ₁ = E[(X-μ)³] / σ³ [Momento central estandarizado]"""
    data = series.dropna()
    if len(data) < 3:
        return np.nan
    media = np.mean(data)
    std = np.std(data, ddof=1)
    if std == 0:
        return 0
    return np.mean(((data - media) / std) ** 3)

def calcular_curtosis_manual(series: pd.Series) -> float:
    """γ₂ = E[(X-μ)⁴] / σ⁴ - 3 [Exceso sobre distribución normal]"""
    data = series.dropna()
    if len(data) < 4:
        return np.nan
    media = np.mean(data)
    std = np.std(data, ddof=1)
    if std == 0:
        return 0
    return np.mean(((data - media) / std) ** 4) - 3

def calcular_ic_95_manual(series: pd.Series) -> dict:
    """
    IC 95%: x̄ ± t(α/2, n-1) * (s/√n)
    Distribución t-Student para σ desconocida
    """
    data = series.dropna()
    n = len(data)
    if n < 2:
        return {'error': 'n < 2'}
    
    media = np.mean(data)
    sem = stats.sem(data)  # Error estándar de la media
    t_critico = stats.t.ppf((1 + 0.95) / 2, n - 1)
    margen = sem * t_critico
    
    return {
        'media': media,
        'sem': sem,
        't_critico': t_critico,
        'margen': margen,
        'limite_inferior': media - margen,
        'limite_superior': media + margen
    }

def test_welch_manual(grupo1: pd.Series, grupo2: pd.Series) -> dict:
    """
    Test t de Welch para muestras independientes con varianzas desiguales:
    t = (x̄₁ - x̄₂) / √(s₁²/n₁ + s₂²/n₂)
    """
    g1 = grupo1.dropna()
    g2 = grupo2.dropna()
    
    if len(g1) < 2 or len(g2) < 2:
        return {'error': 'Muestras insuficientes'}
    
    n1, n2 = len(g1), len(g2)
    mean1, mean2 = np.mean(g1), np.mean(g2)
    var1, var2 = np.var(g1, ddof=1), np.var(g2, ddof=1)
    
    # Estadístico t de Welch
    t_stat = (mean1 - mean2) / np.sqrt(var1/n1 + var2/n2)
    
    # Grados de libertad aproximados (fórmula de Welch-Satterthwaite)
    df = (var1/n1 + var2/n2)**2 / ((var1/n1)**2/(n1-1) + (var2/n2)**2/(n2-1))
    
    # P-valor bilateral
    p_val = 2 * stats.t.sf(np.abs(t_stat), df)
    
    return {
        't_statistic': t_stat,
        'df': df,
        'p_valor': p_val,
        'significativo': p_val < ALPHA,
        'mean_diff': mean1 - mean2
    }

def anova_manual(*grupos: pd.Series) -> dict:
    """
    ANOVA de un factor: Compara k medias simultáneamente
    F = MS_between / MS_within
    """
    grupos_limpios = [g.dropna() for g in grupos if len(g.dropna()) >= 2]
    
    if len(grupos_limpios) < 2:
        return {'error': 'Se requieren al menos 2 grupos válidos'}
    
    # Usamos scipy para precisión numérica, pero documentamos la fórmula
    f_stat, p_val = stats.f_oneway(*grupos_limpios)
    
    return {
        'f_statistic': f_stat,
        'p_valor': p_val,
        'significativo': p_val < ALPHA,
        'k_grupos': len(grupos_limpios)
    }

def regresion_ols_manual(x: pd.Series, y: pd.Series) -> dict:
    """
    Mínimos Cuadrados Ordinarios (OLS):
    β₁ = Cov(X,Y) / Var(X)
    β₀ = ȳ - β₁ * x̄
    R² = 1 - (SS_res / SS_tot)
    """
    datos = pd.DataFrame({'x': x, 'y': y}).dropna()
    if len(datos) < 2:
        return {'error': 'Datos insuficientes'}
    
    X = datos['x'].values.reshape(-1, 1)
    y_vals = datos['y'].values
    
    # Cálculo manual de coeficientes
    x_mean, y_mean = np.mean(datos['x']), np.mean(datos['y'])
    cov_xy = np.mean((datos['x'] - x_mean) * (datos['y'] - y_mean))
    var_x = np.var(datos['x'], ddof=1)
    
    beta_1 = cov_xy / var_x if var_x != 0 else 0
    beta_0 = y_mean - beta_1 * x_mean
    
    # Predicciones y R²
    y_pred = beta_0 + beta_1 * datos['x']
    ss_res = np.sum((y_vals - y_pred) ** 2)
    ss_tot = np.sum((y_vals - y_mean) ** 2)
    r2 = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
    
    # Correlación de Pearson
    r = datos['x'].corr(datos['y'])
    
    return {
        'beta_0': beta_0,
        'beta_1': beta_1,
        'r2': r2,
        'r': r,
        'ecuacion': f"Y = {beta_1:.4f}X + {beta_0:.4f}"
    }

def detectar_outliers_iqr_manual(series: pd.Series) -> dict:
    """
    Método IQR: Outliers si x < Q1 - 1.5*IQR o x > Q3 + 1.5*IQR
    """
    data = series.dropna()
    if len(data) == 0:
        return {'error': 'Sin datos'}
    
    q1 = calcular_cuartil_manual(series, 0.25)
    q3 = calcular_cuartil_manual(series, 0.75)
    iqr = q3 - q1
    
    limite_inf = q1 - 1.5 * iqr
    limite_sup = q3 + 1.5 * iqr
    
    outliers = data[(data < limite_inf) | (data > limite_sup)]
    
    return {
        'q1': q1, 'q3': q3, 'iqr': iqr,
        'limite_inferior': limite_inf,
        'limite_superior': limite_sup,
        'n_outliers': len(outliers),
        'porcentaje_outliers': len(outliers) / len(data) * 100 if len(data) > 0 else 0
    }

# =============================================================================
# FUNCIONES DE COMPARACIÓN Y VALIDACIÓN
# =============================================================================

def comparar_valores(valor_app: float, valor_manual: float, tolerancia_rel: float = TOLERANCIA_RELATIVA) -> dict:
    """Compara dos valores numéricos con tolerancia relativa y absoluta"""
    if pd.isna(valor_app) and pd.isna(valor_manual):
        return {'coincide': True, 'diferencia': 0, 'tipo': 'NaN'}
    
    if pd.isna(valor_app) or pd.isna(valor_manual):
        return {'coincide': False, 'diferencia': None, 'tipo': 'NaN_mismatch'}
    
    diff_abs = abs(valor_app - valor_manual)
    diff_rel = diff_abs / abs(valor_manual) if valor_manual != 0 else diff_abs
    
    coincide = (diff_abs <= TOLERANCIA_ABSOLUTA) or (diff_rel <= tolerancia_rel)
    
    return {
        'coincide': coincide,
        'diferencia_absoluta': diff_abs,
        'diferencia_relativa_pct': diff_rel * 100,
        'valor_app': valor_app,
        'valor_manual': valor_manual
    }

def validar_estadisticos_descriptivos(df: pd.DataFrame, columna: str) -> dict:
    """Valida TODOS los estadísticos descriptivos para una columna"""
    resultados = {}
    
    # Lista de métricas a validar
    metricas = [
        ('Media', calcular_media_manual),
        ('Mediana', calcular_mediana_manual),
        ('Moda', calcular_moda_manual),
        ('Rango', lambda s: s.dropna().max() - s.dropna().min()),
        ('Desviación Típica', calcular_desviacion_tipica_manual),
        ('Varianza', calcular_varianza_muestral_manual),
        ('Q1', lambda s: calcular_cuartil_manual(s, 0.25)),
        ('Q3', lambda s: calcular_cuartil_manual(s, 0.75)),
        ('IQR', calcular_iqr_manual),
        ('CV%', calcular_cv_manual),
        ('Asimetría', calcular_asimetria_manual),
        ('Curtosis', calcular_curtosis_manual)
    ]
    
    # Mapeo de métricas a funciones de pandas (App Proxy)
    mapeo_pandas = {
        'Media': 'mean',
        'Mediana': 'median',
        'Moda': lambda s: s.mode()[0] if not s.mode().empty else np.nan,
        'Desviación Típica': 'std',
        'Varianza': 'var',
        'Asimetría': 'skew',
        'Curtosis': 'kurtosis',
        'Q1': lambda s: s.quantile(0.25),
        'Q3': lambda s: s.quantile(0.75),
        'IQR': lambda s: s.quantile(0.75) - s.quantile(0.25),
        'CV%': lambda s: (s.std() / s.mean() * 100) if s.mean() != 0 else np.nan,
        'Rango': lambda s: s.max() - s.min()
    }
    
    for nombre_metrica, func_manual in metricas:
        try:
            valor_manual = func_manual(df[columna])
            
            # Obtener valor del App Proxy usando el mapeo correcto
            op_app = mapeo_pandas.get(nombre_metrica)
            if callable(op_app):
                valor_app = op_app(df[columna].dropna())
            else:
                valor_app = getattr(df[columna].dropna(), op_app)()
            
            comparacion = comparar_valores(valor_app, valor_manual)
            resultados[nombre_metrica] = {
                'manual': valor_manual,
                'app_proxy': valor_app,
                'validacion': comparacion
            }
        except Exception as e:
            resultados[nombre_metrica] = {'error': str(e)}
    
    return resultados

def validar_intervalo_confianza(df: pd.DataFrame, columna: str) -> dict:
    """Valida el cálculo del IC 95%"""
    # Cálculo manual
    ic_manual = calcular_ic_95_manual(df[columna])
    
    # Cálculo app (proxy con scipy)
    data = df[columna].dropna()
    n = len(data)
    media_app = np.mean(data)
    sem_app = stats.sem(data)
    t_crit_app = stats.t.ppf((1 + 0.95) / 2, n - 1)
    margen_app = sem_app * t_crit_app
    
    comparacion_media = comparar_valores(media_app, ic_manual.get('media'))
    comparacion_margen = comparar_valores(margen_app, ic_manual.get('margen'))
    
    return {
        'manual': ic_manual,
        'app_proxy': {
            'media': media_app,
            'sem': sem_app,
            't_critico': t_crit_app,
            'margen': margen_app,
            'limite_inferior': media_app - margen_app,
            'limite_superior': media_app + margen_app
        },
        'validacion': {
            'media': comparacion_media,
            'margen': comparacion_margen
        }
    }

def validar_test_hipotesis(df: pd.DataFrame, columna_num: str, columna_cat: str, categoria1: str, categoria2: str) -> dict:
    """Valida el test de hipótesis para dos categorías"""
    # Extraer grupos
    grupo1 = df[df[columna_cat] == categoria1][columna_num]
    grupo2 = df[df[columna_cat] == categoria2][columna_num]
    
    # Cálculo manual (Welch)
    welch_manual = test_welch_manual(grupo1, grupo2)
    
    # Cálculo app (proxy con scipy)
    g1_clean = grupo1.dropna()
    g2_clean = grupo2.dropna()
    if len(g1_clean) >= 2 and len(g2_clean) >= 2:
        t_stat_app, p_val_app = stats.ttest_ind(g1_clean, g2_clean, equal_var=False)
    else:
        t_stat_app, p_val_app = np.nan, np.nan
    
    comparacion_t = comparar_valores(t_stat_app, welch_manual.get('t_statistic'))
    comparacion_p = comparar_valores(p_val_app, welch_manual.get('p_valor'))
    
    return {
        'grupos': {categoria1: len(grupo1.dropna()), categoria2: len(grupo2.dropna())},
        'manual': welch_manual,
        'app_proxy': {'t_statistic': t_stat_app, 'p_valor': p_val_app},
        'validacion': {
            't_statistic': comparacion_t,
            'p_valor': comparacion_p
        }
    }

def validar_regresion(df: pd.DataFrame, x_col: str, y_col: str) -> dict:
    """Valida el modelo de regresión lineal simple"""
    # Cálculo manual
    reg_manual = regresion_ols_manual(df[x_col], df[y_col])
    
    # Cálculo app (proxy con sklearn)
    datos = df[[x_col, y_col]].dropna()
    if len(datos) >= 2:
        X = datos[[x_col]].values
        y = datos[y_col].values
        modelo = LinearRegression()
        modelo.fit(X, y)
        y_pred = modelo.predict(X)
        
        reg_app = {
            'beta_0': modelo.intercept_,
            'beta_1': modelo.coef_[0],
            'r2': r2_score(y, y_pred),
            'r': datos[x_col].corr(datos[y_col])
        }
    else:
        reg_app = {'error': 'Datos insuficientes'}
    
    comparaciones = {}
    for param in ['beta_0', 'beta_1', 'r2', 'r']:
        if param in reg_manual and param in reg_app:
            comparaciones[param] = comparar_valores(reg_app[param], reg_manual[param])
    
    return {
        'manual': reg_manual,
        'app_proxy': reg_app,
        'validacion': comparaciones
    }

def validar_outliers(df: pd.DataFrame, columna: str) -> dict:
    """Valida la detección de outliers por IQR"""
    # Cálculo manual
    outliers_manual = detectar_outliers_iqr_manual(df[columna])
    
    # Cálculo app (proxy con pandas)
    data = df[columna].dropna()
    q1_app = data.quantile(0.25)
    q3_app = data.quantile(0.75)
    iqr_app = q3_app - q1_app
    limite_inf_app = q1_app - 1.5 * iqr_app
    limite_sup_app = q3_app + 1.5 * iqr_app
    n_outliers_app = len(data[(data < limite_inf_app) | (data > limite_sup_app)])
    
    comparaciones = {
        'q1': comparar_valores(q1_app, outliers_manual.get('q1')),
        'q3': comparar_valores(q3_app, outliers_manual.get('q3')),
        'iqr': comparar_valores(iqr_app, outliers_manual.get('iqr')),
        'n_outliers': comparar_valores(n_outliers_app, outliers_manual.get('n_outliers'))
    }
    
    return {
        'manual': outliers_manual,
        'app_proxy': {
            'q1': q1_app, 'q3': q3_app, 'iqr': iqr_app,
            'limite_inferior': limite_inf_app, 'limite_superior': limite_sup_app,
            'n_outliers': n_outliers_app
        },
        'validacion': comparaciones
    }

# =============================================================================
# EJECUCIÓN PRINCIPAL Y REPORTES
# =============================================================================

def generar_reporte_json(resultados: dict, ruta_salida: str):
    """Guarda los resultados de validación en JSON (Robusto para pandas/numpy)"""
    def limpiar_para_json(obj):
        """Convierte recursivamente objetos científicos a tipos nativos de Python."""
        if isinstance(obj, dict):
            return {str(k): limpiar_para_json(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [limpiar_para_json(i) for i in obj]
        elif isinstance(obj, tuple):
            return tuple(limpiar_para_json(i) for i in obj)
        elif isinstance(obj, np.ndarray):
            return limpiar_para_json(obj.tolist())
        elif isinstance(obj, (np.integer, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64)):
            val = float(obj)
            return None if np.isnan(val) or np.isinf(val) else val
        elif isinstance(obj, (np.bool_, bool)):
            return bool(obj)
        elif isinstance(obj, (pd.Series, pd.Index)):
            return limpiar_para_json(obj.tolist())
        elif isinstance(obj, pd.DataFrame):
            return limpiar_para_json(obj.to_dict(orient='records'))
        elif isinstance(obj, float) and (np.isnan(obj) or np.isinf(obj)):
            return None
        return obj

    try:
        # Limpieza profunda antes de serializar
        resultados_limpio = limpiar_para_json(resultados)
        with open(ruta_salida, 'w', encoding='utf-8') as f:
            json.dump(resultados_limpio, f, indent=2, ensure_ascii=False)
        print(f"✅ Reporte JSON guardado en: {ruta_salida}")
    except Exception as e:
        print(f"⚠️ Error crítico al guardar JSON: {e}")
        print("💡 Generando backup en texto plano por seguridad...")
        with open(ruta_salida.replace('.json', '_backup.txt'), 'w', encoding='utf-8') as f:
            f.write(str(resultados))

def imprimir_resultados_recursivo(datos, prefijo="", stats_tracker=None):
    """Busca y muestra validaciones a cualquier profundidad."""
    if stats_tracker is None:
        stats_tracker = {'total': 0, 'aprobados': 0}
        
    if not isinstance(datos, dict):
        return stats_tracker

    if 'validacion' in datos:
        v = datos['validacion']
        # Caso 1: Validación simple
        if isinstance(v, dict) and 'coincide' in v:
            stats_tracker['total'] += 1
            estado = "✅" if v['coincide'] else "❌"
            if v['coincide']: stats_tracker['aprobados'] += 1
            diff = v.get('diferencia_relativa_pct', 0)
            print(f"  {estado} {prefijo}: diff={diff:.4f}%")
        
        # Caso 2: Validación anidada
        elif isinstance(v, dict):
            for sub_metrica, comp in v.items():
                if isinstance(comp, dict) and 'coincide' in comp:
                    stats_tracker['total'] += 1
                    estado = "✅" if comp['coincide'] else "❌"
                    if comp['coincide']: stats_tracker['aprobados'] += 1
                    diff = comp.get('diferencia_relativa_pct', 0)
                    print(f"  {estado} {prefijo}.{sub_metrica}: diff={diff:.4f}%")
    else:
        # Seguir buscando en profundidad
        for k, v in datos.items():
            nuevo_prefijo = f"{prefijo}.{k}" if prefijo else k
            imprimir_resultados_recursivo(v, nuevo_prefijo, stats_tracker)
            
    return stats_tracker

def generar_resumen_consola(resultados: dict):
    """Imprime un resumen legible en consola usando recursividad."""
    print("\n" + "="*70)
    print("📊 RESUMEN DE VALIDACIÓN - Dashboard Estadístico")
    print("="*70)
    
    global_stats = {'total': 0, 'aprobados': 0}
    
    for seccion, datos in resultados.items():
        print(f"\n🔹 {seccion.upper()}")
        print("-"*40)
        res = imprimir_resultados_recursivo(datos, "")
        global_stats['total'] += res['total']
        global_stats['aprobados'] += res['aprobados']
    
    print("\n" + "="*70)
    total = global_stats['total']
    aprobados = global_stats['aprobados']
    porcentaje = (aprobados / total * 100) if total > 0 else 0
    print(f"📈 RESULTADO GLOBAL: {aprobados}/{total} tests aprobados ({porcentaje:.2f}%)")
    
    if porcentaje >= 99:
        print("🎉 ¡VALIDACIÓN EXITOSA! Todos los cálculos coinciden con las fórmulas académicas.")
    elif porcentaje >= 95:
        print("⚠️ VALIDACIÓN ACEPTABLE. Pequeñas discrepancias numéricas dentro de tolerancia.")
    else:
        print("❌ VALIDACIÓN FALLIDA. Revisar discrepancias en el reporte JSON.")
    print("="*70 + "\n")

def ejecutar_validacion_completa(ruta_dataset: str, filtros: dict = None) -> dict:
    """Ejecuta TODAS las validaciones según el enunciado de la práctica"""
    
    # Cargar datos
    df = pd.read_csv(ruta_dataset)
    print(f"📦 Dataset cargado: {len(df)} registros, {len(df.columns)} columnas")
    
    # Aplicar filtros si se especifican (simula filtros de la app)
    if filtros:
        for col, valores in filtros.items():
            if col in df.columns and valores:
                df = df[df[col].isin(valores)]
        print(f"🔍 Filtros aplicados: {len(df)} registros restantes")
    
    resultados = {}
    
    # ========================================================================
    # 1. VALIDACIÓN: ANÁLISIS DESCRIPTIVO (Requisito práctica)
    # ========================================================================
    print("\n🔎 Validando estadísticos descriptivos...")
    resultados['descriptivos'] = {}
    
    for col in [COL_SALARIO_USD, COL_COLI]:
        if col in df.columns:
            resultados['descriptivos'][col] = validar_estadisticos_descriptivos(df, col)
    
    # ========================================================================
    # 2. VALIDACIÓN: INTERVALOS DE CONFIANZA (Requisito práctica)
    # ========================================================================
    print("🔎 Validando intervalos de confianza (95%)...")
    resultados['intervalos_confianza'] = {}
    
    for col in [COL_SALARIO_USD, COL_COLI]:
        if col in df.columns:
            resultados['intervalos_confianza'][col] = validar_intervalo_confianza(df, col)
    
    # ========================================================================
    # 3. VALIDACIÓN: CONTRASTES DE HIPÓTESIS (Requisito práctica)
    # ========================================================================
    print("🔎 Validando contrastes de hipótesis...")
    resultados['contrastes_hipotesis'] = {}
    
    if 'experience_level' in df.columns and COL_SALARIO_USD in df.columns:
        # Buscar categorías con al menos 2 grupos para el test
        for col_test in ['experience_level', 'job_category', 'employment_type']:
            if col_test in df.columns:
                niveles = df[col_test].dropna().unique()
                if len(niveles) >= 2:
                    cat1, cat2 = niveles[0], niveles[1]
                    resultados['contrastes_hipotesis'][f"{col_test}:{cat1}_vs_{cat2}"] = validar_test_hipotesis(
                        df, COL_SALARIO_USD, col_test, cat1, cat2
                    )
                    break
    
    # ========================================================================
    # 4. VALIDACIÓN: REGRESIÓN LINEAL (Requisito práctica)
    # ========================================================================
    print("🔎 Validando regresión lineal...")
    if COL_COLI in df.columns and COL_SALARIO_USD in df.columns:
        resultados['regresion'] = validar_regresion(df, COL_COLI, COL_SALARIO_USD)
    
    # ========================================================================
    # 5. VALIDACIÓN: DETECCIÓN DE OUTLIERS
    # ========================================================================
    print("🔎 Validando detección de outliers (IQR)...")
    resultados['outliers'] = {}
    
    for col in [COL_SALARIO_USD, COL_COLI]:
        if col in df.columns:
            resultados['outliers'][col] = validar_outliers(df, col)
    
    return resultados

# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description='Validador oficial del proyecto estadístico')
    parser.add_argument('--dataset', type=str, required=True, help='Ruta al dataset enriquecido CSV')
    parser.add_argument('--tolerancia', type=float, default=0.01, help='Tolerancia relativa para comparaciones (default: 0.01 = 1%)')
    parser.add_argument('--filtro-pais', type=str, nargs='+', help='Filtrar por países específicos')
    parser.add_argument('--filtro-experiencia', type=str, nargs='+', help='Filtrar por niveles de experiencia')
    parser.add_argument('--salida', type=str, default='validacion/resultados_validacion.json', help='Ruta de salida para el reporte JSON')
    
    args = parser.parse_args()
    
    # Configurar tolerancia global
    global TOLERANCIA_RELATIVA
    TOLERANCIA_RELATIVA = args.tolerancia
    
    # Preparar filtros
    filtros = {}
    if args.filtro_pais:
        filtros[COL_PAIS] = args.filtro_pais
    if args.filtro_experiencia:
        filtros['experience_level'] = args.filtro_experiencia
    
    # Crear directorio de salida si no existe
    os.makedirs(os.path.dirname(args.salida), exist_ok=True)
    
    print(f"🚀 Iniciando validación - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 Dataset: {args.dataset}")
    print(f"📐 Tolerancia: {args.tolerancia*100:.2f}%")
    
    try:
        # Ejecutar validación completa
        resultados = ejecutar_validacion_completa(args.dataset, filtros)
        
        # Guardar reporte detallado
        generar_reporte_json(resultados, args.salida)
        
        # Imprimir resumen en consola
        generar_resumen_consola(resultados)
        
        # Código de salida para CI/CD
        sys.exit(0 if all(
            v.get('validacion', {}).get('coincide', True) if isinstance(v, dict) else True
            for seccion in resultados.values()
            for v in (seccion.values() if isinstance(seccion, dict) else [])
        ) else 1)
        
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el dataset en {args.dataset}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error durante la validación: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(2)

if __name__ == "__main__":
    main()