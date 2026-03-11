# 🛠️ Entorno de Desarrollo - Grupo 1 (Estadística y Optimización)

## ⚠️ AVISO PARA EL EQUIPO
Este repositorio está configurado como la **base de desarrollo (SKELETON)**. La arquitectura del proyecto, la integración de la interfaz (Streamlit) y el motor de formateo ya han sido desarrolladores por el Coordinador (Rubén Gámez). 

**Vuestro objetivo es completar la lógica estadística de los archivos asignados para que el proyecto sea 100% funcional.**

---

## 🚀 Cómo empezar a trabajar en Local

1. **Clonar la rama de desarrollo**:
   ```bash
   git clone -b dev [URL_DEL_REPOSITORIO]
   cd proyecto_estadistica
   ```

2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar la App (para ver cambios en tiempo real)**:
   ```bash
   streamlit run app.py
   ```
   *Nota: Inicialmente veréis advertencias amarillas en la app. Estas desaparecerán a medida que completéis vuestro código.*

---

## 📝 Instrucciones de Contribución

Cada integrante debe completar el **90% de la lógica** en sus archivos respectivos. Buscad los comentarios marcados como `TODO` dentro de cada archivo.

### 1. Rafael Rodriguez (Data Manager)
*   **Archivo**: `analisis/estadisticos.py`
*   **Tarea**: Implementar la limpieza de datos y las funciones de estadística descriptiva (media, mediana, moda, etc.).
*   **Archivo**: `app.py` (Sección Escritorio General)
*   **Tarea**: Reconstruir la visualización de métricas generales siguiendo las instrucciones en el código.

### 2. Leslie Ross (Visualization Expert)
*   **Archivo**: `analisis/graficos.py`
*   **Tarea**: Implementar las funciones de gráficas usando Seaborn y Matplotlib (Histogramas, Boxplots y Regresión).

### 3. Bryann Vallejo (Inferential Analyst)
*   **Archivo**: `analisis/inferencial.py`
*   **Tarea**: Implementar el cálculo de Intervalos de Confianza (95%) y la lógica del contraste de hipótesis (T-test).

---

## 🏛️ Reglas del Proyecto
*   **No modificar `app.py`** fuera de las zonas marcadas para Rafael, salvo autorización del Coordinador.
*   **Formato**: Mantened el estilo de codificación y usad comentarios para explicar vuestras fórmulas.
*   **Commits**: Realizad mensajes de commit descriptivos (ej: `feat(stats): implementada limpieza de outliers`).

---
*Cualquier duda técnica, consultad con el Coordinador (Rubén Gámez).*
