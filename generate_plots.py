"""
PROYECTO: Estadística para Ingeniería
ARQUITECTURA Y ESTRUCTURA: RUBEN GAMEZ TORRIJOS (Desarrollador y Coordinador)
IMPLEMENTACIÓN GRÁFICA: LESLIE ROSS (Analista Descriptivo)
App Streamlit para generar todos los gráficos del análisis descriptivo y exportarlos.
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import pandas as pd
from analisis.graficos import (
    crear_histograma,
    crear_boxplot_por_categoria,
    crear_grafico_barras_top_causas,
    crear_grafico_comparacion_sexo,
    crear_grafico_dispersion_regresion,
    crear_grafico_barras_nacionalidad,
)

def generar_todos_los_graficos():
    df = pd.read_csv("datos/dataset_limpio.csv")
    
    os.makedirs("outputs/graficos", exist_ok=True)
    print("Generando gráficos...")

    # 1. Histograma: Defunciones totales
    crear_histograma(df, "Total",
                     "outputs/graficos/01_hist_defunciones.png",
                     "Distribución del Total de Defunciones por Causa")

    # 2. Histograma: Porcentaje de defunciones extranjeras
    crear_histograma(df[df["Porcentaje_extranjera"].notna()], "Porcentaje_extranjera",
                     "outputs/graficos/02_hist_pct_extranjera.png",
                     "Distribución del % de Defunciones Extranjeras")

    # 3. Boxplot: Total de defunciones por Sexo
    crear_boxplot_por_categoria(df[df["Sexo"].isin(["Hombres", "Mujeres"])],
                                "Total", "Sexo",
                                "outputs/graficos/03_box_defunciones_sexo.png",
                                "Defunciones Totales por Sexo")

    # 4. Boxplot: % Extranjera por Sexo
    crear_boxplot_por_categoria(
        df[df["Sexo"].isin(["Hombres", "Mujeres"]) & df["Porcentaje_extranjera"].notna()],
        "Porcentaje_extranjera", "Sexo",
        "outputs/graficos/04_box_pct_extranjera_sexo.png",
        "% Defunciones Extranjeras por Sexo")

    # 5. Top 15 causas de muerte
    crear_grafico_barras_top_causas(df, 15,
                                    "outputs/graficos/05_top15_causas.png",
                                    "Top 15 Causas de Muerte en España")

    # 6. Comparación Hombres vs Mujeres en Top 12 causas
    crear_grafico_comparacion_sexo(df,
                                   "outputs/graficos/06_comparacion_sexo.png",
                                   "Comparativa de Defunciones por Causa y Sexo")

    # 7. Dispersión: Total vs Num_paises_afectados
    crear_grafico_dispersion_regresion(df, "Total", "Num_paises_afectados",
                                       "outputs/graficos/07_dispersion_regresion.png",
                                       "Relación: Defunciones Totales vs Nº Países Afectados")

    # 8. Defunciones por grupo de nacionalidad
    crear_grafico_barras_nacionalidad(df,
                                      "outputs/graficos/08_barras_nacionalidad.png",
                                      "Defunciones por Grupo de Nacionalidad")

    print("¡Todos los gráficos generados correctamente en outputs/graficos/!")

if __name__ == "__main__":
    generar_todos_los_graficos()
