#import semua modules
import numpy as np
import dash
from dash import dcc, html, Output, Input, State
from flask import Flask
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# from main import *

#inisiasi aplikasi
server = Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])


#membaca file
qin = "Q inflow "

qout = "Q outflow"

url_in = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQlkwInbZ751STr1BkqfcVaL5-Z4WISdwllRNdmq8eZ_IGndyaRzadYie21AsLdlNR3nMHp4x2egBiz/pub?output=csv&sheet={air_masuk1}"
url_out = url="https://docs.google.com/spreadsheets/d/e/2PACX-1vQNbasikjHPoNoNK9d5mHCb1-jN-ugMwVxncvVlAQ8XJV0Gn5b2ynBGmYdgTvBLvR0J3va9ucvBe-lz/pub?output=csv&sheet={air_keluar1}"


df_in = pd.read_csv(url_in)
df_out = pd.read_csv(url_out)



#membangun komponen
header = html.Div([html.H1("Mini Project Embung E Simulation"), html.H3("Group 5")],style={
    "textAlign" : "center",
    "height": "4 rem",
    "padding": "2rem 1rem",
    "background-color": "lightgreen",
})
subHeader = html.Div([html.H1("Anggota Kelompok"), html.P("Ketua Kelompok : Yahya Agung Nadabunda"),html.P("Anggota Kelompok : Rita, Wigrace, Kiagus, Retno, Shinta,  Cut ")],style={
    "textAlign" : "none",
    "top": 0,
    "left": 0,
    "right": 0,
    "height": "2 rem",
    "padding": "1rem 1rem",
    "background-color": "lightgray",
})




subtitle = html.P("Embung E merupakan...",style={})
datamasuk_gam = go.FigureWidget()
datamasuk_gam.add_bar(name="Chart Air Masuk Pertama", x=df_in['Bulan'], y=df_in['Q inflow'])
datamasuk_gam.layout.title = 'Chart Inflow Embung '

datakeluar_gam = go.FigureWidget()
datakeluar_gam.add_scatter(name="Outflow Pertama" , x=df_out['Bulan'], y=df_out['Q outflow'])
datakeluar_gam.layout.title = 'Chart Outflow Embung'

simulation_fig = go.FigureWidget()
# simulation_fig.add_scatter(name='Outflow', x=df_outflow['Bulan'], y=df_outflow['Data'])
simulation_fig.layout.title = 'Simulation'


#layout aplikasi
app.layout = html.Div(
    [
        dbc.Row([header, subtitle])  ,
        dbc.Row(
            [
                dbc.Col([dcc.Graph(figure=datamasuk_gam)]),
               
            ]
            ),
        dbc.Row(
            [
                dbc.Col([dcc.Graph(figure=datakeluar_gam)]),
                
            ]
            ),
        html.Div(
            [
                dbc.Button('Simulasi', color="danger",id='run-button', n_clicks=0)
            ],style = {'textAlign': 'center'})
        , 
        html.Div(id='output-container-button', children='Klik run untuk menjalankan simulasi.', style = {'textAlign': 'center'}),
        dbc.Row(
            [
                dbc.Col([dcc.Graph(id='simulation-result', figure=simulation_fig)])
            ]
        ),
        subHeader
    ]
    
)

#interaksi aplikasi
@app.callback(
    Output(component_id='simulation-result', component_property='figure'),
    Input('run-button', 'n_clicks')
)


def graph_update(n_clicks):
    # filtering based on the slide and dropdown selection
    if n_clicks >=1:
        #program numerik ---start----
        masuk_keluar =  (df_in['Q inflow'].values - df_out['Q outflow'].values)
        N = len(masuk_keluar)
        u = np.zeros(N)
        u0 = 12750
        u[0] = u0
        dt = 1

        #metode Euler
        for n in range(N-1):
            u[n + 1] = u[n] + dt*masuk_keluar[n] 
        #program numerik ---end----


        # the figure/plot created using the data filtered above 
        simulation_fig = go.FigureWidget()
        simulation_fig.add_scatter(name='Simulation', x=df_out['Bulan'], y=u)
        simulation_fig.layout.title = 'Simulation'

        return simulation_fig
    else:
        simulation_fig = go.FigureWidget()
        simulation_fig.layout.title = 'Embung D ITERA Simulation'

        return simulation_fig

    


#jalankan aplikasi
if __name__=='__main__':
    app.run_server()

#debug=True, port=11916
