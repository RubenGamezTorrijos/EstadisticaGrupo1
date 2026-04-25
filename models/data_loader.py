import streamlit as st
import pandas as pd
import os
import config.settings as cfg
from config.api_client import get_latest_coli_data

# Fallback para evitar errores NameError si la importación falla o el nombre no está definido globalmente
COL_CURRENCY = getattr(cfg, 'COL_CURRENCY', 'currency')

@st.cache_data(ttl=3600)
def load_processed_data() -> pd.DataFrame:
    """
    Carga, limpia y enriquece el dataset. 
    Aplica caché de Streamlit para optimizar el rendimiento.
    """
    try:
        # 1. Intentar cargar el dataset ya procesado para velocidad
        if os.path.exists(cfg.ENRIQUECIDO_CSV):
            df = pd.read_csv(cfg.ENRIQUECIDO_CSV)
            # Adaptar archivos antiguos al nuevo esquema
            mapping = {
                'salary_in_usd': cfg.COL_SALARIO_USD,
                'salary_in_eur': cfg.COL_SALARIO_EUR,
                'salary_currency': COL_CURRENCY
            }
            renamed = False
            for old, new in mapping.items():
                if old in df.columns and new not in df.columns:
                    df = df.rename(columns={old: new})
                    renamed = True
            
            if renamed:
                df.to_csv(cfg.ENRIQUECIDO_CSV, index=False)
            
            # Si aún falta alguna columna vital, forzar reconstrucción
            if cfg.COL_SALARIO_EUR in df.columns:
                return df
        
        # 2. Si no existe, construirlo desde cero
        if not os.path.exists(cfg.JOBS_CSV):
            st.error(f"Archivo base no encontrado: {cfg.JOBS_CSV}")
            return pd.DataFrame()

        df = pd.read_csv(cfg.JOBS_CSV)
        
        # --- Limpieza y Renombrado Senior ---
        df = df.rename(columns={
            'salary_currency': COL_CURRENCY,
            'salary_in_usd': cfg.COL_SALARIO_USD
        })
        
        df = df.drop_duplicates()
        df = df.dropna(subset=[cfg.COL_SALARIO_USD, 'experience_level', 'job_category'])
        
        # --- Enriquecimiento Multidivisa ---
        df[cfg.COL_SALARIO_EUR] = (df[cfg.COL_SALARIO_USD] * cfg.EUR_USD_RATE).round(2)
        
        # --- Integración de Coste de Vida (COLI) ---
        df_coli = get_latest_coli_data()
        
        # Si la API falla, intentar cargar desde el CSV local
        if df_coli is None or df_coli.empty:
            if os.path.exists(cfg.COLI_CSV):
                df_coli = pd.read_csv(cfg.COLI_CSV)
                st.info("Utilizando datos locales de COLI (Respaldo).")
            else:
                st.warning("Archivo COLI no encontrado. Usando valores por defecto.")
                df['cost_of_living_index'] = 70.0 # Valor neutral
        
        # Si tenemos datos (de API o de CSV), realizar el merge
        if df_coli is not None and not df_coli.empty:
            df = pd.merge(df, df_coli[['country', 'cost_of_living_index']], 
                         left_on=cfg.COL_PAIS, right_on='country', how='left')
            
            if 'country' in df.columns:
                df.drop(columns=['country'], inplace=True)
            
            # Rellenar países faltantes con la media global (Senior Strategy)
            media_coli = df['cost_of_living_index'].mean()
            df['cost_of_living_index'] = df['cost_of_living_index'].fillna(media_coli)
            
        # --- Cálculo de Salario Ajustado (Poder Adquisitivo) ---
        df[cfg.COL_SALARIO_AJUSTADO] = (df[cfg.COL_SALARIO_USD] / df['cost_of_living_index'] * 100).round(2)
        
        # Guardar para la próxima sesión
        df.to_csv(cfg.ENRIQUECIDO_CSV, index=False)
        return df

    except Exception as e:
        st.error(f"Error crítico en la carga de datos: {str(e)}")
        return pd.DataFrame()

def filter_data(df: pd.DataFrame, experience=None, categories=None, countries=None) -> pd.DataFrame:
    """Filtro unificado de alta performance."""
    df_filtered = df.copy()
    
    if experience:
        df_filtered = df_filtered[df_filtered['experience_level'].isin(experience)]
    if categories:
        df_filtered = df_filtered[df_filtered['job_category'].isin(categories)]
    if countries:
        df_filtered = df_filtered[df_filtered[cfg.COL_PAIS].isin(countries)]
        
    return df_filtered
