"""
views/sidebar.py
================
Componente de la interfaz para los filtros laterales y navegación.
Restaura el diseño original Navy Blue y las opciones de exportación.
"""

import streamlit as st
import pandas as pd
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
        # Logo y Título
        st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=80)
        st.markdown("""
        <h2 style='color: white; font-size: 1.4rem; text-align: center; margin-bottom: 0;'>
            ESTADÍSTICA Y OPTIMIZACIÓN
        </h2>
        <p style='color: #0b84f4; text-align: center; font-weight: 600; font-size: 0.9rem;'>
            GRUPO DE TRABAJO 1
        </p>
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
        
        divisa_key = 'salary_in_usd' if "USD" in divisa_label else 'salary_in_eur'
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
        
        # Filtro Experiencia
        exp_filter = st.multiselect(
            "Nivel Experiencia:", 
            options=df_full['experience_level'].unique(), 
            default=df_full['experience_level'].unique()
        )
        
        # Filtro Países
        all_countries = sorted(df_full['company_location'].unique())
        selected_countries = st.multiselect(
            "📍 Filtrar por Países",
            options=all_countries,
            default=[],
            help="Si no seleccionas ninguno, se mostrarán todos."
        )
        
        # Filtro Categoría
        cat_filter = st.multiselect(
            "Categoría Puesto:", 
            options=df_full['job_category'].unique(), 
            default=df_full['job_category'].unique()
        )
        
        # Lógica de filtrado aplicada
        df_filtered = df_full.copy()
        df_filtered = df_filtered[df_filtered['experience_level'].isin(exp_filter)]
        df_filtered = df_filtered[df_filtered['job_category'].isin(cat_filter)]
        if selected_countries:
            df_filtered = df_filtered[df_filtered['company_location'].isin(selected_countries)]

        # --- EXPORTACIÓN ---
        handle_exports(df_filtered, divisa_label, simbolo, divisa_key)
        
    return df_filtered, opcion_nav, divisa_key, simbolo

def handle_exports(df_filtered, currency_label, current_sym, divisa_key):
    st.sidebar.markdown("---")
    st.sidebar.subheader("📥 Exportar Resultados")
    
    # 1. Preparar datos para Excel
    df_stats = calcular_estadisticos(df_filtered)
    
    # Inferencia (Resumen)
    ic_95 = calcular_ic_95(df_filtered[divisa_key])
    df_inferencial = pd.DataFrame([ic_95]).T
    df_inferencial.columns = ['Valor']
    
    # Regresión
    _, reg_stats = crear_scatter_regresion(df_filtered, 'cost_of_living_index', divisa_key, "")
    df_regresion = pd.DataFrame([reg_stats]).T
    df_regresion.columns = ['Métrica']

    # Botón Excel
    excel_data = generar_excel_multipestana(df_filtered, df_stats, df_inferencial, df_regresion)
    st.sidebar.download_button(
        label="📊 Descargar Excel (.xlsx)",
        data=excel_data,
        file_name=f"analisis_salarios_{currency_label.replace(' ', '_')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )
    
    # 2. Preparar PDF
    # Gráficos Dinámicos para el Informe
    df_comp_exp = df_filtered[df_filtered['experience_level'].isin(['Senior', 'Mid-level'])]
    df_comp_mod = df_filtered[df_filtered['work_setting'].isin(['Remote', 'In-person'])]
    
    graficos_dict = {
        "Distribución Salarial (Histograma)": crear_histograma(df_filtered, divisa_key, "Distribución de Salarios"),
        "Comparativa por Experiencia (Boxplot)": crear_boxplot(df_filtered, divisa_key, "experience_level", "Salario por Nivel"),
        "Densidad Salarial (Violin Plot)": crear_violin_plot(df_filtered, 'experience_level', divisa_key, "Salario vs Experiencia"),
        "Top Categorías de Empleo (Barras)": crear_bar_chart(df_filtered, 'job_category', "Presencia en Mercado"),
        "Regresión: Salario vs Coste Vida": crear_scatter_regresion(df_filtered, 'cost_of_living_index', divisa_key, "Influencia del COLI")[0],
        "Evidencia Inferencial (Exp)": crear_grafico_comparativo_ic(df_comp_exp, 'experience_level', divisa_key, "Comparativa IC 95%: Senior vs Mid"),
        "Evidencia Inferencial (Modalidad)": crear_grafico_comparativo_ic(df_comp_mod, 'work_setting', divisa_key, "Comparativa IC 95%: Remoto vs Presencial")
    }
    
    equipo_roles = {
        "Rubén Gámez Torrijos": "Coordinador y Arquitectura",
        "Rafael Rodriguez Mengual": "Data Manager",
        "Bryann Vallejo Luna": "Analista Inferencial",
        "Leslie Ross Aranibar Pozo": "Analista Descriptivo"
    }
    
    pdf_bytes = generar_pdf_profesional(df_filtered, df_stats, equipo_roles, graficos_dict, currency_label, "Filtros activos en esta muestra.")
    
    st.sidebar.download_button(
        label="📄 Descargar Informe PDF",
        data=pdf_bytes,
        file_name=f"informe_estadistica_grupo1_{currency_label.replace(' ', '_')}.pdf",
        mime="application/pdf",
        use_container_width=True
    )
