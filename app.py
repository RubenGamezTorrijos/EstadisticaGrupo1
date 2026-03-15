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
    """Genera un reporte Excel completo con pestañas para cada sección."""
    output = io.BytesIO()
    
    # 1. Datos del Escritorio
    df_escritorio = pd.DataFrame([
        {'Métrica': 'Total Registros', 'Valor': len(df)},
        {'Métrica': 'Media Salarial (USD)', 'Valor': df['salary_in_usd'].mean()},
        {'Métrica': 'Salario Máximo (USD)', 'Valor': df['salary_in_usd'].max()},
        {'Métrica': 'Año más reciente', 'Valor': df['work_year'].max()}
    ])
    
    # 2. Análisis Descriptivo
    df_stats = calcular_estadisticos(df)
    
    # 3. Estadística Inferencial
    ic_95 = calcular_ic_95(df['salary_in_usd'])
    test_exp = contraste_hipotesis(
        df[df['experience_level'] == 'Senior']['salary_in_usd'],
        df[df['experience_level'] == 'Mid-level']['salary_in_usd'],
        "Senior", "Mid-level"
    )
    df_inferencia = pd.DataFrame([
        {'Categoría': 'Intervalo Confianza (Inf)', 'Resultado': ic_95['Inferior']},
        {'Categoría': 'Intervalo Confianza (Sup)', 'Resultado': ic_95['Superior']},
        {'Categoría': 'P-Valor (Senior vs Mid)', 'Resultado': test_exp['P-Valor']},
        {'Categoría': 'Decisión Estadística', 'Resultado': test_exp['Decisión']}
    ])
    
    # 4. Equipo
    df_equipo = pd.DataFrame([
        {'Integrante': 'Rafael Rodriguez', 'Rol': 'Data Manager'},
        {'Integrante': 'Bryann Vallejo', 'Rol': 'Analista Inferencial'},
        {'Integrante': 'Leslie Ross', 'Rol': 'Analista Descriptivo'},
        {'Integrante': 'Ruben Gamez', 'Rol': 'Coordinador e Integrador'}
    ])

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_escritorio.to_excel(writer, index=False, sheet_name='1. Resumen Ejecutivo')
        df_stats.to_excel(writer, index=False, sheet_name='2. Estadisticos')
        df_inferencia.to_excel(writer, index=False, sheet_name='3. Inferencia')
        df_equipo.to_excel(writer, index=False, sheet_name='4. Equipo')
        df.to_excel(writer, index=False, sheet_name='5. Dataset Completo')
        
    return output.getvalue()

