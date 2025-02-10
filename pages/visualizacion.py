import plotly.graph_objects as go 
import plotly as pl
import plotly.express as px
import numpy as np
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.seasonal import STL
import seaborn as sns
from pandas.plotting import lag_plot
import json


def figura_mapa(datos_abreviados,N): #Function for plottin  the map
    
    # fig = px.choropleth(locations=)
    df = pd.DataFrame(datos_abreviados)
    # fig = px.choropleth(locations=["CA", "TX", "NY"], locationmode="USA-states", color=[1,2,3], scope="usa")
    lista_numero = [i for i in range(len(datos_abreviados['abreviatura']))]
    fig = px.choropleth(
                    df,
                    locations=datos_abreviados['abreviatura'],
                    locationmode="USA-states", 
                    color='Clientes', 
                    scope="usa",
                    hover_data='Clientes',
                    hover_name= datos_abreviados['Estado']
                    )
    fig.update_layout(
        template="plotly",  # Plantilla visual
        title_font_size=20,  # Tamaño del título
        title_x=0.5,  # Centrar el título
        title='Clientes',
        geo=dict(
            lakecolor="rgb(255, 255, 255)",  # Color de los lagos
            bgcolor="rgba(255,255,255,255)",  # Fondo transparente
        ),
        coloraxis_colorbar=dict(
            title="Clientes (No.)",  # Título de la barra de colores
            title_side="right"  # Ubicación del título
        )
    )
    return fig


def figure_pie(data, N = 3):
    
    data_ordenada = data.groupby('Segment')['Count'].sum().sort_values(ascending=False).head(N).reset_index()

    # Crear la gráfica de pie
    fig = px.pie(
        data_ordenada,
        values='Count',
        names='Segment',
        title=f'Gráfica de los {N} segmentos',
        hole=0.3,  # Añadir un agujero en el centro para hacer un gráfico de dona (más atractivo)
        color='Segment',  # Usar colores distintos por segmento
        color_discrete_sequence=px.colors.qualitative.Set2  # Elegir una paleta de colores agradable
    )
    
    # Agregar los porcentajes y los valores en las secciones del pie
    fig.update_traces(textinfo='percent+label', pull=[0.1, 0.1, 0.1])  # Puedes ajustar 'pull' para resaltar las primeras secciones

    # Ajustar el layout para mejor presentación
    fig.update_layout(
        title_x=0.5,  # Centrar el título
        title_y=0.95,  # Ajustar la posición del título
        showlegend=True,  # Mostrar la leyenda
        margin=dict(t=40, b=40, l=40, r=40)  # Ajustar márgenes para dar espacio
    )

    return fig

def figura_categoria_segmento(datos,NUM = None):
    CATEGORIA = datos['Segment'].unique()
    CATEGORIA = list(CATEGORIA)

    index = datos.columns
    fig = go.Figure(
        data=[
            go.Bar(
                x=datos[index[0]],  # Eje X con los nombres de las ciudades
                y=datos[index[1]],  # Eje Y con los valores de conteo
                text=datos[index[1]],  # Etiquetas con los valores
                textposition='inside',  # Etiquetas dentro de las barras
                marker_color= datos[index[1]]  # Color de las barras
            )
        ],
        layout_title_text=f"Productos Por Segmento ({(CATEGORIA.pop())})"
    )

    fig.update_layout(
        title_x=0.5,  # Centra el título
        title_y=0.95,  # Ajusta la posición del título
        xaxis_title="Segmento",  # Título del eje X
        yaxis_title="Número de Ventas",  # Título del eje Y
        showlegend=False,  # No mostrar leyenda
        margin=dict(t=40, b=40, l=40, r=40)  # Ajustar márgenes
    )

    return fig

