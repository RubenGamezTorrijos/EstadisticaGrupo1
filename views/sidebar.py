import streamlit as st
import pandas as pd
from models.data_loader import filter_data
from analisis.exportacion import generar_excel_multipestana, generar_pdf_profesional
from analisis.estadisticos import calcular_estadisticos
from analisis.graficos import (
    crear_histograma, crear_boxplot, 
    crear_scatter_regresion, crear_bar_chart, crear_violin_plot
)
from analisis.inferencial import calcular_intervalos_confianza
import config.settings as cfg

def render_sidebar(df_full):
    """Renderiza el sidebar completo con navegación, filtros y exportaciones."""
    
    with st.sidebar:
        st.markdown("""
            <div style="display: flex; align-items: center; justify-content: center; gap: 15px; padding-bottom: 20px;">
                <img src="https://cdn-icons-png.flaticon.com/512/2103/2103633.png" width="50">
                <div style="text-align: left;">
                    <h2 style='color: var(--primary-color); font-size: 1.0rem; margin: 0; line-height: 1.1;'>
                        ESTADÍSTICA Y <br>OPTIMIZACIÓN
                    </h2>
                    <p style='color: var(--text-color); opacity: 0.8; font-weight: 600; font-size: 0.75rem; margin: 3px 0 0 0;'>
                        GRUPO DE TRABAJO 1
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        
        # --- NAVEGACIÓN (MENÚ) ---
        st.markdown("### 🏠 **Menú**")
        opcion_nav = st.radio(
            "Seleccione una vista:",
            ["Escritorio General", "Estadísticos Descriptivos", "Visualizaciones Gráficas", 
             "Estadística Inferencial", "Regresión Lineal", "Equipo Grupo 1"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # --- CONFIGURACIÓN DE DIVISA ---
        st.markdown("### 💰 **Divisas**")
        divisa_label = st.radio(
            "Moneda de visualización:",
            ["USD $", "EUR €"],
            index=0,
            label_visibility="collapsed"
        )
        
        divisa_key = cfg.COL_SALARIO_USD if "USD" in divisa_label else cfg.COL_SALARIO_EUR
        simbolo = "$" if "USD" in divisa_label else "€"
        
        # --- FILTROS GLOBALES ---
        st.markdown("### 🔍 **Filtros**")
        
        exp_filter = st.multiselect(
            "Nivel Experiencia:", 
            options=sorted(df_full['experience_level'].unique()), 
            default=df_full['experience_level'].unique()
        )
        
        cat_filter = st.multiselect(
            "Categoría Puesto:", 
            options=sorted(df_full['job_category'].unique()), 
            default=df_full['job_category'].unique()
        )
        
        countries = sorted(df_full[cfg.COL_PAIS].unique())
        selected_countries = st.multiselect(
            "Filtrar por Países:",
            options=countries,
            default=[]
        )
        
        # Aplicar filtrado
        df_filtered = filter_data(df_full, experience=exp_filter, categories=cat_filter, countries=selected_countries)

        if not df_filtered.empty:
            df_filtered[cfg.COL_SALARIO_DINAMICO] = df_filtered[divisa_key]

        # --- EXPORTACIÓN ---
        handle_exports(df_filtered, divisa_label, simbolo, cfg.COL_SALARIO_DINAMICO)
        
    return df_filtered, opcion_nav, cfg.COL_SALARIO_DINAMICO, simbolo

def handle_exports(df_filtered, currency_label, current_sym, divisa_key):
    """Gestiona la generación y descarga de informes."""
    st.markdown("---")
    st.markdown("### 📥 **Exportar**")
    
    if df_filtered.empty:
        return

    # --- EXCEL ---
    try:
        df_stats = calcular_estadisticos(df_filtered)
        ic_95 = calcular_intervalos_confianza(df_filtered, divisa_key)
        df_inferencial = pd.DataFrame([ic_95]).T
        
        # Regresión simple para el reporte
        from analisis.modelo_regresion import ejecutar_regresion_simple
        reg_model = ejecutar_regresion_simple(df_filtered, cfg.COL_COLI, divisa_key)
        df_reg = pd.DataFrame([reg_model]).T if reg_model else pd.DataFrame()

        excel_data = generar_excel_multipestana(df_filtered, df_stats, df_inferencial, df_reg)
        
        st.download_button(
            label="📊 Excel (.xlsx)",
            data=excel_data,
            file_name=f"analisis_salarios_{currency_label}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    except Exception as e:
        st.error(f"Error Excel: {e}")

    # --- PDF ---
    try:
        graficos_dict = {
            "Distribución Salarial": crear_histograma(df_filtered, divisa_key),
            "Salario por Experiencia": crear_boxplot(df_filtered, divisa_key, "experience_level"),
            "Densidad de Probabilidad (Violin)": crear_violin_plot(df_filtered, divisa_key, "experience_level"),
            "Categorías de Empleo": crear_bar_chart(df_filtered, 'job_category'),
            "Regresión COLI": crear_scatter_regresion(df_filtered, cfg.COL_COLI, divisa_key)
        }
        
        equipo_roles = {
            "Rubén Gámez Torrijos": "Coordinador y Arquitectura",
            "Rafael Rodriguez Mengual": "Data Manager",
            "Bryann Vallejo Luna": "Analista Inferencial",
            "Leslie Ross Aranibar Pozo": "Analista Descriptivo"
        }
        
        pdf_bytes = generar_pdf_profesional(df_filtered, df_stats, equipo_roles, graficos_dict, currency_label)
        
        st.download_button(
            label="📄 Informe PDF",
            data=pdf_bytes,
            file_name=f"informe_estadistica_grupo1_{currency_label}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    except Exception as e:
        st.error(f"Error PDF: {e}")
