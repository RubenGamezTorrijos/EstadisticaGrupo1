"""
app.py
======
Punto de entrada principal de la aplicación.
Sigue la arquitectura MVC: Llama al Controlador para orquestar la App.
"""

import streamlit as st
from controllers.app_controller import AppController
from views.layout import render_main_layout

# Configuración de página (Debe ser lo primero)
st.set_page_config(
    page_title="PROYECTO ESTADÍSTICA - Grupo 1",
    page_icon="📊",
    layout="wide"
)

def main():
    # 1. Instanciar controlador
    controller = AppController()
    
    # 2. Ejecutar lógica de datos y filtros
    df_filtered = controller.run()
    
    if df_filtered is not None:
        # 3. Renderizar la página principal
        render_main_layout(df_filtered)

if __name__ == "__main__":
    main()
