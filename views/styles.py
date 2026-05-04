"""
views/styles.py
===============
Estilos CSS profesionales para la aplicación Streamlit.
"""

import streamlit as st


def apply_styles():
    st.markdown("""
    <style>
        /* ── ESTÉTICA GENERAL ────────────────────────────────────── */
        .stApp {
            background-attachment: fixed;
        }

        /* Contenedores de tarjetas y métricas */
        div[data-testid="stMetric"],
        div[data-testid="stExpander"],
        div[data-testid="stTable"] {
            background: var(--secondary-background-color);
            border: 1px solid var(--primary-color);
            border-radius: 12px;
            padding: 15px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
        }

        p, span, label, .stMarkdown {
            color: var(--text-color);
        }

        div[data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px var(--primary-color);
            opacity: 0.9;
        }

        /* ── SIDEBAR: FONDO SÓLIDO ADAPTATIVO ───────────────────────
           Usamos var(--secondary-background-color) porque:
           1) Es la variable que Streamlit actualiza al cambiar el tema
              (Light / Dark / System) desde el menú ☰ → Settings.
           2) Es siempre un color opaco (no rgba con alpha).
           3) Lo aplicamos con !important sobre TODOS los nodos del
              sidebar, incluyendo los divs sin data-testid que Streamlit
              usa como wrappers del drawer en mobile.
        ──────────────────────────────────────────────────────────── */
        section[data-testid="stSidebar"],
        section[data-testid="stSidebar"] > div,
        section[data-testid="stSidebar"] > div > div,
        [data-testid="stSidebarContent"],
        [data-testid="stSidebarNav"],
        [data-testid="stSidebarNav"] > ul,
        [data-testid="stSidebarUserContent"] {
            background-color: var(--secondary-background-color) !important;
            background:       var(--secondary-background-color) !important;
            background-image: none !important;
            opacity: 1 !important;
            visibility: visible !important;
            pointer-events: auto !important;
            backdrop-filter: none !important;
            -webkit-backdrop-filter: none !important;
        }

        /* En mobile el sidebar abre como drawer; forzamos todos sus
           descendientes directos para que ningún div hijo sea transparente */
        section[data-testid="stSidebar"] > div > div > div {
            background-color: var(--secondary-background-color) !important;
            opacity: 1 !important;
        }

        /* ── TÍTULOS ─────────────────────────────────────────────── */
        h1, h2, h3 {
            color: var(--primary-color);
            font-weight: 800;
            padding-bottom: 5px;
            margin-top: 20px;
            letter-spacing: -0.01em;
        }

        /* ── BOTONES — AZUL CORPORATIVO ──────────────────────────── */
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

        /* ── TAGS MULTISELECT — AZUL CORPORATIVO ─────────────────── */
        span[data-baseweb="tag"] {
            background-color: #0b84f4 !important;
            color: white !important;
        }

        /* ── RADIO — AZUL CORPORATIVO ────────────────────────────── */
        div[data-testid="stRadio"] label[data-baseweb="radio"] div:first-child div:nth-child(2) {
            background-color: #0b84f4 !important;
        }

        div[data-testid="stRadio"] label[aria-checked="true"] p {
            color: #0b84f4 !important;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)
