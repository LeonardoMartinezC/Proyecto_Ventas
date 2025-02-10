import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
# import seaborn as sns
from pandas.plotting import lag_plot
from sklearn.metrics import mean_squared_error,r2_score
from statsmodels.tsa.stattools import adfuller
import joblib

class Clientes(object):
    def __init__(self, DataFrame_Clientes):
        self.clientes = DataFrame_Clientes
    def distribucion_clientes(self):
        #Primero tener las principales ciudades
        #Sacar donde se concentran mas clientes de cada ciudad
        clientes = self.clientes.drop_duplicates(subset='Customer ID', keep='first')
        conteo_por_ciudad = clientes['State'].value_counts()
    
        # Convertir el resultado a un DataFrame
        df = conteo_por_ciudad.reset_index()
        df.columns = ['State', 'Count']  # Renombrar columnas
        return df
    

    def distribucion_segmentos_clientes(self):
        # Saber laas clase
        clientes = self.clientes.drop_duplicates(subset='Customer ID', keep='first')
        conteo_clases = clientes['Segment'].value_counts()
        #hacerlo un data frame
        df = conteo_clases.reset_index()
        df.columns = ['Segment', 'Count'] # Renombrar columnas
        return df

def cambiar_abreviaturas( E, DC):
        #Cambiar los estados por sus abreviaturas
        i = 0
        clientes = []
        abreviaturas = []
        LISTA_FI = []
        for ESTADO in E:
            abreviaturas.append(list(E[ESTADO]))

        for CLIENTES in  DC:
            clientes.append(list(DC[CLIENTES]))
        

        TAMANO1 = len(clientes[0])
        TAMANO2 = len(abreviaturas[0])
        # Dejar las abrevisturas que si se necesitan 
        for i in range(TAMANO1):
            for j in range(TAMANO2):
                if(clientes[0][i] == abreviaturas[0][j]):
                    LISTA_FI.append(abreviaturas[1][j])
        clientes.append(LISTA_FI)
        diccionario_Clientes = {
            'Estado':clientes[0],
            'Clientes':clientes[1],
            'abreviatura':clientes[2]
        }

        
        return diccionario_Clientes

def filtrado_productos_categoria(ordenes,productos,clientes,CATEGORIA):
    """
        1. Saber que cliente es la CATEGORIA que estamos buscando
        2. Relacionar la CATEGORIA con los productos que compra (ordenes)
        3. Relacionar el producto que compra con La Categoria que es el cliente
    """
    CLIENTE_CATEGORIA = clientes[clientes['Segment'] == CATEGORIA]
    CLIENTE_CATEGORIA = CLIENTE_CATEGORIA[['Customer ID','Segment']].sort_values('Customer ID')

    CLIENTE_PRODUCTOS = ordenes[['Customer ID','Product ID','Quantity']].sort_values('Customer ID')
    
    CLIENTE_PRODUCTO_SEGMENTO = CLIENTE_PRODUCTOS[CLIENTE_PRODUCTOS['Customer ID'].isin(CLIENTE_CATEGORIA['Customer ID'])].sort_values('Product ID')
    CLIENTE_PRODUCTO_SEGMENTO = CLIENTE_PRODUCTO_SEGMENTO.groupby(CLIENTE_PRODUCTO_SEGMENTO['Product ID'])['Quantity'].sum()
    CLIENTE_PRODUCTO_SEGMENTO = CLIENTE_PRODUCTO_SEGMENTO.reset_index()
    CLIENTE_PRODUCTO_SEGMENTO['Segment'] = CATEGORIA
    CLIENTE_PRODUCTO_SEGMENTO.columns = ['Product ID', 'Quantity','Segment']
    CLIENTE_PRODUCTO_SEGMENTO = CLIENTE_PRODUCTO_SEGMENTO.sort_values('Product ID')
    # CLIENTE_PRODUCTO_SEGMENTO = CLIENTE_PRODUCTO_SEGMENTO.groupby(CLIENTE_PRODUCTO_SEGMENTO['Product ID'])['Quantity'].sum()


    PRODUCTO_SEGMENTO = productos[productos['Product ID'].isin(CLIENTE_PRODUCTO_SEGMENTO['Product ID'])].sort_values('Product ID')
    PRODUCTO_SEGMENTO = PRODUCTO_SEGMENTO.drop_duplicates(subset='Product ID', keep='first')
    PRODUCTO_SEGMENTO = pd.merge(PRODUCTO_SEGMENTO,CLIENTE_PRODUCTO_SEGMENTO,on = 'Product ID').sort_values('Product ID')

    PRODUCTO_SEGMENTO = PRODUCTO_SEGMENTO.groupby(PRODUCTO_SEGMENTO['Sub-Category'])['Quantity'].sum()
    PRODUCTO_SEGMENTO = PRODUCTO_SEGMENTO.reset_index()
    PRODUCTO_SEGMENTO['Segment'] = CATEGORIA
    PRODUCTO_SEGMENTO = PRODUCTO_SEGMENTO.sort_values('Quantity',ascending=False)
    # return CLIENTE_PRODUCTO_SEGMENTO
    return PRODUCTO_SEGMENTO
