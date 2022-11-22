#import semua modules
import numpy as np
import dash
from dash import dcc, html, Output, Input, State
from flask import Flask
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


#inisiasi aplikasi
server = Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])


#membaca file
sheet_inflow = "inflow"
sheet_outflow = "outflow"
url_inflow = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQlkwInbZ751STr1BkqfcVaL5-Z4WISdwllRNdmq8eZ_IGndyaRzadYie21AsLdlNR3nMHp4x2egBiz/pub?output=csv"
url_outflow = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQNbasikjHPoNoNK9d5mHCb1-jN-ugMwVxncvVlAQ8XJV0Gn5b2ynBGmYdgTvBLvR0J3va9ucvBe-lz/pub?output=csv"
df_inflow = pd.read_csv(url_inflow)
df_outflow = pd.read_csv(url_outflow)


#membangun komponen
header = html.Div([html.H1("Aplikasi Simulasi Kapasitas Embung"), html.H3("Kelompok 7")],style={
    "textAlign" : "center",
    "top": 0,
    "left": 0,
    "right": 0,
    "height": "6 rem",
    "padding": "2rem 1rem",
    "background-color": "red",
})
subtitle = html.H2("MK Kapita Selekta Matematika Komputasi (MA4103)", style={'textAlign': 'center'})
inflow_fig = go.FigureWidget()
inflow_fig.add_bar(name='Inflow', x=df_inflow['Bulan'], y=df_inflow['Data'])
inflow_fig.layout.title = 'Inflow'

outflow_fig = go.FigureWidget()
outflow_fig.add_scatter(name='Outflow', x=df_outflow['Bulan'], y=df_outflow['Data'])
outflow_fig.layout.title = 'Outflow'

simulation_fig = go.FigureWidget()



# simulation_fig.add_scatter(name='Outflow', x=df_outflow['Bulan'], y=df_outflow['Data'])
simulation_fig.layout.title = 'Simulation'


#layout aplikasi
app.layout = html.Div(
    [
        dbc.Row([header, subtitle]),
        dbc.Row(
            [
                dbc.Col([dcc.Graph(figure=inflow_fig)]), 
                dbc.Col([dcc.Graph(figure=outflow_fig)])
            ]
            ),
         
        
        html.Div(
            [
                html.Button('Run', id='run-button', n_clicks=0)
            ],
            style = {'textAlign': 'center'}
        ), 
        html.Div(id='output-container-button', children='Klik run untuk menjalankan simulasi.', style = {'textAlign': 'center'}),
        dbc.Row(
            [
                dbc.Col([dcc.Graph(id='simulation-result', figure=simulation_fig)])
            ]
        )
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
        inout = df_inflow["Data"].values - df_outflow["Data"].values
        N = len(inout)
        u = np.zeros(N)
       # u0 = 100
        u[0] = 2000
        dt = 1

        #metode Euler
        for n in range(N-1):
            u[n + 1] = u[n] + dt*inout[n]
        #program numerik ---end----


        # the figure/plot created using the data filtered above 
        simulation_fig = go.FigureWidget()
        simulation_fig.add_scatter(name='Simulation', x=df_outflow['Bulan'], y=u)
        simulation_fig.layout.title = 'Simulation'

        return simulation_fig
    else:
        simulation_fig = go.FigureWidget()
        simulation_fig.layout.title = 'Simulation'

        return simulation_fig

    


#jalankan aplikasi
app.run_server(debug=True)
