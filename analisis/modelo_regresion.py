"""
PROYECTO: Estadística para Ingeniería
ANÁLISIS DE REGRESIÓN LINEAL
COORDINADOR: RUBEN GAMEZ TORRIJOS
ROL ASIGNADO (Lógica de Modelado): Leslie Ross Aranibar Pozo
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# =================================================================
# SECCIÓN: MODELADO MATEMÁTICO (RESPONSABLE: LESLIE ROSS)
# =================================================================

def ejecutar_regresion_simple(df, x_col, y_col):
    """Ejecuta un modelo de regresión lineal simple y devuelve métricas."""
    if df.empty or len(df) < 2:
        return {'Coeficiente R2': "0.0", 'Pendiente': "0.0", 'Intercepto': "0.0", 'Conclusion': "Datos insuficientes"}, None
        
    X = df[[x_col]].values
    y = df[y_col].values
    
    modelo = LinearRegression()
    modelo.fit(X, y)
    
    r2 = r2_score(y, modelo.predict(X))
    slope = modelo.coef_[0]
    intercept = modelo.intercept_
    
    resumen = {
        'Coeficiente R2': f"{r2:.4f}",
        'Pendiente': f"{slope:.2f}",
        'Intercepto': f"{intercept:,.2f}",
        'Conclusion': "Modelo ajustado correctamente."
    }
    
    return resumen, modelo
