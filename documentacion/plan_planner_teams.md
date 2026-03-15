# 📅 Plan de Tareas: Microsoft Planner (Teams) - PROYECTO ESTADÍSTICA

Este documento organiza el trabajo en 3 fases clave, adaptadas a la estructura de Planner en Microsoft Teams. Incluye las tareas ya realizadas por el Coordinador y los bloques pendientes para el resto del equipo.

---

## 📂 Fase 1 - Preparación del Entorno (Finalizada por Rubén Gámez)

### 👤 Rubén Gámez
#### **Tarea 1.1: Setup de Infraestructura**
- [x] **1.1.1. Repositorio GitHub**: Creación de ramas `main` y `dev` con protección de ramas.
- [x] **1.1.2. Base del Código**: Estructura de carpetas, `requirements.txt` y configuración `.gitignore`.
- [x] **1.1.3. Streamlit Core**: Desarrollo de `app.py` con navegación, sidebar adaptativo y formateo numérico.

---

## 📂 Fase 2 - Análisis Descriptivo

### 👤 Rafael Rodriguez
#### **Tarea 2.1: Calcular estadísticos**
- [ ] **2.1.1. Tabla por variable**: Generación de tablas de resumen estadístico en `analisis/estadisticos.py`.
- [ ] **2.1.2. Media, mediana y moda**: Implementación de funciones de tendencia central para variables numéricas.

### 👤 Bryann Vallejo
#### **Tarea 2.2: Calcular dispersión**
- [ ] **2.2.1. Rango y desviación**: Implementación de métricas de variabilidad en `analisis/estadisticos.py`.
- [ ] **2.2.2. Varianza por variable**: Cálculo de la varianza para el análisis de dispersión.

### 👤 Leslie Ross
#### **Tarea 2.3: Crear gráficos**
- [ ] **2.3.1. Mínimo o más de 5 gráficos**: Creación de histogramas y boxplots en `analisis/graficos.py`.
- [ ] **2.3.2. Exportar alta calidad en imágenes**: Generación de archivos PNG en `/outputs/graficos/`.

### 👥 Leslie + Bryann
#### **Tarea 2.4: Análisis regresión + Correlación**
- [ ] **2.4.1. Scatter plot**: Implementación de gráfico de dispersión con línea de regresión.
- [ ] **2.4.2. Coeficiente Pearson**: Cálculo del coeficiente de correlación para evaluar la fuerza de la relación.

---

## 📂 Fase 3 - Análisis Inferencial

### 👥 Leslie y Bryann
#### **Tarea 3.1: Calcular IC 95% (Variable 1)**
- [ ] **3.1.1. IC 95% media**: Implementación para `salary_in_usd` en `analisis/inferencial.py`.
- [ ] **3.1.2. Justificar el método**: Documentación sobre la elección de la distribución (Z o T).

### 👤 Leslie
#### **Tarea 3.2: Calcular IC 95% (Variable 2)**
- [ ] **3.2.1. IC 95% media**: Implementación para `salary` (EUR) en `analisis/inferencial.py`.
- [ ] **3.2.2. Justificar método**: Breve descripción técnica del procedimiento seguido.

### 👤 Bryann
#### **Tarea 3.3: Contraste Hipótesis (Variable 1)**
- [ ] **3.3.1. H0 y H1**: Definición de hipótesis nula y alternativa para comparar niveles de experiencia.
- [ ] **3.3.2. Calcular p-valor**: Ejecución de la prueba estadística y obtención de significancia.

### 👥 Rafael y Bryann
#### **Tarea 3.5: Justificación métodos elegidos**
- [ ] **3.5.1. Supuestos verificados**: Verificación de normalidad y homogeneidad de varianzas.
- [ ] **3.5.2. Relevancia Ingeniería**: Interpretación de los resultados desde el punto de vista técnico y profesional.

---

## 🏛️ Notas para el Equipo
1. **GitHub**: Subir los cambios mediante Pull Request a la rama `dev`.
2. **Formato**: Usar el estilo adaptativo (temas claros/oscuros) ya integrado por Rubén.
3. **Sincronización**: Los TODOs en el código corresponden exactamente a los códigos de estas tareas (Ej: 2.1.1).
