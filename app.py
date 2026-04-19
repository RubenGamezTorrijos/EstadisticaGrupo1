import streamlit as st
import pandas as pd
import numpy as np
import os
import shutil
from datetime import datetime

# Importaciones locales
from analisis.estadisticos import limpiar_datos, calcular_estadisticos, calcular_estadisticos_por_categoria
from analisis.graficos import (
    crear_histograma, crear_boxplot, crear_violin_plot, 
    crear_scatter_regresion, crear_bar_chart, crear_grafico_comparativo_ic
)
from analisis.inferencial import (
    calcular_ic_95, contraste_hipotesis, verificar_supuestos_normalidad
)
from analisis.modelo_regresion import render_regresion
from analisis.exportacion import generar_excel_multipestana, generar_pdf_profesional

# Configuración de página
st.set_page_config(
    page_title="PROYECTO ESTADÍSTICA - Grupo 1",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS profesionales
st.markdown("""
<style>
    /* Estética Adaptativa: Glassmorphism */
    .stApp {
        background-attachment: fixed;
    }
    
    /* Contenedores de tarjetas y métricas ADAPTATIVOS */
    div[data-testid="stMetric"], div[data-testid="stExpander"], div[data-testid="stTable"] {
        background: rgba(128, 128, 128, 0.1) !important;
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 12px;
        backdrop-filter: blur(8px);
        padding: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(11, 132, 244, 0.15);
        border-color: rgba(11, 132, 244, 0.4);
    }

    /* Sidebar Identidad Navy Blue Persistente */
    .stSidebar {
        background-color: #0c1c30 !important;
    }
    
    /* Títulos Adaptativos y Robustos */
    h1, h2, h3 {
        color: #0b84f4 !important; /* Azul cobalto para máxima legibilidad */
        font-weight: 800 !important;
        padding-bottom: 5px;
        margin-top: 20px;
        letter-spacing: -0.01em;
    }

    /* Asegurar que el texto normal no se pierda en ningún tema */
    p, span, label, .stMarkdown {
        color: var(--text-color) !important;
    }

    /* Botones y Selectores */
    .stButton>button {
        border-radius: 8px;
        background-color: #0b84f4;
        color: white;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #0d6efd;
        box-shadow: 0 4px 12px rgba(13, 110, 253, 0.3);
    }

    /* Estilo para los tags de multiselect (filtros seleccionados) */
    span[data-baseweb="tag"] {
        background-color: #0b84f4 !important;
        color: white !important;
        border-radius: 4px !important;
    }
    
    span[data-baseweb="tag"] svg {
        fill: white !important;
    }
</style>
""", unsafe_allow_html=True)

# --- CARGA DE DATOS ---
@st.cache_data
def load_data():
    """Carga y limpieza inicial de datos."""
    df_raw = pd.read_csv('datos/jobs_in_data.csv')
    df = limpiar_datos(df_raw)
    
    # Asegurar columna EUR si no existe
    if 'salary_in_eur' not in df.columns:
        df['salary_in_eur'] = df['salary_in_usd'] * 0.92
        
    return df

def main():
    df_full = load_data()
    
    # --- SIDEBAR: LOGO Y TÍTULO ---
    with st.sidebar:
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
        
        # 🟢 MEJORA: SELECTOR DE DIVISA GLOBAL
        st.subheader("⚙️ Configuración")
        divisa_label = st.radio(
            "Seleccionar Divisa Global:",
            ["USD $", "EUR €"],
            index=0,
            help="Cambia todos los cálculos y gráficos a la moneda elegida."
        )
        
        divisa_key = 'salary_in_usd' if "USD" in divisa_label else 'salary_in_eur'
        simbolo = "$" if "USD" in divisa_label else "€"
        
        st.markdown("---")
        
        # Navegación mejorada
        opcion = st.radio(
            "Navegación del Proyecto:",
            ["Escritorio General", "Estadísticos Descriptivos", "Visualizaciones Gráficas", 
             "Estadística Inferencial", "Regresión Lineal", "Equipo Grupo 1"]
        )
        
        st.markdown("---")
        
        # FILTROS GLOBALES
        st.subheader("🔍 Filtros de Muestra")
        exp_filter = st.multiselect("Nivel Experiencia:", df_full['experience_level'].unique(), default=df_full['experience_level'].unique())
        
        # --- FILTRO 3: Países (Localización Empresa) ---
        all_countries = sorted(df_full['company_location'].unique())
        selected_countries = st.multiselect(
            "📍 Filtrar por Países",
            options=all_countries,
            default=[],
            help="Si no seleccionas ninguno, se mostrarán todos."
        )
        
        # --- FILTRO 4: Categoría de Puesto ---
        cat_filter = st.multiselect("Categoría Puesto:", df_full['job_category'].unique(), default=df_full['job_category'].unique())
        
        # Lógica de filtrado
        df_filtered = df_full.copy()
        df_filtered = df_filtered[df_filtered['experience_level'].isin(exp_filter)]
        df_filtered = df_filtered[df_filtered['job_category'].isin(cat_filter)]
        if selected_countries:
            df_filtered = df_filtered[df_filtered['company_location'].isin(selected_countries)]

        # --- NUEVA SECCIÓN: Exportación ---
        handle_exports(df_filtered, divisa_label, simbolo, divisa_key)

    # --- LÓGICA DE SECCIONES ---
    if opcion == "Escritorio General":
        render_escritorio(df_filtered, divisa_key, simbolo)
    elif opcion == "Estadísticos Descriptivos":
        render_estadisticos(df_filtered, divisa_key, simbolo)
    elif opcion == "Visualizaciones Gráficas":
        render_visualizaciones(df_filtered, divisa_key, simbolo)
    elif opcion == "Regresión Lineal":
        render_regresion(df_filtered, divisa_key, simbolo)
    elif opcion == "Estadística Inferencial":
        render_inferencial(df_filtered, divisa_key, simbolo)
    elif opcion == "Equipo Grupo 1":
        render_equipo()

def render_escritorio(df, key, sym):
    st.title("🏠 Escritorio de Control")
    st.write("Resumen ejecutivo de la muestra actual analizada.")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Muestra (N)", len(df))
    with col2:
        st.metric(f"Salario Medio ({sym})", f"{df[key].mean():,.0f} {sym}")
    with col3:
        st.metric("Mediana COLI", f"{df['cost_of_living_index'].median():,.0f}")
    with col4:
        st.metric("Años en Muestra", f"{df['work_year'].nunique()}")
        
    st.markdown("### 📋 Vista Previa de Datos")
    st.dataframe(df.head(10), use_container_width=True)

def render_estadisticos(df, key, sym):
    st.title("📊 Estadísticos Descriptivos")
    st.write("Análisis detallado de tendencia central, dispersión y forma.")
    
    # Tabla Unificada Profecional
    stats_df = calcular_estadisticos(df)
    
    # Formatear para visualización
    st.dataframe(stats_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.subheader(f"📍 Análisis por Nivel de Experiencia ({sym})")
    cat_stats = calcular_estadisticos_por_categoria(df, key, 'experience_level')
    st.table(cat_stats)

def render_visualizaciones(df, key, sym):
    st.title("📈 Visualizaciones de Muestra")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Distribución de Salarios")
        fig_hist = crear_histograma(df, key, f"Histograma de Salarios ({sym})")
        st.pyplot(fig_hist)
        
    with col2:
        st.subheader("Dispersión por Experiencia")
        fig_box = crear_boxplot(df, key, 'experience_level', f"Distribución de Salarios por Nivel ({sym})")
        st.pyplot(fig_box)
        
    st.markdown("---")
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Distribución de Densidad (Violin)")
        fig_violin = crear_violin_plot(df, 'experience_level', key, f"Violin Plot: Salario vs Experiencia ({sym})")
        st.pyplot(fig_violin)
    with col4:
        st.subheader("Presencia por Categoría")
        fig_bar = crear_bar_chart(df, 'job_category', titulo="Top Categorías de Empleo")
        st.pyplot(fig_bar)

def render_regresion(df, key, sym):
    st.title("📈 Análisis de Inferencia Poblacional mediante Regresión")
    st.write("**Metodología:** Evaluación de la dependencia lineal entre el Coste de Vida (COLI) y el Salario.")
    
    fig_reg, stats = crear_scatter_regresion(df, 'cost_of_living_index', key, f"Regresión: Salario ({sym}) vs COLI")
    st.pyplot(fig_reg)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Correlación (r)", f"{stats['correlacion']:.4f}")
    c2.metric("Coef. Determinación (R²)", f"{stats['r_cuadrado']:.4f}")
    c3.metric("Pendiente", f"{stats['pendiente']:.2f}")
    
    st.info(f"Interpretación: Un coeficiente de {stats['correlacion']:.4f} indica una correlación {'fuerte' if abs(stats['correlacion']) > 0.7 else 'moderada' if abs(stats['correlacion']) > 0.4 else 'débil'} entre el coste de vida y el salario.")

def render_inferencial(df, key, sym):
    st.title("🧪 Estadística Inferencial y Contrastes")
    st.write("Análisis de probabilidad para validar hipótesis poblacionales sobre los salarios IT y el coste de vida.")
    
    # --- SECCIÓN 1: INTERVALO DE CONFIANZA SALARIO ---
    st.markdown(f"### 1. Estimación Salarial (Confianza 95%) - {sym}")
    ic_results = calcular_ic_95(df[key])
    
    with st.container():
        c1, c2, c3 = st.columns(3)
        if 'Media' in ic_results:
            c1.metric("Media Muestral (x̄)", f"{ic_results['Media']:,.2f} {sym}")
            c2.metric("Límite Inferior", f"{ic_results['Inferior']:,.2f} {sym}")
            c3.metric("Límite Superior", f"{ic_results['Superior']:,.2f} {sym}")
            st.info(f"💡 **Interpretación Salario:** Con un 95% de confianza, estimamos que el salario medio real se encuentra entre **{ic_results['Inferior']:,.2f} {sym} y {ic_results['Superior']:,.2f} {sym}**.")
        else:
            st.warning("No hay datos suficientes para calcular el intervalo del salario.")

    st.markdown("---")

    # --- SECCIÓN 2: INTERVALO DE CONFIANZA COLI ---
    st.markdown("### 2. Estimación Coste de Vida (Confianza 95%) - COLI")
    ic_coli = calcular_ic_95(df['cost_of_living_index'])
    
    with st.container():
        cc1, cc2, cc3 = st.columns(3)
        if 'Media' in ic_coli:
            cc1.metric("Media COLI (μ)", f"{ic_coli['Media']:,.2f}")
            cc2.metric("Límite Inferior", f"{ic_coli['Inferior']:,.2f}")
            cc3.metric("Límite Superior", f"{ic_coli['Superior']:,.2f}")
            st.info(f"💡 **Interpretación COLI:** El índice de coste de vida promedio poblacional se sitúa entre **{ic_coli['Inferior']:,.2f} y {ic_coli['Superior']:,.2f}**.")
        else:
            st.warning("No hay datos suficientes para calcular el intervalo del COLI.")

    st.markdown("---")
    
    # --- SECCIÓN 3: CONTRASTE 1 (EXPERIENCIA) ---
    st.markdown("### 3. Contraste de Hipótesis: ¿Influye la Experiencia?")
    
    col_left, col_right = st.columns([1, 1.5])
    
    with col_left:
        st.markdown("**Planteamiento del Test:**")
        st.warning("**H₀ (Nula):** No hay diferencia de salario entre niveles 'Senior' y 'Mid-level'.")
        st.info("**H₁ (Alternativa):** El nivel 'Senior' percibe un salario significativamente distinto.")
        
        g1 = df[df['experience_level'] == 'Senior'][key]
        g2 = df[df['experience_level'] == 'Mid-level'][key]
        
        if len(g1) > 1 and len(g2) > 1:
            test_res = contraste_hipotesis(g1, g2, "Senior", "Mid-level")
            
            # Tarjetas de resultados
            c_a, c_b = st.columns(2)
            c_a.metric("p-valor", f"{test_res['p_valor']:.4f}", delta="Significativo" if test_res['rechaza_h0'] else "No Sig.", delta_color="normal")
            c_b.metric("Estadístico T", f"{test_res['t_statistic']:.2f}")
            
            if test_res['rechaza_h0']:
                st.success("✅ **Conclusión:** Existe evidencia suficiente para **RECHAZAR H₀**. La diferencia salarial es real.")
            else:
                st.error("⚠️ **Conclusión:** No hay evidencia para rechazar H₀. Las diferencias observadas pueden ser azarosas.")
        else:
            st.warning("Muestras insuficientes para comparar Senior vs Mid-level.")
                
    with col_right:
        # Gráfico Comparativo de IC para este test
        df_comp = df[df['experience_level'].isin(['Senior', 'Mid-level'])]
        if not df_comp.empty:
            fig_ic_exp = crear_grafico_comparativo_ic(df_comp, 'experience_level', key, "Comparativa IC 95%: Senior vs Mid-level")
            st.pyplot(fig_ic_exp)

    st.markdown("---")
    
    # --- SECCIÓN 4: CONTRASTE 2 (MODALIDAD) ---
    st.markdown("### 4. Contraste de Hipótesis: ¿Importa la Modalidad?")
    
    cl, cr = st.columns([1, 1.5])
    
    with cl:
        st.markdown("**Planteamiento del Test:**")
        st.warning("**H₀ (Nula):** El salario es igual para trabajos 'Remote' y 'In-person'.")
        st.info("**H₁ (Alternativa):** La modalidad de trabajo afecta significativamente a la remuneración.")
        
        r1 = df[df['work_setting'] == 'Remote'][key]
        r2 = df[df['work_setting'] == 'In-person'][key]
        
        if len(r1) > 1 and len(r2) > 1:
            test_remoto = contraste_hipotesis(r1, r2, "Remoto", "Presencial")
            
            # Tarjetas de resultados
            res1, res2 = st.columns(2)
            res1.metric("p-valor", f"{test_remoto['p_valor']:.4f}", delta="Significativo" if test_remoto['rechaza_h0'] else "No Sig.", delta_color="normal")
            res2.metric("Estadístico T", f"{test_remoto['t_statistic']:.2f}")
            
            if test_remoto['rechaza_h0']:
                st.success("✅ **Conclusión:** Existe una diferencia significativa según la modalidad.")
            else:
                st.error("⚠️ **Conclusión:** La modalidad de trabajo NO parece ser un factor determinante en el salario.")
        else:
            st.warning("Muestras insuficientes para comparar Remoto vs Presencial.")
                
    with cr:
        # Gráfico Comparativo de IC para este test
        df_mod = df[df['work_setting'].isin(['Remote', 'In-person'])]
        if not df_mod.empty:
            fig_ic_mod = crear_grafico_comparativo_ic(df_mod, 'work_setting', key, "Comparativa IC 95%: Remoto vs Presencial")
            st.pyplot(fig_ic_mod)

def render_equipo():
    st.title("👥 Equipo de Desarrollo - Grupo 1")
    st.markdown("""
    ### Miembros y Roles Técnicos Actualizados (v.2.0.5):
    
    *   **Rubén Gámez Torrijos (Coordinador de Proyecto)**
        *   **Tareas:** Estructura modular, UI Blue-Aesthetic, Selector de Divisa Global, Exportación técnica (PDF/Excel) y Control de Calidad.
        *   *Estado:* Finalizado - Soporte multidivisa y Mejora 2 integrados.
        
    *   **Rafael Rodriguez Mengual (Data Manager)**
        *   **Tareas:** Limpieza de datos avanzada, integración de la mejora COLI y tabla de estadísticos unificada (N, media, mediana, moda, rango, etc.).
        *   *Estado:* Finalizado - Motor estadístico 100% funcional.
        
    *   **Bryann Vallejo Luna (Analista Inferencial)**
        *   **Tareas:** Cálculo de Intervalos de Confianza (T-Student) y Contrastes de Hipótesis de 1 y 2 muestras.
        *   *TODO:* Refinar las justificaciones de los contrastes en la rama `dev`.
        
    *   **Leslie Ross Aranibar Pozo (Analista Descriptivo)**
        *   **Tareas:** Visualizaciones estadísticas de alta resolución (Histogramas, Boxplots, Violin Plots) y Análisis de Regresión Lineal.
        *   *TODO:* Sincronizar los 5+ gráficos finales en la rama `dev`.
    
    ---
    *© 2026 ESTADÍSTICA Y OPTIMIZACIÓN - GRUPO DE TRABAJO 1 (Producción).*
    """)

def handle_exports(df_filtered, currency_label, current_sym, divisa_key):
    st.sidebar.markdown("---")
    st.sidebar.subheader("📥 Exportar Resultados")
    
    # 1. Preparar datos para Excel (4 pestañas)
    df_stats = calcular_estadisticos(df_filtered)
    
    # Datos de Inferencia (Resumen básico para Excel)
    ic_95 = calcular_ic_95(df_filtered[divisa_key])
    df_inferencial = pd.DataFrame([ic_95]).T
    df_inferencial.columns = ['Valor']
    
    # Datos de Regresión
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
    
    # 2. Preparar PDF (Descarga Directa)
    # Generamos los gráficos necesarios para el informe
    with st.sidebar:
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
        
        filtros_txt = "Filtros activos en esta muestra."
        
        pdf_bytes = generar_pdf_profesional(df_filtered, df_stats, equipo_roles, graficos_dict, currency_label, filtros_txt)
        
        st.sidebar.download_button(
            label="📄 Descargar Informe PDF",
            data=pdf_bytes,
            file_name=f"informe_estadistica_grupo1_{currency_label.replace(' ', '_')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

if __name__ == "__main__":
    main()
