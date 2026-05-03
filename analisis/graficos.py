"""
PROYECTO: Estadística para Ingeniería
MIEMBRO: LESLIE ROSS ARANIBAR POZO (Analista Descriptivo)
TAREA: Visualizaciones estadísticas y Análisis de Regresión
"""
import matplotlib.pyplot as plt
import seaborn as sns
import os
import config.settings as cfg
import plotly.express as px
import plotly.graph_objects as go
import scipy.stats as stats
from matplotlib.ticker import FuncFormatter

# Configuración estética Leslie - Optimizada para v.2.5.3
sns.set_theme(style="darkgrid")
plt.rcParams['figure.dpi'] = 300

def fmt_es(x, pos):
    """Formato español profesional"""
    return f"{x:,.0f}".replace(",", "@").replace(".", ",").replace("@", ".")

formatter = FuncFormatter(fmt_es)

def guardar_grafico(fig, nombre):
    """LESLIE ROSS ARANIBAR POZO - Guardado centralizado"""
    ruta = os.path.join(cfg.OUTPUTS_DIR, 'graficos', nombre)
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    fig.savefig(ruta, bbox_inches='tight')
    plt.close(fig)

def crear_histograma(df, columna):
    """LESLIE ROSS ARANIBAR POZO - Distribución avanzada"""
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(data=df, x=columna, kde=True, ax=ax, color='#00d1b2')
    
    ax.xaxis.set_major_formatter(formatter)
    ax.set_xlabel(cfg.VAR_LABELS.get(columna, columna))
    ax.set_ylabel("Frecuencia (N)")
    ax.set_title(f'Distribución de {cfg.VAR_LABELS.get(columna, columna)}', fontsize=14, pad=15)
    
    guardar_grafico(fig, f'histograma_{columna}.png')
    return fig

def crear_boxplot(df, num, cat):
    """LESLIE ROSS ARANIBAR POZO - Análisis por categoría"""
    fig, ax = plt.subplots(figsize=(12, 7))
    sns.boxplot(data=df, x=cat, y=num, ax=ax, palette="viridis")

    ax.yaxis.set_major_formatter(formatter)
    ax.set_xlabel(cfg.VAR_LABELS.get(cat, cat))
    ax.set_ylabel(cfg.VAR_LABELS.get(num, num))
    ax.set_title(f'{cfg.VAR_LABELS.get(num, num)} por {cfg.VAR_LABELS.get(cat, cat)}', fontsize=14, pad=15)
    
    plt.xticks(rotation=45)
    guardar_grafico(fig, f'boxplot_{num}_{cat}.png')
    return fig

def crear_violin_plot(df, num, cat):
    """LESLIE ROSS ARANIBAR POZO - Densidad de probabilidad"""
    fig, ax = plt.subplots(figsize=(12, 7))
    sns.violinplot(data=df, x=cat, y=num, ax=ax, palette="muted", inner="quartile")

    ax.yaxis.set_major_formatter(formatter)
    ax.set_xlabel(cfg.VAR_LABELS.get(cat, cat))
    ax.set_ylabel(cfg.VAR_LABELS.get(num, num))
    ax.set_title(f'Densidad de {cfg.VAR_LABELS.get(num, num)} por {cfg.VAR_LABELS.get(cat, cat)}', fontsize=14, pad=15)
    
    plt.xticks(rotation=45)
    guardar_grafico(fig, f'violin_{num}_{cat}.png')
    return fig

def crear_scatter_regresion(df, x_col, y_col):
    """LESLIE ROSS ARANIBAR POZO - Dispersión y Correlación"""
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.regplot(data=df, x=x_col, y=y_col, ax=ax, 
                scatter_kws={'alpha': 0.4, 'color': '#0b84f4'}, 
                line_kws={'color': 'red'})

    corr = df[x_col].corr(df[y_col])
    ax.yaxis.set_major_formatter(formatter)
    ax.xaxis.set_major_formatter(formatter)

    ax.set_xlabel(cfg.VAR_LABELS.get(x_col, x_col))
    ax.set_ylabel(cfg.VAR_LABELS.get(y_col, y_col))
    ax.set_title(f'Regresión: {cfg.VAR_LABELS.get(y_col, y_col)} vs {cfg.VAR_LABELS.get(x_col, x_col)} (r={corr:.2f})', 
                 fontsize=14, pad=15)
    
    guardar_grafico(fig, f'scatter_regresion_{x_col}_{y_col}.png')
    return fig