# -----------------------------------------------------------------------
# Analisis de Ventas
# -----------------------------------------------------------------------
def cambiar_abreviaturas_ventas( E, DC):
        #Cambiar los estados por sus abreviaturas
        i = 0
        clientes = []
        abreviaturas = []
        LISTA_FI = []
        for ESTADO in E:
            abreviaturas.append(list(E[ESTADO]))
        for CLIENTES in  DC:
            clientes.append(list(DC[CLIENTES]))
        
        TAMANO1 = len(clientes[0])
        TAMANO2 = len(abreviaturas[0])

        # Dejar las abrevisturas que si se necesitan 
        for i in range(TAMANO1):
            for j in range(TAMANO2):
                if(clientes[0][i] == abreviaturas[0][j]):
                    LISTA_FI.append(abreviaturas[1][j])
        
        clientes.append(LISTA_FI)
        
        diccionario_Clientes = {
                            'Estado':clientes[0],
                            'Ventas':clientes[1],
                            'abreviatura':clientes[2]
        }

        
        return diccionario_Clientes


def juntar_ventas(clientes, ordenes):


    ventas_por_cliente = ordenes.groupby(ordenes['Customer ID'])['Sales'].sum()
    estado_cliente = clientes.sort_values('Customer ID')
    cliente_estado = estado_cliente.drop_duplicates(subset='Customer ID', keep='first')
    
    cliente_estado = cliente_estado.set_index('Customer ID')
    cliente_estado['Sales'] = ventas_por_cliente
    
    cliente_estado = cliente_estado.reset_index()
    datos = cliente_estado.groupby(cliente_estado['State'])['Sales'].sum()
    datos = datos.reset_index()
    datos.columns = ['State','Sales']
    return datos  # return ventas_por_cliente

def segmento_ventas(clientes, ordenes):
    ventas_por_cliente = ordenes.groupby(ordenes['Customer ID'])['Sales'].sum()
    estado_cliente = clientes.sort_values('Customer ID')

    cliente_estado = estado_cliente.drop_duplicates(subset='Customer ID', keep='first')
    cliente_estado = cliente_estado.set_index('Customer ID')
    cliente_estado['Sales'] = ventas_por_cliente
    clientes_segmento = cliente_estado.groupby(cliente_estado['Segment'])['Sales'].sum()
    
    clientes_seg = clientes_segmento.reset_index()
    clientes_seg.columns = ['Segment','Sales']

    return clientes_seg


#----------------------------------------------------------------
# Ventas netas
#----------------------------------------------------------------
def ventas_netas_estado(clientes,ordenes):
    ventas_por_cliente = ordenes.groupby(ordenes['Customer ID'])['Profit'].sum()
    estado_cliente = clientes.sort_values('Customer ID')
    cliente_estado = estado_cliente.drop_duplicates(subset='Customer ID', keep='first')
    
    cliente_estado = cliente_estado.set_index('Customer ID')
    cliente_estado['Sales'] = ventas_por_cliente
    
    cliente_estado = cliente_estado.reset_index()
    datos = cliente_estado.groupby(cliente_estado['State'])['Sales'].sum()
    datos = datos.reset_index()
    datos.columns = ['State','Sales']
    return datos  # return ventas_por_cliente

