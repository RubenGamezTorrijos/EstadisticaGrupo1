"""
PROYECTO: Estadística para Ingeniería
ESTRUCTURA MÓDULO: RUBEN GAMEZ TORRIJOS (Coordinador)

Este archivo centraliza las importaciones del paquete de análisis
para facilitar su uso en la aplicación principal (app.py).
"""

# Estadísticos (Responsable: Rafael / Rubén)
from .estadisticos import (
    calcular_estadisticos, 
    calcular_estadisticos_por_categoria,
    detectar_outliers_iqr
)

# Gráficos (Responsable: Leslie Ross)
from .graficos import (
    crear_histograma, 
    crear_boxplot, 
    crear_bar_chart,
    crear_scatter_regresion,
    sanitize_pdf_text,
    guardar_grafico
)

# Inferencia (Responsable: Bryann Vallejo)
from .inferencial import (
    calcular_intervalos_confianza, 
    contraste_hipotesis, 
    verificar_supuestos,
    realizar_test_hipotesis
)

# Regresión (Responsable: Leslie Ross)
from .modelo_regresion import ejecutar_regresion_simple
