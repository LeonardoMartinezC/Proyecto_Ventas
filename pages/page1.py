# import streamlit as st
# import pandas as pd
# import filtrado as f
# import numpy as np


# import visualizacion as vsl
# st.set_page_config(
#                 page_title="Exploración",
#                 page_icon="🔥"
#                 )
# st.title('Exploración de los Datos')
# st.write('### En esta página se hará toda la Estadística y el Análisis de la Información')


# data_cliente = pd.read_csv('BD/clientes.csv')
# data_cliente_head = data_cliente.iloc[0:5]

# data_localizacion = pd.read_csv('BD/localizacion.csv')
# data_localizacion_head = data_localizacion.iloc[0:5]

# data_ordenes = pd.read_csv('BD/ordenes.csv')
# data_ordenes_head = data_ordenes.iloc[0:5]

# data_productos = pd.read_csv('BD/productos.csv')
# data_productos_head = data_productos.iloc[0:5]


# st.write('#### Información de los Clientes que Existen.')
# st.table(data_cliente_head)
# st.write('#### Información de el País, Estado, Ciudad.')
# st.table(data_localizacion_head)
# st.write('#### Información de las Ordenes con respecto a los clientes y la localización.')
# st.write("###### Esta tabla es la mas importante pues nos dice la información de las ordenes y cantidades")
# st.table(data_ordenes_head)
# st.write('#### Información de todos los productos con sus claves.')
# st.table(data_productos_head)




# st.write('# 1. Análisis de Clientes.')
# df_estados_abreviados = pd.read_csv("BD/estados.csv")


# # -----------------------------------------------------------------------
# # Analisis de Clientes
# # -----------------------------------------------------------------------

# data_cliente_clase = f.Clientes(data_cliente)
# distribucion_clientes = data_cliente_clase.distribucion_clientes()
# # NUM_CLIENTE = st.slider(
# #     f"Numero de barras de 5 hasta {len(distribucion_clientes)}" ,
# #     min_value=6,max_value=len(distribucion_clientes)
# # )
# st.write(f'## En el MAPA se puede ver la cantidad de clientes de cada estado.')
# st.write(f'### Tomando en cuenta esta tabla de datos extraidos de clientes.csv.')
# # st.write(distribucion_clientes.iloc[0:N])
# # fig = vsl.figura(distribucion_clientes,NUM_CLIENTE)
# # st.plotly_chart(fig,use_container_width=True,selection_mode="box")


# # datos = f.estados(distribucion_clientes,df_estados_abreviados)
# # st.write(distribucion_clientes)

# datos_abreviados = f.cambiar_abreviaturas(df_estados_abreviados,distribucion_clientes)
# fig_map = vsl.figura_mapa(datos_abreviados,49)
# st.plotly_chart(fig_map)
# df_datos_abreviados = pd.DataFrame(datos_abreviados)
# st.table(df_datos_abreviados.sort_values('Clientes',ascending=False).head())
# st.write('Total de Clientes =',data_cliente['Customer ID'].drop_duplicates().count())


# distribucion_segmento = data_cliente_clase.distribucion_segmentos_clientes()
# st.write(f'## Gráfica de Pastel que muesta los segmentos y cual compran más.')
# st.write(f'### Tomando en cuenta esta tabla de datos extraidos de clientes.csv.')
# st.table(distribucion_segmento)
# st.write("En esta grafica se muestra cual es el segmento que mas compra")
# fig = vsl.figure_pie(distribucion_segmento)
# st.plotly_chart(fig,theme=None,use_container_width=True)
# # ----------------------------------------------------------------
# # Productos que consume mas cada categoria
# # ----------------------------------------------------------------
# st.write('### 1.1 Productos que consume cada Categoría')
# opciones = data_cliente['Segment'].unique()
# # st.write(list(opciones))
# lista = []
# for elemento in opciones:
#     lista.append(str(elemento))

