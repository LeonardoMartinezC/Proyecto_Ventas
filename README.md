Proyecto enfocado en entender como Graficar en Plotly
Lo que se quiso hacer fue usar Pandas para el filtrado de datos
los objetivos que se presentan son los siguientes:
OBJETIVOS
    Que se debe mostrar en el modelo de exploracion
    1. Mostrar las categorias mas vendidas en ciertas ciudades, cambiando(ciudad ) (region)
    2. categorias y sub-categorias mas vendidas, cambiando (Segment cliente) 
    3. Ciudad que compra una categoria mas que otras cambiando(Categoria)
    Visualizacion de Datos (Exploracion)

1. Análisis de Clientes
        Distribución de clientes por región o estado:
        Visualización: Gráfica de barras o mapa geográfico.
        Objetivo: Identificar dónde se concentran los clientes.
        Herramienta: seaborn para barras o plotly para mapas interactivos.
        
        Segmento de clientes:
        Visualización: Gráfica circular o de barras.
        Objetivo: Ver qué segmentos de clientes (p. ej., consumidor, corporativo) son más comunes.
2. Análisis de Ventas
        Ingresos por región o estado:
        Visualización: Mapa de calor o gráfico de barras.
        Objetivo: Identificar las áreas con mayor o menor cantidad de ventas.

        Ingresos por segmento:
        Visualización: Gráfica de barras.
        Objetivo: Determinar cuál segmento de cliente genera más ingresos.

        Tendencia de ventas:
        Visualización: Gráfica de líneas.
        Objetivo: Analizar cómo evolucionan las ventas a lo largo del tiempo (por mes o año).

        Contribución de categorías y subcategorías:
        Visualización: Gráfica de barras agrupadas o de columnas apiladas.
        Objetivo: Ver cuáles categorías/subcategorías generan más ventas y cuáles son menos rentables.
        
3. Análisis de Productos
        Productos más vendidos:
        Visualización: Gráfica de barras horizontales.
        Objetivo: Mostrar cuáles son los productos más populares.
        Categoría vs. Subcategoría:
        Visualización: Mapa de árbol o gráfico de burbujas.
        Objetivo: Explorar la distribución y popularidad de productos.
        
        Relación entre descuentos y ventas:
        Visualización: Gráfico de dispersión.
        Objetivo: Evaluar si los descuentos tienen un impacto directo en las ventas.



4. Análisis de Rentabilidad
        Productos más rentables vs. menos rentables:
        Visualización: Gráfica de barras dividida en positivo (rentabilidad) y negativo (pérdidas).
        Objetivo: Identificar qué productos son más lucrativos o causan pérdidas.
        

5. Análisis de Envíos
        Tiempo de entrega promedio por región:
        Visualización: Gráfico de barras.
        Objetivo: Determinar en qué regiones se tardan más los envíos.
        
6. Análisis de Devoluciones

        Relación entre devoluciones y descuento:
        Visualización: Gráfico de dispersión.
        Objetivo: Evaluar si los descuentos están relacionados con un aumento en devoluciones.

7. Visualizaciones Multidimensionales
        Matriz de correlación:
        Visualización: Heatmap.
        Objetivo: Analizar relaciones entre ventas, descuentos, cantidad, y rentabilidad.



# Modelo SARIMAX
    El código procesa un conjunto de datos de órdenes de compra para preparar una serie de tiempo y entrenar un modelo de predicción. Primero, carga los datos desde un archivo CSV, organiza las fechas y calcula el promedio de ganancias por día. Luego, limpia los datos eliminando valores nulos y atípicos, asegurando que la serie tenga una estructura adecuada para el análisis temporal. Posteriormente, divide los datos en conjuntos de entrenamiento y prueba, analiza patrones estacionales y entrena un modelo SARIMAX para predecir futuras ganancias. Finalmente, el modelo entrenado se guarda para su uso posterior en predicciones.
        
