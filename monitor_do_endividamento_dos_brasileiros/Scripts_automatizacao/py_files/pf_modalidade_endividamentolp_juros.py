#!/usr/bin/env python
# coding: utf-8

# In[1]:


import zipfile
import os
import pandas as pd
import requests
import deflatebr as dbr
import plotly.graph_objects as go


# In[2]:


def concatenar_csvs(diretorio):
    frames = []

    for arquivo in os.listdir(diretorio):
        if arquivo.endswith('.csv'):
            caminho_arquivo = os.path.join(diretorio, arquivo)
            
            df = pd.read_csv(caminho_arquivo, encoding='utf-8', delimiter=";", decimal=",")
            df = df.rename(columns={df.columns[0]: "data_base"})
            df['data_base'] = pd.to_datetime(df['data_base'], format="%Y-%m-%d")
            df = df[df['cliente'] == "PF"]
            df = df[['data_base', 'modalidade', 'a_vencer_de_361_ate_1080_dias', 'a_vencer_de_1081_ate_1800_dias', 'a_vencer_de_1801_ate_5400_dias', 'a_vencer_acima_de_5400_dias']]
            df['modalidade']=df['modalidade'].str.replace('PF - ','')
            #Nova coluna para endividamento de longo prazo
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


# In[8]:


url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.25435/dados?formato=json' #Taxa média mensal de juros - Pessoas físicas - Total

tx_juros = requests.get(url).json() 


# In[9]:


juros_df = pd.DataFrame(tx_juros)


# In[10]:


juros_df['data'] = pd.to_datetime(juros_df['data'], format = "%d/%m/%Y")


# In[11]:


juros_df['data'] = juros_df['data'].dt.strftime('%Y-%m')


# In[13]:


df_juros_divida = pd.merge(juros_df,
                              df_total,
                              left_on="data",
                              right_on="data_base",
                              how = "inner")


# In[14]:


df_juros_divida = df_juros_divida.drop(columns = ['data_base', 'longo_prazo'])


# In[16]:


# fig = go.Figure()

# for modalidade in df_juros_divida['modalidade'].unique():
#     subset = df_juros_divida[df_juros_divida['modalidade'] == modalidade]
#     fig.add_trace(go.Scatter(x=subset['data'],
#                              y=subset['longo_prazo_deflacionado'],
#                              mode='lines',
#                              name=f'{modalidade}'))

# # Adicionando a coluna 'valor' ao segundo eixo y
# fig.add_trace(go.Scatter(x=df_juros_divida['data'],
#                          y=df_juros_divida['valor'], 
#                          mode='lines',
#                          name='taxa de juros média PF',
#                          yaxis='y2', opacity=1,
#                         line=dict(color='dimgray', width=2, dash='dot')))

# fig.update_layout(yaxis2=dict(overlaying='y',
#                               side='right',
#                              showgrid=False,
#                              title = "Endividamento de longo prazo"),
#                  template="seaborn",
#                   legend=dict(x = 0.5,
#                               y = -0.3,
#                               orientation='h',
#                               xanchor='center'),
#                  xaxis=dict(showgrid=False),
#                  yaxis=dict(showgrid=False,
#                            title = "Taxa de juros média PF"))

# fig.show()


# In[17]:


df_juros_divida.to_csv("df_juros_divida_modalidade.csv")