# # opciones = opciones.append('Todos los años')
# seleccion_segmento = st.selectbox('Selecciona una opción:', lista)
# categoria_producto = f.filtrado_productos_categoria(data_ordenes,data_productos,data_cliente,seleccion_segmento)
# # st.write(categoria_producto)

# figura_categoria_segmento = vsl.figura_categoria_segmento(categoria_producto)
# st.plotly_chart(figura_categoria_segmento)




# # -----------------------------------------------------------------------
# # Analisis de Ventas
# # -----------------------------------------------------------------------
# st.write('# 2. Análisis de Ventas.')
# st.write('### Gráfica de Distribucion de Ventas Brutas.')
# st.write(f'#### Tomando en cuenta esta tabla de datos extraidos de clientes.csv. y tambien ordenes.csv.')
# st.write('##### En esta grafica se mostrara Los estados con sus Datos en Ventas Brutas.')
# Data_ventas_estado = f.juntar_ventas(data_cliente,data_ordenes)
# st.write("### Los 5 Estados con mayor Ventas Brutas.")
# st.table(Data_ventas_estado.sort_values('Sales',ascending=False).head())
# Data_ventas_estado_dict = f.cambiar_abreviaturas_ventas(df_estados_abreviados,Data_ventas_estado)
# figura_ventas_estado = vsl.figura_mapa_ventas(Data_ventas_estado_dict)
# st.plotly_chart(figura_ventas_estado,theme=None,use_container_width=True)
# st.write('Total de Ventas Brutas =',data_ordenes['Sales'].sum())

# # --------------------------------
# # Analisis por Segmento
# # --------------------------------
# st.write('### Gráfica de Distribucion de Ventas por Segmento.')
# st.write(f'####  Se mostrar cuales son los segmentos que mas generan Ventas Brutas($).')
# data_clientes_segmento = f.segmento_ventas(data_cliente,data_ordenes)
# st.table(data_clientes_segmento)
# fig = vsl.figura_segmento(data_clientes_segmento)
# st.write('##### Se muestra las ventas por Segmento.')
# st.plotly_chart(fig,use_container_width=True,selection_mode="box")


# # --------------------------------
# # Analisis de ventas Netas
# # --------------------------------
# st.write('### Gráfica de Distribucion de Ventas Netas por Estado.')
# st.write(f'####  Se mostrar cuales son los segmentos que mas generan Ganancias Netas($) por estado.')
# data_ventas_n_estado = f.ventas_netas_estado(data_cliente,data_ordenes)
# st.write("### Los 5 Estados con mayor Ganancias Netas")
# st.table(data_ventas_n_estado.sort_values('Sales',ascending=False).head())

# Data_ventas_estado_dict_netas = f.cambiar_abreviaturas_ventas(df_estados_abreviados,data_ventas_n_estado)
# figura_ventas_netas = vsl.figura_mapa_ventas(Data_ventas_estado_dict_netas)
# st.plotly_chart(figura_ventas_netas,theme=None,use_container_width=True)
# st.write('Total de Ganancias Netas =',data_ordenes['Profit'].sum())


# # Ventas por segmento netas

# st.write('### Gráfica de Distribucion de Ganancias Netas por Segmento.')
# st.write(f'####  Se mostrar cuales son los segmentos que mas generan Ganancias Netas($).')
# data_clientes_segmento_netas = f.segmento_ventas_netas(data_cliente,data_ordenes)
# st.table(data_clientes_segmento_netas)
# fig = vsl.figura_segmento_netas(data_clientes_segmento_netas)
# st.write('##### Se muestra las Ganancias por Segmento.')
# st.plotly_chart(fig,use_container_width=True,selection_mode="box")




# # --------------------------------
# # Grafica de lineas, como evolucionan las ventas a lo largo del tiempo
# # --------------------------------
# st.write('#### Gráfica de lineas, como evolucionan las ventas a lo largo del tiempo.')
# st.write('#### Datos tomados de ordenes.csv.')
# fechas_ventas = f.fechas_ventas(data_ordenes)

