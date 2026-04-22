Hay una cosa que no se ha definido y es el esquema de tareas definidas por cada rol tareas asociadas a las funciones y archivos desarrollados en esta arquitectura. Y luego que cada uno documente y verifique lo que ha desarrollado en el código para definirlo como tareas en Teams Planner.  Por ejemplo, actualmente tengo estas tareas definidas en Teams Planner:

"
# Fase 0 - Reunion inicial (esto omitelo).
- Hay 6 tareas que he creado previamente para organizar el proyecto y planificarlo. (Rubén Coordinador).

# Fase 1 - Busqueda y validación de los datos (esto omitelo).
- 1.1. Búsqueda de 3 datasets (Todos los cuatro miembros).
- 1.2. Votar dataset definido.(Rubén Coordinador). (Todos los cuatro miembros).
- 1.3. Limpieza de datos CSV o XML. (Rafael y Bryann).
- 1.4. Redactar informe propuesta (1pag.). (Rafael y Leslie).
- 1.5. Entrega y validación. (Rubén).

# Fase 2 - Preparación entorno de desarrollo (esto omítelo).
- 2.1. Github: Arquitectura y desarrollo. (Rubén Coordinador).
    - 2.1.1. Crear y validar entorno Github.
    - 2.1.2. Agregar compañeros a Github como colaboradores.
    - 2.1.3. Permisos repositorio y creación de ramas (main y dev).

- 2.2. Infraestructura Python + Streamlit. (RUbén Coordinador)
    - 2.2.1. Repositorio Github: Crear ramas main y de v con protección.
    - 2.2.2. Base del código: estructura de carpetas, requirements. protecció de ramas.
    - 2.2.3. Streamlit core: Desarrollo de app.py con navegación, sidebar adaptativo.
- 2.3. Clonar estructura MAIN y DEV copiar en ramas individuales. (Tres miembros)
    - 2.3.1. Clonar ramas y dev (Rafael)
    - 2.3.2. Clonar ramas y dev (Leslie)
    - 2.3.3. Clonar ramas y dev (Bryann)

# Fase 3 - Análisis descriptivo: 
- 3.1. Calcular estadísticos: (Rafael)
    - 3.1.1. Tabla por variable implementar en en "estadisticos.py"
    - 3.1.2. Media, mediana y moda: Completar el cálculo de medidas de tendencia.
- 3.2. Calcular dispersión: (Bryann).
    - 3.2.1. Rango y desviación: Implementación de métricas de variabilidad en `analisis/estadisticos.py`.
    - 3.2.2. Varianza por variable: Cálculo de la varianza para el análisis de dispersión.
- 3.3. Crear gráficos: (Leslie)
    - 3.3.1. Mínimo o más de 5 gráficos: Creación de histogramas y boxplots en `analisis/graficos.py`.
    - 3.3.2. Exportar alta calidad en imágenes: Generación de archivos PNG en `/outputs/graficos/`.
- 3.4. Análisis regresión + correlación: (Bryann y Leslie).
    - 3.4.1. Scatter plot: Implementación de gráfico de dispersión con línea de regresión.
    - 3.4.2. Coeficiente Pearson: Cálculo del coeficiente de correlación para evaluar la fuerza de la relación.
- 3.5. Discusión crítica (Los cuatro miembros debemos verificar la información y datos realizados mostrados).
    - 3.5.1. Cada miembro crear 2 párrafos en base a los cálculos.
    - 3.5.2. Cuatro contribuciones en el documento explicando su parte.

- 3.6. Redactar borrador informe de 2 a 3 páginas. (Rafa y Leslie).
    - 3.6.1. Unir tablas + gráficos
    - 3.6.2. Completar formato PDF

- 3.7. Revisión cruzada informe 2: (Rubén y Bryann)
    - 3.7.1. Leer infrome completo anterior del 3.6.2
    - 3.7.2. Comentar errores y validar la información de los datos mostrados.

# Fase 4 - Análisis inferencial:
- 4.1. Calcular IC95% para la variable Salario. (Bryann y Leslie).
    - 4.1.1. IC95% media: implementación para "salary_in_usd/salary_in_eur"
    - 4.1.2. Justificar el método: documentación sobre la elección
- 4.2. Calcular IC 95% para la variable Experiencia. (Leslie).
    - 4.2.1. IC95% media: implementación para "experience_level" y "salary_in_eur"
    - 4.2.2. Justificar el método: documentación sobre la elección
- 4.3. Calcular Contraste de hipótesis. (Bryann).
    - 4.3.1. H0 y H1: Definición de hipótesis nula y alternativa para comparar niveles de experiencia.
    - 4.3.2. Calcular p-valor: Ejecución de la prueba estadística y obtención de significancia.
