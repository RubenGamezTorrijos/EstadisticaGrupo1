# 🤝 GUÍA DE COLABORACIÓN - PROYECTO ESTADÍSTICA

¡Hola equipo! Hemos actualizado la arquitectura del proyecto a un modelo **MVC (Modelo-Vista-Controlador)** para que podamos trabajar de forma más organizada y evitar conflictos en Git.

## 📁 Estructura de Archivos
- `app.py`: Punto de entrada. **No es necesario editarlo**.
- `analisis/`: Aquí es donde ocurre la magia matemática.
- `views/`: Aquí es donde se define cómo se ve la App.
- `models/`: Aquí se gestionan los datos.

---

## 👩‍💻 Instrucciones para LESLIE (Visualización)
Tu trabajo se centra en dos archivos:
1.  **Lógica Gráfica**: `analisis/graficos.py`
    - Implementa las funciones: `crear_histograma`, `crear_boxplot`, `crear_violin_plot`, etc.
2.  **Vista de Gráficos**: `views/layout.py` (pestaña 3)
    - Llama a tus funciones de `graficos.py` para mostrarlas en la app.

---

## 👨‍💻 Instrucciones para BRYANN (Inferencia)
Tu trabajo se centra en:
1.  **Lógica Inferencial**: `analisis/inferencial.py`
    - Implementa: `calcular_ic_95`, `contraste_hipotesis`, `verificar_supuestos`.
2.  **Vista de Inferencia**: `views/layout.py` (pestaña 4)
    - Muestra los resultados de tus tests y los p-valores.

---

## 👨‍💻 Instrucciones para RAFAEL (Data Manager)
Tu territorio es:
1.  **Lógica de Datos**: `models/data_loader.py`
    - Gestión de CSVs, limpieza y merge con la API del Banco Mundial.
2.  **Estadísticos**: `analisis/estadisticos.py`
    - Cálculo de media, mediana, desviación, etc.

---

## 🚀 Cómo ejecutar la App
Desde la terminal, usa:
```powershell
python -m streamlit run app.py
```

---
*Cualquier duda sobre la arquitectura, preguntad a **Rubén (Arquitecto)**.*
