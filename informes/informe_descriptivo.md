# Análisis Descriptivo de Salarios en Data Science

## 1. Estadísticos Descriptivos (Rafael Rodriguez)
Se han calculado las medidas de tendencia central y dispersión para la variable `salary_in_usd`.

| Medida | Valor (USD) |
| :--- | :--- |
| **Media** | 150.299,50 |
| **Mediana** | 143.000,00 |
| **Moda** | 150.000,00 |
| **Desviación Típica** | 63.177,37 |
| **Rango** | 435.000,00 |

**Interpretación**: La media es ligeramente superior a la mediana, lo que indica un sesgo positivo (presencia de salarios muy altos que elevan el promedio). La desviación típica es elevada, reflejando una gran variabilidad en el mercado laboral tecnológico.

## 2. Visualización y Regresión (Leslie Ross)
Se han generado 5 visualizaciones principales situadas en `outputs/graficos/`:
- **Histograma**: Muestra una distribución unimodal con cola a la derecha.
- **Boxplot por Experiencia**: Revela que el nivel "Executive" tiene la mediana más alta, seguido por "Senior".
- **Análisis de Regresión**: Se analizó la relación entre el año (`work_year`) y el salario (`salary_in_usd`).
  - **Coeficiente de Correlación (r)**: 0,11
  - **Tendencia**: Se observa un ligero incremento anual en los salarios medios, aunque la correlación es débil, indicando que otros factores (como el rol o ubicación) influyen más que el simple paso del tiempo.

## 3. Discusión Crítica
El mercado de Data Science muestra una robustez salarial notable, con un promedio que supera los 150.000 USD. Sin embargo, la brecha entre niveles de entrada (Entry) y ejecutivos es amplia. La baja correlación con el año sugiere que no hay una "inflación salarial" lineal simple, sino un mercado maduro con variabilidad basada en especialización.