# -----------------------------------------------------------------------
# Analisis de Clientes
# -----------------------------------------------------------------------
def figura_mapa_ventas(datos_abreviados, limite = 'Todos los Estados'):
    df = pd.DataFrame(datos_abreviados)
    if(limite == 'Todos los Estados'):
        print('No se Filtro nada')
    else:
        limite = float(limite)
        df  = df[df['Ventas'] > limite]

    fig = px.choropleth(
                    df,
                    locations=df['abreviatura'],
                    locationmode="USA-states", 
                    color='Ventas', 
                    scope="usa",
                    hover_data='Ventas',
                    hover_name= df['Estado'],
                    color_continuous_scale=[
                                    (0.0, "rgb(255, 245, 240)"),  # Blanco
                                    (0.5, "rgb(254, 178, 76)"),   # Naranja
                                    (1.0, "rgb(189, 0, 38)")
                    ]  
                    )
    fig.update_layout(
        template="plotly",  # Plantilla visual
        title_font_size=20,  # Tamaño del título
        title_x=0.5,  # Centrar el título
        title = 'Ventas', #numero de ventas por estado
        geo=dict(
            lakecolor="rgb(255, 255, 255)",  # Color de los lagos
            bgcolor="rgba(255,255,255,255)",  # Fondo transparente
        ),
        coloraxis_colorbar=dict(
            title="Ventas ($)",  # Título de la barra de colores
            title_side="right"  # Ubicación del título
        )
    )
    return fig



def figura_segmento(datos):
    
    index = datos.columns
    fig = go.Figure(
        data=[
            go.Bar(
                x=datos[index[0]],  # Eje X con los nombres de las ciudades
                y=datos[index[1]],  # Eje Y con los valores de conteo
                text=datos[index[1]],  # Etiquetas con los valores
                textposition='inside',  # Etiquetas dentro de las barras
                marker_color=(190,190,190)  # Color de las barras
            )
        ],
        layout_title_text="Ventas Brutas Por Segmento"
    )

    fig.update_layout(
        title_x=0.5,  # Centra el título
        title_y=0.95,  # Ajusta la posición del título
        xaxis_title="Segmento",  # Título del eje X
        yaxis_title="Número de Ventas",  # Título del eje Y
        showlegend=False,  # No mostrar leyenda
        margin=dict(t=40, b=40, l=40, r=40)  # Ajustar márgenes
    )

    return fig

def figura_segmento_netas(datos):
    
    index = datos.columns
    fig = go.Figure(
        data=[
            go.Bar(
                x=datos[index[0]],  # Eje X con los nombres de las ciudades
                y=datos[index[1]],  # Eje Y con los valores de conteo
                text=datos[index[1]],  # Etiquetas con los valores
                textposition='inside',  # Etiquetas dentro de las barras
                marker_color=(130,160,190)  # Color de las barras
            )
        ],
        layout_title_text="Ganancias Netas por Segmento"
    )

    fig.update_layout(
        title_x=0.5,  # Centra el título
        title_y=0.95,  # Ajusta la posición del título
        xaxis_title="Segmento",  # Título del eje X
        yaxis_title="Número de Ventas Netas",  # Título del eje Y
        showlegend=False,  # No mostrar leyenda
        margin=dict(t=40, b=40, l=40, r=40)  # Ajustar márgenes
    )

    return fig



