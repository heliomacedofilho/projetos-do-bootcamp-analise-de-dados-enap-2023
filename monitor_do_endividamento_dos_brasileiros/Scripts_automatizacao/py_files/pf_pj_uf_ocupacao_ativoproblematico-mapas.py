#!/usr/bin/env python
# coding: utf-8

# In[1]:


import zipfile
import os
import pandas as pd
import deflatebr as dbr
import json
import requests
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import sidrapy


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
            df = df[df['mes'] == 12]
            df = df[['ano', 'cliente', 'uf', 'ocupacao', 'cnae_secao', 'ativo_problematico']]
            #df.loc[df['ocupacao'] == '-', 'ocupacao'] = df['cnae_secao'] #Adiciona o valor da coluna cnae_secao quando a coluna ocupacao é "-"
            df = df.groupby(['ano','cliente','uf', 'ocupacao', 'cnae_secao'])['ativo_problematico'].sum().reset_index()
            
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


populacao_estados = sidrapy.get_table(table_code='4709',
                         territorial_level="3",
                         ibge_territorial_code="all",
                         variable='93') 


# In[5]:


populacao_estados = populacao_estados.drop(columns = ["NC", "NN", "MC", "MN","D1C","D2C","D2N","D3C"])


# In[6]:


populacao_estados.columns = populacao_estados.iloc[0]

# In[9]:


uf_to_state = {
    'AC': 'Acre',
    'AL': 'Alagoas',
    'AP': 'Amapá',
    'AM': 'Amazonas',
    'BA': 'Bahia',
    'CE': 'Ceará',
    'DF': 'Distrito Federal',
    'ES': 'Espírito Santo',
    'GO': 'Goiás',
    'MA': 'Maranhão',
    'MT': 'Mato Grosso',
    'MS': 'Mato Grosso do Sul',
    'MG': 'Minas Gerais',
    'PA': 'Pará',
    'PB': 'Paraíba',
    'PR': 'Paraná',
    'PE': 'Pernambuco',
    'PI': 'Piauí',
    'RJ': 'Rio de Janeiro',
    'RN': 'Rio Grande do Norte',
    'RS': 'Rio Grande do Sul',
    'RO': 'Rondônia',
    'RR': 'Roraima',
    'SC': 'Santa Catarina',
    'SP': 'São Paulo',
    'SE': 'Sergipe',
    'TO': 'Tocantins'
}


# In[10]:


df_uf_to_state = pd.DataFrame(list(uf_to_state.items()), columns=['uf', 'Estado'])


# In[12]:


df_total = pd.merge(df_total,
                    df_uf_to_state)



# In[15]:


df_total = pd.merge(df_total,
                    populacao_estados,
                   right_on = "Unidade da Federação",
                   left_on = "Estado",
                   how = "inner")



# In[17]:


df_total['Estado'] = df_total['uf'].map(uf_to_state)
df_total['Estado'] = df_total['Estado'].str.upper() 


# In[18]:


df_total['data'] = pd.to_datetime(df_total['ano'], format="%Y")


# In[19]:


df_total['ativo_problematico_deflacionado'] = dbr.deflate(nominal_values=df_total['ativo_problematico'], nominal_dates=df_total['data'], real_date='2022-12')


# In[21]:


df_ocupacao_pf_ativoproblematico = df_total[df_total['cliente'] == "PF"]


# In[23]:


url = "https://raw.githubusercontent.com/jonates/opendata/master/arquivos_geoespaciais/unidades_da_federacao.json" #Temos que dar os créditos
response = requests.get(url)
geojson_data = response.json()


# In[25]:


df_ocupacao_pf_ativoproblematico = df_ocupacao_pf_ativoproblematico.drop(columns = ['cliente', 'uf', 'cnae_secao', 'ativo_problematico', 'Ano',
                                                 'data','Unidade da Federação'])


# In[26]:


df_ocupacao_pf_ativoproblematico['Valor'] = df_ocupacao_pf_ativoproblematico['Valor'].astype(float)


# In[27]:


df_ocupacao_pf_ativoproblematico['ativo_problematico/pop'] = df_ocupacao_pf_ativoproblematico['ativo_problematico_deflacionado'] / df_ocupacao_pf_ativoproblematico['Valor']


# In[28]:


df_ocupacao_pf_ativoproblematico['ocupacao']=df_ocupacao_pf_ativoproblematico['ocupacao'].str.replace('PF - ','')


# In[36]:


df_ocupacao_pf_ativoproblematico.to_csv("df_ocupacao_pf_ativoproblematico.csv")


# In[35]:


# app = Dash(__name__)

