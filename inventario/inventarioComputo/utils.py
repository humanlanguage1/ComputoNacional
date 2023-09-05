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
    plt.xlabel('Codigo de producto')
    plt.ylabel('STOCK')
    plt.tight_layout()
    plt.legend()
    plt.grid(True)    
    graph= get_graph()
    return graph 

def get_prediction(x,y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10,5))    
    plt.title('Stock disponible en el futuro')
    plt.legend()
    plt.xticks(rotation=45)
    x = pd.to_datetime(x)
    plt.plot_date(x,y,linestyle='solid')
    plt.grid(True)
    graph= get_graph()
    return graph


