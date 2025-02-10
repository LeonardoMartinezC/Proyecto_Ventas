import pandas as pd
import numpy as np
import joblib
# import seaborn as sns


# Leer Archivo ordenes.csv
data_ordenes = pd.read_csv('../BD/ordenes.csv',index_col='Order Date')
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
print(df_cleaned)


## Importamos las librerias necesarias para el manejo de SARIMAX
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.seasonal import seasonal_decompose 

train = df_cleaned.iloc[:1000]
test = df_cleaned.iloc[1000:]


result = seasonal_decompose(df_cleaned, model= 'add')
result.plot()

# Entrenar el modelo SARIMAX
"""
    Aplicaremos SARIMAX ya que se probo que era el que daba mejor resultados 
    con un Seasonal de cada 60 dias

"""

model = SARIMAX(df_cleaned['Profit'],order = (1,1,1), seasonal_order=(1,1,1,60),enforce_invertibility=False)
result = model.fit()
joblib.dump(result, "Models/SARIMAX.pkl")





