# opciones = fechas_ventas['Year'].drop_duplicates()
# # st.write(list(opciones))
# lista = []
# for elemento in opciones:
#     lista.append(str(elemento))
# lista.append('Todos los años')

# # opciones = opciones.append('Todos los años')
# seleccion = st.selectbox('Selecciona una opción:', lista)
# figura_tiempo_ventas = vsl.figura_linea_ventas(fechas_ventas,seleccion)
# st.plotly_chart(figura_tiempo_ventas)


# # ------------------------------------
# # Gráfica de Barras de productos mas vendidos
# # ------------------------------------

# st.write('#### Grafica de Barras de Productos, Sub-Categorias y cuanto se vendieron')
# st.write('##### Datos Tomados de ordenes.csv')
# scategorias_productos = f.filtrar_subcategorias(data_ordenes,data_productos)
# fig_subcategorias = vsl.figura_subcategorias(scategorias_productos)
# st.plotly_chart(fig_subcategorias)
# st.write(scategorias_productos)
# st.write('Total de Productos vendidos =',data_ordenes['Quantity'].sum())
# # NUM_Productos = st.slider(
# #     f"Numero de barras de 5 hasta {len()}" ,
# #     min_value=6,max_value=len(distribucion_clientes)
# # )


# # ----------------------------------------------------------------
# # Analisis Relacion entre descuentos y Ventas
# # ----------------------------------------------------------------

# st.write("# 3. Relación entre descuentos y ventas de Productos.")
# st.write('##### Datos tomados de Productos.csv y ordenes.csv.')
# agrupado_producto_descuento = f.filtrar_producto_descuento(data_ordenes)
# st.write(agrupado_producto_descuento)
# st.write('Total de Productos vendidos =',agrupado_producto_descuento['Quantity'].sum())
# figura_dispersion = vsl.figura_dispersion(agrupado_producto_descuento)
# st.plotly_chart(figura_dispersion)

# ----------------------------------------------------------------
# Analisis de Envios
# ----------------------------------------------------------------

# st.write("# 4. Análisis de Envíos")
# st.write('### Datos tomados de Productos.csv y ordenes.csv.')
# st.write('#### Días en los que tarda en enviarse el Producto.')
# # tiempo de Entrega promedio por region
# agrupado_tiempo_region = f.filtrar_tiempo_region(data_ordenes,data_cliente,df_estados_abreviados)
# agrupado_tiempo_region = f.cambiar_abreviaturas_tiempo(df_estados_abreviados,agrupado_tiempo_region)
# st.table(pd.DataFrame(agrupado_tiempo_region).head())

# figura_timpo_entrega = vsl.figura_mapa_tiempo(pd.DataFrame(agrupado_tiempo_region))
# st.plotly_chart(figura_timpo_entrega)


# # ----------------------------------------------------------------
# # Productos mas rentables y menos rentables
# # ----------------------------------------------------------------

# st.write('# 5. Rentabilidad en los productos.')
# st.write('### Se vera cual de los productos son mas rentables y menos rentables.')
# productos_rentables = f.producto_rentable(data_ordenes,data_productos)
# st.table(productos_rentables.iloc[:,2:4].head())
# # st.write(productos_rentables[productos_rentables['Profit']>=0])
# # st.write(productos_rentables[productos_rentables['Profit']<0])
# figura_rentabilidad_productos = vsl.figura_rentabilidad_productos(productos_rentables)
# st.plotly_chart(figura_rentabilidad_productos)

# # ----------------------------------------------------------------
# # Productos Devueltos
# # ----------------------------------------------------------------

# st.write('# 6. Devolucion en los productos.')
# st.write('### Se vera cual de los productos son mas Devueltos.')
# productos_devueltos = f.filtrado_devluciones(data_ordenes,data_productos)
# # st.table(productos_devueltos)
# st.table(productos_devueltos)

# figura_devueltos_productos = vsl.figura_dispersion_devoluciones(productos_devueltos)
# st.plotly_chart(figura_devueltos_productos)


