# 📅 PLANIFICACIÓN DE TAREAS - TEAMS PLANNER v.2.2.1
> **Proyecto**: Análisis de Salarios en Ciencia de Datos
> **Equipo**: Grupo 1 (Rubén Torrijos, Rafael Rodriguez, Leslie Ross, Bryann Vallejo)
> **Fecha**: 22 de Abril de 2025

Este documento define la estructura de tareas para el Planner de Teams, vinculando funciones técnicas específicas con los responsables de la arquitectura.

---

## 🏛️ ESTRUCTURA POR ROLES Y FUNCIONES

### 1. COORDINACIÓN Y ARQUITECTURA (Rubén Torrijos)
*Responsable de la infraestructura base, integración de datos externos y despliegue.*

- [x] **2.1. Infraestructura Git/Github**: Creación de ramas `main` y `dev`, protección y permisos.
- [x] **2.2. Arquitectura de Datos Real**: Creación de `cost_of_living_index.csv` (Numbeo 2023).
- [x] **2.3. Integración Técnica (Scripts)**: Desarrollo de `scripts/preprocesar_coli.py` para merge de datos.
- [ ] **5.1. Core Application**: Desarrollo de `app.py` y navegación entre secciones.
- [ ] **5.2. Generador de Informes**: Implementación de `analisis/exportacion.py` para PDFs.
- [ ] **5.7. Edición y Demo**: Montaje de vídeo final y validación de la web.

### 2. DATA MANAGEMENT (Rafael Rodriguez)
*Responsable de la integridad de los datos y el análisis descriptivo numérico.*

- [x] **1.3. Limpieza de Datos**: Implementación de `limpiar_datos()` en `analisis/estadisticos.py`.
- [ ] **3.1. Estadísticos Descriptivos**: Cálculo de Media, Mediana, Moda y Dispersión (Varianza, Desv. Típica).
- [ ] **3.4. Análisis de Outliers**: Implementación del criterio IQR para detección de valores atípicos.
- [ ] **3.6. Redacción Descriptiva**: Elaboración de la tabla de estadísticos en `informes/informe_descriptivo.md`.

### 3. ANÁLISIS VISUAL Y REGRESIÓN (Leslie Ross)
*Responsable de la comunicación visual y el análisis de correlación.*

- [ ] **3.3. Visualización de Distribuciones**: Implementación de Histogramas y Violin Plots en `analisis/graficos.py`.
- [ ] **3.5. Boxplots por Categoría**: Comparativa de salarios por Nivel de Experiencia y Modalidad.
- [ ] **3.8. Modelo de Regresión**: Gráfico de dispersión Salario vs. COLI + Línea de tendencia.
- [ ] **3.9. Exportación Gráfica**: Generación de PNGs en alta resolución para el informe final.

### 4. ANÁLISIS INFERENCIAL (Bryann Vallejo)
*Responsable de la validación estadística y toma de decisiones.*

- [ ] **4.1. Estimación por Intervalos**: Cálculo de IC 95% para salarios (USD/EUR) en `analisis/inferencial.py`.
- [ ] **4.3. Contraste de Hipótesis**: Test de comparación de medias (Remote vs. On-site).
- [ ] **4.4. ANOVA de Experiencia**: Contraste de hipótesis para múltiples grupos (Entry vs Senior).
- [ ] **4.5. Verificación de Supuestos**: Tests de Normalidad (Shapiro-Wilk) y Homocedasticidad (Levene).

---

## 🚀 FASES DE EJECUCIÓN (LÍNEA TEMPORAL)

### FASE A: Integración y Limpieza (FINALIZADA)
- Consolidación del dataset real Numbeo + Jobs Data.
- Generación de `dataset_enriquecido.csv`.

### FASE B: Desarrollo de Módulos (EN CURSO)
- **Rafael**: `estadisticos.py`
- **Leslie**: `graficos.py`
- **Bryann**: `inferencial.py`

### FASE C: Integración en App y Documentación (PRÓXIMA)
- Unificación en `app.py`.
- Redacción de discusión crítica en `MANUAL_DESARROLLO.md`.

---

## 🛠️ CONTROL DE CALIDAD (CHECKLIST)
- [ ] ¿El p-valor está bien interpretado? (Bryann)
- [ ] ¿Los gráficos tienen títulos claros y leyendas? (Leslie)
- [ ] ¿La tabla de estadísticos incluye todas las medidas del enunciado? (Rafael)
- [ ] ¿El PDF se genera sin errores de formato? (Rubén)

---
*Plan de tareas validado por el Coordinador Rubén Torrijos.*
