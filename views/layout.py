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
    
    from config.settings import COL_SALARIO_USD, COL_SALARIO_EUR
    import plotly.graph_objects as go
    
    # 1. Cálculos de base
    mean_usd = df[COL_SALARIO_USD].mean()
    mean_eur = df[COL_SALARIO_EUR].mean()
    med_coli = df['cost_of_living_index'].median()
    n_muestra = len(df)
    
    if 'work_setting' in df.columns:
        remote_pct = (df['work_setting'] == 'Remote').mean() * 100
    else:
        remote_pct = 0
        
    años_range = f"{df['work_year'].min()} - {df['work_year'].max()}"
    
    # 2. Diseño: Columna Izquierda (Métricas 2x2) | Columna Derecha (Gráficas Duales)
    main_col_left, main_col_right = st.columns([1, 1.2])
    
    with main_col_left:
        # Fila 1 de métricas
        r1_c1, r1_c2 = st.columns(2)
        with r1_c1:
            st.metric("👥 Total Datos", f"{n_muestra:,}")
        with r1_c2:
            st.metric("🏠 Mediana COLI", f"{med_coli:,.2f}")
        
        # Fila 2 de métricas
        r2_c1, r2_c2 = st.columns(2)
        with r2_c1:
            st.metric("📡 % Trabajo Remoto", f"{remote_pct:.1f}%")
        with r2_c2:
            st.metric("📅 Años Analizados", años_range)

    with main_col_right:
        # 3. Gráficos de Aguja Duales (USD y EUR) en una sola figura
        fig = go.Figure()

        # Configuración de formato para USD
        is_high_usd = mean_usd > 140500
        val_usd = mean_usd / 1000 if is_high_usd else mean_usd
        
        # Configuración de formato para EUR
        is_high_eur = mean_eur > 140500
        val_eur = mean_eur / 1000 if is_high_eur else mean_eur

        # Trace para USD
        fig.add_trace(go.Indicator(
            mode = "gauge+number",
            value = val_usd,
            number = {'prefix': "$", 'suffix': "k" if is_high_usd else "", 'valueformat': ".1f" if is_high_usd else ",.0f"},
            title = {'text': "Media USD", 'font': {'size': 14}},
            domain = {'x': [0, 0.48], 'y': [0, 1]},
            gauge = {
                'axis': {'range': [None, (df[COL_SALARIO_USD].max() / 1000 if is_high_usd else df[COL_SALARIO_USD].max()) * 1.1]},
                'bar': {'color': "#1f77b4"},
                'steps': [
                    {'range': [0, 140 if is_high_usd else 140000], 'color': "lavender"},
                    {'range': [140 if is_high_usd else 140000, 500], 'color': "ghostwhite"}
                ]
            }
        ))

        # Trace para EUR
        fig.add_trace(go.Indicator(
            mode = "gauge+number",
            value = val_eur,
            number = {'prefix': "€", 'suffix': "k" if is_high_eur else "", 'valueformat': ".1f" if is_high_eur else ",.0f"},
            title = {'text': "Media EUR", 'font': {'size': 14}},
            domain = {'x': [0.52, 1], 'y': [0, 1]},
            gauge = {
                'axis': {'range': [None, (df[COL_SALARIO_EUR].max() / 1000 if is_high_eur else df[COL_SALARIO_EUR].max()) * 1.1]},
                'bar': {'color': "#ff7f0e"},
                'steps': [
                    {'range': [0, 140 if is_high_eur else 140000], 'color': "lavender"},
                    {'range': [140 if is_high_eur else 140000, 500], 'color': "ghostwhite"}
                ]
            }
        ))

        fig.update_layout(
            height=280, 
            margin=dict(l=10, r=10, t=40, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    st.markdown("---")
        
    st.markdown("### 📋 Vista Previa de Datos")
    st.dataframe(df.head(10), use_container_width=True)

def render_estadisticos(df, key, sym):
    st.title("📊 Estadísticos Descriptivos - Rafael Rodriguez")
    st.write("Análisis detallado de tendencia central, dispersión y forma para ambas divisas.")
    
    from config.settings import COL_SALARIO_USD, COL_SALARIO_EUR
    
    stats_df = calcular_estadisticos(df)
    # Filtrar 'salary' (dinámico) de la tabla descriptiva general para evitar duplicidad visual
    # El usuario prefiere ver las bases fijas aquí.
    from config.settings import COL_SALARIO_DINAMICO
    stats_df = stats_df[stats_df['ID_Variable'] != COL_SALARIO_DINAMICO]
    
    st.dataframe(stats_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.subheader(f"📍 Análisis Detallado por Nivel de Experiencia ({sym})")
    st.info(f"Esta sección se adapta a la moneda seleccionada: **{sym}**")
    cat_stats = calcular_estadisticos_por_categoria(df, key, 'experience_level')
    st.table(cat_stats)

def render_visualizaciones(df, key, sym):
    st.title("📊 Visualizaciones Gráficas - Leslie Ross")
    
    st.markdown("""
        <div style='background-color: #1a2a40; padding: 20px; border-radius: 10px; border: 1px solid #0b84f4; margin-bottom: 25px;'>
            <h3 style='margin-top:0; color: #0b84f4;'>🙇 Tareas de Leslie Ross (Visualización)</h3>
            <p style='color: #a0c4ff;'>Para que esta vista funcione, Leslie debe implementar en el archivo <code>analisis/graficos.py</code>:</p>
            <ol style='color: white;'>
                <li><b>Histograma</b>: Distribución de salarios con KDE.</li>
                <li><b>Boxplot</b>: Comparativa salarial por nivel de experiencia.</li>
                <li><b>Violin Plot</b>: Densidad de probabilidad.</li>
                <li><b>Bar Chart</b>: Frecuencia de categorías de puestos.</li>
            </ol>
            <p style='font-style: italic; color: #0b84f4;'>Utiliza las pistas (💡 PISTA) disponibles en el código.</p>
        </div>
    """, unsafe_allow_html=True)

def render_regresion(df, key, sym):
    st.title("📈 Regresión Lineal - Leslie Ross")
    st.markdown("**Metodología:** Evaluación de la dependencia lineal entre el Coste de Vida (COLI) y el Salario.")
    
    st.markdown("""
        <div style='background-color: #1a2a40; padding: 20px; border-radius: 10px; border: 1px solid #0b84f4; margin-top: 20px;'>
            <h3 style='margin-top:0; color: #0b84f4;'>📈 Tareas de Leslie Ross (Regresión)</h3>
            <p style='color: #a0c4ff;'>Para activar este análisis, Leslie debe completar:</p>
            <ol style='color: white;'>
                <li><code>analisis/graficos.py</code>: Implementar <code>crear_scatter_regresion</code> usando <code>sns.regplot</code>.</li>
                <li><code>analisis/modelo_regresion.py</code>: Implementar <code>ejecutar_regresion_simple</code> usando <code>LinearRegression</code> de <code>scikit-learn</code>.</li>
            </ol>
        </div>
    """, unsafe_allow_html=True)

def render_inferencial(df, key, sym):
    st.title("🧪 Estadística Inferencial - Bryann Vallejo")
    st.markdown("Análisis de probabilidad para validar hipótesis poblacionales.")
    
    st.markdown("""
        <div style='background-color: #1a2a40; padding: 20px; border-radius: 10px; border: 1px solid #0b84f4; margin-top: 20px;'>
            <h3 style='margin-top:0; color: #0b84f4;'>🙇 Tareas de Bryann Vallejo (Estadística Inferencial)</h3>
            <p style='color: #a0c4ff;'>Bryann debe completar la lógica matemática en el archivo <code>analisis/inferencial.py</code> para:</p>
            <ol style='color: white;'>
                <li><b>Intervalos de Confianza</b>: Cálculo manual de grados de libertad, error estándar y T-crítico.</li>
                <li><b>Contrastes de Hipótesis</b>: Implementar <code>stats.ttest_ind</code> y analizar el P-valor.</li>
                <li><b>Supuestos</b>: Validar si los datos siguen una distribución normal.</li>
            </ol>
            <p style='font-style: italic; color: #0b84f4;'>Consulta las pistas en el código para las fórmulas de Numpy y Scipy.</p>
        </div>
    """, unsafe_allow_html=True)

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
