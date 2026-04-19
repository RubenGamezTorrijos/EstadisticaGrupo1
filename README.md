# 🛠️ Entorno de Desarrollo - Grupo 1 (Estadística y Optimización)

## ⚠️ AVISO PARA EL EQUIPO
Este repositorio está configurado como la **base de desarrollo (SKELETON)**. La arquitectura del proyecto, la integración de la interfaz (Streamlit) y el motor de formateo ya ha sido desarrollado.

**Vuestro objetivo es completar la lógica estadística de los archivos asignados para que el proyecto sea 100% funcional.**

---

## 👥 Equipo y Roles Técnicos (Grupo 1)

### 👤 Rubén Gámez Torrijos (Coordinador)
- [x] **Arquitectura Core**: Desarrollo de `app.py` y sistema de navegación modular.
- [x] **Multidivisa**: Implementación del selector global USD/EUR.
- [x] **Exportación**: Sistema de reportes dinámicos en PDF y Excel.

### 👤 Rafael Rodriguez Mengual (Data Manager)
- [x] **Limpieza de Datos**: Script de procesamiento en `analisis/estadisticos.py`.
- [x] **Mejora COLI**: Integración del Índice de Coste de Vida por país.
- [x] **Estadísticos**: Generación de la tabla unificada de medidas de tendencia y dispersión.

### 👤 Bryann Vallejo Luna (Analista Inferencial)
- [x] **Intervalos de Confianza**: Implementación de IC 95% para Salario y COLI.
- [/] **Contrastes de Hipótesis**: Test de medias para Experiencia y Modalidad (En revisión en rama `dev`).
- [ ] **Justificación**: Redacción técnica de p-valores.

### 👤 Leslie Ross Aranibar Pozo (Analista Descriptivo)
- [x] **Visualizaciones**: Implementación de Histogramas, Boxplots y Violin Plots.
- [x] **Regresión**: Modelo lineal Salario vs COLI con coeficiente Pearson.
- [/] **Calidad**: Exportación de gráficos en alta resolución (Rama `dev`).

---

## 🚀 Cómo empezar a trabajar en Local

1. **Requisito de Python**: Se requiere **Python 3.9 o superior** (Recomendado: **3.12**).
2. **Clonar la rama de desarrollo**:
   ```bash
   git clone -b dev https://github.com/RubenGamezTorrijos/EstadisticaGrupo1.git
   cd proyecto_estadistica
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la App (para ver cambios en tiempo real)**:
   ```bash
   streamlit run app.py
   ```

> [!IMPORTANT]
> Si no tienes un entorno virtual, créalo con `python -m venv .venv` y actívalo con `.venv\Scripts\activate`


> [!WARNING]
> Inicialmente veréis advertencias amarillas en la app. Estas desaparecerán a medida que completéis vuestro código.

---

## 📝 Equipo y Asignación de Archivos

| Integrante | Rol | Archivos Desarrollados |
| :--- | :--- | :--- |
| **Rafael Rodriguez** | Data Manager | `analisis/estadisticos.py`, archivos CSV en `datos/` |
| **Bryann Vallejo** | Analista Inferencial | `analisis/inferencial.py`, tablas CSV en `outputs/tablas/` |
| **Leslie Ross** | Analista y Visualización | `analisis/graficos.py`, `generate_plots.py`, gráficos PNG en `outputs/graficos/` |
| **Ruben Gamez** | Coordinación y Desarrollo | `app.py`, `setup_data.py`, `requirements.txt`, `.gitignore` |

### Detalle de Tareas:

#### 1. Rafael Rodriguez
*   **Lógica**: Implementar limpieza de datos y estadísticos (media, mediana, moda, etc.) en `analisis/estadisticos.py`.
*   **UI**: Reconstruir la visualización de métricas en la sección "Escritorio General" de `app.py`.

#### 2. Bryann Vallejo
*   **Inferencia**: Implementar Intervalos de Confianza (95%) y T-tests en `analisis/inferencial.py`.
*   **Output**: Asegurar la correcta generación de tablas de resultados en `outputs/tablas/`.

#### 3. Leslie Ross
*   **Gráficos**: Desarrollar funciones para Histogramas, Boxplots y Regresión en `analisis/graficos.py`.
*   **Scripts**: Mantener `generate_plots.py` para la generación masiva de recursos visuales.

---

## 📸 Capturas de la Aplicación

| Escritorio General | Estadísticos Descriptivos |
| :---: | :---: |
| ![Captura 1](capturas/captura_1_app_streamlit_escritorio_general.jpg?v=2) | ![Captura 2](capturas/captura_2_app_streamlit_analisis_descriptivo_estadisticos.jpg?v=2) |
| **Visualizaciones** | **Regresión Lineal** |
| ![Captura 3](capturas/captura_3_app_streamlit_analisis_descriptivo_visualizaciones.jpg?v=2) | ![Captura 4](capturas/captura_4_app_streamlit_analisis_descriptivo_regresion.jpg?v=2) |
| **Estadística Inferencial** | **Equipo Grupo 1** |
| ![Captura 5](capturas/captura_5_app_streamlit_estadistica_inferencial.jpg?v=2) | ![Captura 6](capturas/captura_6_app_streamlit_equipo_del_grupo1.jpg?v=2) |

---

## 🏛️ Reglas del Proyecto
*   **No modificar `app.py`** fuera de las zonas marcadas, salvo autorización del Coordinador.
*   **Formato**: Mantened el estilo de codificación y usad comentarios para explicar vuestras fórmulas.
*   **Commits**: Realizad mensajes de commit descriptivos (ej: `feat(stats): implementada limpieza de outliers`).

---
> [!CAUTION]
> Cualquier duda técnica, consultad con el Coordinador (Rubén Torrijos).

---
*© 2026 - Universidad Europea - Grado en Ingeniería - Estadística y Optimización*