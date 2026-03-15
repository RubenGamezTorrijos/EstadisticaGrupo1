import streamlit as st
import pandas as pd
import os
from analisis.estadisticos import limpiar_datos, calcular_estadisticos
from analisis.graficos import crear_histograma, crear_boxplot, crear_scatter_regresion, crear_bar_chart
from analisis.inferencial import calcular_ic_95, contraste_hipotesis, verificar_supuestos
import io
from fpdf import FPDF

"""
PROYECTO: Estadística para Ingeniería
INTEGRACIÓN Y UI: RUBEN GAMEZ TORRIJOS (Coordinador y Desarrollador)
App principal de Streamlit para visualizar el análisis estadístico.
"""
# Configuración de página RUBEN
st.set_page_config(
    page_title="Estadística - Salarios en IT",
    page_icon="🤖",
    layout="wide"
)

# Diccionario de traducción de variables para visualización
VAR_LABELS = {
    'work_year': 'Año de Trabajo',
    'experience_level': 'Nivel de Experiencia',
    'salary_in_usd': 'Salario (Moneda Dollar US)',
    'salary': 'Salario (Moneda Euro)',
    'job_category': 'Categoría de Puesto',
    'work_setting': 'Modalidad de Trabajo'
}

# Estilo Blue (#0B84F4) Adaptativo
st.markdown(f"""
    <style>
    /* Estilo para las métricas - Adaptativo */
    [data-testid="stMetric"] {{
        background-color: rgba(11, 132, 244, 0.05);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #0B84F4;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }}
    
    /* Contenedores de tablas */
    [data-testid="stTable"] {{
        background-color: transparent;
        border-radius: 8px;
    }}
    
    /* Barra lateral */
    [data-testid="stSidebar"] {{
        border-right: 1px solid rgba(11, 132, 244, 0.2);
    }}
    
    /* Títulos y acentos */
    h1, h2, h3 {{ 
        font-weight: 700; 
    }}
    
    /* Configuración de Pestañas (Tabs) - Adaptativo */
    .stTabs [data-baseweb="tab-list"] {{ 
        gap: 10px; 
    }}
    .stTabs [data-baseweb="tab"] {{ 
        height: 45px; 
        background-color: rgba(11, 132, 244, 0.05); 
        border-radius: 8px 8px 0 0; 
        color: inherit;
        padding: 0 20px !important;
        font-weight: 500;
        border: 1px solid transparent;
        transition: all 0.3s;
    }}
    .stTabs [data-baseweb="tab"]:hover {{
        border-color: #0B84F4;
        color: #0B84F4;
    }}
    .stTabs [aria-selected="true"] {{ 
        background-color: #0B84F4 !important; 
        color: white !important;
        border-bottom: 2px solid #0B84F4;
    }}
    
    /* Botones y Selectores */
    .stButton>button {{
        background-color: #0B84F4;
        color: white;
        border-radius: 8px;
        border: none;
        width: 100%;
    }}
    
    .stRadio [data-baseweb="radio"] div[aria-checked="true"] > div:first-child {{
        background-color: #0B84F4 !important;
        border-color: #0B84F4 !important;
    }}

    /* Ajuste para inputs en modo claro */
    .stSelectbox div[data-baseweb="select"] {{
        border-radius: 8px;
    }}
    </style>
""", unsafe_allow_html=True)

# Localización de números EUR / USD y Abreviaturas
def abbreviate_number(val):
    if val >= 1_000_000:
        return val / 1_000_000, "M"
    elif val >= 1_000:
        return val / 1_000, "K"
    return val, ""

def fmt_eur(val, is_int=False):
    """Formato Europa: 1.234,56"""
    try:
        val, suffix = abbreviate_number(val)
        if is_int and suffix == "":
            res = f"{val:,.0f}"
        else:
            res = f"{val:,.2f}"
            if res.endswith(".00"):
                res = res[:-3]
        return res.replace(",", "@").replace(".", ",").replace("@", ".") + suffix
    except:
        return val

def fmt_usd(val, is_int=False):
    """Formato USA: 1,234.56"""
    try:
        val, suffix = abbreviate_number(val)
        if is_int and suffix == "":
             res = f"{val:,.0f}"
        else:
             res = f"{val:,.2f}"
             if res.endswith(".00"):
                 res = res[:-3]
        return res + suffix
    except:
        return val

