from flask import Flask, render_template
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Inicializar Flask
server = Flask(__name__)

# Inicializar Dash con estilos de Bootstrap bajo la ruta `/dashboard`
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP], url_base_pathname='/dashboard/')

# URLs de las APIs
urls = [
    "https://fakestoreapiserver.reactbd.com/nextamazon",
    "https://fakestoreapiserver.reactbd.com/walmart",
    "https://fakestoreapi.com/products/category/electronics"
]

# Función para obtener datos de la API
def fetch_data(url):
    response = requests.get(url)  # Realiza una solicitud GET a la API
    return response.json()  # Devuelve los datos en formato JSON

# Obtener datos de las 3 APIs
data_amazon = fetch_data(urls[0])  # Datos de la primera API (Amazon)
data_walmart = fetch_data(urls[1])  # Datos de la segunda API (Walmart)
data_electronics = fetch_data(urls[2])  # Datos de la tercera API (Electrónica)

# Convertir los datos en DataFrames para facilitar el análisis
df_amazon = pd.DataFrame(data_amazon)  # Convierte los datos de Amazon en un DataFrame
df_walmart = pd.DataFrame(data_walmart)  # Convierte los datos de Walmart en un DataFrame
df_electronics = pd.DataFrame(data_electronics)  # Convierte los datos de Electrónica en un DataFrame

# Asegurarse de que los precios sean numéricos
df_amazon['price'] = pd.to_numeric(df_amazon['price'], errors='coerce')  # Convierte los precios de Amazon a numéricos
df_walmart['price'] = pd.to_numeric(df_walmart['price'], errors='coerce')  # Convierte los precios de Walmart a numéricos
df_electronics['price'] = pd.to_numeric(df_electronics['price'], errors='coerce')  # Convierte los precios de Electrónica a numéricos

# KPI existentes
kpi_total_amazon = len(df_amazon)  # Número total de productos en Amazon
kpi_total_walmart = len(df_walmart)  # Número total de productos en Walmart
kpi_total_electronics = len(df_electronics)  # Número total de productos en Electrónica

kpi_avg_price_amazon = df_amazon['price'].mean()  # Precio promedio de productos en Amazon
kpi_avg_price_walmart = df_walmart['price'].mean()  # Precio promedio de productos en Walmart
kpi_avg_price_electronics = df_electronics['price'].mean()  # Precio promedio de productos en Electrónica

kpi_max_price_amazon = df_amazon['price'].max()  # Precio máximo de productos en Amazon
kpi_max_price_walmart = df_walmart['price'].max()  # Precio máximo de productos en Walmart
kpi_max_price_electronics = df_electronics['price'].max()  # Precio máximo de productos en Electrónica

# Nuevos KPI
# 1. Rango de precios (min y max) por tienda
kpi_min_price_amazon = df_amazon['price'].min()  # Precio mínimo de productos en Amazon
kpi_min_price_walmart = df_walmart['price'].min()  # Precio mínimo de productos en Walmart
kpi_min_price_electronics = df_electronics['price'].min()  # Precio mínimo de productos en Electrónica

# 2. Distribución de productos por categorías
categories_amazon = df_amazon['category'].value_counts()  # Conteo de productos por categoría en Amazon
categories_walmart = df_walmart['category'].value_counts()  # Conteo de productos por categoría en Walmart
categories_electronics = df_electronics['category'].value_counts()  # Conteo de productos por categoría en Electrónica

# Nuevo KPI
# 6. Cantidad total de productos por tienda con un precio mayor a $50
threshold = 50
above_threshold_amazon = len(df_amazon[df_amazon['price'] > threshold])
above_threshold_walmart = len(df_walmart[df_walmart['price'] > threshold])
above_threshold_electronics = len(df_electronics[df_electronics['price'] > threshold])

below_threshold_amazon = len(df_amazon[df_amazon['price'] <= threshold])
below_threshold_walmart = len(df_walmart[df_walmart['price'] <= threshold])
below_threshold_electronics = len(df_electronics[df_electronics['price'] <= threshold])

# Concatenar los DataFrames para análisis conjunto
df_combined = pd.concat([df_amazon, df_walmart, df_electronics])  # Combina los tres DataFrames

# Gráficas
# Gráfica de barras: Número de productos por tienda
fig_bar = px.bar(
    x=['Amazon', 'Walmart', 'Electronics'],  # Etiquetas en el eje X
    y=[kpi_total_amazon, kpi_total_walmart, kpi_total_electronics],  # Valores en el eje Y
    labels={'x': 'Tienda', 'y': 'Cantidad de Productos'},  # Etiquetas de los ejes
    title='Número de Productos por Tienda',  # Título de la gráfica
    color_discrete_sequence=px.colors.qualitative.Bold  # Paleta de colores con diferentes tonos
)

# Gráfica de pastel: Distribución de precios promedio
fig_pie = px.pie(
    names=['Amazon', 'Walmart', 'Electronics'],  # Nombres de las secciones
    values=[kpi_avg_price_amazon, kpi_avg_price_walmart, kpi_avg_price_electronics],  # Valores de las secciones
    title='Precios Promedio por Tienda',  # Título de la gráfica
    color_discrete_sequence=px.colors.qualitative.Set2  # Colores diferenciados para cada sección
)