def segmento_ventas_netas(clientes, ordenes):
    ventas_por_cliente = ordenes.groupby(ordenes['Customer ID'])['Profit'].sum()
    estado_cliente = clientes.sort_values('Customer ID')

    cliente_estado = estado_cliente.drop_duplicates(subset='Customer ID', keep='first')
    cliente_estado = cliente_estado.set_index('Customer ID')
    cliente_estado['Sales'] = ventas_por_cliente

    clientes_segmento = cliente_estado.groupby(cliente_estado['Segment'])['Sales'].sum()
    
    clientes_seg = clientes_segmento.reset_index()
    clientes_seg.columns = ['Segment','Sales']

    return clientes_seg

def fechas_ventas(ordenes):
    ordenes['Order Date'] = pd.to_datetime(ordenes['Order Date'])
    ordenes['Year'] = ordenes['Order Date'].dt.year
    ordenes['Month'] = ordenes['Order Date'].dt.month
    ordenes['Day'] = ordenes['Order Date'].dt.day
    ventas_por_mes_anio = ordenes.groupby(['Year', 'Month'])['Sales'].sum().reset_index()
    # ventas_por_mes_anio.columns = ['Order Date', 'Sales']

    return ventas_por_mes_anio



"""
1. primero filtramos los datos de ordenes y sumamos las cantidades con respecto a su producto id
2. Despues ordenamos los datos de productos.csv para que queden ordenados e iguales que en el paso 1
3. Despues eliminamos los duplicados de el paso 2 para que solo queden los productos 1 vez
4. Agregamos una columna llmada Quantity y le ponemos la cantidad de productos de cada producto id
5. Ahora los agrupamos y sumamos por subcategoria
"""
def filtrar_subcategorias(ordenes,productos):
    producto_cantidad = ordenes.groupby(ordenes['Product ID'])['Quantity'].sum()
    producto_filtrado = productos.sort_values('Product ID')

    producto_cantidad_sd = producto_filtrado.drop_duplicates(subset='Product ID', keep='first')
    cantidad = producto_cantidad_sd.set_index('Product ID')
    cantidad['Quantity'] = producto_cantidad

    cantidad_subcategoria = cantidad.groupby(cantidad['Sub-Category'])['Quantity'].sum()
    
    cantidad_seg = cantidad_subcategoria.reset_index()
    cantidad_seg.columns = ['Sub-Category','Quantity']
    cantidad_seg = cantidad_seg.sort_values('Quantity',ascending=False)
    # cantidad_seg = cantidad_seg['Quantity'].sum()
    return cantidad_seg



"""
    Tener la relacion entre porductos que se venden mas y los descuentos que tienen
"""
def filtrar_producto_descuento(ordenes):
    agrupado_p = ordenes.groupby(ordenes['Product ID'])['Quantity'].sum()
    producto_filtrado = ordenes.sort_values('Product ID')

    producto_cantidad_sd = producto_filtrado.drop_duplicates(subset='Product ID', keep='first')
    cantidad = producto_cantidad_sd.set_index('Product ID')
    cantidad['Quantity'] = agrupado_p
    
    cantidad_subcategoria = cantidad.groupby(cantidad['Discount'])['Quantity'].sum()
    cantidad_seg = cantidad_subcategoria.reset_index()
    cantidad_seg.columns = ['Discount','Quantity']
    cantidad_seg = cantidad_seg.sort_values('Discount',ascending=False)
    return cantidad_seg

