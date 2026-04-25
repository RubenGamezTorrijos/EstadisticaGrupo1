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
    crear_violin_plot, 
    crear_bar_chart,
    crear_grafico_comparativo_ic,
    crear_scatter_regresion,
    sanitize_pdf_text,
    obtener_label,
    guardar_grafico
)

# Inferencia (Responsable: Bryann Vallejo)
from .inferencial import (
    calcular_ic_95, 
    contraste_hipotesis, 
    verificar_supuestos
)

# Regresión (Responsable: Leslie Ross)
from .regresion import ejecutar_regresion_simple
