"""
PROYECTO: Estadística para Ingeniería
ARQUITECTURA Y MOCKS: RUBEN GAMEZ TORRIJOS (Desarrollador y Coordinador)
Script para inicializar/generar el dataset dummy temporal del proyecto.
"""
import pandas as pd
import numpy as np

def generar_dataset(n=200):
    np.random.seed(42)
    
    # Variable categórica: Sexo
    sexo = np.random.choice(['Hombre', 'Mujer'], n)
    
    # Variable discreta: Edad (18-90 años)
    edad = np.random.randint(18, 91, n)
    
    # Variables continuas: Altura y Peso (con cierta correlación y diferencias por sexo)
    altura = []
    peso = []
    
    for s in sexo:
        if s == 'Hombre':
            h = np.random.normal(175, 7)
            p = np.random.normal(80, 12) + (h - 175) * 0.5
        else:
            h = np.random.normal(162, 6)
            p = np.random.normal(65, 10) + (h - 162) * 0.4
        altura.append(round(h, 2))
        peso.append(round(p, 2))
        
    df = pd.DataFrame({
        'ID': range(1, n + 1),
        'Edad': edad,
        'Sexo': sexo,
        'Altura': altura,
        'Peso': peso
    })
    
    # Añadir algunos nulos para probar la limpieza
    df.loc[np.random.choice(df.index, 5), 'Peso'] = np.nan
    
    return df

if __name__ == "__main__":
    import os
    df_crudo = generar_dataset()
    os.makedirs('datos', exist_ok=True)
    df_crudo.to_csv('datos/dataset_crudo.csv', index=False)
    print("Dataset crudo generado en datos/dataset_crudo.csv")
    
    # Probar limpieza y estadísticos
    from analisis.estadisticos import limpiar_datos, calcular_estadisticos, exportar_tablas
    
    df_limpio = limpiar_datos(df_crudo)
    df_limpio.to_csv('datos/dataset_limpio.csv', index=False)
    print("Dataset limpio generado en datos/dataset_limpio.csv")
    
    stats = calcular_estadisticos(df_limpio, ['Edad', 'Altura', 'Peso'])
    exportar_tablas(stats, 'outputs/tablas/estadisticos_descriptivos.csv')
