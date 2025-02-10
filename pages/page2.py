

import streamlit as st
import pandas as pd
import filtrado as f
import numpy as np
import visualizacion as vsl


# Configuración inicial
st.set_page_config(page_title="Modelos de ML", page_icon="📊", layout="wide")
# st.title('📊 Aplicación de Modelos de Machine Learning para predecir cierto fenómenos. 🔍')
# st.write('### Modelos de Machine Learning 📊')

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
st.title('📊 Dashboard de Análisis de Datos 🔍')


datos = f.obtener_valores(data_ordenes)
# lista = vsl.figura_series_tiempo(datos,datos_diff)
# st.write('### Se mostraran como se descompusieron las Series de Tiempo para sus Análisis.')
# for i in lista:
#     st.pyplot(i)


st.write('## En esta seccion se podran hacer prediciones por medio del Modelo de SARIMAX.')
st.write('### Solo se podran predecir maximo 100 días despues de la ultima recopilacion del Data Set.')
Informacion = st.slider(
        f"Información de la Serie de Tiempo." ,
        min_value=len(datos),max_value=0
    )
dias = st.slider(
        f"Numero de barras de 0 hasta 100 dias en el futuro." ,
        min_value=0,max_value=100
    )
predicciones = f.modelo_sarimax(datos,int(dias))
st.table(predicciones)

figura_serie = vsl.figura_serie(df_filtrado=datos,df_prediccion=predicciones,limite=int(Informacion))

st.plotly_chart(figura_serie)
