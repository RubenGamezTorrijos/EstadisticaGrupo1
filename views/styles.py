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
        
        /* Contenedores de tarjetas y métricas */
        div[data-testid="stMetric"], div[data-testid="stExpander"], div[data-testid="stTable"] {
            background: rgba(128, 128, 128, 0.1) !important;
            border: 1px solid rgba(128, 128, 128, 0.2);
            border-radius: 12px;
            backdrop-filter: blur(8px);
            padding: 15px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
        }
        
        div[data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(11, 132, 244, 0.15);
            border-color: rgba(11, 132, 244, 0.4);
        }

        /* Sidebar Identity */
        [data-testid="stSidebar"] {
            background-color: #0c1c30 !important;
        }
        
        /* Títulos */
        h1, h2, h3 {
            color: #0b84f4 !important;
            font-weight: 800 !important;
            padding-bottom: 5px;
            margin-top: 20px;
            letter-spacing: -0.01em;
        }

        /* Botones */
        .stButton>button {
            border-radius: 8px;
            background-color: #0b84f4;
            color: white;
            font-weight: 600;
            border: none;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            background-color: #0d6efd;
            box-shadow: 0 4px 12px rgba(13, 110, 253, 0.3);
        }

        /* Tags multiselect */
        span[data-baseweb="tag"] {
            background-color: #0b84f4 !important;
            color: white !important;
        }
    </style>
    """, unsafe_allow_html=True)
