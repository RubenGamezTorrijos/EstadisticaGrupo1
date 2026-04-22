"""
controllers/app_controller.py
============================
Controlador principal que gestiona la navegación y el flujo de datos.
Este archivo es territorio de RUBÉN (Arquitecto).
"""

import streamlit as st
from models.data_loader import load_processed_data, filter_by_year
from views.sidebar import render_sidebar
from views.styles import apply_styles

class AppController:
    def __init__(self):
        self.df_full = None
        self.df_filtered = None

    def run(self):
        """Inicia la ejecución de la aplicación."""
        # 1. Aplicar estilos
        apply_styles()
        
        # 2. Cargar datos (Model)
        self.df_full = load_processed_data()
        
        if self.df_full.empty:
            st.error("No se han podido cargar los datos.")
            return

        # 3. Renderizar Sidebar y obtener filtros (View)
        filters = render_sidebar(self.df_full)
        
        # 4. Aplicar filtros (Model Logic)
        self.df_filtered = self.df_full.copy()
        self.df_filtered = filter_by_year(self.df_filtered, filters['years'])
        
        if filters['experience']:
            self.df_filtered = self.df_filtered[self.df_filtered['experience_level'].isin(filters['experience'])]

        return self.df_filtered
