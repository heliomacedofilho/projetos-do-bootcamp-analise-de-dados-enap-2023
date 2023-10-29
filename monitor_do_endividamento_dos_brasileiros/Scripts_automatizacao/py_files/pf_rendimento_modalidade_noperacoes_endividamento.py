#!/usr/bin/env python
# coding: utf-8

# In[2]:


import zipfile
import os
import pandas as pd
import deflatebr as dbr


# In[3]:


def concatenar_csvs(diretorio):
    frames = []

    for arquivo in os.listdir(diretorio):
        if arquivo.endswith('.csv'):
            caminho_arquivo = os.path.join(diretorio, arquivo)
            
            df = pd.read_csv(caminho_arquivo, encoding='utf-8', delimiter=";", decimal=",")
            df = df.rename(columns={df.columns[0]: "data_base"})
            df['data_base'] = pd.to_datetime(df['data_base'], format="%Y-%m-%d")
            df = df[df['cliente'] == 'PF']
            df['modalidade'] = df['modalidade'].str.replace("PF - ", "")
            df['porte'] = df['porte'].str.replace(' ','')
            df['porte'] = df['porte'].str.replace("PF-", "")
            #Filtros:
            df = df[df['cliente'] == 'PF']
            df = df[['a_vencer_de_1081_ate_1800_dias','data_base', 'modalidade', 'porte', 'numero_de_operacoes', 'a_vencer_de_361_ate_1080_dias', 'a_vencer_de_1801_ate_5400_dias', 'a_vencer_acima_de_5400_dias']]
            df['numero_de_operacoes'] = df['numero_de_operacoes'].astype(str)
            df = df[df['numero_de_operacoes'] != '<= 15']
            df['numero_de_operacoes'] = df['numero_de_operacoes'].astype(float)
            df['longo_prazo'] = df['a_vencer_de_361_ate_1080_dias'] + df['a_vencer_de_1081_ate_1800_dias'] + df['a_vencer_de_1801_ate_5400_dias'] + df['a_vencer_acima_de_5400_dias']
            df = df.drop(columns = ['a_vencer_de_361_ate_1080_dias', 'a_vencer_de_1081_ate_1800_dias', 'a_vencer_de_1801_ate_5400_dias', 'a_vencer_acima_de_5400_dias'], axis = 1)
            df = df.groupby(['data_base','porte', 'modalidade'])[['longo_prazo', 'numero_de_operacoes']].sum().reset_index()

            frames.append(df)

    df_concatenado = pd.concat(frames, ignore_index=True)

    return df_concatenado


# In[4]:


anos = list(range(2012, 2024))
dataframes = []

for ano in anos:
    diretorio = f"planilha_{ano}"
    dataframe_ano = concatenar_csvs(diretorio)
    dataframes.append(dataframe_ano)

df_total = pd.concat(dataframes, ignore_index=False)


# In[5]:


portes = {
    'Acimade20saláriosmínimos': 'Acima de 20 salários mínimos',
    'Até1saláriomínimo': 'Até 1 salário mínimo',
    'Indisponível': 'Indisponível',
    'Maisde10a20saláriosmínimos': 'Mais de 10 a 20 salários mínimos',
    'Maisde1a2saláriosmínimos': 'Mais de 1 a 2 salários mínimos',
    'Maisde2a3saláriosmínimos': 'Mais de 2 a 3 salários mínimos',
    'Maisde3a5saláriosmínimos': 'Mais de 3 a 5 salários mínimos',
    'Maisde5a10saláriosmínimos': 'Mais de 5 a 10 salários mínimos',
    'Semrendimento': 'Sem rendimento'
}

for porte_sem_espaco, porte_com_espaco in portes.items():
    df_total['porte'] = df_total['porte'].str.replace(porte_sem_espaco, porte_com_espaco)


# In[6]:


df_total['longo_prazo_deflacionado'] = dbr.deflate(nominal_values=df_total['longo_prazo'], nominal_dates=df_total['data_base'], real_date='2023-01',
           index='ipca')


# In[9]:


df_total["data_base"] = pd.to_datetime(df_total["data_base"], format='%Y-%m-%d')


# In[17]:


df_total = df_total.sort_values(by='data_base')


# In[19]:


df_total.to_csv("pf_rendimento_modalidade_noperacoes_endividamento.csv")


# # In[10]:


# import dash
# from dash import Dash, dcc, html, Input, Output
# import plotly.express as px


# # In[18]:


# import pandas as pd
# import plotly.express as px
# from dash import Dash, dcc, html, Input, Output

# # Inicializando o aplicativo Dash
# app = Dash(__name__)

# # Layout do aplicativo
# app.layout = html.Div([
#     dcc.Dropdown(
#         id='porte-dropdown',
#         options=[{'label': porte, 'value': porte} for porte in df_total['porte'].unique()],
#         value=df_total['porte'].unique()[0]
#     ),
#     dcc.Graph(id='line-chart')
# ])

# # Callback para atualizar o gráfico com base na seleção do dropdown
# @app.callback(
#     Output('line-chart', 'figure'),
#     [Input('porte-dropdown', 'value')]
# )
# def update_graph(selected_porte):
#     filtered_df = df_total[df_total['porte'] == selected_porte]
    
#     fig = px.line(filtered_df, 
#                   x='data_base', 
#                   y='longo_prazo_deflacionado', 
#                   color='modalidade')
    
#     fig.update_layout(
#         title_text='Endividamento de Longo Prazo por Modalidade',
#         xaxis_title='Data',
#         yaxis_title='Endividamento de Longo Prazo Deflacionado',
#         template="seaborn",
#         legend=dict(
#             x=0.5,
#             y=-0.3,
#             orientation='h',
#             xanchor='center'
#         ),
#         xaxis=dict(showgrid=False),
#         yaxis=dict(showgrid=False)
#     )
#     return fig

# # Executando o aplicativo
# if __name__ == '__main__':
#     app.run_server(debug=True)


# # In[20]:


# import pandas as pd
# import plotly.express as px
# from dash import Dash, dcc, html, Input, Output

# # Inicializando o aplicativo Dash
# app = Dash(__name__)

# # Layout do aplicativo
# app.layout = html.Div([
#     dcc.Dropdown(
#         id='porte-dropdown',
#         options=[{'label': porte, 'value': porte} for porte in df_total['porte'].unique()],
#         value=df_total['porte'].unique()[0]
#     ),
#     dcc.Graph(id='line-chart')
# ])

# # Callback para atualizar o gráfico com base na seleção do dropdown
# @app.callback(
#     Output('line-chart', 'figure'),
#     [Input('porte-dropdown', 'value')]
# )
# def update_graph(selected_porte):
#     filtered_df = df_total[df_total['porte'] == selected_porte]
    
#     fig = px.line(filtered_df, 
#                   x='data_base', 
#                   y='numero_de_operacoes', 
#                   color='modalidade')
    
#     fig.update_layout(
#         title_text='Endividamento de Longo Prazo por Modalidade',
#         xaxis_title='Data',
#         yaxis_title='Endividamento de Longo Prazo Deflacionado',
#         template="seaborn",
#         legend=dict(
#             x=0.5,
#             y=-0.3,
#             orientation='h',
#             xanchor='center'
#         ),
#         xaxis=dict(showgrid=False),
#         yaxis=dict(showgrid=False)
#     )
#     return fig

# # Executando o aplicativo
# if __name__ == '__main__':
#     app.run_server(debug=True)

