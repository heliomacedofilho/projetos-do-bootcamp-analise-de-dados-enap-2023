#!/usr/bin/env python
# coding: utf-8

# In[1]:


import zipfile
import os
import pandas as pd
import plotly.express as px


# In[2]:


def concatenar_csvs(diretorio):
    frames = []

    for arquivo in os.listdir(diretorio):
        if arquivo.endswith('.csv'):
            caminho_arquivo = os.path.join(diretorio, arquivo)
            
            df = pd.read_csv(caminho_arquivo, encoding='utf-8', delimiter=";", decimal=",")
            df = df.rename(columns={df.columns[0]: "data_base"})
            df['data_base'] = pd.to_datetime(df['data_base'], format="%Y-%m-%d")
            df['mes'] = df['data_base'].dt.month #cria uma nova coluna com mês
            df['ano'] = df['data_base'].dt.year
            #Filtros:
            df = df[df['cliente'] == 'PF'] #trocar para o ano que você quer filtrar
            df['porte'] = df['porte'].str.replace(' ','')
#           filtro1 = df['porte'] == "PJ-Micro"
#           filtro2 = df['porte'] == "PJ-Pequeno"
#           df = df.loc[filtro1 | filtro2]
            df = df[['a_vencer_de_1081_ate_1800_dias','data_base', 'modalidade', 'porte', 'a_vencer_de_361_ate_1080_dias', 
  'a_vencer_de_1801_ate_5400_dias', 'a_vencer_acima_de_5400_dias']]
            #Nova coluna para endividamento de LONGO prazo
            df['longo_prazo'] = df['a_vencer_de_361_ate_1080_dias'] + df['a_vencer_de_1081_ate_1800_dias'] + df['a_vencer_de_1801_ate_5400_dias'] + df['a_vencer_acima_de_5400_dias']
            df = df.drop(columns = ['a_vencer_de_361_ate_1080_dias', 'a_vencer_de_1081_ate_1800_dias', 'a_vencer_de_1801_ate_5400_dias', 'a_vencer_acima_de_5400_dias'], axis = 1)
            df['data_base'] = df['data_base'].dt.strftime('%Y-%m')
            #Agrupamentos para análise
            df = df.groupby(['data_base','modalidade','porte'])['longo_prazo'].sum().reset_index()
            
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


# In[4]:


#converter coluna data_base para datetime
#df_total['data_base'] = pd.to_datetime(df_total['data_base'])


# In[5]:


df_total.head(5)


# criar coluna deflator

# In[7]:


#importar a biblioteca
import deflatebr as dbr
nominal_values = df_total['longo_prazo']
nominal_dates = df_total['data_base']
real_date = '2023-01'

#criar uma coluna com o valor deflacionado
df_total['valor_deflacionado'] = dbr.deflate(nominal_values=nominal_values, nominal_dates=nominal_dates, real_date=real_date)


# In[9]:


#agrupar o valor total das dívidas, somando os valores da coluna valor_deflacionado
df_total = df_total.groupby(['data_base','modalidade','porte'])['valor_deflacionado'].sum().reset_index()


# In[10]:


#formatar os valores float
pd.set_option('display.float_format', '{:.2f}'.format)


# In[16]:


df_total['data_base'] = pd.to_datetime(df_total['data_base'])


# In[17]:


#criar coluna ano
df_total['ano'] = df_total['data_base'].dt.year


# In[18]:


#criar coluna mês
df_total['mes'] = df_total['data_base'].dt.month


# In[19]:


df_total['data_divida'] = df_total['data_base'].dt.strftime('%Y-%m')


# *Agregando dados de Inflação no DataFrame*

# In[21]:


# Importando a série do IPCA mensal (a)
#importa a bibliotaca
import requests

#define a url a ser usada
url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json'
# fazendo a requisição à url e trazendo em formato json
inflacao_mensal = requests.get(url).json() 
#response é o nome da 'variável'. Pode ser qualquer outro nome


# In[22]:


inflacao_df = pd.DataFrame(inflacao_mensal)


# In[23]:


inflacao_df['data'] = pd.to_datetime(inflacao_df['data'], format = "%d/%m/%Y")


# In[24]:


inflacao_df['data'] = inflacao_df['data'].dt.strftime('%Y-%m')

# In[26]:


df_inflacao_divida = pd.merge(inflacao_df,
                              df_total,
                              left_on="data",
                              right_on="data_divida",
                              how = "inner")


# In[27]:


df_inflacao_divida = df_inflacao_divida.drop(columns=['data'])


# In[28]:


df_inflacao_divida = df_inflacao_divida.rename(columns={'valor': 'inflacao'})


# In[30]:


df_inflacao_dezembro = df_inflacao_divida[df_inflacao_divida['mes'] == 12]


