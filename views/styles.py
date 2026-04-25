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
            background: var(--secondary-background-color) !important;
            border: 1px solid var(--primary-color);
            border-radius: 12px;
            padding: 15px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
        }
        
        /* Asegurar que el texto sea siempre legible */
        p, span, label, .stMarkdown {
            color: var(--text-color) !important;
        }

        div[data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px var(--primary-color);
            opacity: 0.9;
        }

        /* Sidebar Identity - ADAPTATIVO */
        [data-testid="stSidebar"] {
            background-color: var(--secondary-background-color) !important;
            border-right: 1px solid var(--primary-color);
        }
        
        /* Títulos */
        h1, h2, h3 {
            color: var(--primary-color) !important;
            font-weight: 800 !important;
            padding-bottom: 5px;
            margin-top: 20px;
            letter-spacing: -0.01em;
        }

        /* Botones */
        .stButton>button {
            border-radius: 8px;
            background-color: var(--primary-color);
            color: white !important; /* El texto del botón suele ser mejor en blanco */
            font-weight: 600;
            border: none;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            opacity: 0.8;
            box-shadow: 0 4px 12px var(--primary-color);
        }

        /* Tags multiselect */
        span[data-baseweb="tag"] {
            background-color: var(--primary-color) !important;
            color: white !important;
        }
    </style>
    """, unsafe_allow_html=True)