- 4.4. Calcular contraste de hipótesis para la variable Modalidad. (Rafael y Leslie).
    - 4.4.1. H0 y H1 (Variable 2): Definición de hipótesis (ej: Remoto vs Presencial).
    - 4.4.2. Calcular p-valor: Ejecución del test para la segunda variable de interés.
-4.5. Justificación métodos elegidos: (Rafael y Bryann).
    - 4.5.1. Explicar por qué se eligieron estos métodos y supuestos verificados.
    - 4.5.2. Explicar qué se puede concluir de los resultados y la Relevancia de ingeniería de los datos.
- 4.6. Redactar borrador informe de 2 a 3 páginas. (Bryann y LEslie).
    - 4.6.1. Unir tablas + gráficos.
    - 4.6.2. Completar formato PDF.

- 4.7. Revisión cruzada informe 3: (Rubén y Rafael)
    - 4.7.1. Leer infrome completo anterior del 4.6.2
    - 4.7.2. Comentar errores y validar la información de los datos mostrados.

# Fase 5 - App Streamlit
- 5.1. Desarrollar app Streamlit: (Rubén)
    - 5.1.1. Crear app Streamlit en `app.py`
    - 5.1.2. Crear config Streamlit en `.streamlit/config.toml`
    - 5.1.3. Crear styles Streamlit en `.streamlit/styles.py`

- 5.2. Verificar App Streamlit (main): (Rubén)
    - 5.2.1. Revisar código y dependencias
    - 5.2.2. Revisar app desplegada y funcionalidad
    - 5.2.3. Verificar informes exportados (pdf y xlsx)
    
- 5.3. Redactar borrador conclusiones (1-2 pag.): (Todos los cuatro miembros).
    - 5.3.2. Unir documentación al directorio teams.

- 5.4. Conclusiones consensuadas: (Todos los cuatro miembros).
    - 5.4.1. Reunión votar finales documentación
    - Incorporar al PDF final.

- 5.5. Guión del vídeo (7 - 10 min.): (Todos los cuatro miembros).
    - 5.5.1. Cada uno su sección con el guión.
    - 5.5.2. 1-2 min/persona.

- 5.6. Grabación del vídeo (sin cámara): (Todos los cuatro miembros).
    - 5.6.1. Cada uno graba audio (teams) 1-2min. aprox.
    - 5.6.2. Duración 7-10min. total todos juntos en Teams.

- 5.7. Edición del vídeo (en caso de exista): (Rubén)
    - 5.7.1. Unir o editar audios.
    - 5.7.2. Añadir gráficos y presentación.
    - 5.7.3. Demo final web con Streamlit 

- 5.8. Unificar memoria final PDF. (Rafael y Rubén).
    - 5.8.1. Juntar 4 informes y verificar que están bien.
    - 5.8.2. Completar informe memoria y datos csv limpios.

# Fase 6 - Entrega y cierre:

- 6.1. Registro de partición: (Todos los cuatro miembros).
    - 6.1.1. Calcular % por miembro.
    - 6.1.2. Todos firman conformidad.
    - 6.1.3. Crear un informe individual del trabajo aportado.

- 6.2. Entrega final colectiva: (Todos los cuatro miembros).
    - 6.2.1. Verificar documentación memoria técnica final.
    - 6.2.2. Verificar vídeo-presentación.
    - 6.2.3. Verificar  proyecto Python+Streamlit desplegado.
    - 6.2.4. Verificar participación y % de trabajo realizado.

- 6.3. Eliminar grabaciones de reuniones (después de evaluar): (Rubén).
    - 6.3.1. Borrar de Teams (sólo cuando esté evaluado).
    - 6.3.2. Confirmar borrado (grabaciones de reuniones).

- 6.4. Archivar proyecto en Teams. (Confirmar todos los cuatro miembros).
    - 6.4.1. Mover a Archivo.
    - 6.4.2. Captura final de todo borrado y archivado.

"
# Nueva mejora añadida al proyecto que habría que introducir en el planner de Team (en este caso será Rubén coordinador quién lo completará para adelantar esta mejora).

Toda estas fases es como se encuentran ordenadas de todo el proyecto, y habría que añadir la opción 2 añadir una variable como indice de coste de vida por país, por ejemplo: 

- Ej: USA = 100, España = 70
- Lo unimos con company_location
- Nueva variable: cost_of_living_index

Aquí podemos analizar si los salarios suben porque el país es más caro.

Cómo se puede ver este sería lo que se ha planificado y dividido en tareas todo lo que conlleva el proyecto desde la organización hasta la entrega y cierre. Esto es importante para poder dividir muy bien las tareas incluyendo la parte del desarrollo de este proyecto de código en python+streamlit con las funciones asignadas a los roles, quiero que organices el Planner de Teams  por si falta o sobrase algo o no estuviese bien organizado o faltase algo y definiendo también quiénes  deben hacerlo.