import pandas as pd
from analisis.estadisticos import limpiar_datos, calcular_estadisticos, exportar_tablas

# Cargar el CSV original
df = pd.read_csv('datos/jobs_in_data.csv')

# Limpiar los datos
df_limpio = limpiar_datos(df)

# Calcular estadísticos
df_stats = calcular_estadisticos(df_limpio)

# Exportar los estadísticos a CSV
exportar_tablas(df_stats, 'datos/estadisticos_resumen.csv')

print("✅ Limpieza y estadísticos completados. Revisa la carpeta 'datos/'")