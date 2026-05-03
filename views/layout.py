import streamlit as st
import pandas as pd
import numpy as np
from analisis.estadisticos import calcular_estadisticos, calcular_estadisticos_por_categoria, detectar_outliers_iqr
from analisis.graficos import (
    crear_histograma, crear_boxplot, crear_bar_chart, crear_scatter_regresion, crear_violin_plot,
    crear_histograma_interactivo, crear_boxplot_interactivo, crear_bar_chart_interactivo,
    crear_scatter_regresion_interactivo, crear_violin_interactivo, crear_qq_plot
)
from analisis.inferencial import realizar_test_hipotesis, calcular_intervalos_confianza
from analisis.modelo_regresion import ejecutar_regresion_simple
import config.settings as cfg

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
        f"<div style='text-align: center; color: var(--text-color); opacity: 0.6; font-size: 0.85rem; font-style: italic;'>"
        f"© 2026 ESTADÍSTICA Y OPTIMIZACIÓN - GRUPO DE TRABAJO 1 (v.{cfg.VERSION})"
        "</div>", 
        unsafe_allow_html=True
    )

def render_escritorio(df, key, sym):
    st.title(f"🏠 Escritorio de Control - Rafael Rodriguez")
    
    import plotly.graph_objects as go
    
    # 1. Cálculos de base
    mean_val = df[key].mean()
    med_coli = df[cfg.COL_COLI].median()
    n_muestra = len(df)
    
    if 'work_setting' in df.columns:
        remote_pct = (df['work_setting'] == 'Remote').mean() * 100
    else:
        remote_pct = 0
        
    años_range = f"{df['work_year'].min()} - {df['work_year'].max()}"
    
    # 2. Diseño: Métricas y Gráfico de Aguja
    col_metrics, col_gauge = st.columns([1, 1])
    
    with col_metrics:
        r1_c1, r1_c2 = st.columns(2)
        r1_c1.metric("👥 Muestra", f"{n_muestra:,}")
        r1_c2.metric("🏠 Mediana COLI", f"{med_coli:,.2f}")
        
        r2_c1, r2_c2 = st.columns(2)
        r2_c1.metric("📡 % Remoto", f"{remote_pct:.1f}%")
        r2_c2.metric("📅 Periodo", años_range)

    with col_gauge:
        # Gráfico de Aguja para la divisa seleccionada
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = mean_val,
            number = {'prefix': sym, 'valueformat': ",.0f"},
            title = {'text': f"Media Salarial ({sym})", 'font': {'size': 16}},
            gauge = {
                'axis': {'range': [None, df[key].max() * 1.1]},
                'bar': {'color': "#00d1b2"},
                'steps': [
                    {'range': [0, df[key].median()], 'color': "lavender"},
                    {'range': [df[key].median(), df[key].max()], 'color': "ghostwhite"}
                ]
            }
        ))
        fig.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    st.markdown("---")
    st.markdown("### 📋 Vista Previa de Datos (Filtro Activo)")
    st.dataframe(df, use_container_width=True, height=400)