def figura_linea_ventas(fecha_sales,opcion):
    new_x = fecha_sales['Month'].max()
    new_y = fecha_sales['Sales'].max()
    random_x = np.linspace(0, int(new_x))
    random_y = np.linspace(0,int(new_y))

    lista_años = fecha_sales['Year'].drop_duplicates()
    lista_años = list(lista_años)
    # Create traces
    fig = go.Figure()

    if(opcion == str(lista_años[0])):

        fig.add_trace(go.Scatter(x=fecha_sales['Month'][0:12], y=fecha_sales['Sales'][0:11],
                            mode='lines',
                            name=str(lista_años[0])))
    elif(opcion == str(lista_años[1])):
        fig.add_trace(go.Scatter(x=fecha_sales['Month'][0:12], y=fecha_sales['Sales'][12:23],
                            mode='lines',
                            name=str(lista_años[1])))
    elif(opcion == str(lista_años[2])):
        fig.add_trace(go.Scatter(x=fecha_sales['Month'][0:12], y=fecha_sales['Sales'][24:35],
                            mode='lines',
                            name=str(lista_años[2])))
    elif(opcion == str(lista_años[3])):
        fig.add_trace(go.Scatter(x=fecha_sales['Month'][0:12], y=fecha_sales['Sales'][36:47],
                            mode='lines',
                            name=str(lista_años[3])))
    else:
        fig.add_trace(go.Scatter(x=fecha_sales['Month'][0:12], y=fecha_sales['Sales'][0:11],
                            mode='lines',
                            name=str(lista_años[0])))
        fig.add_trace(go.Scatter(x=fecha_sales['Month'][0:12], y=fecha_sales['Sales'][12:23],
                            mode='lines',
                            name=str(lista_años[1])))
        fig.add_trace(go.Scatter(x=fecha_sales['Month'][0:12], y=fecha_sales['Sales'][24:35],
                            mode='lines',
                            name=str(lista_años[2])))
        fig.add_trace(go.Scatter(x=fecha_sales['Month'][0:12], y=fecha_sales['Sales'][36:47],
                            mode='lines',
                            name=str(lista_años[3])))
    fig.update_layout(
        title=dict(
            text='Como las ventas cambian por cada año que pasa.'
        ),
        xaxis=dict(
            title=dict(
                text='Mes'
            )
        ),
        yaxis=dict(
            title=dict(
                text='Ventas (Sales)'
            )
        ),
)

    return fig

# ----------------------------------------------------------------
# Catogorias
# ----------------------------------------------------------------
def figura_subcategorias(datos):
    num_datos = len(datos.index)
    lista_colores = [x for x in range(0,num_datos,1)]
    index = datos.columns
    fig = go.Figure(
        data=[
            go.Bar(
                x=datos[index[0]],  # Eje X con los nombres de las ciudades
                y=datos[index[1]],  # Eje Y con los valores de conteo
                text=datos[index[1]],  # Etiquetas con los valores
                textposition='inside',  # Etiquetas dentro de las barras
                marker_color=tuple(lista_colores)  # Color de las barras
            )
        ],
        layout_title_text="Sub-Categorais"
    )

    fig.update_layout(
        title_x=0.5,  # Centra el título
        title_y=0.95,  # Ajusta la posición del título
        xaxis_title="Sub-Categorias",  # Título del eje X
        yaxis_title="Número de Ventas",  # Título del eje Y
        showlegend=False,  # No mostrar leyenda
        margin=dict(t=40, b=40, l=40, r=40)  # Ajustar márgenes
    )

    return fig

# ----------------------------------------------------------------
# Descuentos con cantidad de Ventas
# ----------------------------------------------------------------

def figura_dispersion(data):
    # fig = px.choropleth(locations=)
    df = pd.DataFrame(data)
    index = data.columns
    num_datos = len(data.index)
    lista_colores = [x for x in range(0,num_datos,1)]
    # fig = px.choropleth(locations=["CA", "TX", "NY"], locationmode="USA-states", color=[1,2,3], scope="usa")
    # lista_numero = [i for i in range(len(data['abreviatura']))]
    fig = px.scatter(
    df,
    y=data[index[1]],
    x=data[index[0]],
    width=800,
    height=500,
    color= lista_colores,
    # size=[5, 10, 15],
    # hover_name=["B1", "B2", "B3"],
    # text=["1", "2", "3"],
    # error_y=[1, 2, 1],
    # color_discrete_map={"a": "red", "b": "green"},
    title="Bubble Chart",
    opacity=0.7,
    marginal_x="histogram",
                    )
    fig.update_layout(
        template="plotly",  # Plantilla visual
        title_font_size=20,  # Tamaño del título
        title_x=0.5,  # Centrar el título
        title='Cantidad de productos en relacion a su Descuento',
        geo=dict(
            lakecolor="rgb(255, 255, 255)",  # Color de los lagos
            bgcolor="rgba(255,255,255,255)",  # Fondo transparente
        ),
        coloraxis_colorbar=dict(
            title="Ventas",  # Título de la barra de colores
            title_side="right"  # Ubicación del título
        )
    )
    return fig


