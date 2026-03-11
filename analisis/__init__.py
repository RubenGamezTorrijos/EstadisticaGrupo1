"""
PROYECTO: Estadística para Ingeniería
ESTRUCTURA MÓDULO: RUBEN GAMEZ TORRIJOS (Desarrollador y Coordinador)
Inicializador del paquete de análisis.
"""
from .estadisticos import limpiar_datos, calcular_estadisticos
from .graficos import crear_histograma, crear_boxplot, crear_scatter_regresion, crear_bar_chart
from .inferencial import calcular_ic_95, contraste_hipotesis
