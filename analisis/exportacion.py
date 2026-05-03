"""
analisis/exportacion.py
=======================
Módulo para la generación de reportes profesionales en PDF y Excel.
"""

import pandas as pd
import os
from fpdf import FPDF
from io import BytesIO
import config.settings as cfg
from config.utils import formatear_moneda, formatear_porcentaje

def sanitize_pdf_text(text):
    """Limpia caracteres especiales para evitar errores en FPDF."""
    if text is None: return ""
    # El símbolo € no es soportado por las fuentes estándar (Helvetica/Times) en FPDF2 
    # sin cargar fuentes Unicode externas (.ttf). Reemplazamos por 'EUR' para evitar crashes.
    text_safe = str(text).replace('€', 'EUR')
    return text_safe.encode('latin-1', 'replace').decode('latin-1')

def generar_excel_multipestana(df_full, df_stats, df_inferencial, df_reg):
    """Genera un archivo Excel con múltiples pestañas."""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_full.to_excel(writer, sheet_name='Datos Filtrados', index=False)
        df_stats.to_excel(writer, sheet_name='Estadísticos Descriptivos', index=False)
        df_inferencial.to_excel(writer, sheet_name='Análisis Inferencial')
        if not df_reg.empty:
            df_reg.to_excel(writer, sheet_name='Modelo Regresión')
    return output.getvalue()

