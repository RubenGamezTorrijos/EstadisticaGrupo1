# Informe de Propuesta de Variables

**Proyecto**: Empleos y Salarios en Data Science (2020-2023)
**Equipo**: Rafael Rodriguez, Bryann Vallejo, Leslie Ross, Ruben Gamez

## Breve Explicación de los Datos
El dataset seleccionado proviene de Kaggle ("Jobs and Salaries in Data Science") y contiene información sobre roles tecnológicos, sus salarios, ubicación y niveles de experiencia. El objetivo es analizar cómo el nivel de experiencia y el tipo de trabajo (remoto vs presencial) influyen en la remuneración económica.

## Variables Seleccionadas
Para cumplir con los requisitos de la asignatura:

1. **Variables Numéricas Continuas**:
   - `salary_in_usd`: Salario bruto anual convertido a dólares estadounidenses.
   - `salary`: Salario en la moneda original del contrato.
2. **Variable Discreta**:
   - `work_year`: Año en el cual se registró el salario (2020, 2021, 2022, 2023).
3. **Variable Categórica**:
   - `experience_level`: Nivel de experiencia del empleado (Entry, Mid, Senior, Executive).

## Muestra de Datos
| work_year | job_title | salary_in_usd | experience_level |
| :--- | :--- | :--- | :--- |
| 2023 | Data DevOps Engineer | 95.012,00 | Mid-level |
| 2023 | Data Scientist | 212.000,00 | Senior |
| 2023 | Data Analyst | 75.000,00 | Entry-level |

## Pregunta de Investigación
¿Existe una diferencia estadísticamente significativa entre los salarios de los empleados de nivel "Senior" y "Mid-level" en la industria de los datos, y cómo ha evolucionado el salario medio entre 2020 y 2023?
