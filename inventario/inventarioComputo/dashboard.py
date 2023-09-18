import matplotlib.pyplot as plt
import base64
from io import BytesIO
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np
import seaborn as sn
import pandas as pd 
import plotly.express as px
from sklearn import metrics
import datetime as dt
from sktime.forecasting.base import ForecastingHorizon
from sktime.forecasting.model_selection import temporal_train_test_split
from sktime.forecasting.theta import ThetaForecaster
from sktime.performance_metrics.forecasting import mean_absolute_percentage_error
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

df = px.data.tips()

app = Dash(__name__)

app.layout = html.Div(
    [
        html.H4("Analysis of the restaurant sales"),
        dcc.Graph(id="graph"),
        html.P("Names:"),
        dcc.Dropdown(
            id="names",
            options=["smoker", "day", "time", "sex"],
            value="day",
            clearable=False,
        ),
        html.P("Values:"),
        dcc.Dropdown(
            id="values",
            options=["total_bill", "tip", "size"],
            value="total_bill",
            clearable=False,
        ),
    ]
)
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
def get_plot1(x,y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(14,7))
    plt.title('Categorías y Productos')
    plt.scatter(x,y)
    plt.xticks(rotation=45)
    plt.xlabel('Codigo de producto')
    plt.ylabel('Categoria de producto')
    plt.tight_layout()
    plt.legend()
    plt.grid(True)    
    graph= get_graph()
    return graph 

def get_piechart(x1,y1):
    plt.switch_backend('AGG')
    fig = px.pie(x1, y1)
    plt.legend()
    graph= fig.show()   
    return graph

