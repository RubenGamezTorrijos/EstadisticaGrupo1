"""
PROYECTO: Estadística para Ingeniería
ANÁLISIS DE REGRESIÓN LINEAL
COORDINADOR: RUBEN GAMEZ TORRIJOS
ROL ASIGNADO (Lógica de Modelado): Leslie Ross Aranibar Pozo
ESTADO: COMPLETADO (Integrado v.2.5.3)
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

def ejecutar_regresion_simple(df, x_col, y_col):
    """
    MODULO: Regresión Lineal
    ROL ASIGNADO: Leslie Ross Aranibar Pozo
    Implementación Senior usando Scikit-Learn.
    """
    try:
        # Preparación de datos (Eliminación de nulos)
        datos = df[[x_col, y_col]].dropna()
        if len(datos) < 2:
            return None

        X = datos[[x_col]].values
        y = datos[y_col].values

        # Entrenamiento del modelo
        modelo = LinearRegression()
        modelo.fit(X, y)

        # Predicción y cálculo de métricas
        y_pred = modelo.predict(X)
        r2 = r2_score(y, y_pred)
        pendiente = modelo.coef_[0]
        intercepto = modelo.intercept_

        # Interpretación lógica del coeficiente
        if pendiente > 0:
            interpretacion = f"Relación POSITIVA: Por cada unidad que aumenta el {x_col}, el {y_col} tiende a subir en {pendiente:.2f} unidades."
        elif pendiente < 0:
            interpretacion = f"Relación NEGATIVA: Existe una tendencia inversa entre el {x_col} y el {y_col}."
        else:
            interpretacion = "No se observa una relación lineal significativa entre las variables."

        # Retornamos el diccionario esperado por la vista (layout.py)
        return {
            'r2': r2,
            'coeficiente': pendiente,
            'intercepto': intercepto,
            'interpretacion': interpretacion,
            'modelo': modelo,
            'Estado': 'COMPLETADO'
        }
    
    except Exception as e:
        print(f"Error al ejecutar regresión: {e}")
        return None