def format_currency(val, var_name, is_int=False):
    """Aplica el formato correcto según la variable."""
    if var_name == 'salary_in_usd':
        return fmt_usd(val, is_int)
    else:
        return fmt_eur(val, is_int)

@st.cache_data
def get_data():
    if not os.path.exists('datos/dataset_crudo.csv'):
        # Crear copia si no existe
        if os.path.exists('datos/jobs_in_data.csv'):
            import shutil
            shutil.copy('datos/jobs_in_data.csv', 'datos/dataset_crudo.csv')
    
    df = pd.read_csv('datos/dataset_crudo.csv')
    return limpiar_datos(df)

def create_excel(df):
    """Genera un reporte Excel con tres pestañas: Datos, Estadísticos e Inferencia."""
    output = io.BytesIO()
    
    # Obtener cálculos de los módulos
    df_stats = calcular_estadisticos(df)
    ic_95 = calcular_ic_95(df['salary_in_usd'])
    test_exp = contraste_hipotesis(
        df[df['experience_level'] == 'Senior']['salary_in_usd'],
        df[df['experience_level'] == 'Mid-level']['salary_in_usd'],
        "Senior", "Mid-level"
    )
    
    # Crear DataFrame para inferencia
    df_inferencia = pd.DataFrame([
        {'Concepto': 'Media Salarial', 'Valor': ic_95['Media']},
        {'Concepto': 'IC 95% Inferior', 'Valor': ic_95['Inferior']},
        {'Concepto': 'IC 95% Superior', 'Valor': ic_95['Superior']},
        {'Concepto': 'P-Valor (Senior vs Mid)', 'Valor': test_exp['P-Valor']},
        {'Concepto': 'Conclusión', 'Valor': test_exp['Conclusión']}
    ])

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='1. Dataset Original')
        df_stats.to_excel(writer, index=False, sheet_name='2. Estadisticos Descriptivos')
        df_inferencia.to_excel(writer, index=False, sheet_name='3. Inferencia Estadistica')
        
    return output.getvalue()

def create_pdf(df):
    """Genera un informe técnico completo en PDF."""
    # Obtener cálculos
    df_stats = calcular_estadisticos(df)
    ic_95 = calcular_ic_95(df['salary_in_usd'])
    
    pdf = FPDF()
    pdf.add_page()
    
    # Título Profesional
    pdf.set_font("helvetica", 'B', 18)
    pdf.set_text_color(11, 132, 244) # Azul Rubén
    pdf.cell(0, 15, "INFORME TÉCNICO: ANÁLISIS DE SALARIOS IT", ln=True, align='C')
    pdf.ln(10)
    
    # 1. Resumen Ejecutivo
    pdf.set_font("helvetica", 'B', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, "1. Resumen Descriptivo", ln=True)
    pdf.set_font("helvetica", size=10)
    pdf.multi_cell(0, 7, f"El dataset analizado contiene un total de {len(df)} registros válidos. "
                   f"La media salarial global se sitúa en los ${df['salary_in_usd'].mean():,.2f} USD.")
    pdf.ln(5)
    
    # Tabla de Estadísticos
    pdf.set_font("helvetica", 'B', 10)
    pdf.cell(50, 8, "Métrica", border=1)
    pdf.cell(50, 8, "Valor (USD)", border=1, ln=True)
    pdf.set_font("helvetica", size=9)
    
    # Extraer datos de la fila de 'salary_in_usd' del df_stats
    stats_row = df_stats[df_stats['Variable'] == 'salary_in_usd'].iloc[0]
    for metric in ['Media', 'Mediana', 'Desviación Típica', 'Rango']:
        pdf.cell(50, 7, metric, border=1)
        pdf.cell(50, 7, f"{stats_row[metric]:,.2f}", border=1, ln=True)
    pdf.ln(10)
    
    # 2. Análisis Inferencial
    pdf.set_font("helvetica", 'B', 14)
    pdf.cell(0, 10, "2. Análisis Inferencial (IC 95%)", ln=True)
    pdf.set_font("helvetica", size=10)
    pdf.multi_cell(0, 7, f"Se ha calculado el Intervalo de Confianza para la media salarial real con un nivel del 95%. "
                   f"Podemos afirmar que el salario medio poblacional se encuentra entre "
                   f"${ic_95['Inferior']:,.2f} y ${ic_95['Superior']:,.2f} USD.")
    pdf.ln(10)
    
    # Pie de página
    pdf.set_y(-30)
    pdf.set_font("helvetica", 'I', 8)
    pdf.cell(0, 10, "Informe generado automáticamente - Universidad Europea - Grupo 1", align='C')
    
    # IMPORTANTE: Convertir bytearray a bytes para que Streamlit lo procese bien
    return bytes(pdf.output())

