# MEMORIA TÉCNICA DE INGENIERÍA: DASHBOARD ESTADÍSTICO
**Coordinador y Desarrollador:** Rubén Gámez Torrijos
**Proyecto:** Análisis Estadístico v2.5.3

## 1. Introducción
La presente memoria técnica describe la arquitectura y el desarrollo de la aplicación "Dashboard Estadístico", una herramienta diseñada para facilitar el análisis de datos complejos en el ámbito de la ingeniería. Bajo la dirección de Rubén Gámez Torrijos, se ha creado una plataforma que combina potencia de cálculo con una interfaz de usuario premium.

## 2. Arquitectura de Software
La aplicación sigue una estructura modular orientada a la mantenibilidad y la eficiencia:
- **Módulo de Entrada:** Capacidad para procesar archivos CSV y Excel con detección automática de tipos y limpieza de datos (eliminación de nulos y duplicados).
- **Módulo de Estilos (`views/styles.py`):** Implementación de una capa de personalización CSS que sobrescribe el diseño estándar de Streamlit para ofrecer una estética corporativa y profesional.
- **Módulo de Análisis:** Utilización de librerías científicas (`SciPy`, `Pandas`) para realizar análisis descriptivos, cálculos de intervalos de confianza, tests de normalidad y correlaciones.

## 3. Validación Científica de los Cálculos
Para garantizar la precisión de los resultados, el sistema implementa los siguientes fundamentos matemáticos:

### 3.1. Estadísticos Descriptivos
- **Media y Desviación:** Se utiliza la corrección de Bessel ($n-1$) para el cálculo de la desviación típica muestral, asegurando un estimador insesgado de la varianza poblacional.
- **Asimetría y Curtosis:** Implementados mediante los momentos centrales de la distribución para caracterizar la forma de la campana de datos.

### 3.2. Intervalos de Confianza (IC 95%)
El cálculo del IC para la media se basa en la distribución **t-Student**, ideal para muestras de ingeniería donde la varianza poblacional es desconocida:
$$IC = \bar{x} \pm t_{\alpha/2, n-1} \cdot \frac{s}{\sqrt{n}}$$
Donde:
- $t_{\alpha/2, n-1}$ es el valor crítico obtenido mediante la API `scipy.stats.t.ppf`.
- $s/\sqrt{n}$ es el error estándar de la media (`scipy.stats.sem`).

### 3.3. Contraste de Hipótesis y Normalidad
- **Normalidad:** El sistema selecciona automáticamente el test más robusto según el tamaño de la muestra ($n$):
    - Si $n \leq 5000$: Test de **Shapiro-Wilk** (`stats.shapiro`).
    - Si $n > 5000$: Test de **Kolmogorov-Smirnov** (`stats.kstest`).
- **Comparación de Grupos:** Se utiliza **ANOVA de una vía** para múltiples grupos y el **Test T de Welch** para dos grupos, el cual no asume igualdad de varianzas (heterocedasticidad), siendo más preciso en datos reales de ingeniería.

## 4. Integración Exhaustiva de APIs
El dashboard orquestra diversas APIs de alto nivel para el manejo de datos:

- **Pandas API:** Gestión de DataFrames, agregación avanzada (`groupby().agg()`) y limpieza de duplicados. Es el motor que garantiza la integridad estructural del dataset.
- **NumPy API:** Operaciones vectorizadas y manejo de valores `NaN`, optimizando el rendimiento computacional.
- **SciPy Stats API:** Proveedor de todas las funciones de distribución de probabilidad y tests inferenciales. Garantiza que los p-valores calculados sigan los estándares estadísticos rigurosos.
- **Matplotlib & Seaborn API:** Generación de histogramas con curvas de densidad (KDE) y diagramas de caja (Boxplots) para la visualización de la distribución y outliers.

## 5. Diseño y UX (Interfaz Adaptativa)
- **Tema Dinámico:** El sistema utiliza variables CSS (`var(--background-color)`) sincronizadas con el motor de Streamlit.
- **Corrección Mobile:** Se han implementado overrides de CSS con alta especificidad (`!important`) para anular estilos en línea de opacidad cero en dispositivos móviles, garantizando que el menú sea sólido y legible en cualquier pantalla.

## 6. Conclusión
La arquitectura actual representa una solución de ingeniería de software madura, enfocada en la precisión del dato y la excelencia en la experiencia de usuario. La validación matemática mediante librerías científicas asegura que el dashboard sea una herramienta de decisión confiable para el análisis estadístico profesional.