def filtrar_tiempo_region(ordenes, clientes,estados):
    """
        1. Sacar los dias que se tardar en llegar el envio 
        2. 
    """

    ordenes['Order Date'] = pd.to_datetime(ordenes['Order Date'])
    # ordenes['Year'] = ordenes['Order Date'].dt.year
    # ordenes['Month'] = ordenes['Order Date'].dt.month
    # ordenes['Day'] = ordenes['Order Date'].dt.day
    ordenes['Ship Date'] = pd.to_datetime(ordenes['Ship Date'])
    # ordenes['Year_s'] = ordenes['Ship Date'].dt.year
    # ordenes['Month_s'] = ordenes['Ship Date'].dt.month
    # ordenes['Day_s'] = ordenes['Ship Date'].dt.day
    # Codigo para tener la Diferencia entre las fechas en Dais
    lista_tiempo = abs((ordenes['Ship Date'] - ordenes['Order Date']) / np.timedelta64(1, 'D'))
    ordenes['Time Wait'] = lista_tiempo
    """
        1. Tomar los estados de Clientes para que el recorrido sea mas lento
    """
    clientes_estado = clientes.drop_duplicates(subset='City', keep='first')
    lista_estados_ordenes =pd.merge(ordenes, clientes_estado, on="City", how="left")
    
    lista_estados_ordenes = lista_estados_ordenes.groupby(lista_estados_ordenes['State'])['Time Wait'].mean()
    lista_estados_ordenes = lista_estados_ordenes.reset_index()
    lista_estados_ordenes.columns = ['State','Time Wait']
    lista_estados_ordenes = lista_estados_ordenes.sort_values('Time Wait',ascending=False)


    return lista_estados_ordenes

def cambiar_abreviaturas_tiempo( E, DC):
        #Cambiar los estados por sus abreviaturas
        i = 0
        clientes = []
        abreviaturas = []
        LISTA_FI = []
        for ESTADO in E:
            abreviaturas.append(list(E[ESTADO]))
        for CLIENTES in  DC:
            clientes.append(list(DC[CLIENTES]))
        
        TAMANO1 = len(clientes[0])
        TAMANO2 = len(abreviaturas[0])

        # Dejar las abrevisturas que si se necesitan 
        for i in range(TAMANO1):
            for j in range(TAMANO2):
                if(clientes[0][i] == abreviaturas[0][j]):
                    LISTA_FI.append(abreviaturas[1][j])
        
        clientes.append(LISTA_FI)
        
        diccionario_Clientes = {
                            'State':clientes[0],
                            'Time Wait':clientes[1],
                            'abreviatura':clientes[2]
        }

        
        return diccionario_Clientes


def producto_rentable(ordenes,productos):
    """
        1. filtrar por producto y su profit (Ganancias que genero)
        2. Tomando los productos y la cantidad de profit ver cuales son esos
            productos que mas se venden
        3. De productos eliminar productos dubplicados para que no se repitan 
            el profit y gener desvalance
        4. Agregar el Profit en cada producto de donde se eliminaron los duplicados
    """

    productos_profit = ordenes.groupby(ordenes['Product ID'])['Profit'].sum()
    producto_ordenado = productos.sort_values('Product ID')

    producto_ordenado = producto_ordenado.drop_duplicates(subset='Product ID', keep='first')
    producto_ordenado = producto_ordenado.set_index('Product ID')
    producto_ordenado['Profit'] = productos_profit
    producto_ordenado = producto_ordenado.sort_values('Profit')
    return producto_ordenado


def filtrado_devluciones(ordenes,productos):
    """
        1. Buscar y sumar los mismos productos y si han sido devueltos
        2. Empatarlos con el nombre del producto y si han sido devueltos
        3. Reset index para que se pueda volver en un DataFrame
    """
    producto_devuelto = ordenes[ordenes['Devolucion'] == 1]
    producto_devuelto = producto_devuelto.sort_values('Product ID')
    # producto_devuelto = producto_devuelto_ordenado.groupby(producto_devuelto_ordenado['Product ID'])['Devolucion'].sum()

    producto_descuento_devuelto = producto_devuelto.groupby(producto_devuelto['Discount'])['Devolucion'].sum()
    producto_descuento_devuelto = producto_descuento_devuelto.reset_index()
    producto_descuento_devuelto.columns = ['Discount','Devolucion']

    return producto_descuento_devuelto