# # ----------------------------------------------------------------
# # Matriz de Correlacion
# # ----------------------------------------------------------------
# st.write('# 7. Matriz de Correlacion')
# st.write('### Explicar los valores de la matriz de Correlacion.')
# datos_correlacion = f.filtrado_correlacion(data_ordenes)
# # st .write(data_ordenes.head())
# st.write(datos_correlacion)
# figura_correlacion = vsl.figura_matriz_correlacion(datos_correlacion)

# st.pyplot(figura_correlacion)
# st.write("##### 7.1 Las unicas variables que parecen tener una relacion importante es en Profit(Ganancias) y Sales (Ventas Brutas)")









import streamlit as st
import pandas as pd
import filtrado as f
import numpy as np
import visualizacion as vsl

# Configuración inicial
st.set_page_config(page_title="Exploración", page_icon="🔥", layout="wide")
st.title('🔥 Exploración de los Datos 🔍')
st.write('### Análisis Estadístico e Información General 📊')

# Sección: Carga de Datos
st.sidebar.title("📂 Carga de Datos")
st.sidebar.write("Archivos utilizados:")
st.sidebar.write("- `clientes.csv`")
st.sidebar.write("- `localizacion.csv`")
st.sidebar.write("- `ordenes.csv`")
st.sidebar.write("- `productos.csv`")

data_cliente = pd.read_csv('BD/clientes.csv')
data_localizacion = pd.read_csv('BD/localizacion.csv')
data_ordenes = pd.read_csv('BD/ordenes.csv')
data_productos = pd.read_csv('BD/productos.csv')

# Mostrar una vista previa de los datos
st.markdown("## **Vista General de los Datos**")
cols = st.columns(2)

with cols[0]:
    st.write('#### Información de Clientes')
    st.table(data_cliente.iloc[:5])

    st.write('#### Información de Localización')
    st.table(data_localizacion.iloc[:5])

with cols[1]:
    st.write('#### Información de Órdenes')
    st.write("###### Tabla clave que detalla las órdenes y cantidades")
    st.table(data_ordenes.iloc[:5])

    st.write('#### Información de Productos')
    st.table(data_productos.iloc[:5])

# # -----------------------------------------------------------------------
# # Analisis de Clientes
# # -----------------------------------------------------------------------

# Sección: Análisis de Clientes
st.markdown("# 📌 1. Análisis de Clientes")
df_estados_abreviados = pd.read_csv("BD/estados.csv")

# Distribución por estado
data_cliente_clase = f.Clientes(data_cliente)
distribucion_clientes = data_cliente_clase.distribucion_clientes()

st.write("## 🗺️ Distribución de Clientes por Estado")
st.write("### Visualización en Mapa")
datos_abreviados = f.cambiar_abreviaturas(df_estados_abreviados, distribucion_clientes)
fig_map = vsl.figura_mapa(datos_abreviados, 49)
st.plotly_chart(fig_map, use_container_width=True)

st.write("### Tabla Ordenada de Clientes por Estado")
st.table(pd.DataFrame(datos_abreviados).sort_values('Clientes', ascending=False).head())

st.write("**Total de Clientes:**", data_cliente['Customer ID'].drop_duplicates().count())

# Distribución por segmentos
distribucion_segmento = data_cliente_clase.distribucion_segmentos_clientes()
st.write("## 📊 Segmentos de Clientes")
st.write("### Visualización de Compras por Segmento (Gráfica de Pastel)")
fig = vsl.figure_pie(distribucion_segmento)
st.plotly_chart(fig, use_container_width=True)
st.table(distribucion_segmento)
# # ----------------------------------------------------------------
# # Productos que consume mas cada categoria
# # ----------------------------------------------------------------

st.write('### 1.1 Productos que consume cada Categoría')
opciones = data_cliente['Segment'].unique()
# st.write(list(opciones))
lista = []
for elemento in opciones:
    lista.append(str(elemento))

