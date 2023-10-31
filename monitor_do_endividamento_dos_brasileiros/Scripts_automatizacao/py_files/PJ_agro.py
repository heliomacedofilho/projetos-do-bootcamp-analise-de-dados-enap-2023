#!/usr/bin/env python
# coding: utf-8

# In[7]:


import zipfile
import os
import pandas as pd
import deflatebr as dbr
import plotly.express as px
import numpy as np

# In[2]:


def concatenar_csvs(diretorio):
    frames = []

    for arquivo in os.listdir(diretorio):
        if arquivo.endswith('.csv'):
            caminho_arquivo = os.path.join(diretorio, arquivo)
            
            df = pd.read_csv(caminho_arquivo, encoding='utf-8', delimiter=";", decimal=",")
            df = df.rename(columns={df.columns[0]: "data_base"})
            df = df.rename(columns={df.columns[6]: "cnae_secao"})
            df = df.rename(columns={df.columns[7]: "cnae_subclasse"})
            df['data_base'] = pd.to_datetime(df['data_base'], format="%Y-%m-%d")
            df['mes'] = df['data_base'].dt.month #cria uma nova coluna com mês
            df['ano'] = df['data_base'].dt.year
            #Filtros:
            df = df[df['mes'] == 12] #trocar para o ano que você quer filtrar
            df = df[df['cliente'] == 'PJ']
            df = df[df['cnae_secao'] == "PJ - Agricultura, pecuária, produção florestal, pesca e aqüicultura"]
            df = df[['data_base', 'cnae_secao', 'cnae_subclasse','carteira_ativa']]
            df['data_base'] = df['data_base'].dt.strftime('%Y-%m')
            #Agrupamentos para análise
            df = df.groupby(['data_base', 'cnae_secao', 'cnae_subclasse'])['carteira_ativa'].sum().reset_index()
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


# In[8]:


df_total['valor_deflacionado'] = dbr.deflate(nominal_values=df_total['carteira_ativa'], nominal_dates=df_total['data_base'], real_date='2022-12')


# In[41]:


df_total_2022 = df_total[df_total['data_base'] == '2022-12']


# In[43]:


soma_valor_deflacionado = df_total_2022['valor_deflacionado'].sum()

df_total_2022['perc'] = df_total_2022['valor_deflacionado']/soma_valor_deflacionado * 100


# In[45]:


df_total_2022 = df_total_2022.sort_values(by='perc', ascending=False)
df_total_2022['cumperc'] = df_total_2022['perc'].cumsum()


# In[100]:


df_acumulado_corte = df_total_2022[df_total_2022['cumperc'] < 81]


# In[71]:


df_acumulado_corte['cnae_secao'] = df_acumulado_corte['cnae_secao'].str.replace("PJ - ", "")
df_acumulado_corte['cnae_subclasse'] = df_acumulado_corte['cnae_subclasse'].str.replace("PJ - ", "")
df_acumulado_corte['cnae_subclasse'] = df_acumulado_corte['cnae_subclasse'].str.replace("-", "Indisponível")


# In[78]:

df_acumulado_corte.to_csv("pj_cnaesecao_cnaesubclasse_endividamento.csv")


# # In[106]:


# fig = px.treemap(df_acumulado_corte, 
#                  path=['cnae_secao', 'cnae_subclasse'],
#                  values='valor_deflacionado')

# fig.update_layout(title='Endividamento do Agro por subsetor - Ano 2022',
#                   margin=dict(t=50, l=25, r=25, b=25),
#                  template = "seaborn")

# fig.update_traces(textinfo='label+percent entry',
#                  marker_line_width = 1,
#                   hovertemplate='%{label} <br> $%{value:,.2f} <br> %{percentRoot}',
#                  textposition="top left",
#                  textfont_size = 12,
#                  textfont_color = 'white')

# fig.show()


# # In[ ]:




