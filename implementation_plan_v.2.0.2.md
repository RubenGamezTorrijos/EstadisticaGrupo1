# Visualización de la Estadística Inferencial en Reportes

Este plan tiene como objetivo sustituir las tablas densas de números por gráficos intuitivos en la sección de Estadística Inferencial del PDF, tal como solicita el usuario.

## User Review Required

> [!IMPORTANT]
> - El PDF incluirá ahora un **Violin Plot** comparativo específicamente para la prueba de hipótesis (Senior vs Mid-level).
> - Se añadirá una visualización de **Barras de Error** que representa los Intervalos de Confianza (IC 95%) por nivel de experiencia, lo que permite ver a simple vista si hay solapamiento o no.

## Proposed Changes

### [Component] analisis/graficos.py ---

#### [MODIFY] [graficos.py](file:///C:/Users/ruben/Proyectos\Antigravity\proyecto_estadistica\analisis\graficos.py)
- Implementar `crear_grafico_comparativo_ic(df, variable_num, variable_cat)`: Un gráfico de barras con barras de error que representen los límites superior e inferior del IC 95% calculado dinámicamente.

### [Component] app.py ---

#### [MODIFY] [app.py](file:///C:/Users/ruben/Proyectos\Antigravity\proyecto_estadistica\app.py)
- **Función `create_pdf`**:
    - En la sección "2. Estadística Inferencial", insertar el nuevo gráfico de comparación de IC.
    - Insertar el **Violin Plot** (Leslie) para dar soporte visual al Contraste de Hipótesis.
    - Sincronizar los colores y etiquetas con la nomenclatura del país/moneda detectado.

## Open Questions

- ¿Te gustaría que el gráfico de Inferencia compare todos los niveles de experiencia o solo Senior vs Mid-level como en la prueba de hipótesis actual? (Propuesta: Comparar todos para dar una visión global del mercado en ese país).

## Verification Plan

### Automated Tests
- Generar el PDF y verificar que la sección 2 contiene al menos dos gráficos (Barras de IC y Violin Plot).

### Manual Verification
- Comprobar que los gráficos del PDF reflejan correctamente el filtrado geográfico (ej. si se filtra España, los gráficos deben corresponder solo a los salarios de España).