# Gráfica de dispersión: Precios máximos por tienda
fig_scatter = px.scatter(
    x=['Amazon', 'Walmart', 'Electronics'],  # Etiquetas en el eje X
    y=[kpi_max_price_amazon, kpi_max_price_walmart, kpi_max_price_electronics],  # Valores en el eje Y
    labels={'x': 'Tienda', 'y': 'Precio Máximo ($)'},  # Etiquetas de los ejes
    title='Precios Máximos por Tienda',  # Título de la gráfica
    color_discrete_sequence=px.colors.qualitative.Pastel  # Paleta de colores pastel para los puntos
)

# Gráfica de boxplot: Rango de precios por tienda
fig_box = px.box(
    df_combined,  # DataFrame combinado
    x='category',  # Eje X para categorías
    y='price',  # Eje Y para precios
    title='Rango de Precios por Categoría y Tienda',  # Título de la gráfica
    color_discrete_sequence=px.colors.qualitative.Dark2  # Paleta de colores oscuros
)

# Gráfica de histograma: Distribución de productos por categoría
fig_histogram = px.histogram(
    df_combined,  # DataFrame combinado
    x='category',  # Eje X para categorías
    color='category',  # Colores según la categoría
    title='Distribución de Productos por Categoría',  # Título de la gráfica
    color_discrete_sequence=px.colors.qualitative.Set3  # Paleta de colores para las barras
)

# Gráfica de barras apiladas: Productos por tienda por encima y por debajo del umbral
fig_stacked_bar = go.Figure(data=[
    go.Bar(
        name='Por Debajo de $50',  # Nombre de la serie para el umbral inferior
        x=['Amazon', 'Walmart', 'Electronics'],  # Etiquetas en el eje X
        y=[below_threshold_amazon, below_threshold_walmart, below_threshold_electronics],  # Valores para el umbral inferior
        marker_color='red'  # Color de las barras por debajo del umbral
    ),
    go.Bar(
        name='Por Encima de $50',  # Nombre de la serie para el umbral superior
        x=['Amazon', 'Walmart', 'Electronics'],  # Etiquetas en el eje X
        y=[above_threshold_amazon, above_threshold_walmart, above_threshold_electronics],  # Valores para el umbral superior
        marker_color='green'  # Color de las barras por encima del umbral
    )
])

# Configurar la disposición de la gráfica apilada
fig_stacked_bar.update_layout(
    barmode='stack',  # Configurar las barras en modo apilado
    title='Productos por Encima y Debajo de $50',  # Título de la gráfica
    xaxis_title='Tienda',  # Etiqueta del eje X
    yaxis_title='Cantidad de Productos',  # Etiqueta del eje Y
    font=dict(size=10),  # Ajustar el tamaño de la fuente para evitar cortes
    title_font=dict(size=14)  # Tamaño del título ajustado
)

# Ajustes de tamaño para los gráficos más pequeños
small_graph_style = {
    "height": "250px",  # Altura más pequeña para los gráficos
    "border": "2px solid #dee2e6",  # Borde alrededor de cada gráfica
    "padding": "5px",  # Espaciado interno más pequeño
    "borderRadius": "5px",  # Bordes redondeados (notación camelCase)
    "boxShadow": "2px 2px 10px rgba(0, 0, 0, 0.1)",  # Sombra ligera (notación camelCase)
    "marginBottom": "10px"  # Espaciado reducido entre gráficas (notación camelCase)
}

# Ajustes para gráficos más grandes
large_graph_style = {
    "height": "300px",  # Altura adecuada para gráficos grandes
    "border": "2px solid #dee2e6",  # Borde alrededor de cada gráfica
    "padding": "5px",  # Espaciado interno más pequeño
    "borderRadius": "5px",  # Bordes redondeados (notación camelCase)
    "boxShadow": "2px 2px 10px rgba(0, 0, 0, 0.1)",  # Sombra ligera (notación camelCase)
    "marginBottom": "10px"  # Espaciado reducido entre gráficas (notación camelCase)
}

# Layout de Dash con Bootstrap ajustado para una sola pantalla
app.layout = dbc.Container([
    dbc.Row([  # Primera fila con tres gráficos grandes
        dbc.Col(dcc.Graph(figure=fig_bar, style=large_graph_style), width=4),  # Gráfico 1: Barras
        dbc.Col(dcc.Graph(figure=fig_pie, style=large_graph_style), width=4),  # Gráfico 2: Pastel
        dbc.Col(dcc.Graph(figure=fig_stacked_bar, style=large_graph_style), width=4),  # Gráfico 3: Barras apiladas
    ], className="mb-4"),  # Margen inferior entre las filas

    dbc.Row([  # Segunda fila con dos gráficos más pequeños
        dbc.Col(dcc.Graph(figure=fig_scatter, style=small_graph_style), width=6),  # Gráfico pequeño 1: Dispersión
        dbc.Col(dcc.Graph(figure=fig_histogram, style=small_graph_style), width=6),  # Gráfico pequeño 2: Histograma
    ], className="mb-4"),  # Margen inferior entre las filas

    dbc.Row([  # Tercera fila con un gráfico adicional
        dbc.Col(dcc.Graph(figure=fig_box, style=small_graph_style), width=12),  # Gráfico pequeño 3: Boxplot
    ])
], fluid=True)  # Contenedor con fluidez para adaptarse al tamaño de la pantalla

# Ruta principal en Flask
@server.route('/')
def index():
    return render_template('index.html')  # Renderiza la plantilla HTML principal

# Ruta para el dashboard
@server.route('/dashboard')
def render_dashboard():
    return app.index()  # Renderiza el dashboard en la subruta /dashboard

#if __name__ == '__main__':
 #   server.run(debug=False, port=4600)
