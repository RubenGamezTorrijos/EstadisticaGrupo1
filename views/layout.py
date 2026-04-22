"""
views/layout.py
===============
Organización de la página principal en secciones navegables.
Restaura el diseño y contenido original de cada vista.
"""

import streamlit as st
import pandas as pd
from analisis.estadisticos import calcular_estadisticos, calcular_estadisticos_por_categoria
from analisis.graficos import (
    crear_histograma, crear_boxplot, crear_violin_plot, 
    crear_bar_chart, crear_scatter_regresion, crear_grafico_comparativo_ic
)
from analisis.inferencial import calcular_ic_95, contraste_hipotesis
from analisis.modelo_regresion import ejecutar_regresion_simple

def render_main_layout(df, opcion, key, sym):
    """Orquesta el renderizado de la sección seleccionada."""
    
    if opcion == "Escritorio General":
        render_escritorio(df, key, sym)
    elif opcion == "Estadísticos Descriptivos":
        render_estadisticos(df, key, sym)
    elif opcion == "Visualizaciones Gráficas":
        render_visualizaciones(df, key, sym)
    elif opcion == "Regresión Lineal":
        render_regresion(df, key, sym)
    elif opcion == "Estadística Inferencial":
        render_inferencial(df, key, sym)
    elif opcion == "Equipo Grupo 1":
        render_equipo()
        
    render_footer()

def render_footer():
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #888; font-size: 0.85rem; font-style: italic;'>"
        "Rubén: Coordinador y arquitectura de la aplicación Python y Streamlit"
        "</div>", 
        unsafe_allow_html=True
    )

def render_escritorio(df, key, sym):
    st.title(f"🏠 Escritorio de Control - Rafael Rodriguez")
    st.write("Resumen ejecutivo de la muestra actual analizada.")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Muestra (N)", len(df))
    with col2:
        st.metric(f"Salario Medio ({sym})", f"{df[key].mean():,.0f} {sym}")
    with col3:
        st.metric("Mediana COLI", f"{df['cost_of_living_index'].median():,.2f}")
    with col4:
        st.metric("Años en Muestra", f"{df['work_year'].nunique()}")
        
    st.markdown("### 📋 Vista Previa de Datos")
    st.dataframe(df.head(10), use_container_width=True)

def render_estadisticos(df, key, sym):
    st.title("📊 Estadísticos Descriptivos - Rafael Rodriguez")
    st.write("Análisis detallado de tendencia central, dispersión y forma.")
    
    stats_df = calcular_estadisticos(df)
    st.dataframe(stats_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.subheader(f"📍 Análisis por Nivel de Experiencia ({sym})")
    cat_stats = calcular_estadisticos_por_categoria(df, key, 'experience_level')
    st.table(cat_stats)

def render_visualizaciones(df, key, sym):
    st.title("📊 Visualizaciones Gráficas - Leslie Ross")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Distribución de Salarios")
        fig_hist = crear_histograma(df, key, f"Histograma de Salarios ({sym})")
        if fig_hist: st.pyplot(fig_hist)
        else: st.warning("Leslie: Implementar Histograma en `graficos.py`")
        
    with col2:
        st.subheader("Dispersión por Experiencia")
        fig_box = crear_boxplot(df, key, 'experience_level', f"Distribución de Salarios por Nivel ({sym})")
        if fig_box: st.pyplot(fig_box)
        else: st.warning("Leslie: Implementar Boxplot en `graficos.py`")
        
    st.markdown("---")
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Distribución de Densidad (Violin)")
        fig_violin = crear_violin_plot(df, 'experience_level', key, f"Violin Plot: Salario vs Experiencia ({sym})")
        if fig_violin: st.pyplot(fig_violin)
        else: st.warning("Leslie: Implementar Violin Plot en `graficos.py`")
    with col4:
        st.subheader("Presencia por Categoría")
        fig_bar = crear_bar_chart(df, 'job_category', titulo="Top Categorías de Empleo")
        if fig_bar: st.pyplot(fig_bar)
        else: st.warning("Leslie: Implementar Bar Chart en `graficos.py`")

def render_regresion(df, key, sym):
    st.title("📈 Regresión Lineal - Leslie Ross")
    st.write("**Metodología:** Evaluación de la dependencia lineal entre el Coste de Vida (COLI) y el Salario.")
    
    fig_reg, stats_reg = crear_scatter_regresion(df, 'cost_of_living_index', key, f"Regresión: Salario ({sym}) vs COLI")
    resumen_modelo, modelo_obj = ejecutar_regresion_simple(df, 'cost_of_living_index', key)

    if fig_reg is None or modelo_obj is None:
        st.warning("Leslie: Implementar lógica de regresión en `modelo_regresion.py` y `graficos.py`.")
        return

    st.pyplot(fig_reg)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Coeficiente R2", resumen_modelo['Coeficiente R2'])
    c2.metric("Pendiente", resumen_modelo['Pendiente'])
    c3.metric("Intercepto", resumen_modelo['Intercepto'])
    
    st.info(f"**Conclusión Técnica:** {resumen_modelo['Conclusion']}")

def render_inferencial(df, key, sym):
    st.title("🧪 Estadística Inferencial - Bryann Vallejo")
    st.write("Análisis de probabilidad para validar hipótesis poblacionales.")
    
    ic_results = calcular_ic_95(df[key])
    
    if ic_results.get('Estado') == 'PENDIENTE':
        st.info("Bryann: Implementar lógica de intervalos de confianza en `inferencial.py`.")
        return

    # Mostrar resultados si Bryann ha implementado
    st.markdown(f"### 1. Estimación Salarial (Confianza 95%) - {sym}")
    c1, c2, c3 = st.columns(3)
    c1.metric("Media Muestral (x̄)", f"{ic_results['Media']:,.2f} {sym}")
    c2.metric("Límite Inferior", f"{ic_results['Inferior']:,.2f} {sym}")
    c3.metric("Límite Superior", f"{ic_results['Superior']:,.2f} {sym}")

    st.markdown("---")
    st.markdown("### 2. Contrastes de Hipótesis")
    st.info("Utilice el sidebar para filtrar y los resultados se actualizarán automáticamente.")

def render_equipo():
    st.title("👥 Equipo de Desarrollo - Grupo 1")
    st.markdown("""
    ### Estructura y Responsabilidades Técnicas:
    
    *   **Rubén Gámez Torrijos (Coordinador y Arquitectura)**
        *   **Responsabilidades:** Diseño MVC, estilos CSS, motor de exportación PDF/Excel.
    *   **Rafael Rodriguez Mengual (Data Manager)**
        *   **Responsabilidades:** Pipeline de limpieza, integración COLI, estadísticos.
    *   **Bryann Vallejo Luna (Analista Inferencial)**
        *   **Responsabilidades:** Intervalos de confianza, contrastes de hipótesis.
    *   **Leslie Ross Aranibar Pozo (Analista Descriptivo)**
        *   **Responsabilidades:** Catálogo visual, regresión lineal.
    """)
