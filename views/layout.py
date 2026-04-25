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
from analisis.regresion import ejecutar_regresion_simple

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
    
    # Aviso de estado para el equipo
    st.warning("🚧 **ESTADO: PENDIENTE** - Leslie Ross debe completar la lógica en `analisis/graficos.py`.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Distribución de Salarios")
        fig_hist = crear_histograma(df, key, f"Histograma de Salarios ({sym})")
        if fig_hist: st.pyplot(fig_hist)
        else: st.info("Leslie: Implementar Histograma en `graficos.py` (Se mostrará aquí)")
        
    with col2:
        st.subheader("Dispersión por Experiencia")
        fig_box = crear_boxplot(df, key, 'experience_level', f"Distribución de Salarios por Nivel ({sym})")
        if fig_box: st.pyplot(fig_box)
        else: st.info("Leslie: Implementar Boxplot en `graficos.py` (Se mostrará aquí)")
        
    st.markdown("---")
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Distribución de Densidad (Violin)")
        fig_violin = crear_violin_plot(df, 'experience_level', key, f"Violin Plot: Salario vs Experiencia ({sym})")
        if fig_violin: st.pyplot(fig_violin)
        else: st.info("Leslie: Implementar Violin Plot en `graficos.py` (Se mostrará aquí)")
    with col4:
        st.subheader("Presencia por Categoría")
        fig_bar = crear_bar_chart(df, 'job_category', titulo="Top Categorías de Empleo")
        if fig_bar: st.pyplot(fig_bar)
        else: st.info("Leslie: Implementar Bar Chart en `graficos.py` (Se mostrará aquí)")

def render_regresion(df, key, sym):
    st.title("📈 Regresión Lineal y Correlación")
    st.write("**Análisis de Dependencia:** Evaluación de cómo influye el Coste de Vida (COLI) en el Salario percibido.")
    
    # Aviso de estado para el equipo
    st.warning("🚧 **ESTADO: PENDIENTE** - Leslie Ross debe completar la lógica en `analisis/regresion.py`.")
    
    fig_reg, stats_reg = crear_scatter_regresion(df, 'cost_of_living_index', key, f"Regresión: Salario ({sym}) vs Índice COLI")
    
    if fig_reg is not None:
        st.pyplot(fig_reg)
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Coeficiente R²", f"{stats_reg['r_cuadrado']:.4f}")
        c2.metric("Pendiente (Beta)", f"{stats_reg['pendiente']:.2f}")
        c3.metric("Intercepto", f"{stats_reg['intercepto']:,.0f}")
        c4.metric("P-Valor", f"{stats_reg['p_valor']:.4f}")
        
        # Interpretación técnica
        st.markdown("### 📝 Interpretación de Resultados")
        r2 = stats_reg['r_cuadrado']
        if r2 > 0.7:
            interp = "Existe una **correlación fuerte**. El coste de vida explica gran parte de la variabilidad salarial."
        elif r2 > 0.3:
            interp = "Existe una **correlación moderada**. Otros factores influyen significativamente en el salario."
        else:
            interp = "La **correlación es débil**. El coste de vida no es el factor determinante principal en esta muestra."
            
        st.info(f"**Análisis Crítico:** {interp}")
    else:
        st.info("Leslie: La visualización de regresión se mostrará aquí una vez implementada la lógica.")

def render_inferencial(df, key, sym):
    st.title("🧪 Estadística Inferencial")
    st.write("Validación de hipótesis poblacionales con un nivel de confianza del 95%.")
    
    # Aviso de estado para el equipo
    st.warning("🚧 **ESTADO: PENDIENTE** - Bryann Vallejo debe completar la lógica en `analisis/inferencial.py`.")
    
    # 1. Intervalos de Confianza
    st.subheader(f"1. Intervalos de Confianza (Media de Salario {sym})")
    ic_results = calcular_ic_95(df[key])
    
    if ic_results['Estado'] == 'COMPLETO':
        c1, c2, c3 = st.columns(3)
        c1.metric("Media Muestral (x̄)", f"{ic_results['Media']:,.2f} {sym}")
        c2.metric("Límite Inferior (LCL)", f"{ic_results['Inferior']:,.2f} {sym}")
        c3.metric("Límite Superior (UCL)", f"{ic_results['Superior']:,.2f} {sym}")
        
        st.caption(f"Error estándar de la media: {ic_results['Error Estándar']:,.2f}")
    else:
        st.info("Bryann: Los resultados del intervalo se mostrarán aquí una vez implementada la función `calcular_ic_95`.")
    
    st.markdown("---")
    
    # 2. Contrastes de Hipótesis
    st.subheader("2. Contrastes de Hipótesis (T-Test)")
    st.write("Comparativa de salarios entre grupos significativos.")
    
    # Grupos para el contraste (Senior vs Junior)
    g_senior = df[df['experience_level'] == 'Senior'][key]
    g_junior = df[df['experience_level'] == 'Entry-level'][key]
    
    if not g_senior.empty and not g_junior.empty:
        test_res = contraste_hipotesis(g_senior, g_junior)
        
        if test_res.get('Estado') == 'COMPLETO':
            col_a, col_b = st.columns([1, 2])
            with col_a:
                st.write("**H₀:** No hay diferencia de salarios entre Senior y Junior.")
                st.write("**H₁:** Existe una diferencia significativa.")
                st.metric("P-Valor", f"{test_res['p_valor']:.6f}")
            
            with col_b:
                if test_res['rechaza_h0']:
                    st.success(f"✅ **Resultado:** {test_res['Conclusion']}. Se rechaza la hipótesis nula.")
                else:
                    st.warning(f"⚠️ **Resultado:** {test_res['Conclusion']}. No hay evidencia para rechazar la hipótesis nula.")
                
                st.write(f"Estadístico T: `{test_res['t_statistic']:.4f}`")
        else:
            st.info("Bryann: Los resultados del contraste T-Test se mostrarán aquí.")
    else:
        st.warning("No hay suficientes datos para realizar el contraste entre niveles de experiencia.")
    
    st.markdown("---")
    st.subheader("3. Impacto del Coste de Vida (COLI)")
    st.write("¿Influye el coste de vida del país en la media salarial?")
    
    median_coli = df['cost_of_living_index'].median()
    g_high_coli = df[df['cost_of_living_index'] >= median_coli][key]
    g_low_coli = df[df['cost_of_living_index'] < median_coli][key]
    
    if not g_high_coli.empty and not g_low_coli.empty:
        test_coli = contraste_hipotesis(g_high_coli, g_low_coli)
        st.write(f"Comparando países con COLI alto (>= {median_coli:.1f}) vs COLI bajo.")
        if test_coli.get('Estado') == 'COMPLETO':
            st.metric("P-Valor (Impacto COLI)", f"{test_coli['p_valor']:.6f}")
            st.info(f"**Conclusión:** {test_coli['Conclusion']}")
        else:
            st.info("Bryann: Los resultados del impacto COLI se mostrarán aquí.")

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
