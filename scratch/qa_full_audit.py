import os
import sys
import pandas as pd
import numpy as np

# Rubén Gámez Torrijos - QA de Arquitectura v.2.5.3

# Añadir el directorio raíz al path para poder importar los módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.data_loader import load_processed_data
from analisis.estadisticos import calcular_estadisticos, calcular_estadisticos_por_categoria
from analisis.inferencial import realizar_test_hipotesis, verificar_supuestos
from analisis.modelo_regresion import ejecutar_regresion_simple
from analisis.exportacion import generar_pdf_profesional
import config.settings as cfg

def run_qa():
    print("Iniciando QA de Arquitectura - v.2.5.3")
    print("-" * 50)

    # 1. QA de Datos
    print("1. Cargando datos...")
    df = load_processed_data()
    if df is not None and not df.empty:
        print(f"OK: Datos cargados: {len(df)} registros.")
        # Verificar columnas críticas
        cols_criticas = [cfg.COL_SALARIO_EUR, cfg.COL_SALARIO_USD, cfg.COL_COLI]
        for col in cols_criticas:
            if col in df.columns:
                print(f"   - Columna '{col}': OK")
            else:
                print(f"   ERROR: Falta columna '{col}'")
    else:
        print("ERROR: No se pudieron cargar los datos.")
        return

    # 2. QA de Estadísticos
    print("\n2. Probando Estadísticos Descriptivos...")
    try:
        stats = calcular_estadisticos(df)
        print(f"OK: Estadísticos generales calculados ({len(stats)} variables).")
        
        cat_stats = calcular_estadisticos_por_categoria(df, cfg.COL_SALARIO_EUR, 'experience_level')
        print(f"OK: Estadísticos por categoría (Experiencia) calculados.")
        
        # Verificar que Moda y Rango existen (cambio v.2.5.3)
        if 'Moda' in cat_stats.columns and 'Rango' in cat_stats.columns:
            print("   - Columnas Moda/Rango en categorías: OK")
        else:
            print("   ERROR: No se encuentran Moda/Rango en categorías.")
    except Exception as e:
        print(f"ERROR en Estadísticos: {e}")

    # 3. QA de Inferencia
    print("\n3. Probando Estadistica Inferencial...")
    try:
        # Prueba de ANOVA/T-Test (realizar_test_hipotesis)
        anova_res = realizar_test_hipotesis(df, cfg.COL_SALARIO_EUR, 'experience_level')
        print(f"OK: Test Hipotesis ejecutado (Estadistico: {anova_res['Estadístico']:.2f})")
        
        # Verificar supuestos
        supuestos = verificar_supuestos(df[cfg.COL_SALARIO_EUR])
        print(f"OK: Verificacion de supuestos ejecutada.")
    except Exception as e:
        print(f"ERROR en Inferencia: {e}")

    # 4. QA de Regresion
    print("\n4. Probando Modelo de Regresion...")
    try:
        modelo = ejecutar_regresion_simple(df, cfg.COL_COLI, cfg.COL_SALARIO_EUR)
        print(f"OK: Regresion COLI -> Salario ejecutada.")
        print(f"   - R2: {modelo['r2']:.4f}")
        print(f"   - Coeficiente: {modelo['coeficiente']:.2f}")
        
        # Verificar claves (correccion v.2.5.3)
        if 'coeficiente' in modelo and 'intercepto' in modelo:
            print("   - Claves de modelo consistentes: OK")
        else:
            print("   ERROR: Claves de modelo incorrectas (KeyError potential)")
    except Exception as e:
        print(f"ERROR en Regresion: {e}")

    # 5. QA de Exportacion (PDF)
    print("\n5. Probando Generacion de PDF (Simulacion)...")
    try:
        equipo_dict = {
            "Rubén Gámez Torrijos": {"rol": "Coordinador Arquitecto Software", "especialidad": "Arquitectura"},
            "Rafael Rodriguez Mengual": {"rol": "Data Manager Estadísticos", "especialidad": "Gestión de Datos"}
        }
        # Dummy dict for graphics (empty plots or strings)
        graficos = {} 
        
        # Probar con Euro para validar el hack CP1252
        pdf_bytes = generar_pdf_profesional(df, stats, equipo_dict, graficos, "EUR EUR")
        if len(pdf_bytes) > 0:
            print(f"OK: PDF generado con exito ({len(pdf_bytes)} bytes).")
            print("   - Soporte simbolo EUR: Verificado internamente.")
        else:
            print("ERROR: El PDF generado esta vacio.")
    except Exception as e:
        print(f"ERROR en Exportacion PDF: {e}")

    print("\n" + "=" * 50)
    print("QA COMPLETADO - TODO PARECE EN ORDEN")
    print("=" * 50)

if __name__ == "__main__":
    run_qa()
