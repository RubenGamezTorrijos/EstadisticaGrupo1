# Plan de Cumplimiento Total v.2.0.4 (Versión de Referencia)

Este plan detalla los pasos finales para asegurar que la rama `main` sea un "Solucionario" perfecto, cumpliendo punto por punto con el plan v.2.0.4 sin romper la estabilidad actual.

## User Review Required

> [!IMPORTANT]
> Se reestructurará el menú lateral para incluir **6 secciones** exactas, separando "Estadísticos" de "Visualizaciones" para coincidir con el README y la documentación del proyecto.

## Proposed Changes

### 1. Motor Estadístico (`analisis/estadisticos.py`)

#### [MODIFY] [estadisticos.py](file:///c:/Users/ruben/Proyectos/Antigravity/proyecto_estadistica/analisis/estadisticos.py)
*   Actualizar `calcular_estadisticos` para incluir todas las variables numéricas requeridas:
    *   `salary_in_usd`
    *   `salary_in_eur`
    *   `work_year` (Variable discreta)
    *   `cost_of_living_index` (Variable continua adicional)
*   Esto garantiza que la tabla descriptiva sea "completa" según el punto 4 del plan v.2.0.4.

### 2. Refinamiento de Interfaz (`app.py`)

#### [MODIFY] [app.py](file:///c:/Users/ruben/Proyectos/Antigravity/proyecto_estadistica/app.py)
*   **Menú Lateral (6 Secciones)**:
    1.  `🏠 Escritorio General (Rafael Rodriguez)`
    2.  `📊 Estadísticos Descriptivos (Rafael Rodriguez)`
    3.  `🖼️ Visualizaciones (Leslie Ross)`
    4.  `🤖 Regresión Lineal (Leslie Ross)`
    5.  `🔍 Estadística Inferencial (Bryann Vallejo)`
    6.  `👥 Equipo Grupo 1 (Rubén Gámez)`
*   **Sección de Estadísticos**: Mostrar una tabla comparativa de **todas** las variables numéricas, no solo el salario.
*   **Refuerzo de Roles**: Asegurar que cada `st.header` incluya el nombre del responsable de forma prominente.

### 3. Generación de Reportes

#### [MODIFY] [app.py](file:///c:/Users/ruben/Proyectos/Antigravity/proyecto_estadistica/app.py)
*   Actualizar `create_pdf` para que incluya en el informe los estadísticos de COLI y Año, además del Salario.

## Open Questions

*   ¿Prefieres que la tabla de estadísticos descriptivos se muestre en formato transpuesta (variables en columnas) o el formato estándar de una variable por fila? (El formato de una variable por fila suele ser más legible para 15+ estadísticos).

## Verification Plan

### Automated Tests
*   **Verificación de EUR**: Cambiar a EUR y confirmar que la tabla descriptiva actualiza tanto el Salario como el COLI (si procediera).
*   **Verificación de Regresión**: Confirmar que los cálculos de Leslie se muestran con 4 decimales de precisión.
*   **Prueba de PDF**: Generar el informe y validar que aparecen los roles de los 4 integrantes.
