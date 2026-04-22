"""
models/data_loader.py
=====================
Módulo encargado de la carga y preparación del dataset enriquecido.
Este archivo es territorio de RAFAEL.
"""

import pandas as pd
import os
import sys
from config.settings import JOBS_CSV, COLI_CSV, ENRIQUECIDO_CSV, COL_PAIS, COL_SALARIO_USD, COL_COLI, COL_SALARIO_AJUSTADO

def load_processed_data() -> pd.DataFrame:
    """
    Carga el dataset enriquecido. Si no existe, intenta generarlo
    combinando jobs_in_data.csv con el índice de coste de vida.
    """
    if os.path.exists(ENRIQUECIDO_CSV):
        return pd.read_csv(ENRIQUECIDO_CSV)
    
    # Si no existe, realizar el proceso de unión básico
    print("[!] Dataset enriquecido no encontrado. Generando automáticamente...")
    
    if not os.path.exists(JOBS_CSV) or not os.path.exists(COLI_CSV):
        print(f"ERROR: Faltan archivos base en {DATOS_DIR}")
        return pd.DataFrame()

    df_jobs = pd.read_csv(JOBS_CSV)
    df_coli = pd.read_csv(COLI_CSV)
    
    # Merge por país
    df_merged = pd.merge(df_jobs, df_coli[['country', 'cost_of_living_index']], 
                         left_on=COL_PAIS, right_on='country', how='left')
    
    # Limpieza: Eliminar columna duplicada de país si existe
    if 'country' in df_merged.columns:
        df_merged.drop(columns=['country'], inplace=True)
    
    # Cálculo de salario ajustado
    df_merged[COL_SALARIO_AJUSTADO] = (df_merged[COL_SALARIO_USD] / df_merged[COL_COLI]) * 100
    
    # Guardar para futuros usos
    df_merged.to_csv(ENRIQUECIDO_CSV, index=False)
    return df_merged

def filter_by_year(df: pd.DataFrame, years: list) -> pd.DataFrame:
    """Filtra el dataframe por una lista de años."""
    if not years:
        return df
    return df[df['work_year'].isin(years)]
