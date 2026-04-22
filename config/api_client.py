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
    Intenta obtener los datos más recientes. 
    Si la API falla, devuelve los datos locales de respaldo.
    """
    params = {
        "format": "json",
        "date": "2020:2023",
        "per_page": 5000,
        "source": 2 # World Development Indicators
    }
    
    try:
        # Nota: Algunos indicadores pueden requerir fuentes específicas
        response = requests.get(f"{WB_URL}{WB_INDICATOR}", params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if len(data) > 1:
                records = data[1]
                # Procesar registros...
                return pd.DataFrame([
                    {"country": r['country']['value'], "year": int(r['date']), "index": r['value']}
                    for r in records if r['value'] is not None
                ])
    except Exception:
        pass
    
    # Fallback a datos locales si la API no está disponible
    return pd.read_csv(COLI_CSV) if os.path.exists(COLI_CSV) else None