# ----------------------------------------------------------------
# Analisis de Tiempo
# ----------------------------------------------------------------
def figura_mapa_tiempo(datos_abreviados):
    df = pd.DataFrame(datos_abreviados)
    # fig = px.choropleth(locations=["CA", "TX", "NY"], locationmode="USA-states", color=[1,2,3], scope="usa")
    lista_numero = [i for i in range(len(datos_abreviados['abreviatura']))]
    fig = px.choropleth(
                    df,
                    locations=datos_abreviados['abreviatura'],
                    locationmode="USA-states", 
                    color='Time Wait', 
                    scope="usa",
                    hover_data='Time Wait',
                    hover_name= datos_abreviados['State'],
                    color_continuous_scale=[
                                    (0.0, "rgb(255, 245, 240)"),  # Blanco
                                    (0.5, "rgb(254, 178, 76)"),   # Naranja
                                    (1.0, "rgb(189, 0, 38)")
                    ]  
                    )
    fig.update_layout(
        template="plotly",  # Plantilla visual
        title_font_size=20,  # Tamaño del título
        title_x=0.5,  # Centrar el título
        title = 'Tiempo de Espera de fecha de Orden y Fecha de Envío (Días)', #numero de ventas por estado
        geo=dict(
            lakecolor="rgb(255, 255, 255)",  # Color de los lagos
            bgcolor="rgba(255,255,255,255)",  # Fondo transparente
        ),
        coloraxis_colorbar=dict(
            title="Tiempo (Días)",  # Título de la barra de colores
            title_side="right"  # Ubicación del título
        )
    )
    return fig
# ----------------------------------------------------------------
# Rentabilidad de productos
# ----------------------------------------------------------------
def figura_rentabilidad_productos(rentabilidad,N = 20):
    datos_positivos = rentabilidad[rentabilidad['Profit']>=0]
    datos_positivos = datos_positivos.sort_values('Profit', ascending = False)
    datos_negativos = rentabilidad[rentabilidad['Profit']<0]
    # Crear la gráfica de barras
    fig = go.Figure()

    # Barras positivas
    fig.add_trace(go.Bar(
        # x=datos_positivos['Product Name'],
        y=[v if v > 0 else 0 for v in datos_positivos['Profit'][:N]],
        name='Positivos',
        marker_color='skyblue',
        hovertext=datos_positivos['Product Name'][:N],
        hoverinfo="text+y"
    ))

    # Barras negativas
    fig.add_trace(go.Bar(
        # x=rentabilidad['Product Name'],
        y=[v if v < 0 else 0 for v in datos_negativos['Profit'][:N]],
        name='Negativos',
        marker_color='red',
        hovertext=datos_negativos['Product Name'][:N],
        hoverinfo="text+y"
    ))

    # Configurar el diseño
    fig.update_layout(
        title="Gráfica de Barras Positivas y Negativas",
        xaxis_title="Productos",
        yaxis_title="Ganancias",
        barmode='relative',  # Modo relativo para que las barras se apilen correctamente
        bargap=0.2,  # Espaciado entre barras
        bargroupgap=0.1,  # Espaciado entre grupos
        legend_title="Signo"
    )
    return fig