def crear_bar_chart(df, cat):
    """LESLIE ROSS ARANIBAR POZO - Frecuencias Top 10"""
    fig, ax = plt.subplots(figsize=(12, 6))
    counts = df[cat].value_counts().head(10)

    sns.barplot(x=counts.index, y=counts.values, ax=ax, palette="magma")
    ax.set_xlabel(cfg.VAR_LABELS.get(cat, cat))
    ax.set_ylabel("Cantidad de Registros")
    ax.set_title(f'Top 10: {cfg.VAR_LABELS.get(cat, cat)}', fontsize=14, pad=15)
    
    plt.xticks(rotation=45)
    guardar_grafico(fig, f'barras_{cat}.png')
    return fig

def sanitize_pdf_text(text):
    """Limpia caracteres problemáticos para FPDF."""
    if text is None: return ""
    return str(text).encode('latin-1', 'replace').decode('latin-1')

# --- FUNCIONES INTERACTIVAS (PLOTLY) PARA LA WEB ---

def crear_histograma_interactivo(df, columna):
    """Versión interactiva para la web."""
    label = cfg.VAR_LABELS.get(columna, columna)
    fig = px.histogram(df, x=columna, nbins=30, marginal="box", 
                       title=f'Distribución de {label}',
                       labels={columna: label},
                       color_discrete_sequence=['#00d1b2'])
    
    fig.update_layout(
        template="plotly_white",
        xaxis_title=label,
        yaxis_title="Frecuencia",
        hovermode="x unified",
        bargap=0.1
    )
    return fig

def crear_boxplot_interactivo(df, num, cat):
    """Versión interactiva para la web."""
    label_num = cfg.VAR_LABELS.get(num, num)
    label_cat = cfg.VAR_LABELS.get(cat, cat)
    
    fig = px.box(df, x=cat, y=num, color=cat,
                 title=f'{label_num} por {label_cat}',
                 labels={num: label_num, cat: label_cat},
                 points="outliers")
    
    fig.update_layout(template="plotly_white", showlegend=False)
    return fig

def crear_violin_interactivo(df, num, cat):
    """Versión interactiva para la web."""
    label_num = cfg.VAR_LABELS.get(num, num)
    label_cat = cfg.VAR_LABELS.get(cat, cat)
    
    fig = px.violin(df, x=cat, y=num, color=cat, box=True,
                    title=f'Densidad de {label_num} por {label_cat}',
                    labels={num: label_num, cat: label_cat})
    
    fig.update_layout(template="plotly_white", showlegend=False)
    return fig

def crear_scatter_regresion_interactivo(df, x_col, y_col):
    """Versión interactiva con línea de tendencia."""
    label_x = cfg.VAR_LABELS.get(x_col, x_col)
    label_y = cfg.VAR_LABELS.get(y_col, y_col)
    
    fig = px.scatter(df, x=x_col, y=y_col, trendline="ols",
                     title=f'Relación: {label_y} vs {label_x}',
                     labels={x_col: label_x, y_col: label_y},
                     hover_data=['job_title', 'experience_level'],
                     trendline_color_override="red")
    
    fig.update_layout(template="plotly_white")
    return fig

def crear_bar_chart_interactivo(df, cat):
    """Versión interactiva para categorías."""
    label_cat = cfg.VAR_LABELS.get(cat, cat)
    counts = df[cat].value_counts().head(10).reset_index()
    counts.columns = [cat, 'count']
    
    fig = px.bar(counts, x=cat, y='count', color='count',
                 title=f'Top 10: {label_cat}',
                 labels={cat: label_cat, 'count': 'Frecuencia'},
                 color_continuous_scale="Viridis")
    
    fig.update_layout(template="plotly_white", xaxis={'categoryorder':'total descending'})
    return fig

def crear_qq_plot(data):
    """Leslie Ross - Gráfico Q-Q para validación de normalidad."""
    qq_data = stats.probplot(data, dist="norm")
    x = qq_data[0][0]
    y = qq_data[0][1]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='markers', name='Datos', marker=dict(color='#0b84f4')))
    
    # Línea ideal
    line_x = [min(x), max(x)]
    line_y = [qq_data[1][0]*min(x) + qq_data[1][1], qq_data[1][0]*max(x) + qq_data[1][1]]
    fig.add_trace(go.Scatter(x=line_x, y=line_y, mode='lines', name='Normal Ideal', line=dict(color='red')))
    
    fig.update_layout(title="Gráfico Q-Q (Probabilidad Normal)", 
                      xaxis_title="Cuantiles Teóricos", 
                      yaxis_title="Cuantiles Muestrales",
                      template="plotly_white")
    return fig
