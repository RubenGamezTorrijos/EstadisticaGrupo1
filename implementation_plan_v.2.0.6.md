# Plan de Restauración: Filtros por País y Exportación Pro (v.2.0.6)

Este plan aborda la restauración de funcionalidades críticas identificadas por el usuario que se perdieron en la consolidación anterior: el sistema de filtrado/comparación por países y la generación de reportes profesionales en Excel y PDF.

## User Review Required

> [!IMPORTANT]
> **Definición de Exportación**: La generación del PDF requiere guardar gráficos temporalmente en memoria para incrustarlos. Esto puede aumentar ligeramente el tiempo de respuesta al generar el informe.
> **Comparativa de Países**: Se implementará una lógica que, al detectar múltiples países seleccionados, active visualizaciones comparativas (Barras agrupadas o Facetas).

## Proposed Changes

### 1. Módulo de Exportación [NEW]
#### [NEW] [exportacion.py](file:///c:/Users/ruben/Proyectos/Antigravity/proyecto_estadistica/analisis/exportacion.py)
- Implementar `generar_excel_multipestana`:
    - Hoja 1: Datos filtrados.
    - Hoja 2: Estadísticos descriptivos.
    - Hoja 3: Resultados de inferencia.
- Implementar `generar_informe_pdf_completo`:
    - Portada con logo/título y miembros del equipo.
    - Resumen de filtros aplicados (incluyendo países).
    - Tablas de estadísticos clave.
    - Inserción de gráficos (Histograma, Boxplot, Regresión).
    - Conclusiones automáticas basadas en los datos.

### 2. Interfaz de Usuario [MODIFY]
#### [MODIFY] [app.py](file:///c:/Users/ruben/Proyectos/Antigravity/proyecto_estadistica/app.py)
- **Filtros Sidebar**:
    - Añadir `st.multiselect` para "Comparativa por Países" (`company_location`).
    - Lógica de filtrado: `df = df[df['company_location'].isin(paises)]` si hay selección.
- **Sección de Exportación**:
    - Añadir una nueva opción de navegación "7. Exportar Informe" o botones directos en el Sidebar.
    - Integrar `st.download_button` para Excel y PDF.
- **Lógica de Comparación**:
    - Si se seleccionan varios países, añadir una sub-sección visual en "Visualizaciones" que compare sus medias salariales.

### 3. Módulo de Estadísticos [MODIFY]
#### [MODIFY] [estadisticos.py](file:///c:/Users/ruben/Proyectos/Antigravity/proyecto_estadistica/analisis/estadisticos.py)
- Asegurar que el mapeo de países sea legible (ej: convertir códigos ISO si fuera necesario, aunque el dataset parece usar nombres completos).

## Open Questions

1. **Selección de Gráficos**: ¿Prefieres que el PDF incluya **todos** los gráficos de la aplicación o solo los 3 más importantes (Histograma, Boxplot y Regresión)?
2. **Ubicación de Exportar**: ¿Prefieres los botones de descarga en el menú lateral (siempre visibles) o en una sección propia al final del menú?

## Verification Plan

### Automated Tests
- Verificar que `generar_excel` devuelve un objeto `BytesIO` válido con múltiples hojas.
- Verificar que `generar_pdf` no falla al procesar caracteres especiales (usando el helper `sanitize_pdf_text`).

### Manual Verification
1. Filtrar por "Spain" y "United States".
2. Descargar Excel y comprobar que los datos corresponden al filtro.
3. Descargar PDF y verificar que aparecen los nombres de los integrantes (Rafael, Bryann, Leslie, Rubén) y los gráficos.
