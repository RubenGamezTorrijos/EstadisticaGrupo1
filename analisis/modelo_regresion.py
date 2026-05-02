"""
PROYECTO: Estadística para Ingeniería
ANÁLISIS DE REGRESIÓN LINEAL
COORDINADOR: RUBEN GAMEZ TORRIJOS
ROL ASIGNADO (Lógica de Modelado): Leslie Ross Aranibar Pozo
ESTADO: PENDIENTE (Rama DEV)
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# =================================================================
# SECCIÓN: MODELADO MATEMÁTICO (RESPONSABLE: LESLIE ROSS)
# =================================================================

def ejecutar_regresion_simple(df, x_col, y_col):
    """
    MODULO: Regresión Lineal
    ROL ASIGNADO: Leslie Ross Aranibar Pozo
    
    # 💡 PISTA DE IMPLEMENTACIÓN:
    # 1. Definir X e y a partir de las columnas
    # 2. Ajustar LinearRegression()
    # 3. Calcular R2, Slope e Intercept
    # 4. Retornar resumen y modelo (o None si falla)
    """
    
    try:
        datos = df[[x_col, y_col]].dropna()

        X = datos[[x_col]]
        y = datos[y_col]

        modelo = LinearRegression()
        modelo.fit(X, y)

        y_pred = modelo.predict(X)

        r2 = r2_score(y, y_pred)
        pendiente = modelo.coef_[0]
        intercepto = modelo.intercept_

        resumen = {
            'Coeficiente R2': f"{r2:.4f}",
            'Pendiente': f"{pendiente:.2f}",
            'Intercepto': f"{intercepto:.2f}",
            'Conclusion': "Modelo de regresión calculado correctamente",
            'Estado': 'COMPLETADO'
        }
        return resumen, modelo
    
    except Exception as e:
        print(f"Error al ejecutar regresión: {e}")
        resumen = {
            'Coeficiente R2': "0.0000",
            'Pendiente': "0.00",
            'Intercepto': "0.00",
            'Conclusion': "No se pudo calcular la regresión con los datos indicados",
            'Estado': 'ERROR'
            }
        return resumen, None
