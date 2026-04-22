"""
fetch_worldbank_data.py
=======================
Módulo de adquisición de datos oficiales: API del Banco Mundial.
Obtiene el Price Level Index (PPP) para todos los países del mundo
en el rango temporal 2020-2023.

Autor: Rubén Torrijos
Fecha: Abril 2025
"""

import requests
import pandas as pd
import os

# Indicador: Price level ratio of PPP conversion factor (GDP) to market exchange rate
# Nos da una medida del coste de vida relativo. USA = 1.0
INDICATOR = "PA.NUS.PPPC.RF"
BASE_URL = "https://api.worldbank.org/v2/country/all/indicator/"


def fetch_coli_data(start_year=2020, end_year=2023):
    """Consulta la API del Banco Mundial y devuelve un DataFrame con el COLI."""
    print(f"[*] Consultando API Banco Mundial ({start_year}-{end_year})...")
    
    params = {
        "format": "json",
        "date": f"{start_year}:{end_year}",
        "per_page": 5000
    }
    
    try:
        response = requests.get(f"{BASE_URL}{INDICATOR}", params=params)
        response.raise_for_status()
        data = response.json()
        
        if len(data) < 2:
            print("[!] No se obtuvieron datos de la API.")
            return None
            
        records = data[1]
        rows = []
        for rec in records:
            if rec['value'] is not None:
                rows.append({
                    "country": rec['country']['value'],
                    "country_iso": rec['countryiso3code'],
                    "year": int(rec['date']),
                    "cost_of_living_index": round(rec['value'] * 100, 2), # Escala 100
                    "source": "World Bank (PA.NUS.PPPC.RF)"
                })
        
        df = pd.DataFrame(rows)
        print(f"[OK] Se han obtenido {len(df)} registros oficiales.")
        return df
        
    except Exception as e:
        print(f"[!] Error al conectar con la API: {e}")
        return None


def main():
    df = fetch_coli_data()
    if df is not None:
        path = os.path.join("datos", "cost_of_living_wb.csv")
        df.to_csv(path, index=False)
        print(f"[OK] Datos guardados en {path}")


if __name__ == "__main__":
    main()
