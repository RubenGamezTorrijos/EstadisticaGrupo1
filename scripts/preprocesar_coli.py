"""
preprocesar_coli.py
===================
Script de preprocesamiento: Integración del Índice de Coste de Vida (COLI)
basado en datos reales de Numbeo 2023 con el dataset principal jobs_in_data.csv.

Autor: Rubén Torrijos (Coordinador de Arquitectura)
Fecha: Abril 2025
Versión: 1.0.0

Flujo:
    1. Carga jobs_in_data.csv  →  dataset principal
    2. Carga cost_of_living_index.csv  →  fuente externa Numbeo 2023
    3. Merge LEFT JOIN por 'company_location'
    4. Verifica cobertura: países sin COLI asignado
    5. Exporta datos/dataset_enriquecido.csv  →  dataset final listo
    6. Genera informe de cobertura en consola

Uso:
    python scripts/preprocesar_coli.py
"""

import pandas as pd
import os
import sys

# ── Rutas de archivos ────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JOBS_CSV  = os.path.join(BASE_DIR, "datos", "jobs_in_data.csv")
COLI_CSV  = os.path.join(BASE_DIR, "datos", "cost_of_living_index.csv")
OUT_CSV   = os.path.join(BASE_DIR, "datos", "dataset_enriquecido.csv")


def cargar_datasets() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Carga los dos datasets fuente con validación básica."""
    print("[1/5] Cargando datasets...")

    if not os.path.exists(JOBS_CSV):
        sys.exit(f"ERROR: No se encuentra {JOBS_CSV}")
    if not os.path.exists(COLI_CSV):
        sys.exit(f"ERROR: No se encuentra {COLI_CSV}")

    df_jobs = pd.read_csv(JOBS_CSV)
    df_coli = pd.read_csv(COLI_CSV)

    print(f"  [OK] jobs_in_data.csv    -> {len(df_jobs):,} registros | "
          f"{df_jobs['company_location'].nunique()} países únicos")
    print(f"  [OK] cost_of_living.csv  -> {len(df_coli):,} registros de países")
    return df_jobs, df_coli


def realizar_merge(df_jobs: pd.DataFrame, df_coli: pd.DataFrame) -> pd.DataFrame:
    """
    Realiza LEFT JOIN entre df_jobs y df_coli por 'company_location'.
    Conserva TODOS los registros de jobs aunque no haya COLI disponible.
    """
    print("[2/5] Realizando merge LEFT JOIN por 'company_location'...")

    # Solo nos interesan las columnas relevantes del COLI
    df_coli_slim = df_coli[["country", "cost_of_living_index", "source", "year"]].copy()
    df_coli_slim = df_coli_slim.rename(columns={"country": "company_location"})

    df_merged = df_jobs.merge(
        df_coli_slim,
        on="company_location",
        how="left"
    )
    print(f"  [OK] Dataset resultante: {len(df_merged):,} registros")
    return df_merged


def verificar_cobertura(df_merged: pd.DataFrame) -> None:
    """Informa sobre países del dataset sin cobertura COLI y cobertura total."""
    print("[3/5] Verificando cobertura del COLI...")

    total   = len(df_merged)
    sin_coli = df_merged["cost_of_living_index"].isna().sum()
    cobertura_pct = 100 * (1 - sin_coli / total)

    paises_sin_coli = (
        df_merged[df_merged["cost_of_living_index"].isna()]["company_location"]
        .value_counts()
    )

    print(f"  [OK] Registros con COLI asignado : {total - sin_coli:,} "
          f"({cobertura_pct:.1f}%)")
    print(f"  [WARN] Registros sin COLI         : {sin_coli:,} "
          f"({100 - cobertura_pct:.1f}%)")

    if not paises_sin_coli.empty:
        print("\n  Países sin cobertura COLI:")
        for pais, cnt in paises_sin_coli.items():
            print(f"    - {pais}: {cnt} registros  -> "
                  "AÑADIR a cost_of_living_index.csv")
    else:
        print("  [OK] Cobertura completa al 100%.")


def agregar_salario_ajustado(df_merged: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula 'salary_adjusted_coli': normaliza el salario USD según el COLI
    para hacer comparaciones de poder adquisitivo real entre países.

    Fórmula:
        salary_adjusted_coli = salary_in_usd / (cost_of_living_index / 100)

    Un valor mayor indica mayor poder adquisitivo real.
    """
    print("[4/5] Calculando salario ajustado por poder adquisitivo...")

    df_merged["salary_adjusted_coli"] = (
        df_merged["salary_in_usd"] / (df_merged["cost_of_living_index"] / 100)
    ).round(2)

    print("  [OK] Nueva variable 'salary_adjusted_coli' creada")
    return df_merged


def exportar(df_merged: pd.DataFrame) -> None:
    """Exporta el dataset enriquecido."""
    print(f"[5/5] Exportando dataset enriquecido...")
    df_merged.to_csv(OUT_CSV, index=False)
    size_kb = os.path.getsize(OUT_CSV) / 1024
    print(f"  [OK] Guardado en: {OUT_CSV}")
    print(f"  [OK] Tamaño: {size_kb:.1f} KB")
    print(f"  [OK] Columnas finales: {list(df_merged.columns)}")


def resumen_estadistico(df_merged: pd.DataFrame) -> None:
    """Muestra un resumen estadístico de las variables COLI incorporadas."""
    print("\n-- Resumen estadístico del COLI integrado ------------------------------")
    coli_stats = df_merged["cost_of_living_index"].describe()
    print(coli_stats.to_string())

    print("\n-- Top 5 países por COLI más alto --------------------------------------")
    top = (
        df_merged.groupby("company_location")["cost_of_living_index"]
        .first()
        .sort_values(ascending=False)
        .head(5)
    )
    print(top.to_string())

    print("\n-- Top 5 países por COLI más bajo --------------------------------------")
    low = (
        df_merged.groupby("company_location")["cost_of_living_index"]
        .first()
        .sort_values(ascending=True)
        .head(5)
    )
    print(low.to_string())

    print("\n-- Correlación COLI vs Salario USD --------------------------------------")
    correlacion = df_merged[["salary_in_usd", "cost_of_living_index"]].dropna().corr()
    print(correlacion.to_string())


def main():
    print("=" * 65)
    print("  PREPROCESAMIENTO COLI - Integración Datos Reales Numbeo 2023")
    print("=" * 65)

    df_jobs, df_coli = cargar_datasets()
    df_merged        = realizar_merge(df_jobs, df_coli)
    verificar_cobertura(df_merged)
    df_merged        = agregar_salario_ajustado(df_merged)
    exportar(df_merged)
    resumen_estadistico(df_merged)

    print("\n[DONE] Preprocesamiento completado. Usa 'dataset_enriquecido.csv' en app.py.")
    print("=" * 65)


if __name__ == "__main__":
    main()
