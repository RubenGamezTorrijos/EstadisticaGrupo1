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
from analisis.inferencial import calcular_ic_95, contraste_hipotesis, verificar_supuestos
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
        "<div style='text-align: center; color: var(--text-color); opacity: 0.6; font-size: 0.85rem; font-style: italic;'>"
        "© 2026 ESTADÍSTICA Y OPTIMIZACIÓN - GRUPO DE TRABAJO 1 (v.2.5.1-dev)"
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
    
    # --- Estado de Avance ---
    st.success("✅ **Estado:** Finalizado e Integrado por Rafael Rodriguez")
    
    if df.empty:
        st.warning("⚠️ No hay datos disponibles para la muestra seleccionada. Ajusta los filtros en el sidebar.")
        return

    st.write("Análisis detallado de tendencia central, dispersión y forma para ambas divisas.")
    
    from config.settings import COL_SALARIO_USD, COL_SALARIO_EUR
    
    stats_df = calcular_estadisticos(df)
    # Filtrar 'salary' (dinámico) de la tabla descriptiva general para evitar duplicidad visual
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
    
    # --- Estado de Avance ---
    st.warning("🛠️ **Estado:** Pendiente de Implementación por Leslie Ross")
    
    if df.empty:
        st.warning("⚠️ No hay datos disponibles para la muestra seleccionada.")
        return

    # Verificación de implementación de Leslie
    st.info("""
    ### 👩‍💻 Tareas de Leslie Ross (Visualización)
    Para que esta vista funcione, Leslie debe implementar en el archivo `analisis/graficos.py`:
    1. **Histograma**: Distribución de salarios con KDE.
    2. **Boxplot**: Comparativa salarial por nivel de experiencia.
    3. **Violin Plot**: Densidad de probabilidad.
    4. **Bar Chart**: Frecuencia de categorías de puestos.
    
    *Utiliza las pistas (`# 💡 PISTA`) disponibles en el código.*
    """)

def render_regresion(df, key, sym):
    st.title("📈 Regresión Lineal - Leslie Ross")
    
    # --- Estado de Avance ---
    st.warning("🛠️ **Estado:** Pendiente de Implementación por Leslie Ross")
    
    if df.empty:
        st.warning("⚠️ No hay datos disponibles para la muestra seleccionada.")
        return

    st.markdown("**Metodología:** Evaluación de la dependencia lineal entre el Coste de Vida (COLI) y el Salario.")
    
    # Verificación de implementación de Leslie para Regresión
    st.info("""
    ### 📈 Tareas de Leslie Ross (Regresión)
    Para activar este análisis, Leslie debe completar:
    1. **`analisis/graficos.py`**: Implementar `crear_scatter_regresion` usando `sns.regplot`.
    2. **`analisis/modelo_regresion.py`**: Implementar `ejecutar_regresion_simple` usando `LinearRegression` de scikit-learn.
    """)
    
    st.caption("Nota: El análisis COLI permite responder si el coste de vida de un país justifica el salario percibido.")

def render_inferencial(df, key, sym):
    st.title("🧪 Estadística Inferencial - Bryann Vallejo")
    
    # --- Estado de Avance ---
    st.success("✅ **Estado:** Finalizado e Integrado por Bryann Vallejo")
    
    if df.empty:
        st.warning("⚠️ No hay datos disponibles para la muestra seleccionada.")
        return

    st.markdown("Análisis de probabilidad para validar hipótesis poblacionales sobre los salarios.")
    
    # --- 1. Intervalo de Confianza ---
    st.subheader(f"📍 Intervalo de Confianza (95%) - {sym}")
    try:
        ic_data = calcular_ic_95(df[key])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Media Muestral", f"{ic_data['Media']:,.2f} {sym}")
        with col2:
            st.metric("Límite Inferior", f"{ic_data['Inferior']:,.2f} {sym}")
        with col3:
            st.metric("Límite Superior", f"{ic_data['Superior']:,.2f} {sym}")
        
        st.caption(f"Interpretación: Con un 95% de confianza, la media poblacional se encuentra entre {ic_data['Inferior']:,.0f} y {ic_data['Superior']:,.0f} {sym}.")
    except Exception as e:
        st.error(f"Error en el cálculo del IC: {str(e)}")

    st.markdown("---")
    
    # --- 2. Verificación de Supuestos ---
    st.subheader("🛡️ Verificación de Supuestos")
    try:
        supuestos = verificar_supuestos(df[key])
        
        col_s1, col_s2 = st.columns([1, 2])
        with col_s1:
            if supuestos['Normal']:
                st.success(f"✅ Normalidad: {supuestos['Prueba']}")
            else:
                st.warning(f"⚠️ Normalidad: No detectada ({supuestos['Prueba']})")
                st.info("Nota: La falta de normalidad es común en datos salariales (sesgados). Se recomienda usar métodos robustos.")
        with col_s2:
            st.write(f"**P-Valor:** `{supuestos['P-Valor']:.4e}`")
            st.write("Si el P-Valor es > 0.05, los datos siguen una distribución normal.")
    except Exception as e:
        st.error(f"Error en verificación de supuestos: {str(e)}")

    st.markdown("---")
    
    # --- 3. Contraste de Hipótesis ---
    st.subheader("⚖️ Contraste de Hipótesis (Welch T-Test)")
    st.write("¿Existe una diferencia significativa entre el trabajo **Remoto** y **Presencial**?")
    
    if 'work_setting' in df.columns:
        remote = df[df['work_setting'] == 'Remote'][key]
        presencial = df[df['work_setting'] == 'In-person'][key]
        
        if len(remote) > 1 and len(presencial) > 1:
            try:
                res_h = contraste_hipotesis(remote, presencial, "Remoto", "Presencial")
                
                st.info(f"**Resultado:** {res_h['Decisión']}")
                st.write(f"**Conclusión:** {res_h['Conclusion']}")
                
                # Gráfico comparativo (opcional, si existe en analisis/graficos.py)
                try:
                    fig_ic = crear_grafico_comparativo_ic(df, key, 'work_setting', sym)
                    st.pyplot(fig_ic)
                except Exception:
                    st.warning("⚠️ Gráfico comparativo pendiente por Leslie Ross.")
            except Exception as e:
                st.error(f"Error en el contraste: {str(e)}")
        else:
            st.warning("No hay suficientes datos para realizar el contraste entre Remoto y Presencial (se requieren al menos 2 datos por grupo).")
    else:
        st.warning("La variable 'work_setting' no está disponible para el contraste.")

