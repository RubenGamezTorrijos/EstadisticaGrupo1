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

        /* Sidebar Identity - ADAPTATIVO */
        [data-testid="stSidebar"] {
            background-color: var(--secondary-background-color);
            border-right: 1px solid var(--primary-color);
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
