import pandas as pd
import io
import os
from fpdf import FPDF
import tempfile
from datetime import datetime
from analisis.graficos import sanitize_pdf_text

def generar_excel_multipestana(df_filtered, df_stats, df_inferencial, df_regresion):
    """
    Genera un archivo Excel con 4 pestañas profesionales.
    """
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Pestaña 1: Datos Listado
        df_filtered.to_excel(writer, sheet_name='1. Datos Filtrados', index=False)
        
        # Pestaña 2: Estadísticos Descriptivos
        df_stats.to_excel(writer, sheet_name='2. Estadísticos', index=False)
        
        # Pestaña 3: Inferencia Estadística
        if df_inferencial is not None:
            df_inferencial.to_excel(writer, sheet_name='3. Inferencia', index=True)
        
        # Pestaña 4: Regresión Lineal
        if df_regresion is not None:
            df_regresion.to_excel(writer, sheet_name='4. Regresión', index=True)
        
    return output.getvalue()

class PDFReport(FPDF):
    def header(self):
        # Fondo azul en la cabecera
        self.set_fill_color(11, 132, 244) # Blue Aesthetic #0b84f4
        self.rect(0, 0, 210, 35, 'F')
        
        self.set_font('Helvetica', 'B', 22)
        self.set_text_color(255, 255, 255)
        self.cell(0, 15, sanitize_pdf_text('ESTADÍSTICA Y OPTIMIZACIÓN - INFORME FINAL'), 0, 1, 'C')
        self.set_font('Helvetica', 'I', 11)
        self.cell(0, 5, sanitize_pdf_text('GRUPO DE TRABAJO 1: Solución de Producción'), 0, 1, 'C')
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, sanitize_pdf_text(f'Generado por Grupo 1 de Estadística y Optimización | Página {self.page_no()}'), 0, 0, 'C')

def generar_pdf_profesional(df, stats_df, equipo, graficos_figs, currency_label, filtros_seleccionados):
    """
    Genera un informe PDF masivo con todas las tablas y gráficos de la app.
    """
    pdf = PDFReport()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # --- PORTADA Y EQUIPO ---
    pdf.set_text_color(30, 58, 138)
    pdf.set_font('Helvetica', 'B', 18)
    pdf.cell(0, 15, sanitize_pdf_text('1. Miembros del Equipo del Grupo 1'), 0, 1, 'L')
    
    pdf.set_font('Helvetica', '', 12)
    pdf.set_text_color(0, 0, 0)
    for nombre, rol in equipo.items():
        pdf.cell(10)
        pdf.cell(0, 8, sanitize_pdf_text(f'* {nombre} - {rol}'), 0, 1, 'L')
    
    pdf.ln(10)
    
    # --- RESUMEN TÉCNICO ---
    pdf.set_text_color(30, 58, 138)
    pdf.set_font('Helvetica', 'B', 18)
    pdf.cell(0, 15, sanitize_pdf_text('2. Resumen del Análisis'), 0, 1, 'L')
    
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(10)
    pdf.cell(0, 7, sanitize_pdf_text(f'Divisa de Referencia: {currency_label}'), 0, 1, 'L')
    pdf.cell(10)
    pdf.cell(0, 7, sanitize_pdf_text(f'Muestra: {len(df)} registros analizados.'), 0, 1, 'L')
    
    pdf.ln(10)
    
    # --- TABLA DE ESTADÍSTICOS ---
    pdf.set_text_color(30, 58, 138)
    pdf.set_font('Helvetica', 'B', 18)
    pdf.cell(0, 15, sanitize_pdf_text('3. Estadísticos Descriptivos Principales'), 0, 1, 'L')
    
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_fill_color(220, 235, 255)
    pdf.set_text_color(0, 0, 0)
    
    col_widths = [55, 30, 30, 35, 35]
    headers = ['Variable', 'Media', 'Mediana', 'Desv. Tipica', 'CV%']
    for i, h in enumerate(headers):
        pdf.cell(col_widths[i], 10, h, 1, 0, 'C', True)
    pdf.ln()
    
    pdf.set_font('Helvetica', '', 8)
    for _, row in stats_df.iterrows():
        pdf.cell(col_widths[0], 8, sanitize_pdf_text(row['Variable']), 1, 0, 'L')
        pdf.cell(col_widths[1], 8, f"{row['Media']:,.2f}", 1, 0, 'R')
        pdf.cell(col_widths[2], 8, f"{row['Mediana']:,.2f}", 1, 0, 'R')
        pdf.cell(col_widths[3], 8, f"{row['Desviación Típica']:,.2f}", 1, 0, 'R')
        pdf.cell(col_widths[4], 8, f"{row['CV%']:,.2f}%", 1, 1, 'R')

    # --- SECCIÓN DE GRÁFICOS (TODOS) ---
    pdf.add_page()
    pdf.set_text_color(30, 58, 138)
    pdf.set_font('Helvetica', 'B', 18)
    pdf.cell(0, 15, sanitize_pdf_text('4. Visualizaciones y Gráficos del Proyecto'), 0, 1, 'L')
    
    for i, (nombre_graf, fig) in enumerate(graficos_figs.items()):
        # Si el gráfico no ha sido implementado (es None), lo saltamos
        if fig is None:
            continue
            
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmpfile:
            tmp_path = tmpfile.name
            fig.savefig(tmp_path, format='png', dpi=120, bbox_inches='tight')
            
        if pdf.get_y() > 180:
            pdf.add_page()
        
        pdf.set_text_color(100, 100, 100)
        pdf.set_font('Helvetica', 'B', 11)
        pdf.cell(0, 10, sanitize_pdf_text(f'Gráfico {i+1}: {nombre_graf}'), 0, 1, 'C')
        pdf.image(tmp_path, x=15, w=180)
        pdf.ln(10)
        
        try:
            os.unlink(tmp_path)
        except:
            pass

    return bytes(pdf.output())