# opciones = opciones.append('Todos los años')
seleccion_segmento = st.selectbox('Selecciona una opción:', lista)
categoria_producto = f.filtrado_productos_categoria(data_ordenes,data_productos,data_cliente,seleccion_segmento)
# st.write(categoria_producto)

figura_categoria_segmento = vsl.figura_categoria_segmento(categoria_producto)
st.plotly_chart(figura_categoria_segmento)



# # -----------------------------------------------------------------------
# # Analisis de Ventas
# # -----------------------------------------------------------------------
# Sección: Análisis de Ventas
st.markdown("# 📌 2. Análisis de Ventas")
st.write("## 🗺️Ventas Brutas por Estado")

st.write('### Gráfica de Distribucion de Ventas Brutas.')
st.write(f'#### Tomando en cuenta esta tabla de datos extraidos de clientes.csv. y tambien ordenes.csv.')
st.write('##### En esta grafica se mostrara Los estados con sus Datos en Ventas Brutas.')
Data_ventas_estado = f.juntar_ventas(data_cliente,data_ordenes)
st.write("### Los 5 Estados con mayor Ventas Brutas.")
st.table(Data_ventas_estado.sort_values('Sales',ascending=False).head())
Data_ventas_estado_dict = f.cambiar_abreviaturas_ventas(df_estados_abreviados,Data_ventas_estado)
figura_ventas_estado = vsl.figura_mapa_ventas(Data_ventas_estado_dict)
st.plotly_chart(figura_ventas_estado,theme=None,use_container_width=True)
st.write('Total de Ventas Brutas =',data_ordenes['Sales'].sum())

# --------------------------------
# Analisis por Segmento
# --------------------------------
st.write('### Gráfica de Distribucion de Ventas por Segmento.')
st.write(f'####  Se mostrar cuales son los segmentos que mas generan Ventas Brutas($).')
data_clientes_segmento = f.segmento_ventas(data_cliente,data_ordenes)
st.table(data_clientes_segmento)
fig = vsl.figura_segmento(data_clientes_segmento)
st.write('##### Se muestra las ventas por Segmento.')
st.plotly_chart(fig,use_container_width=True,selection_mode="box")


# --------------------------------
# Analisis de ventas Netas
# --------------------------------
st.write('### 🗺️ Gráfica de Distribucion de Ventas Netas por Estado.')
st.write(f'####  Se mostrar cuales son los segmentos que mas generan Ganancias Netas($) por estado.')
data_ventas_n_estado = f.ventas_netas_estado(data_cliente,data_ordenes)
st.write("### Los 5 Estados con mayor Ganancias Netas")
st.table(data_ventas_n_estado.sort_values('Sales',ascending=False).head())

Data_ventas_estado_dict_netas = f.cambiar_abreviaturas_ventas(df_estados_abreviados,data_ventas_n_estado)
figura_ventas_netas = vsl.figura_mapa_ventas(Data_ventas_estado_dict_netas)
st.plotly_chart(figura_ventas_netas,theme=None,use_container_width=True)
st.write('Total de Ganancias Netas =',data_ordenes['Profit'].sum())


# Ventas por segmento netas

st.write('### Gráfica de Distribucion de Ganancias Netas por Segmento.')
st.write(f'####  Se mostrar cuales son los segmentos que mas generan Ganancias Netas($).')
data_clientes_segmento_netas = f.segmento_ventas_netas(data_cliente,data_ordenes)
st.table(data_clientes_segmento_netas)
fig = vsl.figura_segmento_netas(data_clientes_segmento_netas)
st.write('##### Se muestra las Ganancias por Segmento.')
st.plotly_chart(fig,use_container_width=True,selection_mode="box")




# --------------------------------
# Grafica de lineas, como evolucionan las ventas a lo largo del tiempo
# --------------------------------
st.write('#### Gráfica de lineas, como evolucionan las ventas a lo largo del tiempo.')
st.write('#### Datos tomados de ordenes.csv.')
fechas_ventas = f.fechas_ventas(data_ordenes)

