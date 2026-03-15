# 📅 Plan de Tareas: Microsoft Planner (Teams)

Este documento detalla la planificación de tareas para el equipo, adaptada a las fases y objetivos definidos en Microsoft Teams. Cada integrante es responsable de completar la lógica en los archivos correspondientes según este esquema.

---

## 📂 Fase 2 - Análisis Descriptivo

### 👤 Rafael Rodriguez
#### **Tarea 2.1: Calcular estadísticos**
- [ ] **2.1.1. Tabla por variable**: Implementar en `analisis/estadisticos.py` la generación de tablas resumen.
- [ ] **2.1.2. Media, mediana y moda**: Completar el cálculo de medidas de tendencia central.

### 👤 Bryann Vallejo
#### **Tarea 2.2: Calcular dispersión**
- [ ] **2.2.1. Rango y desviación**: Implementar medidas de dispersión en `analisis/estadisticos.py`.
- [ ] **2.2.2. Varianza por variable**: Completar el cálculo de la varianza.

### 👤 Leslie Ross
#### **Tarea 2.3: Crear gráficos**
- [ ] **2.3.1. Mínimo o más de 5 gráficos**: Implementar las funciones de dibujo en `analisis/graficos.py`.
- [ ] **2.3.2. Exportar alta calidad en imágenes**: Asegurar que `generate_plots.py` guarda los archivos en `/outputs/graficos/`.

### 👥 Leslie + Bryann
#### **Tarea 2.4: Análisis regresión + Correlación**
- [ ] **2.4.1. Scatter plot**: Implementar gráfico de dispersión con línea de tendencia en `analisis/graficos.py`.
- [ ] **2.4.2. Coeficiente Pearson**: Calcular la correlación estadística entre variables numéricas.

---

## 📂 Fase 3 - Análisis Inferencial

### 👥 Leslie y Bryann
#### **Tarea 3.1: Calcular IC 95% (Variable 1)**
- [ ] **3.1.1. IC 95% media**: Implementar en `analisis/inferencial.py` para la variable `salary_in_usd`.
- [ ] **3.1.2. Justificar el método**: Documentar el uso de la distribución T o Z según la muestra.

### 👤 Leslie
#### **Tarea 3.2: Calcular IC 95% (Variable 2)**
- [ ] **3.2.1. IC 95% media**: Implementar en `analisis/inferencial.py` para la variable `salary`.
- [ ] **3.2.2. Justificar método**: Documentar la selección técnica del procedimiento.

### 👤 Bryann
#### **Tarea 3.3: Contraste Hipótesis (Variable 1)**
- [ ] **3.3.1. H0 y H1**: Definir las hipótesis nula y alternativa en el código de `analisis/inferencial.py`.
- [ ] **3.3.2. Calcular p-valor**: Implementar la ejecución del T-test.

### 👥 Rafael y Bryann
#### **Tarea 3.5: Justificación métodos elegidos**
- [ ] **3.5.1. Supuestos verificados**: Implementar en `analisis/inferencial.py` las pruebas de normalidad y homocedasticidad.
- [ ] **3.5.2. Relevancia Ingeniería**: Documentar las conclusiones técnicas de los resultados obtenidos.

---

## 🏛️ Notas del Coordinador (Rubén Gámez)
- **Integración**: Los resultados de estas tareas se verán reflejados automáticamente en la App tras completar los archivos `.py`.
- **Formato**: Respetar el formato de localización español (puntos para miles, comas para decimales).
