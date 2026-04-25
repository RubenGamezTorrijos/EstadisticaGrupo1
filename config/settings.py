"""
config/settings.py
==================
Configuraciones globales del proyecto, rutas y constantes.
"""

import os

# --- Rutas ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS_DIR = os.path.join(BASE_DIR, "datos")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")

# Archivos
JOBS_CSV = os.path.join(DATOS_DIR, "jobs_in_data.csv")
COLI_CSV = os.path.join(DATOS_DIR, "cost_of_living_index.csv")
ENRIQUECIDO_CSV = os.path.join(DATOS_DIR, "dataset_enriquecido.csv")

# --- Columnas ---
COL_SALARIO_USD = "salary_dollar_usd"
COL_SALARIO_EUR = "salary_euro"
COL_SALARIO_DINAMICO = "salary"
COL_COLI = "cost_of_living_index"
COL_PAIS = "company_location"
COL_SALARIO_AJUSTADO = "salary_adjusted_coli"
COL_CURRENCY = "currency"

# --- Tasas de Cambio ---
EUR_USD_RATE = 0.92 # 1 USD = 0.92 EUR (Aproximado)

# --- Estética ---
APP_TITLE = "Análisis de Salarios y Coste de Vida (2020-2023)"
PRIMARY_COLOR = "#007BFF"
SECONDARY_COLOR = "#6C757D"

# --- Etiquetas de Variables (Centralizado para Reportes Profesionales) ---
VAR_LABELS = {
    'work_year': 'Año Fiscal',
    'experience_level': 'Nivel de Experiencia',
    'employment_type': 'Tipo de Contrato',
    'job_title': 'Rol Profesional',
    'salary': 'Salario Base (Moneda Seleccionada)',
    'currency': 'Divisa Original',
    'salary_dollar_usd': 'Salario Bruto Anual (USD)',
    'salary_euro': 'Salario Bruto Anual (EUR)',
    'employee_residence': 'País de Residencia',
    'remote_ratio': 'Porcentaje de Remoto',
    'company_location': 'Ubicación de la Sede',
    'company_size': 'Tamaño de Compañía',
    'job_category': 'Área de Especialización',
    'work_setting': 'Entorno Laboral',
    'cost_of_living_index': 'Índice de Coste de Vida (COLI)',
    'salary_adjusted_coli': 'Poder Adquisitivo Real (Ajustado)'
}
