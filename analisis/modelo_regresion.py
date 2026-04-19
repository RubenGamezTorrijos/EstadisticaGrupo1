import streamlit as st
from analisis.graficos import crear_scatter_regresion

def render_regresion(df):
    """
    Renders the Regression and Correlation analysis section.
    Attributed to: Leslie Ross Aranibar Pozo (Analista Descriptivo)
    """
    st.title("📈 4. Análisis de Regresión y Correlación")
    st.markdown("""
    En esta sección analizamos la relación entre el **Salario** y el **Índice de Coste de Vida (COLI)**.
    Buscamos responder: *¿Suben los salarios en países con mayor coste de vida?*
    """)
    
    # Determinar columna de salario según moneda
    col_salario = "salary_in_usd" if "USD" in st.session_state.get('moneda', 'USD') else "salary_in_eur"
    
    st.subheader("Modelo de Regresión Lineal Simple")
    
    fig, stats = crear_scatter_regresion(df, "cost_of_living_index", col_salario, "Regresión: Salario vs COLI")
    
    st.pyplot(fig)
    
    st.markdown("---")
    st.subheader("Métricas del Modelo")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Coef. Correlación (r)", f"{stats['correlacion']:.4f}")
    c2.metric("Coef. Determinación (R²)", f"{stats['r_cuadrado']:.4f}")
    c3.metric("Pendiente", f"{stats['pendiente']:.2f}")
    
    # Interpretación
    st.info(f"**Interpretación:** La ecuación de la recta es:  \n"
            f"**Salario = {stats['pendiente']:.2f} * COLI + {stats['intercepto']:.2f}**")
    
    if abs(stats['correlacion']) > 0.7:
        st.success("✅ Existe una correlación FUERTE entre las variables.")
    elif abs(stats['correlacion']) > 0.4:
        st.warning("⚠️ Existe una correlación MODERADA.")
    else:
        st.error("❌ No existe una correlación clara entre el salario y el coste de vida en esta muestra.")
