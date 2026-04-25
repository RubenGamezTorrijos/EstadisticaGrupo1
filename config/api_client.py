"""
config/api_client.py
====================
Cliente para la obtención de datos externos vía API.
"""

import requests
import pandas as pd
import os
from .settings import COLI_CSV

# Usaremos un indicador estable del Banco Mundial para el Coste de Vida (PPP ratio)
WB_INDICATOR = "PA.NUS.PPPC.RF"
WB_URL = "https://api.worldbank.org/v2/country/all/indicator/"

def get_latest_coli_data():
    """
    Obtiene el factor de conversión PPP (Coste de Vida) del Banco Mundial.
    Normaliza el índice a base 100 (USA = 100) para compatibilidad.
    """
    params = {
        "format": "json",
        "date": "2022:2023",
        "per_page": 300,
        "source": 2
    }
    
    try:
        response = requests.get(f"{WB_URL}{WB_INDICATOR}", params=params, timeout=15)
        if response.status_code == 200:
            json_data = response.json()
            if isinstance(json_data, list) and len(json_data) > 1:
                records = json_data[1]
                # Crear DataFrame y normalizar (API devuelve ratio, queremos base 100)
                df_api = pd.DataFrame([
                    {
                        "country": r['country']['value'], 
                        "cost_of_living_index": float(r['value']) * 100 if r['value'] else None
                    }
                    for r in records
                ])
                # Limpiar nulos y duplicados (quedarse con el más reciente)
                return df_api.dropna().drop_duplicates(subset=['country'])
    except Exception as e:
        print(f"Error consultando World Bank API: {e}")
    
    return None
