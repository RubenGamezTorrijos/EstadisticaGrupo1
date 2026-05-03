# Walkthrough - Finalización Dashboard v.2.5.3

Hemos completado el pulido final de la aplicación, asegurando que cumple con los estándares profesionales solicitados y la normativa académica.

## Cambios Implementados

### 1. Sistema de Formateo Localizado
- **Monedas**: Implementación estricta de precisión y separadores.
  - **EUR**: `.` para miles, `,` para decimales. 1 decimal para `K`, 2 para `M`. (Ej: `€243,6K`, `€1,24M`).
  - **USD**: `,` para miles, `.` para decimales. (Ej: `$243.6K`, `$1.24M`).
- **Fechas/Años**: Eliminación de separadores en años (Ej: `2025` en lugar de `2.025`).
- **Porcentajes (COLI)**: Formateo con dos decimales y separador localizado según divisa.

### 2. Rediseño de la Vista de Equipo
- Se ha revertido el uso de tarjetas fijas por **Expanders estilizados** que mantienen el diseño de tarjeta profesional en su interior.
- Se han actualizado los listados de archivos atribuidos a cada miembro del equipo para reflejar la realidad del repositorio.

### 3. Optimización del Motor de Exportación
- **PDF**: Se ha integrado el **Gráfico de Violín** en el reporte PDF.
- **Estructura**: El PDF ahora se organiza por secciones numeradas coincidiendo con las vistas de la App.
- **Excel**: Se han sincronizado las pestañas para incluir los datos filtrados, estadísticos, inferencia y regresión.

### 4. Robustez y Gestión de Errores
- **Guardián de Datos**: Implementación de validaciones en todas las vistas para mostrar advertencias profesionales en lugar de errores cuando los filtros dejan el DataFrame vacío.
- **Validación de Normalidad**: Corrección de la lógica de P-Valor y manejo de muestras pequeñas (n < 3) en la prueba de Shapiro-Wilk.

## Verificación Visual

### Formateo de Divisas
- **EUR**: `€1.234.567` -> `€1,23M`
- **USD**: `$1,234,567` -> `$1.23M`

### Gráficos
- Los ejes de los gráficos ahora respetan los separadores de miles y decimales configurados en el selector de divisa.

---
*© 2026 - Universidad Europea - v.2.5.3 Final*
