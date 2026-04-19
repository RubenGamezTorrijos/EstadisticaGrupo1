# Plan de Consolidación de Rama Main (v.2.0.4)

Este plan detalla los pasos para convertir la rama `main` en la versión de referencia (Solucionario) 100% funcional, integrando la mejora de multidivisa traducido y asegurando el cumplimiento de la rúbrica junto con la nueva funcionalidad de la variable COLI.

## Análisis de Estado Actual vs "enunciado_practica.md"

Tras analizar el código actual en `main`, he detectado las siguientes discrepancias/mejoras necesarias para cumplir el plan v.2.0.3:

1.  **Selector de Divisa (Prioridad Alta)**: Falta un radio button en el sidebar para alternar globalmente entre USD y EUR.
2.  **Integración de Regresión**: Aunque existe `modelo_regresion.py`, `app.py` no lo utiliza plenamente en la interfaz de usuario, limitándose a un gráfico básico de `graficos.py`.
3.  **Bilingüismo en Informes**: Los informes PDF/Excel deben adaptarse dinámicamente a la moneda seleccionada.
4.  **Completitud Estadística**: Asegurar que la tabla descriptiva muestre Rango y Varianza para todas las variables numéricas (incluyendo el nuevo COLI).

## Cambios Propuestos

### 1. Interfaz de Usuario (`app.py`)
- [MODIFY] Añadir `st.sidebar.radio` para seleccionar "Divisa de Análisis" (USD / EUR).
- [MODIFY] Refactorizar funciones de formateo para que dependan de la selección global.
- [NEW] Integrar formalmente la pestaña "4. Regresión y Correlación" usando el módulo de Leslie.

### 2. Módulo de Regresión (`analisis/modelo_regresion.py`)
- [VERIFY] Asegurar que calcula $R^2$, correlación y la ecuación de la recta de forma profesional.

### 3. Generación de Reportes
- [MODIFY] Actualizar `create_pdf` y `create_excel` para que acepten el parámetro de moneda y generen los resultados descriptivos e inferenciales acordes.

### 4. Estilo y Roles
- [MODIFY] Reforzar los encabezados de Rafael, Bryann y Leslie en cada sección de la app para clarificar responsabilidades.

### 5. Definición de Tareas y Roles (NUEVO)
- [MODIFY] **README.md**: Ampliar la sección "Detalle de Tareas" para incluir a los cuatro integrantes (añadiendo a Rubén) y detallar las responsabilidades técnicas específicas de cada uno según el estado final del proyecto.
- [MODIFY] **app.py (Vista de Equipos)**: Transformar la tabla actual de "Sobre el Equipo" en una vista más detallada que liste las tareas completadas por cada integrante, sincronizándola con el README.

## Verificación de Rúbrica (Checklist)
- [x] Muestra > 100 registros.
- [x] Variables: 2 continuas (Salario, COLI), 1 discreta (Año), 1 categórica (Experiencia).
- [x] Estadísticos: Media, Mediana, Moda, Desv. Típ., Varianza, Rango.
- [x] Gráficos: Histograma, Barra, Caja, Dispersión.
- [x] Regresión: Modelo lineal entre continuas.
- [x] Inferencia: IC y Contrastes de Hipótesis.

## Preguntas al Usuario
- ¿La tasa de conversión USD -> EUR de **0.92** es aceptable para el grupo o prefieres que sea un input ajustable?
- ¿Deseas que mantenga los comentarios de "TODO" visibles en la UI de la rama `main` para que sirvan de guía directa?
