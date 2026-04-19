# Plan de Restauración del Sistema de Exportación Profesional (v.2.1.0)

El usuario desea que el sistema de exportación sea idéntico al original en cuanto a comodidad (un solo clic para descargar) y completitud (todos los gráficos y pestañas técnicas).

## User Review Required

> [!IMPORTANT]
> - **UX**: El botón "Generar Informe PDF" pasará a ser "Descargar Informe PDF (Completo)" y realizará la descarga en un solo paso.
> - **Contenido**: Se incluirán gráficos que faltaban: **Violin Plot**, **Diagrama de Barras por Categoria** y el **Histograma con Distribución** (que el usuario identifica como de velas).
> - **Excel**: Se ampliará a **4 pestañas** técnicas unificadas.

## Proposed Changes

### Identidad y Estética (UI)

#### [MODIFY] [app.py](file:///c:/Users/ruben/Proyectos/Antigravity/proyecto_estadistica/app.py)
*   **Título Sidebar**: Cambiar "ESTADÍSTICA IT" por **"ESTADÍSTICA IT - GRUPO 1"**.
*   **CSS para Filtros**: 
    *   Target para los tags del `st.multiselect` (los "botones" de filtros).
    *   Cambiar fondo de rojo/gris a **Azul Agradable (#0b84f4)** y texto a blanco.
    *   Asegurar que los botones de descarga sigan esta misma línea estética.

### Módulo de Exportación

#### [MODIFY] [exportacion.py](file:///c:/Users/ruben/Proyectos/Antigravity/proyecto_estadistica/analisis/exportacion.py)
*   **Excel**: Incluir 4 pestañas: Datos Filtrados, Estadísticos (Descriptivos), Inferencia (IC + Tests de Normalidad/Varianza) y Regresión.
*   **PDF**: Incluir la lista completa de gráficos: Histograma, Boxplot, Violin Plot, Bar Chart (Categorías) y Regresión.

## Open Questions

- Respecto a la "gráfica de velas", incluiré tanto el **Boxplot** como el **Histograma con curva de distribución** para cubrir todas las bases. 
- En el Excel de Inferencia, incluiré los resultados de los tests de **Normalidad (Shapiro)** por defecto.

## Verification Plan

### Automated Tests
- Ejecutar la descarga de Excel y verificar que las 4 pestañas contienen datos coherentes.
- Generar el PDF y verificar visualmente que aparecen los 5-6 gráficos solicitados.

### Manual Verification
- Comprobar que el botón de PDF descarga el archivo inmediatamente sin pasos intermedios.
