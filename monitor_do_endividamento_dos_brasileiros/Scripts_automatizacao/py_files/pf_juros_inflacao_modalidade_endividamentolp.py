#!/usr/bin/env python
# coding: utf-8

# In[36]:


import zipfile
import os
import pandas as pd
import deflatebr as dbr
import requests
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


# In[2]:


def concatenar_csvs(diretorio):
    frames = []

    for arquivo in os.listdir(diretorio):
        if arquivo.endswith('.csv'):
            caminho_arquivo = os.path.join(diretorio, arquivo)
            
            df = pd.read_csv(caminho_arquivo, encoding='utf-8', delimiter=";", decimal=",")
            df = df.rename(columns={df.columns[0]: "data_base"})
            df['data_base'] = pd.to_datetime(df['data_base'], format="%Y-%m-%d")
            #Filtros:
            df = df[df['cliente'] == 'PF']
            df['modalidade'] = df['modalidade'].str.replace('PF - ','')
            df = df[['data_base', 'modalidade', 'a_vencer_de_361_ate_1080_dias', 'a_vencer_de_1081_ate_1800_dias', 'a_vencer_de_1801_ate_5400_dias', 'a_vencer_acima_de_5400_dias']]
            df['longo_prazo'] = df['a_vencer_de_361_ate_1080_dias'] + df['a_vencer_de_1081_ate_1800_dias'] + df['a_vencer_de_1801_ate_5400_dias'] + df['a_vencer_acima_de_5400_dias']
            df = df.drop(columns = ['a_vencer_de_361_ate_1080_dias', 'a_vencer_de_1081_ate_1800_dias', 'a_vencer_de_1801_ate_5400_dias', 'a_vencer_acima_de_5400_dias'], axis = 1)
            df['data_base'] = df['data_base'].dt.strftime('%Y-%m')
            #Agrupamentos para análise
            df = df.groupby(['data_base','modalidade'])['longo_prazo'].sum().reset_index()
            
            frames.append(df)

    df_concatenado = pd.concat(frames, ignore_index=True)

    return df_concatenado


# In[3]:


anos = list(range(2012, 2024))
dataframes = []

for ano in anos:
    diretorio = f"planilha_{ano}"
    dataframe_ano = concatenar_csvs(diretorio)
    dataframes.append(dataframe_ano)

df_total = pd.concat(dataframes, ignore_index=False)


# In[6]:


df_total['longo_prazo_deflacionado'] = dbr.deflate(nominal_values=df_total['longo_prazo'], nominal_dates=df_total['data_base'], real_date='2023-01')


# In[62]:


url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.25435/dados?formato=json' #Taxa média mensal de juros - Pessoas físicas - Total
tx_juros = requests.get(url).json()
juros_df = pd.DataFrame(tx_juros)
juros_df['data'] = pd.to_datetime(juros_df['data'], format = "%d/%m/%Y")
juros_df['data'] = juros_df['data'].dt.strftime('%Y-%m')
juros_df = juros_df.rename(columns={'data': 'data_base', 'valor': 'Taxa média mensal de juros - PF'})


# In[63]:


url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json'
inflacao_mensal = requests.get(url).json() 
inflacao_mensal = pd.DataFrame(inflacao_mensal)
inflacao_mensal['data'] = pd.to_datetime(inflacao_mensal['data'], format = "%d/%m/%Y")
inflacao_mensal['data'] = inflacao_mensal['data'].dt.strftime('%Y-%m')
inflacao_mensal = inflacao_mensal.rename(columns={'data': 'data_base', 'valor': 'IPCA'})


# In[64]:


df_modalidade_endividamentolp = pd.merge(inflacao_mensal, juros_df)


# In[65]:


df_modalidade_endividamentolp = pd.merge(df_modalidade_endividamentolp, df_total)


# In[66]:


df_modalidade_endividamentolp['IPCA'] = df_modalidade_endividamentolp['IPCA'].astype("float")
df_modalidade_endividamentolp['Taxa média mensal de juros - PF'] = df_modalidade_endividamentolp['Taxa média mensal de juros - PF'].astype("float")


# In[67]:


df_modalidade_endividamentolp.to_csv("df_juros_inflacao_modalidade.csv")


# In[68]:


#df_modalidade_endividamentolp.info()


# In[69]:


# app = dash.Dash(__name__)

# app.layout = html.Div([
#     dcc.Dropdown(
#         id='yaxis-column',
#         options=[
#             {'label': 'Índice de preços ao consumidor (IPCA)', 'value': 'IPCA'},
#             {'label': 'Taxa média mensal de juros - PF', 'value': 'Taxa média mensal de juros - PF'}
#         ],
#         value='IPCA'
#     ),
#     dcc.Graph(id='graph-output')
# ])

# @app.callback(
#     Output('graph-output', 'figure'),
#     [Input('yaxis-column', 'value')]
# )
# def update_graph(yaxis_column_name):
#     fig = go.Figure()

#     # Adicionando linhas da modalidade ao eixo y2
#     for modalidade in df_modalidade_endividamentolp['modalidade'].unique():
#         subset = df_modalidade_endividamentolp[df_modalidade_endividamentolp['modalidade'] == modalidade]
#         fig.add_trace(go.Scatter(x=subset['data_base'],
#                                  y=subset['longo_prazo_deflacionado'],
#                                  mode='lines',
#                                  name=f'{modalidade}',
#                                  yaxis='y2',
#                                  line=dict(width=2)))

#     # Adicionando a coluna selecionada ao eixo y principal
#     fig.add_trace(go.Scatter(x=df_modalidade_endividamentolp['data_base'],
#                              y=df_modalidade_endividamentolp[yaxis_column_name],
#                              mode='lines',
#                              name=yaxis_column_name,
#                              line=dict(width=2)))

#     fig.update_layout(
#         yaxis2=dict(
#             overlaying='y',
#             side='right',
#             showgrid=False,
#             title="Endividamento de longo prazo"
#         ),
#         template="seaborn",
#         legend=dict(
#             x=0.5,
#             y=-0.3,
#             orientation='h',
#             xanchor='center'
#         ),
#         xaxis=dict(showgrid=False),
#         yaxis=dict(
#             showgrid=False,
#             title=yaxis_column_name
#         ),
#         height=600,
#         width=700,
#     )

#     return fig

# if __name__ == '__main__':
#     app.run_server(debug=True)