# In[26]:


# fig = px.bar(df_inflacao_dezembro, 
#              x='ano', 
#              y='valor_deflacionado',
#              color='porte',
#              barmode = 'group',
#              animation_frame = 'modalidade') 

# fig.update_layout(title_text='Endividamento de longo prazo PF - porte x modalidade',
#                   xaxis_title='ano',
#                   yaxis_title='endividamento',
#                   height=800,
#                   width=900)
                  

# fig.show()


# In[31]:


df_inflacao_divida['porte'] = df_inflacao_divida['porte'].str.replace('PF-','')
df_inflacao_divida['modalidade'] = df_inflacao_divida['modalidade'].str.replace('PF - ','')


# In[32]:


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
    df_inflacao_divida['porte'] = df_inflacao_divida['porte'].str.replace(porte_sem_espaco, porte_com_espaco)


# In[36]:


pf_porte_endividamentolp = df_inflacao_divida.drop(columns = ["inflacao", "ano", "mes", "data_divida"])       


# In[35]:


# app = dash.Dash(__name__)

# app.layout = html.Div([
#     dcc.Dropdown(
#         id='porte-dropdown',
#         options=[{'label': porte, 'value': porte} for porte in pf_porte_endividamentolp['porte'].unique()],
#         value=pf_porte_endividamentolp['porte'].unique()[0]
#     ),
#     dcc.Graph(id='line-chart')
# ])

# @app.callback(
#     Output('line-chart', 'figure'),
#     [Input('porte-dropdown', 'value')]
# )
# def update_graph(selected_porte):
#     filtered_df = pf_porte_endividamentolp[pf_porte_endividamentolp['porte'] == selected_porte]
    
#     fig = px.line(filtered_df, 
#                   x='data_base', 
#                   y='valor_deflacionado', 
#                   color='modalidade')
    
#     fig.update_layout(
#         title_text='Endividamento de longo prazo PF - porte x modalidade',
#         xaxis_title='ano',
#         yaxis_title='Valor Dívida',
#         template="seaborn",
#         legend=dict(
#             x=0.5,
#             y=-0.3,
#             orientation='h',
#             xanchor='center'
#         ),
#         xaxis=dict(showgrid=False),
#         yaxis=dict(showgrid=False),
#         height=800,
#         width=600
#     )
#     return fig

# if __name__ == '__main__':
#     app.run_server(debug=True)

# In[39]:


df_inflaco_porte_agrupado = df_inflacao_divida.groupby(['data_divida', 'porte'])['valor_deflacionado'].sum().reset_index()


# In[41]:


df_inflaco_porte_agrupado = pd.merge(inflacao_df,
                              df_inflaco_porte_agrupado,
                              left_on="data",
                              right_on="data_divida",
                              how = "inner")


# In[42]:


df_inflaco_porte_agrupado['valor'] = df_inflaco_porte_agrupado['valor'].astype('float')


# In[43]:


df_inflaco_porte_agrupado['porte'] = df_inflaco_porte_agrupado['porte'].str.replace('PF-','')

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
    df_inflaco_porte_agrupado['porte'] = df_inflaco_porte_agrupado['porte'].str.replace(porte_sem_espaco, porte_com_espaco)


# In[45]:


df_inflaco_porte_agrupado.to_csv("pf_porte_endividamentolp_inflacao.csv")


# In[44]:


# import plotly.graph_objects as go

# fig = go.Figure()

# for porte in df_inflaco_porte_agrupado['porte'].unique():
#     subset = df_inflaco_porte_agrupado[df_inflaco_porte_agrupado['porte'] == porte]
    
#     fig.add_trace(go.Scatter(
#         x=subset['data_divida'],
#         y=subset['valor_deflacionado'],
#         mode='lines',
#         opacity=0.7,
#         name=f'{porte}',
#         yaxis='y2'
#     ))

# fig.add_trace(go.Scatter(
#     x=df_inflaco_porte_agrupado['data_divida'],
#     y=df_inflaco_porte_agrupado['valor'],
#     opacity=1,
#     line=dict(color='dimgray', width=2, dash='dot'),
#     mode='lines',
#     name='IPCA'
# ))

# fig.update_layout(
#     yaxis=dict(
#         title="IPCA",
#         showgrid=False
#     ),
#     yaxis2=dict(
#         title="Endividamento de longo prazo",
#         overlaying='y',
#         side='right',
#         showgrid=False
#     ),
#     xaxis=dict(
#         showgrid=False
#     ),
#     legend=dict(
#         y=-0.2,
#         traceorder='normal',
#         orientation='h',
#         font=dict(size=12)
#     ),
#     template="seaborn"
# )

# fig.show()

