# Análisis Inferencial de Salarios

## 1. Intervalos de Confianza (Bryann Vallejo)
Para la variable continua `salary_in_usd`, se ha calculado el intervalo de confianza al 95%.

- **Media Muestral**: 150.299,50 USD
- **Intervalo**: [149.019,10, 151.579,89] USD

**Interpretación**: Tenemos una confianza del 95% de que el salario medio real de la población de profesionales de datos se encuentra en este rango. El margen de error es estrecho debido al gran tamaño de la muestra (N > 9000).

## 2. Contraste de Hipótesis
Se planteó la siguiente prueba de hipótesis para comparar los salarios de niveles **Senior** vs **Mid-level**:

- **H0 (Hipótesis Nula)**: No hay diferencia entre las medias salariales.
- **H1 (Hipótesis Alternativa)**: La media salarial de los Senior es diferente a la de los Mid-level.
- **Prueba**: T-test de Welch (no asume varianza igual).
- **P-Valor**: 1,89e-178 (prácticamente cero).

**Resultado**: Se **rechaza la hipótesis nula**.
**Justificación**: Existe evidencia estadística abrumadora de que los profesionales Senior perciben salarios significativamente más altos que los de nivel intermedio.

## 3. Verificación de Supuestos
- **Normalidad**: Dado el gran tamaño de la muestra, el Teorema del Límite Central nos permite realizar inferencias sobre la media a pesar de que la distribución original es ligeramente sesgada.
- **Independencia**: Los registros representan individuos/contratos distintos en diferentes empresas.