def main():
    # Header de la barra lateral (Arquitectura Rubén)
    st.sidebar.markdown(f"""
        <div style="text-align: center; padding: 10px; border-radius: 50%; background-color: rgba(11, 132, 244, 0.1); border: 2px solid #0B84F4; width: 60px; height: 60px; margin: 0 auto 15px auto; display: flex; align-items: center; justify-content: center;">
            <span style="font-size: 30px;">📊</span>
        </div>
        <h2 style="text-align: center; margin-bottom: 25px;">Estadística y Optimización <br> Grupo 1</h2>
    """, unsafe_allow_html=True)
    st.sidebar.markdown("---")
    menu = st.sidebar.radio(
        "Seleccionar opción:",
        ["Escritorio General", "Análisis Descriptivo", "Estadística Inferencial", "Sobre el Equipo"]
    )

    df = get_data()

    # --- SECCIÓN DE EXPORTACIÓN (ARQUITECTURA RUBÉN) ---
    st.sidebar.markdown("---")
    st.sidebar.subheader("📥 Exportar Datos")
    
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        excel_data = create_excel(df)
        st.download_button(
            label="📊 Excel",
            data=excel_data,
            file_name="dataset_salarios_it.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
        
    with col2:
        try:
            pdf_data = create_pdf(df)
            st.download_button(
                label="📕 PDF",
                data=pdf_data,
                file_name="resumen_estadistico.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Error PDF: {str(e)}")

    if menu == "Escritorio General":
        st.title("🚀 Escritorio de Salarios en IT")
        st.markdown("Bienvenido al centro de control del análisis estadístico de salarios en Data Science.")
        
        # TODO (Rafael): Implementar las 4 métricas principales del Escritorio.
        # Usa st.columns(4) y st.metric() para mostrar:
        # 1. Total de registros (len(df))
        # 2. Media Salarial en USD (df['salary_in_usd'].mean())
        # 3. Último Año (df['work_year'].max())
        # 4. Total de Categorías distintas (df['job_category'].nunique())
        
        # --- Tu código aquí (aprox. 10 líneas) ---
        st.info("💡 **Zona de trabajo para Rafael:** Sustituye este mensaje por las 4 columnas de métricas (st.columns y st.metric).")

        st.markdown("### 📋 Vista Previa de Datos (Rafael Rodriguez)")
        
        # TODO (Rafael): Mostrar las primeras 10 filas del DataFrame 'df' renombrando las columnas.
        # 1. Extrae las primeras 10 filas: df.head(10)
        # 2. Renombra las columnas o simplemente dale formato si aplicas VAR_LABELS.
        # 3. Muestra la tabla usando st.dataframe().
        
        # --- Tu código aquí (aprox. 5 líneas) ---
        st.warning("⚠️ Renderizar la vista previa de datos aquí usando st.dataframe.")

    elif menu == "Análisis Descriptivo":
        st.title("📈 Análisis Descriptivo")
        st.write("Exploración detallada de la distribución y relaciones entre variables.")

        tab1, tab2, tab3 = st.tabs(["📊 Estadísticos", "🖼️ Visualizaciones", "📉 Regresión"])
        
        with tab1:
            st.subheader("Medidas Descriptivas (Rafael Rodriguez)")
            df_stats = calcular_estadisticos(df)
            if not df_stats.empty:
                # Estilos condicionales por fila
                def formato_fila(row):
                    if row['Variable'] == 'salary_in_usd':
                        fmt_func = fmt_usd
                    else:
                        fmt_func = fmt_eur
                    
                    return pd.Series([
                        fmt_func(row['Media']), fmt_func(row['Mediana']),
                        fmt_func(row['Moda']), fmt_func(row['Rango']),
                        fmt_func(row['Desviación Típica']), fmt_func(row['Varianza'])
                    ], index=['Media', 'Mediana', 'Moda', 'Rango', 'Desviación Típica', 'Varianza'])
                
                df_format = df_stats.copy()
                cols_to_format = ['Media', 'Mediana', 'Moda', 'Rango', 'Desviación Típica', 'Varianza']
                df_format[cols_to_format] = df_format.apply(formato_fila, axis=1)
                
                # Renombrar variables
                df_format['Variable'] = df_format['Variable'].map(VAR_LABELS).fillna(df_format['Variable'])
                st.table(df_format)
            
        with tab2:
            st.subheader("Histogramas y Boxplots (Leslie Ross)")
            col_var, col_cat = st.columns(2)
            with col_var:
                var_sel = st.selectbox("Seleccione Variable Numérica:", ['salary_in_usd', 'salary'], format_func=lambda x: VAR_LABELS.get(x, x))
            with col_cat:
                cat_sel = st.selectbox("Dividir por Categoría:", ['experience_level', 'job_category', 'work_setting'], format_func=lambda x: VAR_LABELS.get(x, x))
            
            c1, c2 = st.columns(2)
            with c1:
                st.pyplot(crear_histograma(df, var_sel))
            with c2:
                st.pyplot(crear_boxplot(df, var_sel, cat_sel))
                
        with tab3:
            st.subheader("Relación y Regresión (Leslie Ross)")
            st.markdown("Analizando la evolución salarial a lo largo de los años.")
            st.pyplot(crear_scatter_regresion(df, 'work_year', 'salary_in_usd'))

    elif menu == "Estadística Inferencial":
        st.title("🔬 Análisis Inferencial (Bryann Vallejo)")
        st.write("Deducciones estadísticas sobre la población total de profesionales.")

        st.subheader("1. Intervalos de Confianza (95%)")
        var_ic = st.selectbox("Variable para IC:", ['salary_in_usd', 'salary'], format_func=lambda x: VAR_LABELS.get(x, x))
        ic = calcular_ic_95(df[var_ic])
        
        moneda = "USD" if var_ic == 'salary_in_usd' else "EUR"
        
        c_ic1, c_ic2 = st.columns([2, 1])
        with c_ic1:
            st.success(f"Deducción para **{VAR_LABELS[var_ic]}**:")
            st.info(f"👉 **[{format_currency(ic['Inferior'], var_ic)}  —  {format_currency(ic['Superior'], var_ic)}] {moneda}**")
        with c_ic2:
            st.metric("Margen de Error", f"± {format_currency(ic['Margen Error'], var_ic)} {moneda}")
            st.metric("Media Muestral", f"{format_currency(ic['Media'], var_ic)} {moneda}")

        st.markdown("---")
        st.subheader("2. Contraste de Hipótesis")
        st.write("**Pregunta:** ¿Existe diferencia significativa entre salarios Senior y Mid-level?")
        
        sal_senior = df[df['experience_level'] == 'Senior']['salary_in_usd']
        sal_mid = df[df['experience_level'] == 'Mid-level']['salary_in_usd']
        
        res_test = contraste_hipotesis(sal_senior, sal_mid, "Nivel Senior", "Nivel Mid")
        
        c1, c2 = st.columns(2)
        with c1:
            if res_test['P-Valor'] < 0.0001:
                p_display = "< 0,0001"
            else:
                p_display = f"{res_test['P-Valor']:.4f}".replace(".", ",")
            st.metric("P-Valor Obtenido", p_display)
        with c2:
            st.metric("Decisión Estadística", res_test['Decisión'])
            
        st.warning(f"**Conclusión:** {res_test['Conclusión']}")
        st.caption(f"Valor p exacto: {res_test['P-Valor']:.2e}")

    elif menu == "Sobre el Equipo":
        st.title("👥 Equipo de Desarrollo")
        st.markdown("""
        Esta aplicación es el resultado del trabajo colaborativo de 4 ingenieros, siguiendo los requerimientos de la asignatura de Estadística.
        
        | Integrante | Rol | Archivos Desarrollados |
        | :--- | :--- | :--- |
        | **Rafael Rodriguez** | Data Manager | `analisis/estadisticos.py`, archivos CSV en `datos/` |
        | **Bryann Vallejo** | Analista Inferencial | `analisis/inferencial.py`, tablas CSV en `outputs/tablas/` |
        | **Leslie Ross** | Vis. Experta | `analisis/graficos.py`, `generate_plots.py`, gráficos PNG en `outputs/graficos/` |
        | **Ruben Gamez** | Desarrollador y Coordinador | `app.py`, `setup_data.py`, `requirements.txt`, `.gitignore` |
        """)
        
        st.info("💡 **Nota del Coordinador:** El proyecto cumple con todos los requisitos: muestra > 100, variables continuas/discretas/categóricas y análisis bivariable.")

if __name__ == "__main__":
    main()
