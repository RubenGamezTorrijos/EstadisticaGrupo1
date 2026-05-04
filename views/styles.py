"""
views/styles.py
===============
Estilos CSS profesionales para la aplicación Streamlit.
"""

import streamlit as st


def _get_sidebar_colors():
    """
    Lee los colores reales del tema de Streamlit para inyectarlos como
    valores sólidos en el sidebar. Devuelve (color_claro, color_oscuro).
    """
    # Intentar leer secondaryBackgroundColor de la config (es el color nativo del sidebar)
    secondary = st.get_option("theme.secondaryBackgroundColor")

    # Defaults exactos de Streamlit para Light y Dark
    light_bg = secondary if secondary else "#f0f2f6"
    dark_bg  = "#262730"  # Streamlit dark sidebar default siempre es este valor

    return light_bg, dark_bg


def apply_styles():
    light_sidebar, dark_sidebar = _get_sidebar_colors()

    st.markdown(f"""
    <style>
        /* Estética Adaptativa */
        .stApp {{
            background-attachment: fixed;
        }}

        /* Contenedores de tarjetas y métricas */
        div[data-testid="stMetric"], div[data-testid="stExpander"], div[data-testid="stTable"] {{
            background: var(--secondary-background-color);
            border: 1px solid var(--primary-color);
            border-radius: 12px;
            padding: 15px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
        }}

        /* Texto legible */
        p, span, label, .stMarkdown {{
            color: var(--text-color);
        }}

        div[data-testid="stMetric"]:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px var(--primary-color);
            opacity: 0.9;
        }}

        /* ================================================================
           SIDEBAR: FONDO SÓLIDO — MODO CLARO
           Inyectamos el color exacto leído de la config de Streamlit.
           Esto garantiza que el drawer móvil sea 100% opaco.
        ================================================================ */
        [data-testid="stSidebar"],
        section[data-testid="stSidebar"],
        [data-testid="stSidebarContent"],
        [data-testid="stSidebarNav"],
        [data-testid="stSidebarNav"] > ul,
        [data-testid="stSidebarUserContent"],
        [data-testid="stSidebar"] > div,
        [data-testid="stSidebar"] > div:first-child {{
            background-color: {light_sidebar} !important;
            background:       {light_sidebar} !important;
            background-image: none !important;
            opacity: 1 !important;
            backdrop-filter: none !important;
            -webkit-backdrop-filter: none !important;
        }}

        /* SIDEBAR: FONDO SÓLIDO — MODO OSCURO (sistema/manual) */
        @media (prefers-color-scheme: dark) {{
            [data-testid="stSidebar"],
            section[data-testid="stSidebar"],
            [data-testid="stSidebarContent"],
            [data-testid="stSidebarNav"],
            [data-testid="stSidebarNav"] > ul,
            [data-testid="stSidebarUserContent"],
            [data-testid="stSidebar"] > div,
            [data-testid="stSidebar"] > div:first-child {{
                background-color: {dark_sidebar} !important;
                background:       {dark_sidebar} !important;
                background-image: none !important;
                opacity: 1 !important;
                backdrop-filter: none !important;
                -webkit-backdrop-filter: none !important;
            }}
        }}

        /* Títulos */
        h1, h2, h3 {{
            color: var(--primary-color);
            font-weight: 800;
            padding-bottom: 5px;
            margin-top: 20px;
            letter-spacing: -0.01em;
        }}

        /* Botones — AZUL CORPORATIVO */
        .stButton>button {{
            border-radius: 8px;
            background-color: #0b84f4 !important;
            color: white !important;
            font-weight: 600;
            border: none;
            transition: all 0.3s ease;
        }}

        .stButton>button:hover {{
            background-color: #0d6efd !important;
            box-shadow: 0 4px 12px rgba(11, 132, 244, 0.3);
        }}

        /* Tags multiselect — AZUL CORPORATIVO */
        span[data-baseweb="tag"] {{
            background-color: #0b84f4 !important;
            color: white !important;
        }}

        /* Selectores de Radio — AZUL CORPORATIVO */
        div[data-testid="stRadio"] label[data-baseweb="radio"] div:first-child div:nth-child(2) {{
            background-color: #0b84f4 !important;
        }}

        div[data-testid="stRadio"] label[aria-checked="true"] p {{
            color: #0b84f4 !important;
            font-weight: bold;
        }}
    </style>
    """, unsafe_allow_html=True)
