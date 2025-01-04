import filtrado as f
import pandas as pd
data_cliente = pd.read_csv('BD/clientes.csv')
data_cliente_head = data_cliente.iloc[0:5]

data_localizacion = pd.read_csv('BD/localizacion.csv')
data_localizacion_head = data_localizacion.iloc[0:5]

data_ordenes = pd.read_csv('BD/ordenes.csv')
data_ordenes_head = data_ordenes.iloc[0:5]

data_productos = pd.read_csv('BD/productos.csv')
data_productos_head = data_productos.iloc[0:5]


df_estados_abreviados = pd.read_csv("BD/estados.csv")

data_cliente_clase = f.Clientes(data_cliente)
distribucion_clientes = data_cliente_clase.distribucion_clientes()


datos_abreviados = f.fechas_ventas(data_ordenes)
print(datos_abreviados)
