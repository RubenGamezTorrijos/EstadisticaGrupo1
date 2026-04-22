"""
views/sidebar.py
================
Componente de la interfaz para los filtros laterales.
"""

import streamlit as st

def render_sidebar(df):
    """Renderiza los filtros en el sidebar y devuelve los valores seleccionados."""
    st.sidebar.header("Filtros de Análisis")
    
    # Filtro de Año
    available_years = sorted(df['work_year'].unique().tolist())
    selected_years = st.sidebar.multiselect(
        "Seleccionar Años",
        options=available_years,
        default=available_years
    )
    
    # Filtro de Experiencia
    exp_levels = sorted(df['experience_level'].unique().tolist())
    selected_exp = st.sidebar.multiselect(
        "Nivel de Experiencia",
        options=exp_levels,
        default=exp_levels
    )
    
    # Filtro de Moneda (opcional)
    st.sidebar.divider()
    st.sidebar.info("Nota: Los salarios se muestran ajustados por el Índice de Coste de Vida (COLI).")
    
    return {
        "years": selected_years,
        "experience": selected_exp
    }
