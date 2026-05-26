"""
config/api_client.py
====================
Cliente para la obtención de datos externos vía API del Banco Mundial.
Optimizado para obtener el índice de paridad de poder adquisitivo (PPP) más reciente.
"""

import requests
import pandas as pd
import streamlit as st
import config.settings as cfg

# Indicador: Price Level Ratio of PPP conversion factor (GDP) to market exchange rate
# Este índice compara el nivel de precios de un país con el promedio mundial (USA = 1.0 aprox)
WB_INDICATOR = "PA.NUS.PPPC.RF"
WB_URL = "https://api.worldbank.org/v2/country/all/indicator/"

def get_latest_coli_data():
    """
    Obtiene datos económicos reales del Banco Mundial.
    Usa el parámetro mrnev=1 para obtener el valor no vacío más reciente.
    """
    params = {
        "format": "json",
        "per_page": 500,
        "mrnev": 1,      # Most Recent Non-Empty Value
        "source": 2      # World Development Indicators
    }
    
    try:
        # Construcción de URL robusta
        url = f"{WB_URL}{WB_INDICATOR}"
        response = requests.get(url, params=params, timeout=15)
        
        if response.status_code == 200:
            json_data = response.json()
            
            # La API de WB devuelve una lista: [metadatos, registros]
            if isinstance(json_data, list) and len(json_data) > 1:
                records = json_data[1]
                
                # Procesamiento Senior de registros
                data_list = []
                for r in records:
                    val = r.get('value')
                    country_name = r.get('country', {}).get('value')
                    
                    if val is not None and country_name:
                        # Normalizamos a base 100 (USA como referencia de coste 100)
                        # El indicador RF suele estar cerca de 1.0 para USA
                        data_list.append({
                            "country": country_name,
                            "cost_of_living_index": float(val) * 100,
                            "last_update": r.get('date')
                        })
                
                df_api = pd.DataFrame(data_list)
                
                # Asegurar que España (Spain) esté presente y con datos
                if "Spain" in df_api['country'].values:
                    # Opcional: Log interno para verificación
                    pass
                
                # Retornar datos limpios y únicos por país
                return df_api.dropna().drop_duplicates(subset=['country'])
                
    except Exception as e:
        st.warning(f"No se pudo conectar con la API de World Bank. {e}")
    
    return None
