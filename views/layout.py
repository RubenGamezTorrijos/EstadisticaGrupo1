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
from config.utils import formatear_moneda, formatear_numero_entero, validar_datos_insuficientes, formatear_porcentaje

def render_main_layout(df, opcion, key, sym):
    """Orquesta el renderizado de la sección seleccionada."""
    
    if df is None or df.empty:
        st.warning("⚠️ No hay datos disponibles para los filtros seleccionados.")
        st.info("Por favor, ajusta los filtros en el menú lateral para visualizar los análisis.")
        render_footer()
        return

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
        r1_c1.metric("👥 Muestra", f"{n_muestra}")
        r1_c2.metric("🏠 Mediana COLI", f"{med_coli:.2f}")
        
        r2_c1, r2_c2 = st.columns(2)
        r2_c1.metric("📡 % Remoto", f"{remote_pct:.1f}%")
        
        min_year = formatear_numero_entero(df['work_year'].min())
        max_year = formatear_numero_entero(df['work_year'].max())
        r2_c2.metric("📅 Periodo", f"{min_year}-{max_year}")

    with col_gauge:
        # Gráfico de Aguja para la divisa seleccionada
        # Configurar el formato del número en el gauge (v.2.5.3)
        divisa_detectada = "EUR" if sym == "€" else "USD"
        val_formateado = formatear_moneda(mean_val, divisa_detectada)
        
        fig = go.Figure(go.Indicator(
            mode = "gauge",
            value = mean_val,
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
        # Sobrescribir el texto del valor para que use el formato de utils.py
        fig.add_annotation(
            x=0.5, y=0.15,
            text=val_formateado,
            showarrow=False,
            font=dict(size=32, color="#00d1b2", family="Arial Black")
        )
        fig.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    st.markdown("---")
    st.markdown("### 📋 Vista Previa de Datos (Filtro Activo)")
    st.dataframe(df, use_container_width=True, height=400)

def render_estadisticos(df, key, sym):
    st.title("📊 Estadísticos Descriptivos - Rafael Rodriguez")
    
    st.markdown("### 📊 **Análisis de tendencia central y dispersión**")
    
    stats_df = calcular_estadisticos(df)
    divisa = "EUR" if sym == "€" else "USD"
    df_display = stats_df.copy()
    
    def format_val(val, var_name, current_sym):
        if pd.isna(val):
            return "N/A"
        if "COLI" in str(var_name):
            return formatear_porcentaje(val, current_sym == "€")
        elif "USD" in str(var_name):
            return formatear_moneda(val, "USD")
        elif "EUR" in str(var_name):
            return formatear_moneda(val, "EUR")
        else:
            return formatear_moneda(val, "EUR" if current_sym == "€" else "USD")

    cols_to_format = ['Media', 'Mediana', 'Moda', 'Rango', 'Desviación Típica', 'Varianza', 'Mínimo', 'Máximo', 'Q1', 'Q3', 'IQR']
    for col in cols_to_format:
        df_display[col] = df_display.apply(
            lambda row: format_val(row[col], row['Variable'], sym), 
            axis=1
        )
    df_display['CV%'] = df_display['CV%'].apply(lambda x: formatear_porcentaje(x, sym == "€"))
    
    st.dataframe(df_display, use_container_width=True, hide_index=True)
    
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
    fig_hist = crear_histograma_interactivo(df, key, sym)
    st.plotly_chart(fig_hist, use_container_width=True)
    
    st.markdown("---")
    st.markdown("#### 📦 Salarios por Experiencia")
    fig_box = crear_boxplot_interactivo(df, key, 'experience_level', sym)
    st.plotly_chart(fig_box, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 🏷️ Frecuencia de Roles (Top 10)")
    fig_bar = crear_bar_chart_interactivo(df, 'job_title')
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 🎻 Densidad de Probabilidad (Violin Plot)")
    fig_violin = crear_violin_interactivo(df, key, 'experience_level', sym)
    st.plotly_chart(fig_violin, use_container_width=True)

def render_regresion(df, key, sym):
    st.title("📈 Regresión Lineal - Leslie Ross")
    
    # 1. Gráfico de dispersión interactivo
    fig_reg = crear_scatter_regresion_interactivo(df, cfg.COL_COLI, key, sym)
    st.plotly_chart(fig_reg, use_container_width=True)
    
    # 2. Métricas del modelo (Rafael/Leslie colaborativo)
    try:
        modelo = ejecutar_regresion_simple(df, cfg.COL_COLI, key)
        c1, c2, c3 = st.columns(3)
        c1.metric("Coeficiente (Pendiente)", f"{modelo['coeficiente']:.2f}".replace(".", "," if sym == "€" else "."))
        c2.metric("Intercepción", formatear_moneda(modelo['intercepto'], sym))
        c3.metric("R² (Bondad de ajuste)", f"{modelo['r2']:.4f}".replace(".", "," if sym == "€" else "."))
        
        st.info(f"**Interpretación:** {modelo['interpretacion']}")
    except Exception as e:
        st.error(f"Error al ejecutar el modelo de regresión: {e}")

def render_inferencial(df, key, sym):
    st.title("🧪 Estadística Inferencial - Bryann Loza")
    
    if not validar_datos_insuficientes(df):
        st.warning("⚠️ No hay suficientes datos para realizar el análisis inferencial con los filtros actuales.")
        return

    ic = calcular_intervalos_confianza(df, key)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Media Muestral", formatear_moneda(ic['Media'], key))
    c2.metric("Límite Inferior", formatear_moneda(ic['Límite Inferior'], key))
    c3.metric("Límite Superior", formatear_moneda(ic['Límite Superior'], key))
    
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
                p_val_fmt = f"{res['P-Valor']:.4f}".replace(".", "," if sym == "€" else ".")
                st.metric("P-Valor", p_val_fmt)
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
            p_val = supuestos['P-Valor']
            p_val_fmt = f"{p_val:.4f}".replace(".", "," if sym == "€" else ".")
            st.write(f"**P-Valor:** `{p_val_fmt}`")
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
    st.subheader("Estructura organizativa y cumplimiento de objetivos técnicos.")

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="border: 1px solid #0b84f4; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            <h4 style="color: #0b84f4; margin-top: 0;">👑 Rubén Gámez Torrijos - Coordinador Arquitecto Software</h4>
            <p style="font-style: italic; font-size: 0.9rem;">Liderazgo técnico, diseño estructural y orquestación del proyecto.</p>
            <hr style="margin: 10px 0;">
            <p style="font-size: 0.9rem;"><strong>Contribución:</strong></p>
            <ul style="font-size: 0.85rem;">
                <li>Arquitectura modular MVC y controladores.</li>
                <li>Motor de exportación profesional PDF/Excel.</li>
                <li>Sistema de estilos y gestión de configuración global.</li>
                <li>Integración de APIs externas (WorldBank/COLI).</li>
            </ul>
            <p style="font-size: 0.85rem;"><strong>Archivos:</strong><br>
            <code>app.py</code>, <code>config/</code>, <code>controllers/</code>, <code>views/</code>, <code>models/data_loader.py</code>, <code>config/api_client.py</code>, <code>requirements.txt</code>, <code>README.md</code>, <code>GUIA_COLABORACION.md</code></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="border: 1px solid #00d1b2; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            <h4 style="color: #00d1b2; margin-top: 0;">📊 Rafael Rodriguez Mengual - Data Manager Estadísticos</h4>
            <p style="font-style: italic; font-size: 0.9rem;">Especialista en procesamiento, limpieza y análisis descriptivo.</p>
            <hr style="margin: 10px 0;">
            <p style="font-size: 0.9rem;"><strong>Contribución:</strong></p>
            <ul style="font-size: 0.85rem;">
                <li>Pipeline de limpieza y validación de tipos.</li>
                <li>Lógica de estadísticos descriptivos.</li>
                <li>Gestión y detección de Outliers.</li>
                <li>Mapeo de datos internacionales.</li>
            </ul>
            <p style="font-size: 0.85rem;"><strong>Archivos:</strong><br>
            <code>estadisticos.py</code></p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="border: 1px solid #7c4dff; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            <h4 style="color: #7c4dff; margin-top: 0;">🧪 Bryann Vallejo Luna - Especialista Estadística Inferencial</h4>
            <p style="font-style: italic; font-size: 0.9rem;">Especialista en modelos probabilísticos y validación de hipótesis.</p>
            <hr style="margin: 10px 0;">
            <p style="font-size: 0.9rem;"><strong>Contribución:</strong></p>
            <ul style="font-size: 0.85rem;">
                <li>Desarrollo de modelos de probabilidad.</li>
                <li>Cálculo de intervalos de confianza.</li>
                <li>Ejecución de contrastes de hipótesis.</li>
                <li>Pruebas de normalidad (Shapiro-Wilk).</li>
            </ul>
            <p style="font-size: 0.85rem;"><strong>Archivos:</strong><br>
            <code>inferencial.py</code></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="border: 1px solid #ff4081; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            <h4 style="color: #ff4081; margin-top: 0;">🎨 Leslie Ross Aranibar Pozo - Especialista Gráficas y Regresión</h4>
            <p style="font-style: italic; font-size: 0.9rem;">Especialista en visualización avanzada y modelado de correlación.</p>
            <hr style="margin: 10px 0;">
            <p style="font-size: 0.9rem;"><strong>Contribución:</strong></p>
            <ul style="font-size: 0.85rem;">
                <li>Visualizaciones dinámicas Plotly.</li>
                <li>Desarrollo del modelo de regresión lineal.</li>
                <li>Análisis de correlación COLI-Salario.</li>
                <li>Visualizaciones comparativas.</li>
            </ul>
            <p style="font-size: 0.85rem;"><strong>Archivos:</strong><br>
            <code>graficos.py</code>, <code>modelo_regresion.py</code></p>
        </div>
        """, unsafe_allow_html=True)

    st.info("✅ Proyecto consolidado siguiendo los estándares de producción v.2.5.3")

def render_footer():
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray; font-size: 0.8rem;'>"
        "© 2026 ESTADÍSTICA Y OPTIMIZACIÓN - GRUPO DE TRABAJO 1 (v.2.5.3)"
        "</div>",
        unsafe_allow_html=True
    )