def render_equipo():
    st.title("👥 Equipo de Desarrollo - Grupo 1")
    st.info("Estructura organizativa y estado de cumplimiento de los objetivos técnicos.")

    col1, col2 = st.columns(2)
    
    with col1:
        with st.expander("👑 Rubén Gámez Torrijos", expanded=True):
            st.markdown("**Coordinador y Arquitectura**")
            st.write("**Descripción:** Liderazgo técnico, diseño estructural y orquestación del proyecto.")
            st.write("**Responsabilidades:** Diseño de la arquitectura modular de la aplicación, sistema de estilos CSS adaptativos para temas Light/Dark y desarrollo del motor de exportación profesional (PDF/Excel).")
            st.write("**Archivos clave:** `app.py` (Orquestación), `analisis/exportacion.py` (Generación de Reportes), `config/styles.py`.")
            st.success("✅ **Estado:** FINALIZADO Y VERIFICADO")
            
        with st.expander("📊 Rafael Rodriguez Mengual", expanded=True):
            st.markdown("**Data Manager**")
            st.write("**Descripción:** Especialista en procesamiento, limpieza y análisis descriptivo de datos.")
            st.write("**Responsabilidades:** Implementación del pipeline de limpieza de datos, integración de variables externas (Índice de coste de vida) y desarrollo de la lógica para estadísticos de tendencia central y dispersión.")
            st.write("**Archivos clave:** `analisis/utils.py` (Limpieza), `analisis/estadisticos.py` (Motor estadístico).")
            st.success("✅ **Estado:** FINALIZADO Y VERIFICADO")

    with col2:
        with st.expander("🧪 Bryann Vallejo Luna", expanded=True):
            st.markdown("**Analista Inferencial**")
            st.write("**Descripción:** Experto en modelos probabilísticos y validación de hipótesis estadísticas.")
            st.write("**Responsabilidades:** Desarrollo de modelos de probabilidad poblacional, cálculo de intervalos de confianza mediante T-Student y ejecución de contrastes de hipótesis paramétricos de una y dos muestras.")
            st.write("**Archivos clave:** `analisis/inferencial.py`, `app.py` (Sección Inferencia).")
            st.success("✅ **Estado:** FINALIZADO Y VERIFICADO")
            
        with st.expander("🎨 Leslie Ross Aranibar Pozo", expanded=True):
            st.markdown("**Analista Descriptivo**")
            st.write("**Descripción:** Especialista en visualización avanzada y modelado de correlación lineal.")
            st.write("**Responsabilidades:** Creación del catálogo de visualizaciones gráficas avanzadas (Histogramas, Boxplots y Violin Plots) y desarrollo del modelo de regresión lineal simple para análisis de correlación COLI-Salario.")
            st.write("**Archivos clave:** `analisis/graficos.py`, `analisis/modelo_regresion.py`.")
            st.warning("🛠️ **Estado:** TAREAS PENDIENTES (Implementar Visualizaciones)")

    st.markdown("---")
    st.caption("© 2026 ESTADÍSTICA Y OPTIMIZACIÓN - GRUPO DE TRABAJO 1 (v.2.5.1-dev)")
