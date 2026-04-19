import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

def ejecutar_regresion_simple(df, x_col, y_col):
    """
    MODULO: Análisis de Regresión
    ROL ASIGNADO: Leslie Ross Aranibar Pozo
    
    TODO: Implementar ajuste del modelo, obtención de coeficientes y R2.
    El dataframe ya viene filtrado y con la divisa correcta.
    """
    # Preparar datos
    X = df[[x_col]].values
    y = df[y_col].values
    
    # Plantilla de modelo
    # TODO: Leslie debe implementar el ajuste aquí
    modelo = LinearRegression()
    modelo.fit(X, y)
    
    # Extraer métricas
    y_pred = modelo.predict(X)
    r2 = r2_score(y, y_pred)
    pendiente = modelo.coef_[0]
    intercepto = modelo.intercept_
    
    resumen = {
        'Coeficiente R2': f"{r2:.4f} [Leslie: Pendiente Validar]",
        'Pendiente': f"{pendiente:.2f}",
        'Intercepto': f"{intercepto:.2f}",
        'Conclusion': "Plantilla cargada. Leslie debe redactar conclusión técnica."
    }
    
    return resumen, modelo
