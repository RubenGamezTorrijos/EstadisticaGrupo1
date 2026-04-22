# 📅 Planner de Teams - Proyecto Estadística (v.2.2.1)
*Actualizado por Rubén (Coordinador) para la nueva arquitectura MVC*

---

## 🏗️ Fase 3 - Desarrollo de la Infraestructura (En curso)

### 👨‍💻 RAFAEL RODRIGUEZ (Data Manager)
- **Tarea 3.1: Pipeline de Datos Robusto**
    - [x] Merge inicial con dataset COLI.
    - [x] Implementación de lógica multimoneda (USD/EUR) en `models/data_loader.py`.
    - [ ] **[NUEVA]** Integración con API del Banco Mundial (Inflación/PIB) para enriquecimiento dinámico.
    - [ ] **[NUEVA]** Sistema de validación de integridad (manejo de países sin índice COLI).
- **Tarea 3.2: Estadísticos Base**
    - [x] Implementar `calcular_estadisticos` en `analisis/estadisticos.py`.
    - [ ] Realizar análisis de tendencia central por país y categoría.

### 👩‍💻 LESLIE ROSS (Analista Visual)
- **Tarea 3.3: Catálogo Visual Descriptivo**
    - [ ] Implementar `crear_histograma` y `crear_boxplot` en `analisis/graficos.py`.
    - [ ] Implementar `crear_violin_plot` y `crear_bar_chart` en `analisis/graficos.py`.
- **Tarea 3.4: Regresión Lineal**
    - [ ] Implementar lógica de `crear_scatter_regresion` y calcular coeficientes en `analisis/modelo_regresion.py`.
- **Tarea 3.5: Integración Visual**
    - [ ] Configurar el renderizado de gráficos en `views/layout.py` (Pestañas 3 y 5).

### 👨‍💻 BRYANN VALLEJO (Analista Inferencial)
- **Tarea 3.6: Motor Inferencial**
    - [ ] Implementar `calcular_ic_95` para salarios en `analisis/inferencial.py`.
    - [ ] Desarrollar `contraste_hipotesis` (T-test) para comparar niveles de experiencia.
- **Tarea 3.7: Validación de Supuestos**
    - [ ] Implementar test de normalidad (Shapiro-Wilk) en `analisis/inferencial.py`.
- **Tarea 3.8: Integración de Resultados**
    - [ ] Configurar la visualización de p-valores e intervalos en `views/layout.py` (Pestaña 4).

### 👨‍💻 RUBÉN GÁMEZ (Coordinador)
- **Tarea 3.9: Orquestación y UI**
    - [x] Diseño del Sidebar Navy Blue con centrado de logo.
    - [x] Sistema de navegación y filtros globales.
    - [x] Motor de exportación PDF y Excel multiplataforma.
    - [ ] **[NUEVA]** Revisión de código y resolución de conflictos entre ramas main/dev.

---

## 📄 Notas de Referencia
*   La rama **`main`** sirve como referencia de producción (contiene el código objetivo).
*   La rama **`dev`** es la zona de desarrollo donde Leslie y Bryann deben completar sus tareas.
*   Rafael tiene ahora la responsabilidad adicional de automatizar la entrada de datos vía API.