def filtrado_correlacion(ordenes):
    """
        1. Tomar todo los valores de :
            Ventas
            Descuentos
            Cantidad
            Rentabilidad (Profit)

        2. Relacionar estas variables en una matris de correlacion
    """
    r = ordenes.iloc[:,7:11]
    
    # plt.savefig('corrTax.png', dpi = 600)
    return r.corr()

# ----------------------------------------------------------------
# ----------------------------------------------------------------
# ----------------------------------------------------------------

#obtendra el Data-set de Ordenes.csv para ver como es que se comporta las devoluciones
def obtener_valores(data):
    # Leer Archivo ordenes.csv
    data_ordenes = pd.read_csv('BD/ordenes.csv',index_col='Order Date')
# Ordenar Valores por fechas de Orden
    data_ordenes.sort_values('Order Date')
    #Agrupar las que son de la misma fecha y tener el promedio
    data_ordenes = data_ordenes.groupby(data_ordenes.index)['Profit'].mean().reset_index()
    # data_ordenes =data_ordenes['Profit']
    # print(data_ordenes)



    #Volvemos a ordenar
    df = data_ordenes.sort_values('Order Date')
    # Filtramos los valores que son igual a 0
    df = df[df['Profit'] != 0]
    # Configuramos el indice para que sean las Fechas de orden
    df = df.set_index('Order Date')

    # Hacemos tipo datetime las fechas del indice
    df.index = pd.to_datetime(df.index)
    #Hacemos que la frecuencia de la serie de tiempo sea igual a Day
    df = df.asfreq('D')

    # df.index.freq = 'MS'
    df['Profit'] = df['Profit'].fillna(df['Profit'].mean())

    # Asignamos a las columnas en nombre column
    df.columns = ['Profit']


    ## Para Tener en cuenta que existen los outliers sin que representen un problema para los modelos SARIMAX   
    # Primero obtenemos la media
    mean = df['Profit'].mean()
    # Despues la desviacion estandar 
    std_dev = df['Profit'].std()

    # Definir límites
    lower_bound = mean - 3 * std_dev
    upper_bound = mean + 3 * std_dev

    # Filtrar outliers
    df_cleaned = df[(df['Profit'] >= lower_bound) & (df['Profit'] <= upper_bound)]
    df_cleaned.plot(figsize=(20,5))
    # df.plot(figsize=(20,5),label = True, legend="pp")

    df_cleaned.index = pd.to_datetime(df_cleaned.index)
    df_cleaned = df_cleaned.asfreq('D')
    df_cleaned['Profit'] = df_cleaned['Profit'].fillna(df_cleaned['Profit'].mean())


    df.columns = ['Profit']
    return df_cleaned
def modelo_sarimax(datos,cantidad_dias):
    if(cantidad_dias<=100 and cantidad_dias != 0):
        ruta = "pages/Models/SARIMAX.pkl" 
        modelo_cargado = joblib.load(ruta)
        start_index = len(datos)
        end_index = start_index + cantidad_dias 
        predicciones = modelo_cargado.predict(start=start_index,end=end_index)
        predicciones = predicciones.iloc[1:]
        # predicciones_df = pd.DataFrame(predicciones, columns=['Profit'])
        predicciones_index = pd.date_range(start=datos.index[-1] + pd.Timedelta(days=1), periods=cantidad_dias, freq='D')

        # Convertir las predicciones en un DataFrame y asignar el índice temporal
        predicciones_df = pd.DataFrame(predicciones.values, index=predicciones_index, columns=['Profit'])

        return predicciones_df
    else:
        return None
def verificar_estacionariedad(serie):
    resultado = adfuller(serie)
    print(f"p-valor: {resultado[1]}")
    if resultado[1] > 0.05:
        print("La serie no es estacionaria.")
    else:
        print("La serie es estacionaria.")
    # return datos_pred, ax
# if __name__ == '__main__':
#     data_ordenes = pd.read_csv('../BD/ordenes.csv')
#     datos,datos_diff = obtener_valores(data_ordenes)
#     # verificar_estacionariedad(datos_diff)
#     modelo_arima(datos_diff)
    
