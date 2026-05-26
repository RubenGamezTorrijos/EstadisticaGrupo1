"""
controllers/app_controller.py
============================
Controlador principal que gestiona la navegación y el flujo de datos.
Sincroniza el sidebar con el layout principal.
"""

import streamlit as st
from models.data_loader import load_processed_data
from views.sidebar import render_sidebar
from views.styles import apply_styles
from views.layout import render_main_layout

class AppController:
    def __init__(self):
        self.df_full = None

    def run(self):
        """Inicia la ejecución de la aplicación."""
        # 1. Aplicar estilos
        apply_styles()
        
        # 2. Cargar datos (Model)
        self.df_full = load_processed_data()
        
        if self.df_full is None or self.df_full.empty:
            st.error("No se han podido cargar los datos.")
            return

        # 3. Renderizar Sidebar y obtener filtros/navegación (View)
        df_filtered, opcion_nav, divisa_key, simbolo = render_sidebar(self.df_full)
        
        # 4. Renderizar la página principal según la opción (View)
        render_main_layout(df_filtered, opcion_nav, divisa_key, simbolo)
