"""
views/styles.py
===============
Estilos CSS profesionales para la aplicación Streamlit.
"""

import streamlit as st

def apply_styles():
    st.markdown("""
    <style>
        /* Estética Adaptativa: Glassmorphism */
        .stApp {
            background-attachment: fixed;
        }
        
        /* Contenedores de tarjetas y métricas - ADAPTATIVOS */
        div[data-testid="stMetric"], div[data-testid="stExpander"], div[data-testid="stTable"] {
            background: var(--secondary-background-color);
            border: 1px solid var(--primary-color);
            border-radius: 12px;
            padding: 15px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
        }
        
        /* Asegurar que el texto sea siempre legible */
        p, span, label, .stMarkdown {
            color: var(--text-color);
        }

        div[data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px var(--primary-color);
            opacity: 0.9;
        }

        /* ===== SIDEBAR: FONDO SÓLIDO (TODOS LOS MODOS, INCLUIDO MOBILE) ===== */

        /* Contenedor principal del sidebar - escritorio y mobile */
        [data-testid="stSidebar"],
        section[data-testid="stSidebar"] {
            background-color: var(--secondary-background-color) !important;
            background-image: none !important;
            border-right: 1px solid var(--primary-color) !important;
            opacity: 1 !important;
        }

        /* Contenedor interno del sidebar (drawer en mobile) */
        [data-testid="stSidebar"] > div,
        [data-testid="stSidebar"] > div:first-child,
        section[data-testid="stSidebar"] > div {
            background-color: var(--secondary-background-color) !important;
            background-image: none !important;
            opacity: 1 !important;
        }

        /* Contenido del sidebar en mobile (overlay drawer) */
        [data-testid="stSidebarContent"],
        .stSidebar > div,
        [class*="sidebar"] > div {
            background-color: var(--secondary-background-color) !important;
            background-image: none !important;
        }

        /* Navegación interna del sidebar */
        [data-testid="stSidebarNav"],
        [data-testid="stSidebarNav"] > ul,
        [data-testid="stSidebarUserContent"] {
            background-color: var(--secondary-background-color) !important;
            background-image: none !important;
            opacity: 1 !important;
        }

        /* Fix específico mobile: el sidebar como overlay quita transparencia */
        @media (max-width: 768px) {
            [data-testid="stSidebar"],
            [data-testid="stSidebar"] > div,
            [data-testid="stSidebarContent"],
            [data-testid="stSidebarUserContent"],
            section[data-testid="stSidebar"] {
                /* Usamos var(--background-color) porque es SIEMPRE un color sólido (blanco/oscuro) que se adapta al modo que elijas en Streamlit */
                background: var(--background-color) !important;
                background-color: var(--background-color) !important;
                background-image: none !important;
                backdrop-filter: none !important;
                -webkit-backdrop-filter: none !important;
                opacity: 1 !important;
                box-shadow: 2px 0 15px rgba(0,0,0,0.5) !important;
                z-index: 999999 !important;
            }
        }
        
        /* Títulos */
        h1, h2, h3 {
            color: var(--primary-color);
            font-weight: 800;
            padding-bottom: 5px;
            margin-top: 20px;
            letter-spacing: -0.01em;
        }

        /* Botones y Selectores - AZUL CORPORATIVO */
        .stButton>button {
            border-radius: 8px;
            background-color: #0b84f4 !important;
            color: white !important;
            font-weight: 600;
            border: none;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            background-color: #0d6efd !important;
            box-shadow: 0 4px 12px rgba(11, 132, 244, 0.3);
        }

        /* Tags multiselect - AZUL CORPORATIVO */
        span[data-baseweb="tag"] {
            background-color: #0b84f4 !important;
            color: white !important;
        }

        /* Selectores de Radio (Divisa y Navegación) - AZUL CORPORATIVO */
        div[data-testid="stRadio"] label[data-baseweb="radio"] div:first-child div:nth-child(2) {
            background-color: #0b84f4 !important;
        }
        
        div[data-testid="stRadio"] label[aria-checked="true"] p {
            color: #0b84f4 !important;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)
