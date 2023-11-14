from django.http import HttpResponse
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np
import seaborn as sn
import pandas as pd 
from sklearn import metrics
import datetime as dt
from sktime.forecasting.base import ForecastingHorizon
from sktime.forecasting.model_selection import temporal_train_test_split
from sktime.forecasting.theta import ThetaForecaster
from sktime.performance_metrics.forecasting import mean_absolute_percentage_error
from django.template.loader import get_template

#Método para generar grafico
def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

#Método para generar los plots
def get_plot(x,y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(14,7))
    plt.title('Stock disponible')
    plt.plot(x,y)
    plt.xticks(rotation=45)
    plt.xlabel('Categoría')
    plt.ylabel('Producto')
    plt.tight_layout()
    plt.legend()
    plt.grid(True)    
    graph= get_graph()
    return graph 

def get_prediction(x, y):
    x = pd.array(x)
    y = pd.array(y)
    #construcción del modelo
    X_train, X_test, Y_train, Y_test = train_test_split(x.reshape(-1, 1), y, test_size = 0.6, random_state=30)
    lin_reg = LinearRegression()
    lin_reg.fit(X_train, Y_train)
    predicciones = lin_reg.predict(X_test)
    #representación gráfica
    plt.switch_backend('AGG')
    plt.figure(figsize=(14,7))
    plt.xlabel('Stock disponible')
    plt.ylabel('Stock de predicción')
    plt.scatter(Y_test, predicciones)
    #plt.plot(X_test, predicciones, "g-") 
    plt.grid(True)
    graph = get_graph()
    return graph