def create_pdf(df):
    """Genera un informe técnico completo con gráficos y explicaciones."""
    # Instanciar PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # --- PÁGINA 1: PORTADA ---
    pdf.add_page()
    pdf.set_font("helvetica", 'B', 24)
    pdf.set_text_color(11, 132, 244) # Azul Rubén
    pdf.cell(0, 60, "MEMORIA TÉCNICA", ln=True, align='C')
    pdf.set_font("helvetica", 'B', 16)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, "PROYECTO: ESTADÍSTICA Y OPTIMIZACIÓN", ln=True, align='C')
    pdf.cell(0, 10, "Análisis de Salarios en el Sector IT", ln=True, align='C')
    pdf.ln(30)
    
    # Listado de intervinientes en la portada
    pdf.set_font("helvetica", 'B', 12)
    pdf.set_text_color(11, 132, 244)
    pdf.cell(0, 10, "Integrantes del Equipo:", ln=True, align='C')
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("helvetica", size=10)
    
    pdf.cell(0, 7, "Rafael Rodriguez - Data Manager", ln=True, align='C')
    pdf.cell(0, 7, "Bryann Vallejo - Analista Inferencial", ln=True, align='C')
    pdf.cell(0, 7, "Leslie Ross - Analista Descriptivo", ln=True, align='C')
    pdf.cell(0, 7, "Rubén Gámez - Coordinador e Integrador", ln=True, align='C')
    
    pdf.ln(20)
    pdf.set_font("helvetica", 'I', 11)
    pdf.cell(0, 10, "Grupo 1 - Universidad Europea", ln=True, align='C')
    
    # --- PÁGINA 2: ESCRITORIO Y DESCRIPTIVA ---
    pdf.add_page()
    pdf.set_font("helvetica", 'B', 16)
    pdf.set_text_color(11, 132, 244)
    pdf.cell(0, 10, "1. Resumen Ejecutivo y Descriptivo", ln=True)
    pdf.ln(5)
    
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("helvetica", size=11)
    resumen_text = (
        f"El presente análisis se basa en un dataset de {len(df)} registros. "
        f"La media aritmética del salario se calcula sumando todos los valores de la muestra "
        f"y dividiendo entre N. En este caso, el salario medio es de ${df['salary_in_usd'].mean():,.2f} USD."
    )
    pdf.multi_cell(0, 7, resumen_text)
    pdf.ln(5)
    
    # Generar y añadir gráfico (Histograma)
    fig_hist = crear_histograma(df, 'salary_in_usd')
    img_buf = io.BytesIO()
    fig_hist.savefig(img_buf, format='png', bbox_inches='tight', dpi=150)
    pdf.image(img_buf, x=15, w=180)
    pdf.ln(5)
    
    # --- PÁGINA 3: ESTADÍSTICOS DETALLADOS ---
    pdf.add_page()
    pdf.set_font("helvetica", 'B', 14)
    pdf.cell(0, 10, "2. Estadísticos y Medidas de Dispersión", ln=True)
    pdf.ln(5)
    
    pdf.set_font("helvetica", size=10)
    pdf.multi_cell(0, 7, "A continuación se presentan las medidas de tendencia central y dispersión "
                   "calculadas mediante el módulo estadisticos.py:")
    pdf.ln(5)
    
    df_stats = calcular_estadisticos(df)
    stats_row = df_stats[df_stats['Variable'] == 'salary_in_usd'].iloc[0]
    
    # Dibujar tabla
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("helvetica", 'B', 10)
    pdf.cell(60, 10, "Métrica", border=1, fill=True)
    pdf.cell(60, 10, "Valor Calculado", border=1, fill=True, ln=True)
    pdf.set_font("helvetica", size=10)
    
    metricas = {
        'Media (Promedio)': f"${stats_row['Media']:,.2f}",
        'Mediana (Q2)': f"${stats_row['Mediana']:,.2f}",
        'Moda': f"${stats_row['Moda']:,.2f}",
        'Desviación Típica': f"{stats_row['Desviación Típica']:,.2f}",
        'Varianza': f"{stats_row['Varianza']:,.2f}",
        'Rango Salarial': f"${stats_row['Rango']:,.2f}"
    }
    
    for k, v in metricas.items():
        pdf.cell(60, 10, k, border=1)
        pdf.cell(60, 10, v, border=1, ln=True)
        
    # --- PÁGINA 4: ESTADÍSTICA INFERENCIAL ---
    pdf.add_page()
    pdf.set_font("helvetica", 'B', 16)
    pdf.set_text_color(11, 132, 244)
    pdf.cell(0, 10, "3. Estadística Inferencial", ln=True)
    pdf.ln(5)
    
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("helvetica", size=11)
    ic_95 = calcular_ic_95(df['salary_in_usd'])
    inf_text = (
        "Se ha aplicado una distribución T de Student para estimar la media poblacional real. "
        "Con un nivel de confianza del 95%, podemos afirmar que el verdadero salario medio "
        f"se encuentra en el intervalo [{ic_95['Inferior']:,.2f}, {ic_95['Superior']:,.2f}] USD. "
        f"El margen de error de esta estimación es de ±{ic_95['Margen Error']:,.2f} USD."
    )
    pdf.multi_cell(0, 7, inf_text)
    pdf.ln(10)
    
    pdf.set_font("helvetica", 'B', 14)
    pdf.cell(0, 10, "Contraste de Hipótesis", ln=True)
    test_exp = contraste_hipotesis(
        df[df['experience_level'] == 'Senior']['salary_in_usd'],
        df[df['experience_level'] == 'Mid-level']['salary_in_usd'],
        "Senior", "Mid-level"
    )
    pdf.set_font("helvetica", size=10)
    pdf.multi_cell(0, 7, f"H0: No hay diferencia entre Senior y Mid-level.\n"
                   f"P-Valor obtenido: {test_exp['P-Valor']:.4f}\n"
                   f"Resultado: {test_exp['Decisión']}. {test_exp['Conclusión']}.")
    
    # --- PÁGINA 5: EQUIPO ---
    pdf.add_page()
    pdf.set_font("helvetica", 'B', 16)
    pdf.cell(0, 20, "4. Equipo de Trabajo", ln=True, align='C')
    pdf.ln(10)
    
    equipo = [
        ("Rafael Rodriguez", "Data Manager - Limpieza y Estadísticos"),
        ("Bryann Vallejo", "Analista Inferencial - IC y Hipótesis"),
        ("Leslie Ross", "Visualization Expert - Gráficos y Regresión"),
        ("Rubén Gámez", "Coordinador - Integración y Arquitectura")
    ]
    
    pdf.set_font("helvetica", 'B', 12)
    for nombre, rol in equipo:
        pdf.set_text_color(11, 132, 244)
        pdf.cell(0, 10, nombre, ln=True)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("helvetica", size=10)
        pdf.cell(0, 7, rol, ln=True)
        pdf.ln(5)
        pdf.set_font("helvetica", 'B', 12)
        
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