opciones = fechas_ventas['Year'].drop_duplicates()
# st.write(list(opciones))
lista = []
for elemento in opciones:
    lista.append(str(elemento))
lista.append('Todos los años')

# opciones = opciones.append('Todos los años')
seleccion = st.selectbox('Selecciona una opción:', lista)
figura_tiempo_ventas = vsl.figura_linea_ventas(fechas_ventas,seleccion)
st.plotly_chart(figura_tiempo_ventas)


# ------------------------------------
# Gráfica de Barras de productos mas vendidos
# ------------------------------------

st.write('#### Grafica de Barras de Productos, Sub-Categorias y cuanto se vendieron')
st.write('##### Datos Tomados de ordenes.csv')
scategorias_productos = f.filtrar_subcategorias(data_ordenes,data_productos)
fig_subcategorias = vsl.figura_subcategorias(scategorias_productos)
st.plotly_chart(fig_subcategorias)
st.write(scategorias_productos)
st.write('Total de Productos vendidos =',data_ordenes['Quantity'].sum())
# NUM_Productos = st.slider(
#     f"Numero de barras de 5 hasta {len()}" ,
#     min_value=6,max_value=len(distribucion_clientes)
# )



# Sección: Relación entre Descuentos y Ventas
st.markdown("# 📌 3. Relación entre Descuentos y Ventas")
agrupado_producto_descuento = f.filtrar_producto_descuento(data_ordenes)
figura_dispersion = vsl.figura_dispersion(agrupado_producto_descuento)
st.plotly_chart(figura_dispersion, use_container_width=True)

# Otros análisis (se pueden estructurar similarmente)
st.markdown("# 📌 4. Análisis de Envíos")
st.write('### Datos tomados de Productos.csv y ordenes.csv.')
st.write('#### Días en los que tarda en enviarse el Producto.')
# tiempo de Entrega promedio por region
agrupado_tiempo_region = f.filtrar_tiempo_region(data_ordenes,data_cliente,df_estados_abreviados)
agrupado_tiempo_region = f.cambiar_abreviaturas_tiempo(df_estados_abreviados,agrupado_tiempo_region)
st.table(pd.DataFrame(agrupado_tiempo_region).head())

figura_timpo_entrega = vsl.figura_mapa_tiempo(pd.DataFrame(agrupado_tiempo_region))
st.plotly_chart(figura_timpo_entrega)


st.markdown("# 📌 5. Rentabilidad de Productos")
st.write('### Se vera cual de los productos son mas rentables y menos rentables.')
productos_rentables = f.producto_rentable(data_ordenes,data_productos)
st.table(productos_rentables.iloc[:,2:4].head())
# st.write(productos_rentables[productos_rentables['Profit']>=0])
# st.write(productos_rentables[productos_rentables['Profit']<0])
figura_rentabilidad_productos = vsl.figura_rentabilidad_productos(productos_rentables)
st.plotly_chart(figura_rentabilidad_productos)


st.markdown("# 📌 6. Devoluciones")
st.write('### Se vera cual de los productos son mas Devueltos.')
productos_devueltos = f.filtrado_devluciones(data_ordenes,data_productos)
# st.table(productos_devueltos)
st.table(productos_devueltos)

figura_devueltos_productos = vsl.figura_dispersion_devoluciones(productos_devueltos)
st.plotly_chart(figura_devueltos_productos)



st.markdown("# 📌 7. Matriz de Correlación")


st.write('### Explicar los valores de la matriz de Correlacion.')
st.write('#### Se vera la correlacion entre las columnas (Sales, Quantity, Discount, Profit).')
datos_correlacion = f.filtrado_correlacion(data_ordenes)
# st .write(data_ordenes.head())
st.write(datos_correlacion)
figura_correlacion = vsl.figura_matriz_correlacion(datos_correlacion)

st.pyplot(figura_correlacion)
st.write("##### 7.1 Las unicas **variables** que parecen tener una relacion importante es en Profit(Ganancias) y Sales (Ventas Brutas)")


