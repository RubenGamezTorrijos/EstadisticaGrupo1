# Plan de Implementación: Entorno de Colaboración Estricto (v.2.1.10)

Este plan detalla cómo transformar la rama `dev` en un "Puzle Técnico" real. A diferencia de la versión actual, las gráficas y resultados inferenciales **no se mostrarán por defecto**, obligando a Leslie y Bryann a implementar la lógica para que la aplicación cobre vida.

## Cambios Propuestos

### 1. "Vaciado" Estricto de Lógica (`analisis/`)

Moveremos el código funcional actual al bloque de `# 💡 PISTA` y dejaremos las funciones en estado de "Pendiente".

#### [MODIFY] [graficos.py](file:///c:/Users/ruben/Proyectos/Antigravity/proyecto_estadistica/analisis/graficos.py)
- Las funciones como `crear_histograma` dejarán de ejecutar `sns.histplot`.
- Retornarán `None` o una figura vacía con un texto central: "IMPLEMENTACIÓN PENDIENTE: LESLIE".
- El código útil de referencia quedará 100% comentado.

#### [MODIFY] [inferencial.py](file:///c:/Users/ruben/Proyectos/Antigravity/proyecto_estadistica/analisis/inferencial.py)
- `calcular_ic_95` y `contraste_hipotesis` retornarán diccionarios vacíos o con valores `0.0`.
- Se añadirán advertencias en los comentarios sobre la necesidad de usar `scipy.stats`.

---

### 2. UI Inteligente en `app.py`

Modificaremos la interfaz para que detecte si un módulo está "vacío" y muestre una tarjeta de tarea en su lugar.

#### [MODIFY] [app.py](file:///c:/Users/ruben/Proyectos/Antigravity/proyecto_estadistica/app.py)
- Implementar bloques `if result is None:` para mostrar `st.info()` o `st.warning()` con las instrucciones del rol.
- **Leslie**: "Gráfico no disponible. Leslie debe implementar la función `crear_histograma` siguiendo las pistas en el archivo."
- **Bryann**: "Análisis inferencial pendiente. Bryann debe completar el contraste de hipótesis."

---

### 3. Informe Comparativo Final

Crearé un documento que compare esta nueva estructura con el commit `6413946a` solicitado, demostrando que:
- `6413946a` era el código "resuelto" (Referencia).
- `dev` v.2.1.10 es el "puzle" (Tareas).

## User Review Required

> [!IMPORTANT]
> ¿Estás de acuerdo con que la aplicación **no muestre nada** (solo el banner de tarea) hasta que ellos escriban el código? 
> Esto forzará a que tengan que trabajar, pero la página se verá con muchos banners azules/amarillos inicialmente.

## Plan de Verificación

### Pruebas Manuales
1. Arrancar `streamlit run app.py` y verificar que las secciones de Leslie y Bryann muestran el banner de "Tarea Pendiente".
2. Simular la finalización de una tarea (copiando una pista al código activo) y verificar que el gráfico/dato aparece automáticamente.
3. Asegurarse de que el botón de descarga de informes no de error `ImportError`.