# app.layout = html.Div([
#     html.H1('Análise do Ativo Problemático'),
    
#     html.Div([
#         html.Label('Selecione uma ocupação:'),
#         dcc.Dropdown(
#             id='ocupacao-dropdown',
#             options=[{'label': i, 'value': i} for i in df_ocupacao_pf_ativoproblematico['ocupacao'].unique()],
#             value=df_ocupacao_pf_ativoproblematico['ocupacao'].iloc[0]
#         ),
#     ]),
    
#     dcc.Graph(id='choropleth-map')
# ])

# @app.callback(
#     Output('choropleth-map', 'figure'),
#     [Input('ocupacao-dropdown', 'value')]
# )
# def update_choropleth(ocupacao_value):
    
#     filtered_df = df_ocupacao_pf_ativoproblematico[df_ocupacao_pf_ativoproblematico['ocupacao'] == ocupacao_value]
    
#     fig = px.choropleth_mapbox(filtered_df, 
#                                geojson=geojson_data, 
#                                locations='Estado', 
#                                color='ativo_problematico/pop',
#                                color_continuous_scale="sunsetdark",
#                                range_color=(0, max(filtered_df['ativo_problematico/pop'])),
#                                animation_frame='ano', 
#                                mapbox_style="open-street-map",
#                                zoom=3, 
#                                center={"lat": -17.14, "lon": -57.33},
#                                opacity=1,
#                                labels={'ativo_problematico/pop':'Carteira Ativa',
#                                        'uf': 'Unidade da Federação do Brasil'},
#                                featureidkey="properties.NM_ESTADO")
    
#     fig.update_layout(margin={'r':0,'t':0,'l':0, 'b':0})
    
#     return fig

# if __name__ == '__main__':
#     app.run_server(debug=True)


# In[37]:


df_cnae_pj_ativoproblematico = df_total[df_total['cliente'] == "PJ"]


# In[40]:


df_cnae_pj_ativoproblematico = df_cnae_pj_ativoproblematico.drop(columns = ['cliente', 'uf', 'ocupacao', 'ativo_problematico', 'Unidade da Federação', 'Ano',
                                                 'data'])

# In[42]:


df_cnae_pj_ativoproblematico['Valor'] = df_cnae_pj_ativoproblematico['Valor'].astype(float)


# In[43]:


df_cnae_pj_ativoproblematico['ativo_problematico/pop'] = df_cnae_pj_ativoproblematico['ativo_problematico_deflacionado'] / df_cnae_pj_ativoproblematico['Valor']


# In[44]:


df_cnae_pj_ativoproblematico['cnae_secao']=df_cnae_pj_ativoproblematico['cnae_secao'].str.replace('PJ - ','')


# In[46]:


df_cnae_pj_ativoproblematico.to_csv("df_cnae_pj_ativoproblematico.csv")


# In[ ]:


# app = Dash(__name__)

# app.layout = html.Div([
#     html.H1('Análise do Ativo Problemático'),
    
#     html.Div([
#         html.Label('Selecione um setor de atuação:'),
#         dcc.Dropdown(
#             id='cnae-dropdown',
#             options=[{'label': i, 'value': i} for i in df_cnae_pj_ativoproblematico['cnae_secao'].unique()],
#             value=df_cnae_pj_ativoproblematico['cnae_secao'].iloc[0]
#         ),
#     ]),
    
#     dcc.Graph(id='choropleth-map')
# ])

# @app.callback(
#     Output('choropleth-map', 'figure'),
#     [Input('cnae-dropdown', 'value')]
# )
# def update_choropleth(cnae_value):
    
#     filtered_df = df_cnae_pj_ativoproblematico[df_cnae_pj_ativoproblematico['cnae_secao'] == cnae_value]
    
#     fig = px.choropleth_mapbox(filtered_df, 
#                                geojson=geojson_data, 
#                                locations='Estado', 
#                                color='ativo_problematico/pop',
#                                color_continuous_scale="sunsetdark",
#                                range_color=(0, max(filtered_df['ativo_problematico/pop'])),
#                                animation_frame='ano', 
#                                mapbox_style="open-street-map",
#                                zoom=3, 
#                                center={"lat": -17.14, "lon": -57.33},
#                                opacity=1,
#                                labels={'ativo_problematico/pop':'Carteira Ativa',
#                                        'uf': 'Unidade da Federação do Brasil'},
#                                featureidkey="properties.NM_ESTADO")
    
#     fig.update_layout(margin={'r':0,'t':0,'l':0, 'b':0})
    
#     return fig

# if __name__ == '__main__':
#     app.run_server(debug=True)

