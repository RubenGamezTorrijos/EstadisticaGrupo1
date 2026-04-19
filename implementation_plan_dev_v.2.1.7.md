# Plan v.2.1.7: Estabilidad, MVC y Guía Colaborativa

El objetivo es eliminar el `ImportError` en la rama `dev`, asegurar que el proyecto sigue un patrón MVC estricto y proporcionar a Leslie y Bryann las "pistas" necesarias para que puedan completar su parte basándose en la versión estable de `main`.

## User Review Required

> [!IMPORTANT]
> **Arquitectura MVC**: Se moverá toda lógica de Streamlit (`st.`) de los archivos de `analisis/` hacia `app.py`. Los archivos en `analisis/` solo devolverán datos o figuras de Matplotlib.

> [!NOTE]
> **Pistas en Rama Dev**: En lugar de borrar el código de `main` en la rama `dev`, se dejará como comentario marcado como `REFERENCIA` para que el equipo pueda aprender e implementarlo por su cuenta.

## Proposed Changes

### [app.py](file:///c:/Users/ruben/Proyectos\Antigravity\proyecto_estadistica\app.py) [MODIFY]
- Corregir importación de `verificar_supuestos_normalidad` (sincronizar con `inferencial.py`).
- Eliminar la importación errónea `render_regresion` de `analisis.modelo_regresion`.
- Asegurar que `st.set_page_config` se mantenga como primera instrucción.

---

### [Módulo Inferencial](file:///c:/Users/ruben/Proyectos\Antigravity\proyecto_estadistica\analisis\inferencial.py) [MODIFY]
- Sincronizar nombre de función: `verificar_supuestos` -> `verificar_supuestos_normalidad`.
- Añadir bloques de "PISTA DE IMPLEMENTACIÓN" comentados con el código de `main`.

### [Módulo Regresión](file:///c:/Users/ruben/Proyectos\Antigravity\proyecto_estadistica\analisis\modelo_regresion.py) [MODIFY]
- Separar lógica matemática (`ejecutar_regresion_simple`) de cualquier llamada a Streamlit.
- Añadir pistas comentadas sobre el ajuste del modelo y cálculo de métricas.

### [Módulo Gráficos](file:///c:/Users/ruben/Proyectos\Antigravity\proyecto_estadistica\analisis\graficos.py) [MODIFY]
- Limpiar cualquier dependencia de Streamlit.
- Añadir ejemplos comentados de personalización de `seaborn` (estética premium).

---

### [Módulo Estadísticos](file:///c:/Users/ruben/Proyectos\Antigravity\proyecto_estadistica\analisis\estadisticos.py) [VERIFY]
- Verificar que el trabajo de **Rafael Rodriguez** esté intacto y completo como "Data Manager".

## Open Questions

- ¿Deseas que las "pistas" en el código de `dev` sean muy detalladas (casi la solución) o solo guías matemáticas? He optado por guías técnicas y código comentado como "Referencia".

## Verification Plan

### Automated Tests
- Ejecutar `python -m streamlit run app.py` y verificar que no hay `ImportError`.
- Comprobar que en la rama `dev` se visualizan los banners de "Módulo en Desarrollo".

### Manual Verification
- Navegar a "Estadística Inferencial" y verificar que el Intervalo de Confianza se muestra (aunque sea con la plantilla).
- Navegar a "Regresión" y verificar que el gráfico y las métricas se cargan correctamente.