def generar_pdf_profesional(df, stats_df, equipo, graficos_dict, currency_label="USD"):
    """Genera un informe PDF con diseño profesional."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # --- PORTADA ---
    pdf.add_page()
    pdf.set_fill_color(30, 58, 138) # Azul corporativo
    pdf.rect(0, 0, 210, 297, 'F')
    
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 24)
    pdf.ln(60)
    pdf.cell(0, 20, sanitize_pdf_text('INFORME ESTADÍSTICO'), 0, 1, 'C')
    pdf.set_font('Helvetica', '', 16)
    pdf.cell(0, 10, sanitize_pdf_text('Análisis de Salarios y Coste de Vida (COLI)'), 0, 1, 'C')
    
    pdf.ln(100)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, sanitize_pdf_text('Grupo de Trabajo 1'), 0, 1, 'C')
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 5, sanitize_pdf_text('v.2.5.3 - Producción'), 0, 1, 'C')

    # --- EQUIPO ---
    pdf.add_page()
    pdf.set_text_color(30, 58, 138)
    pdf.set_font('Helvetica', 'B', 18)
    pdf.cell(0, 15, sanitize_pdf_text('1. Equipo de Proyecto'), 0, 1, 'L')
    pdf.ln(5)
    
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Helvetica', '', 12)
    for nombre, rol in equipo.items():
        pdf.set_font('Helvetica', 'B', 11)
        pdf.cell(60, 8, sanitize_pdf_text(nombre), 0, 0)
        pdf.set_font('Helvetica', '', 11)
        pdf.cell(0, 8, sanitize_pdf_text(f"- {rol}"), 0, 1)

    # --- RESUMEN EJECUTIVO ---
    pdf.ln(10)
    pdf.set_text_color(30, 58, 138)
    pdf.set_font('Helvetica', 'B', 18)
    pdf.cell(0, 15, sanitize_pdf_text('2. Resumen Ejecutivo'), 0, 1, 'L')
    
    w_text = pdf.epw
    
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Helvetica', '', 11)
    
    # Normalizar etiqueta de divisa para el reporte (v.2.5.3)
    # Nota: El símbolo € será convertido a 'EUR' en sanitize_pdf_text para evitar crashes en el PDF
    curr_display = "Euros (€)" if "EUR" in currency_label.upper() else "Dólares ($)"
    
    pdf.multi_cell(w_text, 8, sanitize_pdf_text(
        f"Este informe presenta el análisis estadístico detallado sobre una muestra de {len(df)} registros. "
        f"El análisis se ha centrado en la variable de remuneración utilizando {curr_display} como base monetaria "
        "y el índice COLI como factor de ajuste económico."
    ))

    # --- ESTADÍSTICOS ---
    pdf.add_page()
    pdf.set_text_color(30, 58, 138)
    pdf.set_font('Helvetica', 'B', 18)
    pdf.cell(0, 15, sanitize_pdf_text('3. Estadísticos Descriptivos'), 0, 1, 'L')
    
    pdf.set_fill_color(240, 240, 240)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Helvetica', 'B', 10)
    
    col_widths = [45, 35, 35, 40, 30]
    headers = ['Variable', 'Media', 'Mediana', 'Desv. Típica', 'CV%']
    
    for i, h in enumerate(headers):
        pdf.cell(col_widths[i], 10, sanitize_pdf_text(h), 1, 0, 'C', True)
    pdf.ln()
    
    pdf.set_font('Helvetica', '', 8)
    divisa = currency_label.split(" ")[0]
    es_euro = divisa == "EUR"

    for _, row in stats_df.iterrows():
        pdf.cell(col_widths[0], 8, sanitize_pdf_text(row['Variable']), 1, 0, 'L')
        
        is_coli = "COLI" in str(row['Variable'])
        
        if is_coli:
            val_media = formatear_porcentaje(row['Media'], es_euro)
            val_mediana = formatear_porcentaje(row['Mediana'], es_euro)
            val_desv = formatear_porcentaje(row['Desviación Típica'], es_euro)
        else:
            # Detectar moneda específica por variable (v.2.5.3)
            row_curr = divisa
            if "USD" in str(row['Variable']).upper():
                row_curr = "USD"
            elif "EUR" in str(row['Variable']).upper():
                row_curr = "EUR"
                
            val_media = formatear_moneda(row['Media'], row_curr)
            val_mediana = formatear_moneda(row['Mediana'], row_curr)
            val_desv = formatear_moneda(row['Desviación Típica'], row_curr)
        
        pdf.cell(col_widths[1], 8, sanitize_pdf_text(val_media), 1, 0, 'R')
        pdf.cell(col_widths[2], 8, sanitize_pdf_text(val_mediana), 1, 0, 'R')
        pdf.cell(col_widths[3], 8, sanitize_pdf_text(val_desv), 1, 0, 'R')
        pdf.cell(col_widths[4], 8, sanitize_pdf_text(formatear_porcentaje(row['CV%'], es_euro)), 1, 1, 'R')

    # --- INFERENCIAL ---
    pdf.ln(10)
    pdf.set_text_color(30, 58, 138)
    pdf.set_font('Helvetica', 'B', 18)
    pdf.cell(0, 15, sanitize_pdf_text('4. Análisis Inferencial'), 0, 1, 'L')
    
    from analisis.inferencial import calcular_intervalos_confianza, realizar_test_hipotesis, verificar_supuestos
    
    # 4.1 Intervalos de Confianza
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 10, sanitize_pdf_text('4.1 Intervalos de Confianza (95%)'), 0, 1)
    pdf.set_font('Helvetica', '', 10)
    
    # Salario
    target_col = cfg.COL_SALARIO_DINAMICO if cfg.COL_SALARIO_DINAMICO in df.columns else cfg.COL_SALARIO_USD
    ic_salario = calcular_intervalos_confianza(df, target_col)
    pdf.cell(0, 8, sanitize_pdf_text(f"- Salario: [{formatear_moneda(ic_salario['Límite Inferior'], divisa)} , {formatear_moneda(ic_salario['Límite Superior'], divisa)}]"), 0, 1)
    
    # COLI
    ic_coli = calcular_intervalos_confianza(df, cfg.COL_COLI)
    pdf.cell(0, 8, sanitize_pdf_text(f"- Índice COLI: [{formatear_porcentaje(ic_coli['Límite Inferior'], es_euro)} , {formatear_porcentaje(ic_coli['Límite Superior'], es_euro)}]"), 0, 1)
    
    # 4.2 Pruebas de Normalidad
    pdf.ln(5)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 10, sanitize_pdf_text('4.2 Pruebas de Normalidad (Distribución)'), 0, 1)
    pdf.set_font('Helvetica', '', 10)
    
    sup_salario = verificar_supuestos(df[target_col])
    sup_coli = verificar_supuestos(df[cfg.COL_COLI])
    
    def fmt_pval(p):
        if p < 0.0001 and p > 0: return f"{p:.2e}".replace(".", "," if es_euro else ".")
        return f"{p:.4f}".replace(".", "," if es_euro else ".")

    # Asegurar margen izquierdo y ancho efectivo
    pdf.multi_cell(w_text, 8, sanitize_pdf_text(f"- Salario ({sup_salario['Prueba']}): Estadístico={sup_salario['Stat']:.4f}, P-Valor={fmt_pval(sup_salario['P-Valor'])}. {'Sigue' if sup_salario['P-Valor'] > 0.05 else 'No sigue'} distribución normal."))
    pdf.ln(2)
    pdf.multi_cell(w_text, 8, sanitize_pdf_text(f"- COLI ({sup_coli['Prueba']}): Estadístico={sup_coli['Stat']:.4f}, P-Valor={fmt_pval(sup_coli['P-Valor'])}. {'Sigue' if sup_coli['P-Valor'] > 0.05 else 'No sigue'} distribución normal."))

    # 4.3 Contrastes de Hipótesis por Categoría
    pdf.ln(5)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 10, sanitize_pdf_text('4.3 Contrastes de Hipótesis (por Nivel de Experiencia)'), 0, 1)
    pdf.set_font('Helvetica', '', 10)
    
    test_cat = realizar_test_hipotesis(df, target_col, 'experience_level')
    if "error" not in test_cat:
        stat_val = test_cat['Estadístico']
        pdf.multi_cell(w_text, 8, sanitize_pdf_text(f"- {test_cat['Test']}: Estadístico={stat_val:.4f}, P-Valor={fmt_pval(test_cat['P-Valor'])}. Diferencia significativa: {test_cat['Significativo (5%)']}."))
    else:
        pdf.multi_cell(w_text, 8, sanitize_pdf_text(f"- {test_cat['error']}"))

    # --- REGRESIÓN ---
    pdf.ln(10)
    pdf.set_text_color(30, 58, 138)
    pdf.set_font('Helvetica', 'B', 18)
    pdf.cell(0, 15, sanitize_pdf_text('5. Modelo de Regresión Lineal'), 0, 1, 'L')
    
    from analisis.modelo_regresion import ejecutar_regresion_simple
    reg = ejecutar_regresion_simple(df, cfg.COL_COLI, target_col)
    
    if reg:
        pdf.set_text_color(0, 0, 0)
        pdf.set_font('Helvetica', '', 10)
        pdf.cell(0, 8, sanitize_pdf_text(f"- Variable Independiente (X): Índice COLI"), 0, 1)
        pdf.cell(0, 8, sanitize_pdf_text(f"- Variable Dependiente (Y): Salario"), 0, 1)
        pdf.cell(0, 8, sanitize_pdf_text(f"- Coeficiente de Determinación (R2): {reg['r2']:.4f}"), 0, 1)
        pdf.cell(0, 8, sanitize_pdf_text(f"- Ecuación: Y = {reg['coeficiente']:.2f}X + {reg['intercepto']:.2f}"), 0, 1)
        pdf.multi_cell(w_text, 8, sanitize_pdf_text(f"- Correlación: La relación es {'fuerte' if abs(reg['r2']) > 0.7 else 'moderada' if abs(reg['r2']) > 0.4 else 'débil'}."))

    # --- VISUALIZACIONES (Incluyendo Violin Plot) ---
    pdf.add_page()
    pdf.set_text_color(30, 58, 138)
    pdf.set_font('Helvetica', 'B', 18)
    pdf.cell(0, 15, sanitize_pdf_text('6. Visualizaciones Estadísticas'), 0, 1, 'L')
    
    if not os.path.exists("outputs/temp"):
        os.makedirs("outputs/temp")

    for titulo, fig in graficos_dict.items():
        if fig is not None:
            temp_path = f"outputs/temp/{titulo.lower().replace(' ', '_')}.png"
            fig.savefig(temp_path, dpi=150, bbox_inches='tight')
            
            # Verificar si cabe en la página o necesita nueva
            if pdf.get_y() > 200:
                pdf.add_page()
                
            pdf.set_text_color(0, 0, 0)
            pdf.set_font('Helvetica', 'B', 12)
            pdf.cell(0, 10, sanitize_pdf_text(titulo), 0, 1, 'C')
            pdf.image(temp_path, x=20, w=170)
            pdf.ln(5)
            
            # Limpiar temporal
            if os.path.exists(temp_path):
                os.remove(temp_path)

    # --- CONCLUSIONES ---
    pdf.add_page()
    pdf.set_text_color(30, 58, 138)
    pdf.set_font('Helvetica', 'B', 18)
    pdf.cell(0, 15, sanitize_pdf_text('7. Conclusiones y Análisis Crítico'), 0, 1, 'L')
    
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Helvetica', '', 11)
    conclusiones = [
        "1. El análisis descriptivo revela una alta variabilidad salarial entre categorías, con una concentración significativa en roles senior.",
        "2. Se observa una correlación positiva moderada entre el índice de coste de vida (COLI) y los salarios brutos, sugiriendo que las empresas ajustan parcialmente la remuneración según la ubicación.",
        "3. Las pruebas de normalidad indican que los salarios no siguen una distribución normal perfecta, lo que justifica el uso de métodos robustos.",
        "4. El modelo de regresión permite estimar el salario base con un margen de confianza aceptable, aunque existen factores no observados que influyen en la varianza.",
        "5. La integración de la métrica COLI aporta una dimensión crítica para entender el poder adquisitivo real más allá del salario nominal."
    ]
    
    for conc in conclusiones:
        pdf.multi_cell(w_text, 10, sanitize_pdf_text(conc))
        pdf.ln(2)

    # --- PIE DE PÁGINA ---
    pdf.set_y(-15)
    pdf.set_font('Helvetica', 'I', 8)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 10, sanitize_pdf_text('© 2026 ESTADÍSTICA Y OPTIMIZACIÓN - GRUPO DE TRABAJO 1 (v.2.5.3)'), 0, 0, 'C')

    return bytes(pdf.output())
