import streamlit as st
import pandas as pd
from models.data_loader import filter_data
from analisis.exportacion import generar_excel_multipestana, generar_pdf_profesional
from analisis.estadisticos import calcular_estadisticos
from analisis.graficos import (
    crear_histograma, crear_boxplot, crear_violin_plot, 
    crear_scatter_regresion, crear_bar_chart, crear_grafico_comparativo_ic
)
from analisis.inferencial import calcular_ic_95

def render_sidebar(df_full):
    """Renderiza el sidebar completo con navegación, filtros y exportaciones."""
    
    with st.sidebar:
        # Logo y Título Centrados
        # Logo y Título Centrados Horizontalmente
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
        
        # --- CONFIGURACIÓN DE DIVISA ---
        st.subheader("⚙️ Configuración")
        divisa_label = st.radio(
            "Seleccionar Divisa Global:",
            ["USD $", "EUR €"],
            index=0,
            help="Cambia todos los cálculos y gráficos a la moneda elegida."
        )
        
        import config.settings as cfg
        divisa_key = cfg.COL_SALARIO_USD if "USD" in divisa_label else cfg.COL_SALARIO_EUR
        simbolo = "$" if "USD" in divisa_label else "€"
        
        # --- NAVEGACIÓN ---
        st.markdown("---")
        opcion_nav = st.radio(
            "Navegación del Proyecto:",
            ["Escritorio General", "Estadísticos Descriptivos", "Visualizaciones Gráficas", 
             "Estadística Inferencial", "Regresión Lineal", "Equipo Grupo 1"]
        )
        
        # --- FILTROS GLOBALES ---
        st.markdown("---")
        st.subheader("🔍 Filtros de Muestra")
        
        # Selección de Filtros
        exp_filter = st.multiselect(
            "Nivel Experiencia:", 
            options=sorted(df_full['experience_level'].unique()), 
            default=df_full['experience_level'].unique()
        )
        
        all_countries = sorted(df_full['company_location'].unique())
        selected_countries = st.multiselect(
            "📍 Filtrar por Países",
            options=all_countries,
            default=[],
            help="Si no seleccionas ninguno, se mostrarán todos."
        )
        
        cat_filter = st.multiselect(
            "Categoría Puesto:", 
            options=sorted(df_full['job_category'].unique()), 
            default=df_full['job_category'].unique()
        )
        
        # Aplicar filtrado unificado
        df_filtered = filter_data(df_full, experience=exp_filter, categories=cat_filter, countries=selected_countries)

        # --- Inyección de Columna Dinámica (Senior Strategy) ---
        # Esto permite que todos los análisis usen 'salary' sin importar la divisa elegida
        if not df_filtered.empty:
            df_filtered[cfg.COL_SALARIO_DINAMICO] = df_filtered[divisa_key]

        # --- EXPORTACIÓN ---
        handle_exports(df_filtered, divisa_label, simbolo, cfg.COL_SALARIO_DINAMICO, selected_countries)
        
    return df_filtered, opcion_nav, cfg.COL_SALARIO_DINAMICO, simbolo

def handle_exports(df_filtered, currency_label, current_sym, divisa_key, countries):
    """Gestiona la generación y descarga de informes de forma robusta."""
    st.markdown("---")
    st.subheader("📥 Exportar Resultados")
    
    if df_filtered.empty:
        st.warning("Muestra vacía. Ajusta los filtros.")
        return

    # --- EXPORTAR EXCEL ---
    try:
        df_stats = calcular_estadisticos(df_filtered)
        ic_95 = calcular_ic_95(df_filtered[divisa_key])
        df_inferencial = pd.DataFrame([ic_95]).T
        df_inferencial.columns = ['Valor']
        
        _, reg_stats = crear_scatter_regresion(df_filtered, 'cost_of_living_index', divisa_key, "")
        df_regresion = pd.DataFrame([reg_stats]).T
        df_regresion.columns = ['Métrica']

        excel_data = generar_excel_multipestana(df_filtered, df_stats, df_inferencial, df_regresion)
        
        st.download_button(
            label="📊 Descargar Excel (.xlsx)",
            data=excel_data,
            file_name=f"analisis_salarios_{currency_label.replace(' ', '_')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    except Exception as e:
        st.error(f"Error en Excel: {str(e)}")

    # --- EXPORTAR PDF ---
    try:
        # Filtrados específicos para comparativas en el informe
        df_comp_exp = df_filtered[df_filtered['experience_level'].isin(['Senior', 'Mid-level'])]
        df_comp_mod = df_filtered[df_filtered['work_setting'].isin(['Remote', 'In-person'])]
        
        graficos_dict = {
            "Distribución Salarial": crear_histograma(df_filtered, divisa_key, "Distribución de Salarios"),
            "Salario por Experiencia": crear_boxplot(df_filtered, divisa_key, "experience_level", "Comparativa Salarial"),
            "Densidad Salarial": crear_violin_plot(df_filtered, 'experience_level', divisa_key, "Densidad por Nivel"),
            "Categorías de Empleo": crear_bar_chart(df_filtered, 'job_category', "Presencia en Mercado"),
            "Regresión COLI": crear_scatter_regresion(df_filtered, 'cost_of_living_index', divisa_key, "Influencia del COLI")[0]
        }
        
        # Añadir comparativas solo si hay datos
        if not df_comp_exp.empty:
            graficos_dict["Evidencia: Senior vs Mid"] = crear_grafico_comparativo_ic(df_comp_exp, 'experience_level', divisa_key, "Comparativa IC 95%")
        if not df_comp_mod.empty:
            graficos_dict["Evidencia: Modalidad"] = crear_grafico_comparativo_ic(df_comp_mod, 'work_setting', divisa_key, "Comparativa IC 95%")
        
        equipo_roles = {
            "Rubén Gámez Torrijos": "Coordinador y Arquitectura",
            "Rafael Rodriguez Mengual": "Data Manager",
            "Bryann Vallejo Luna": "Analista Inferencial",
            "Leslie Ross Aranibar Pozo": "Analista Descriptivo"
        }
        
        filtros_data = {
            'target_col': divisa_key, 
            'simbolo': current_sym, 
            'label': currency_label,
            'countries': countries
        }
        pdf_bytes = generar_pdf_profesional(df_filtered, df_stats, equipo_roles, graficos_dict, currency_label, filtros_data)
        
        st.download_button(
            label="📄 Descargar Informe PDF",
            data=pdf_bytes,
            file_name=f"informe_estadistica_grupo1_{currency_label.replace(' ', '_')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    except Exception as e:
        st.error(f"Error en PDF: {str(e)}")
