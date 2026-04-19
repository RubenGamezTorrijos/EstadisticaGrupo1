import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def crear_histograma(df, x_col, titulo="Distribución Salarial"):
    """
    MODULO: Visualizaciones Descriptivas
    ROL ASIGNADO: Leslie Ross Aranibar Pozo
    
    # 💡 PISTA DE IMPLEMENTACIÓN (REFERENCIA MAIN):
    # ==========================================
    # sns.histplot(df[x_col], ax=ax, kde=True, color='#0b84f4')
    # ax.set_xlabel("Salario (USD)")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    # Plantilla básica: implementar estilo v.2.1.4 aquí
    sns.histplot(df[x_col], ax=ax, color='#0b84f4')
    ax.set_title(f"{titulo} [Leslie: Pendiente Refinar]")
    return fig

def crear_boxplot(df, y_col, x_col, titulo="Comparativa Salarial"):
    """
    MODULO: Visualizaciones Descriptivas
    ROL ASIGNADO: Leslie Ross Aranibar Pozo
    
    # 💡 PISTA DE IMPLEMENTACIÓN (REFERENCIA MAIN):
    # ==========================================
    # sns.boxplot(data=df, x=x_col, y=y_col, ax=ax, palette="RdBu_r")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    # Plantilla básica
    sns.boxplot(data=df, x=x_col, y=y_col, ax=ax, palette="Blues")
    ax.set_title(f"{titulo} [Leslie: Pendiente Refinar]")
    plt.xticks(rotation=45)
    return fig

def crear_violin_plot(df, x_col, y_col, titulo="Densidad Salarial"):
    """
    MODULO: Visualizaciones Descriptivas
    ROL ASIGNADO: Leslie Ross Aranibar Pozo
    
    TODO: Implementar Violin Plot para mostrar densidad de probabilidad.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    # Plantilla básica
    sns.violinplot(data=df, x=x_col, y=y_col, ax=ax, color='#1e3a8a')
    ax.set_title(f"{titulo} [Leslie: Pendiente Refinar]")
    return fig

def crear_bar_chart(df, col, titulo="Presencia en Mercado"):
    """
    MODULO: Visualizaciones Descriptivas
    ROL ASIGNADO: Leslie Ross Aranibar Pozo
    
    TODO: Implementar gráfico de barras para variables categóricas (Top 10).
    """
    counts = df[col].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    # Plantilla básica
    counts.plot(kind='bar', ax=ax, color='#0b84f4')
    ax.set_title(f"{titulo} [Leslie: Pendiente Refinar]")
    plt.xticks(rotation=45)
    return fig

def crear_grafico_comparativo_ic(df, x_col, y_col, titulo="Evidencia Inferencial"):
    """
    MODULO: Evidencia Inferencial
    ROL ASIGNADO: Leslie Ross Aranibar Pozo (En colaboración con Bryann)
    
    TODO: Implementar gráfico de barras de error (Barplot con errorbars=95).
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    # Plantilla básica
    if not df.empty:
        sns.barplot(data=df, x=x_col, y=y_col, ax=ax, errorbar=('ci', 95), palette="Blues")
    ax.set_title(f"{titulo} [Leslie: Pendiente Refinar]")
    return fig

def crear_scatter_regresion(df, x_col, y_col, titulo="Relación Salario vs COLI"):
    """
    MODULO: Regresión Lineal
    ROL ASIGNADO: Leslie Ross Aranibar Pozo
    
    # 💡 PISTA DE IMPLEMENTACIÓN (REFERENCIA MAIN):
    # ==========================================
    # sns.regplot(data=df, x=x_col, y=y_col, ax=ax, 
    #             scatter_kws={'alpha':0.5, 'color':'#0b84f4'},
    #             line_kws={'color':'#ff4b4b', 'lw':3})
    
    fig, ax = plt.subplots(figsize=(10, 6))
    # Plantilla básica
    sns.regplot(data=df, x=x_col, y=y_col, ax=ax, line_kws={'color': 'red'})
    ax.set_title(f"{titulo} [Leslie: Pendiente Refinar]")
    
    # Placeholder de estadísticas (Sincronizado con app.py)
    stats = {
        'correlacion': 0.0,
        'r_cuadrado': 0.0,
        'pendiente': 0.0,
        'intercepto': 0.0
    }
    return fig, stats
