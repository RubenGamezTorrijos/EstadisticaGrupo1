# Plan: Creación de Entorno de Desarrollo Colaborativo (v.2.1.6)

Este plan transformará la rama `dev` en un entorno de "Plantilla Modular" donde Leslie y Bryann puedan trabajar en sus respectivas áreas sin solaparse, siguiendo una arquitectura desacoplada (MVC).

## Cambios Propuestos

### 1. Sincronización y Preparación
- [ ] Fusionar rama `main` en `dev` para tener la arquitectura más reciente.
- [ ] Crear un archivo `GUIA_DESARROLLO.md` que explique el flujo de trabajo y la propiedad de cada archivo.

### 2. Espacio de Trabajo de Leslie (Descriptiva y Regresión)
- [MODIFY] `analisis/graficos.py`:
    - Reemplazar funciones complejas con versiones simplificadas (ej. un gráfico de barras básico).
    - Insertar docstrings con `TODO: Implementar visualización premium segun rúbrica`.
- [MODIFY] `analisis/modelo_regresion.py`:
    - Dejar la estructura del modelo pero con una lógica trivial.
    - Añadir guías técnicas sobre cómo calcular el coeficiente $R^2$.

### 3. Espacio de Trabajo de Bryann (Inferencial)
- [MODIFY] `analisis/inferencial.py`:
    - Convertir las funciones de IC y Contrastes en "Stubs" (esbozos).
    - Definir claramente los parámetros de entrada y salida necesarios para que `app.py` no falle.
- [MODIFY] `app.py`:
    - En la sección de Inferencia, añadir un mensaje `st.warning("⚠️ Sección bajo desarrollo por Bryann")`.

### 4. Arquitectura de Rubén y Rafael
- Estos módulos se mantienen completos ya que sirven como la base estable sobre la que se construye el resto.

## Verificación Planificada
- [ ] Correr `streamlit run app.py` para asegurar que las secciones "vacías" no provocan errores de Python.
- [ ] Verificar que el menú lateral navega correctamente a todas las vistas.

## Preguntas al Usuario
- ¿Deseas que deje la solución real comentada en los archivos o prefieres que los archivos estén totalmente limpios de la lógica compleja para que ellos la construyan desde cero?
- ¿Añadimos un "Modo Desarrollador" en la barra lateral que cambie entre la vista Template y la vista Final (si se desea)?
