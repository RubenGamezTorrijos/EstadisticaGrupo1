# Plan de Definición de Tareas y Metodología (Fase 3 & 4)

Este plan define la estructura final de responsabilidades y el "Manual de Procedimiento" para que el equipo (Rafael, Leslie y Bryann) complete el desarrollo del proyecto **v.2.2.1**.

## User Review Required

> [!IMPORTANT]
> He definido los archivos específicos por rol basándome en la arquitectura modular. Por favor, confirma si estás de acuerdo con este reparto técnico antes de que lo formalice en el Manual de Desarrollo.

## Proposed Changes

### Documentación de Gestión y Técnica

#### [NEW] [manual_desarrollo_v2.2.1.md](file:///c:/Users/ruben/Proyectos/Antigravity/proyecto_estadistica/manual_desarrollo_v2.2.1.md)
Documento detallado que explica a cada miembro:
1. Qué archivos debe abrir.
2. Qué librerías usar (Pandas, Seaborn, SciPy).
3. Cómo implementar la lógica matemática dentro de los stubs (Modo Puzle).

#### [MODIFY] [final_planner_guide_v.2.2.1.md](file:///c:/Users/ruben/Proyectos/Antigravity/proyecto_estadistica/brain/9d81e5cb-6f5d-423d-890b-5685868688ee/final_planner_guide_v.2.2.1.md)
Actualizar el Planner para incluir los enlaces directos a los archivos y referencias al Manual de Desarrollo.

### Reparto Técnico por Rol

| Miembro | Rol | Archivos Clave | Tecnologías |
| :--- | :--- | :--- | :--- |
| **Rafael Rodriguez** | Data Manager | `estadisticos.py`, `setup_data.py` | Pandas, NumPy |
| **Leslie Ross** | Descriptivo | `graficos.py` | Seaborn, Matplotlib |
| **Bryann Vallejo** | Inferencial | `inferencial.py` | SciPy Stats, Sklearn |

---

## Open Questions

- ¿Quieres que incluya una sección en el manual sobre cómo usar **Git** para que suban sus cambios de forma segura a sus respectivas tareas?
- ¿Los miembros del equipo tienen conocimientos previos de las librerías mencionadas o prefieres que los "Cómo" incluyan ejemplos de código básicos?

## Verification Plan

### Manual Verification
1. Verificar que cada archivo (`estadisticos.py`, `graficos.py`, `inferencial.py`) contiene los comentarios `# TODO` y `# 💡 PISTA` correctos.
2. Validar que el manual sea legible y profesional.
