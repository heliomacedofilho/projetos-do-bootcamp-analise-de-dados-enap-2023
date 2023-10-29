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
            df['porte'] = df['porte'].str.replace(' ','')
            df = df[['data_base', 'porte', 'a_vencer_de_361_ate_1080_dias', 'a_vencer_de_1081_ate_1800_dias', 'a_vencer_de_1801_ate_5400_dias', 'a_vencer_acima_de_5400_dias']]
            #Nova coluna para endividamento de curto prazo
            df['longo_prazo'] = df['a_vencer_de_361_ate_1080_dias'] + df['a_vencer_de_1081_ate_1800_dias'] + df['a_vencer_de_1801_ate_5400_dias'] + df['a_vencer_acima_de_5400_dias']
            df = df.drop(columns = ['a_vencer_de_361_ate_1080_dias', 'a_vencer_de_1081_ate_1800_dias', 'a_vencer_de_1801_ate_5400_dias', 'a_vencer_acima_de_5400_dias'], axis = 1)
            df['data_base'] = df['data_base'].dt.strftime('%Y-%m')
            #Agrupamentos para análise
            df = df.groupby(['data_base','porte'])['longo_prazo'].sum().reset_index()
            
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


df_total['longo_prazo_deflacionado'] = dbr.deflate(nominal_values=df_total['longo_prazo'], nominal_dates=df_total['data_base'], real_date='2022-01')

# In[8]:


url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.24369/dados?formato=json'

taxa_desocupacao = requests.get(url).json() 


# In[9]:


desocupacao_df = pd.DataFrame(taxa_desocupacao)


# In[10]:


desocupacao_df['data'] = pd.to_datetime(desocupacao_df['data'], format = "%d/%m/%Y")


# In[11]:


desocupacao_df['data'] = desocupacao_df['data'].dt.strftime('%Y-%m')

# In[13]:


df_desemprego_divida = pd.merge(desocupacao_df,
                              df_total,
                              left_on="data",
                              right_on="data_base",
                              how = "inner")


# In[14]:


df_desemprego_divida = df_desemprego_divida.drop(columns = ['data_base', 'longo_prazo'])


# In[17]:


# fig = go.Figure()

# for porte in df_desemprego_divida['porte'].unique():
#     subset = df_desemprego_divida[df_desemprego_divida['porte'] == porte]
#     fig.add_trace(go.Scatter(x=subset['data'],
#                              y=subset['longo_prazo_deflacionado'],
#                              mode='lines',
#                              name=f'{porte}'))

# # Adicionando a coluna 'valor' ao segundo eixo y
# fig.add_trace(go.Scatter(x=df_desemprego_divida['data'],
#                          y=df_desemprego_divida['valor'], 
#                          mode='lines',
#                          name='Taxa de desocupação',
#                          yaxis='y2'))

# fig.update_layout(yaxis2=dict(overlaying='y',
#                               side='right'))

# fig.show()


# In[19]:


def categoria_renda(dados_porte):
    if dados_porte in ['PF-Acimade20saláriosmínimos', 'PF-Mais de 10a20saláriosmínimos', 'PF-Maisde5a10saláriosmínimos']:
        return 'alta renda'
    elif dados_porte == 'PF-Indisponível':
        return 'renda indisponível'
    elif dados_porte == 'PF-Maisde3a5saláriosmínimos':
        return 'renda média'
    else:
        return 'baixa renda'

df_desemprego_divida['categoria_renda'] = df_desemprego_divida['porte'].apply(categoria_renda)


# In[21]:


df_desemprego_divida_grupo = df_desemprego_divida.groupby(['data','categoria_renda'])['longo_prazo_deflacionado'].sum().reset_index()


# In[23]:


df_desemprego_divida_grupo = pd.merge(df_desemprego_divida_grupo,
                              desocupacao_df,
                              how = "inner")


# In[27]:


# fig = go.Figure()

# for categoria_renda in df_desemprego_divida_grupo['categoria_renda'].unique():
#     subset = df_desemprego_divida_grupo[df_desemprego_divida_grupo['categoria_renda'] == categoria_renda]
#     fig.add_trace(go.Scatter(x=subset['data'],
#                              y=subset['longo_prazo_deflacionado'],
#                              mode='lines',
#                              name=f'{categoria_renda}',
#                              yaxis='y2',
#                              opacity=0.7))

# fig.add_trace(go.Scatter(x=df_desemprego_divida_grupo['data'],
#                          y=df_desemprego_divida_grupo['valor'], 
#                          mode='lines',
#                          name='taxa de desocupação',
#                          opacity=1,
#                         line=dict(color='dimgray', width=2, dash='dot')))

# fig.add_shape(
#     go.layout.Shape(
#         type="line",
#         x0="2017-07-01",
#         x1="2017-07-01",
#         y0=0,
#         y1=1,
#         yref='paper',
#         line=dict(color="black", width=2)
#     )
# )

# fig.add_annotation(
#     go.layout.Annotation(
#         text="Reforma Trabalhista",
#         x="2017-06-01",
#         y=0.45,
#         yref='paper',
#         showarrow=False,
#         font=dict(color="black", size=12),
#         textangle = 90
#     )
# )

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
#                            title = "Taxa de desocupação"))

# fig.show()


# In[29]:


df_desemprego_divida_grupo.to_csv("df_desemprego_divida_grupo.csv")