# ----------------------------------------------------------------
# Devoluciones productos
# ----------------------------------------------------------------
def figura_dispersion_devoluciones(data):
    # fig = px.choropleth(locations=)
    df = pd.DataFrame(data)
    index = data.columns
    num_datos = len(data.index)
    lista_colores = [x for x in range(0,num_datos,1)]
    # fig = px.choropleth(locations=["CA", "TX", "NY"], locationmode="USA-states", color=[1,2,3], scope="usa")
    # lista_numero = [i for i in range(len(data['abreviatura']))]
    fig = px.scatter(
    df,
    y=data[index[1]],
    x=data[index[0]],
    width=800,
    height=500,
    color= data['Discount'],
    # size=[5, 10, 15],
    # hover_name=["B1", "B2", "B3"],
    # text=["1", "2", "3"],
    # error_y=[1, 2, 1],
    # color_discrete_map={"a": "red", "b": "green"},
    title="Bubble Chart",
    opacity=0.7,
    marginal_x="histogram",
                    )
    fig.update_layout(
        template="plotly",  # Plantilla visual
        title_font_size=20,  # Tamaño del título
        title_x=0.5,  # Centrar el título
        xaxis_title="Descuento",
        yaxis_title="Cantidad de Devoluciones",
        title='Cantidad de productos Devueltos con sus Descuentos',
        geo=dict(
            lakecolor="rgb(255, 255, 255)",  # Color de los lagos
            bgcolor="rgba(255,255,255,255)",  # Fondo transparente
        ),
        coloraxis_colorbar=dict(
            title="Descuento",  # Título de la barra de colores
            title_side="right"  # Ubicación del título
        )
    )
    return fig

def figura_matriz_correlacion(r):
    f, ax = plt.subplots(figsize=(5, 3))

    sns.heatmap(r, annot=True, cmap="coolwarm", fmt=".2f")

    # plt.figure(figsize=(1,1))
    plt.title("Matriz de Correlación")
    return plt


# ----------------------------------------------------------------
# Modelo Arima y analisis de Series de Tiempo
# ----------------------------------------------------------------

def figura_series_tiempo(datos,datos_diff):
    fig1, ax = plt.subplots(figsize=(20, 7))
    sns.lineplot(data = datos,y = 'Profit', x= 'Fecha', linewidth= .5)
    # plt.show()


    fig2, ax = plt.subplots(figsize=(20, 7))
    sns.kdeplot(data = datos, x = 'Profit', hue = 'Year', fill = True, alpha = 0.5, linewidth = 0, palette='viridis' )
    plt.show()
    lag_plot(datos['Profit'])
    # plt.show()


    fig3, ax = plt.subplots(figsize=(20, 7))
    sns.lineplot(data = datos_diff,y = 'Profit', x= 'Fecha', linewidth= .5)
    # plt.show()

    fig4, ax = plt.subplots(figsize=(20, 7))
    sns.kdeplot(data = datos_diff, x = 'Profit', hue = 'Year', fill = True, alpha = 0.5, linewidth = 0, palette='viridis' )
    # plt.show()

    plt.rc('figure',figsize = (16,12))
    plt.rc('font',size = 10)
    Y = datos_diff['Profit'].fillna(0)
    stl = STL(Y,period = 12)
    res = stl.fit()
    fig5 = res.plot()
    # plt.show()

    lista = [fig1, fig2, fig3, fig4, fig5]
    return lista


# MAPA POR ESTADO PARA EL FILTRADO DE CADA MAPA 


# Graficacion de la Serie de Tiempo

def figura_serie(df_filtrado, df_prediccion=None,limite = None):
    fig = go.Figure()
    if(limite == None):
        pass
    else:
        df_filtrado = df_filtrado[-limite:]
    # Gráfica de la serie temporal real
    fig.add_trace(go.Scatter(
        x=df_filtrado.index, 
        y=df_filtrado['Profit'],
        mode='lines',
        name="Datos reales",
        line=dict(color='royalblue', width=2),
        hoverinfo='x+y'
    ))

    # Si hay predicciones, añadirlas a la gráfica
    if df_prediccion is not None:
        fig.add_trace(go.Scatter(
            x=df_prediccion.index,
            y=df_prediccion['Profit'],
            mode='lines',
            name="Predicción",
            line=dict(color='red', dash='dot', width=2),
            hoverinfo='x+y'
        ))

    # Estilizar la gráfica
    fig.update_layout(
        title="Serie Temporal de Profit",
        title_font=dict(size=20, family="Arial", color="white"),
        xaxis=dict(title="Fecha", showgrid=False, tickformat="%Y-%m-%d"),
        yaxis=dict(title="Profit", showgrid=True, zeroline=False),
        template="plotly_white",
        hovermode="x unified",
        margin=dict(l=40, r=40, t=60, b=40),
        height=500
    )

    return fig
