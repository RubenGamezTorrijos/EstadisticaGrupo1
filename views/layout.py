"""
views/layout.py
===============
Organización de la página principal en pestañas y contenedores.
"""

import streamlit as st
from analisis.estadisticos import calcular_estadisticos
from analisis.graficos import crear_histograma, crear_boxplot

def render_main_layout(df):
    """Organiza la visualización principal en pestañas."""
    
    st.title("📊 Análisis de Salarios en Ciencia de Datos")
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "🏠 Escritorio", 
        "📊 Descriptiva", 
        "📈 Gráficos", 
        "🧪 Inferencia"
    ])
    
    with tab1:
        st.subheader("Resumen de Muestra")
        col1, col2, col3 = st.columns(3)
        col1.metric("Registros", len(df))
        col2.metric("Salario Medio (USD)", f"${df['salary_in_usd'].mean():,.0f}")
        col3.metric("Años", f"{df['work_year'].nunique()}")
        
        st.dataframe(df.head(10), use_container_width=True)
        
    with tab2:
        st.subheader("Estadísticos Descriptivos")
        stats = calcular_estadisticos(df)
        st.dataframe(stats, use_container_width=True)
        
    with tab3:
        st.subheader("Visualizaciones")
        c1, c2 = st.columns(2)
        with c1:
            fig1 = crear_histograma(df, 'salary_in_usd', "Distribución Salarial")
            if fig1: st.pyplot(fig1)
            else: st.info("Leslie: Implementar Histograma")
        with c2:
            fig2 = crear_boxplot(df, 'salary_in_usd', 'experience_level', "Salarios por Nivel")
            if fig2: st.pyplot(fig2)
            else: st.info("Leslie: Implementar Boxplot")
            
    with tab4:
        st.subheader("Estadística Inferencial")
        st.info("Bryann: Implementar lógica de contraste de hipótesis e intervalos de confianza.")