def render_estadisticos(df, key, sym):
    st.title("📊 Estadísticos Descriptivos - Rafael Rodriguez")
    
    st.markdown("### 📊 **Análisis de tendencia central y dispersión**")
    
    stats_df = calcular_estadisticos(df)
    st.dataframe(stats_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.subheader(f"📍 Salarios por Nivel de Experiencia ({sym})")
    cat_stats = calcular_estadisticos_por_categoria(df, key, 'experience_level')
    st.table(cat_stats)
    
    st.subheader("⚠️ Análisis de Outliers")
    outliers = detectar_outliers_iqr(df, key)
    st.table(outliers)

def render_visualizaciones(df, key, sym):
    st.title("📊 Visualizaciones Gráficas - Leslie Ross")
    
    # Una gráfica por fila para mayor visibilidad e interacción
    st.markdown("#### 📈 Distribución Salarial")
    fig_hist = crear_histograma_interactivo(df, key)
    st.plotly_chart(fig_hist, use_container_width=True)
    
    st.markdown("---")
    st.markdown("#### 📦 Salarios por Experiencia")
    fig_box = crear_boxplot_interactivo(df, key, 'experience_level')
    st.plotly_chart(fig_box, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 🏷️ Frecuencia de Roles (Top 10)")
    fig_bar = crear_bar_chart_interactivo(df, 'job_title')
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 🎻 Densidad de Probabilidad (Violin Plot)")
    fig_violin = crear_violin_interactivo(df, key, 'experience_level')
    st.plotly_chart(fig_violin, use_container_width=True)

def render_regresion(df, key, sym):
    st.title("📈 Regresión Lineal - Leslie Ross")
    
    # 1. Gráfico de dispersión interactivo
    fig_reg = crear_scatter_regresion_interactivo(df, cfg.COL_COLI, key)
    st.plotly_chart(fig_reg, use_container_width=True)
    
    # 2. Métricas del modelo (Rafael/Leslie colaborativo)
    try:
        modelo = ejecutar_regresion_simple(df, cfg.COL_COLI, key)
        c1, c2, c3 = st.columns(3)
        c1.metric("Coeficiente (Pendiente)", f"{modelo['coeficiente']:.2f}")
        c2.metric("Intercepción", f"{modelo['intercepto']:,.0f}")
        c3.metric("R² (Bondad de ajuste)", f"{modelo['r2']:.4f}")
        
        st.info(f"**Interpretación:** {modelo['interpretacion']}")
    except Exception as e:
        st.error(f"Error al ejecutar el modelo de regresión: {e}")

def render_inferencial(df, key, sym):
    st.title("🧪 Estadística Inferencial - Bryann Loza")
    
    # 1. Intervalo de Confianza
    st.subheader(f"📍 Estimación por Intervalo (95% Confianza) - {sym}")
    ic = calcular_intervalos_confianza(df, key)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Media Muestral", f"{ic['Media']:,.2f} {sym}")
    c2.metric("Límite Inferior", f"{ic['Límite Inferior']:,.2f} {sym}")
    c3.metric("Límite Superior", f"{ic['Límite Superior']:,.2f} {sym}")
    
    st.markdown("---")
    
    # 2. Contraste de Hipótesis
    st.subheader("⚖️ Contraste de Hipótesis")
    st.write("Comparación de medias entre categorías (Remoto vs Presencial, etc.)")
    
    if 'work_setting' in df.columns:
        st.write("**Contraste: Remoto vs Presencial**")
        res = realizar_test_hipotesis(df, key, 'work_setting')
        if "error" not in res:
            c1, c2 = st.columns(2)
            with c1:
                st.metric("Test Realizado", res['Test'])
                st.write(f"**Estadístico:** `{res.get('Estadístico', 0):.4f}`")
            with c2:
                st.metric("P-Valor", f"{res['P-Valor']:.4e}")
                st.write(f"**Significativo (5%):** {res['Significativo (5%)']}")
            
            if res['P-Valor'] < 0.05:
                st.success("Existe evidencia estadística suficiente para rechazar la hipótesis nula.")
            else:
                st.info("No hay evidencia suficiente para rechazar la hipótesis nula.")
        else:
            st.warning(res["error"])

    # 3. Verificación de Supuestos
    st.markdown("---")
    from analisis.inferencial import verificar_supuestos
    try:
        supuestos = verificar_supuestos(df[key])
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.write(f"**Prueba:** {supuestos['Prueba']}")
            st.write(f"**P-Valor:** `{supuestos['P-Valor']:.4e}`")
            
            p_val = supuestos['P-Valor']
            if p_val < 0.05:
                st.error("❌ Los datos NO siguen una distribución normal (P < 0.05).")
            else:
                st.success("✅ Los datos siguen una distribución normal (P >= 0.05).")
        
        with col_s2:
            fig_qq = crear_qq_plot(df[key])
            st.plotly_chart(fig_qq, use_container_width=True)
            
    except Exception as e:
        st.error(f"Error en verificación de supuestos: {e}")

def render_equipo():
    st.title("👥 Equipo de Desarrollo - Grupo 1")
    st.subheader("Estructura organizativa y estado de cumplimiento de los objetivos técnicos.")
    
    # Estilo de tarjeta para los miembros
    def member_card(nombre, rol, desc, resp, archivos, estado, icon="✅"):
        st.markdown(f"""
        <div style="border: 1px solid #0b84f4; border-radius: 10px; padding: 20px; margin-bottom: 20px; background-color: rgba(11, 132, 244, 0.05);">
            <h3 style="margin-top: 0;">{icon} {nombre}</h3>
            <p><b>{rol}</b></p>
            <p style="font-style: italic; font-size: 0.9rem;">{desc}</p>
            <hr style="margin: 10px 0; border-color: rgba(11, 132, 244, 0.2);">
            <p><b>Responsabilidades:</b> {resp}</p>
            <p><b>Archivos clave:</b> <code>{archivos}</code></p>
            <div style="text-align: right; font-weight: bold; color: #0b84f4;">Estado: {estado}</div>
        </div>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    
    with col1:
        member_card(
            "Rubén Gámez Torrijos", "Coordinador y Arquitectura",
            "Liderazgo técnico, diseño estructural y orquestación del proyecto.",
            "Diseño de la arquitectura modular de la aplicación, sistema de estilos CSS adaptativos para temas Light/Dark y desarrollo del motor de exportación profesional (PDF/Excel).",
            "app.py, analisis/exportacion.py, config/styles.py",
            "FINALIZADO Y VERIFICADO", "👑"
        )
        
        member_card(
            "Rafael Rodriguez Mengual", "Data Manager",
            "Especialista en procesamiento, limpieza y análisis descriptivo de datos.",
            "Implementación del pipeline de limpieza de datos, integración de variables externas (Índice de coste de vida) y desarrollo de la lógica para estadísticos de tendencia central y dispersión.",
            "analisis/utils.py, analisis/estadisticos.py",
            "FINALIZADO Y VERIFICADO", "📊"
        )

    with col2:
        member_card(
            "Bryann Vallejo Luna", "Analista Inferencial",
            "Experto en modelos probabilísticos y validación de hipótesis estadísticas.",
            "Desarrollo de modelos de probabilidad poblacional, cálculo de intervalos de confianza mediante T-Student y ejecución de contrastes de hipótesis paramétricos de una y dos muestras.",
            "analisis/inferencial.py, app.py (Sección Inferencia)",
            "FINALIZADO Y VERIFICADO", "🧪"
        )
        
        member_card(
            "Leslie Ross Aranibar Pozo", "Analista Descriptivo",
            "Especialista en visualización avanzada y modelado de correlación lineal.",
            "Creación del catálogo de visualizaciones gráficas avanzadas (Histogramas, Boxplots y Violin Plots) y desarrollo del modelo de regresión lineal simple para análisis de correlación COLI-Salario.",
            "analisis/graficos.py, analisis/modelo_regresion.py",
            "FINALIZADO Y VERIFICADO", "🎨"
        )

    st.markdown("---")
    st.caption(f"© 2026 ESTADÍSTICA Y OPTIMIZACIÓN - GRUPO DE TRABAJO 1 (v.{cfg.VERSION})")
