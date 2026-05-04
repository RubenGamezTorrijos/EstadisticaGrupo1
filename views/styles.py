"""
views/styles.py
===============
Estilos CSS profesionales para la aplicación Streamlit.
"""

import streamlit as st

def apply_styles():
    st.markdown("""
    <style>
        /* Estética Adaptativa */
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

        /* ===== SIDEBAR: FONDO SOLIDO GARANTIZADO (ESCRITORIO + MOBILE OVERLAY) ===== */
        /* Ataca el section raiz y TODOS sus descendientes sin excepcion */
        section[data-testid="stSidebar"],
        section[data-testid="stSidebar"] *,
        [data-testid="stSidebar"],
        [data-testid="stSidebar"] * {
            background-color: var(--secondary-background-color) !important;
            background-image: none !important;
            backdrop-filter: none !important;
            -webkit-backdrop-filter: none !important;
        }

        section[data-testid="stSidebar"] {
            border-right: 1px solid var(--primary-color) !important;
            opacity: 1 !important;
        }

        /* Titulos */
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

        /* Selectores de Radio - AZUL CORPORATIVO */
        div[data-testid="stRadio"] label[data-baseweb="radio"] div:first-child div:nth-child(2) {
            background-color: #0b84f4 !important;
        }

        div[data-testid="stRadio"] label[aria-checked="true"] p {
            color: #0b84f4 !important;
            font-weight: bold;
        }
    </style>

    <script>
    (function fixSidebarBackground() {
        function applyBg() {
            var sidebar = document.querySelector('section[data-testid="stSidebar"]');
            if (!sidebar) return;

            // Detectar si el tema es oscuro
            var isDark = window.matchMedia('(prefers-color-scheme: dark)').matches
                      || document.documentElement.getAttribute('data-theme') === 'dark';

            // Colores por defecto de Streamlit para modo claro y oscuro
            var bgColor = isDark ? 'rgb(14, 17, 23)' : 'rgb(240, 242, 246)';

            // Obtener el color calculado de la variable CSS del tema si existe
            var computedBg = getComputedStyle(document.documentElement)
                                 .getPropertyValue('--secondary-background-color');
            if (computedBg && computedBg.trim() !== '') {
                bgColor = computedBg.trim();
            }

            // Aplicar fondo solido al sidebar y a TODOS sus hijos
            sidebar.style.setProperty('background-color', bgColor, 'important');
            sidebar.style.setProperty('background-image', 'none', 'important');
            sidebar.style.setProperty('backdrop-filter', 'none', 'important');

            sidebar.querySelectorAll('*').forEach(function(el) {
                el.style.setProperty('background-color', bgColor, 'important');
                el.style.setProperty('background-image', 'none', 'important');
                el.style.setProperty('backdrop-filter', 'none', 'important');
            });
        }

        // Ejecutar inmediatamente y tambien al detectar cambios en el DOM
        applyBg();
        var observer = new MutationObserver(function(mutations) {
            applyBg();
        });
        observer.observe(document.body, { childList: true, subtree: true, attributes: true });
    })();
    </script>
    """, unsafe_allow_html=True)
