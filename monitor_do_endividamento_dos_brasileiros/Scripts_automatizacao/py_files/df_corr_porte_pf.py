#!/usr/bin/env python
# coding: utf-8

# In[1]:


import zipfile
import os
import pandas as pd
import requests
import deflatebr as dbr
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


def concatenar_csvs(diretorio):
    frames = []

    for arquivo in os.listdir(diretorio):
        if arquivo.endswith('.csv'):
            caminho_arquivo = os.path.join(diretorio, arquivo)
            
            df = pd.read_csv(caminho_arquivo, encoding='utf-8', delimiter=";", decimal=",")
            df = df.rename(columns={df.columns[0]: "data_base"})
            df = df[df['cliente'] == "PF"]
            df['porte'] = df['porte'].str.replace(' ','')
            df['porte']=df['porte'].str.replace('PF-','')
            df = df.iloc[:, [0, 8, 20, 22]]
            df['data_base'] = pd.to_datetime(df['data_base'], format="%Y-%m-%d")
            df['mes'] = df['data_base'].dt.month
            df = df[df['mes'] == 12]
            
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


# In[191]:


def categoria_renda(dados_porte):
    if dados_porte in ['Acima de 20 salários mínimos', 'Mais de 10 a 20 salários mínimos', 'Mais de 3 a 5 salários mínimos']:
        return 'alta renda'
    elif dados_porte == 'Indisponível':
        return 'renda indisponível'
    elif dados_porte == 'Mais de 5 a 10 salários mínimos':
        return 'renda média'
    else:
        return 'baixa renda'

df_total['categoria_renda'] = df_total['porte'].apply(categoria_renda)


# In[192]:


df_total_group = df_total.groupby(['data_base', 'categoria_renda'])[['carteira_ativa', 'ativo_problematico']].sum().reset_index()


# In[194]:


df_pivot = df_total_group.pivot_table(index="data_base",
                                      columns='categoria_renda', 
                                      values=['carteira_ativa', 'ativo_problematico'],
                                      aggfunc='sum').reset_index()

df_pivot.columns = ['_'.join(col).rstrip('_') for col in df_pivot.columns.values] #para que as colunas não sejam multinível


# In[ ]:


df_pivot['data_base'] = df_pivot['data_base'].dt.strftime('%Y') #Converti apenas para o ano porque algumas das séries que vou usar do bacen são anuais


# In[11]:


#Extraindo informações do Sistema Gerenciador de Séries Temporais do BCB
codigos_series = [24868, 24881, 25149, 20716, 29404]
series_bacen = []

for codigo in codigos_series:
    url = f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados?formato=json'
    resposta = requests.get(url)
    serie_data = resposta.json()
    serie_df = pd.DataFrame(serie_data)
    serie_df['data'] = pd.to_datetime(serie_df['data'], format="%d/%m/%Y")
    serie_df['data'] = serie_df['data'].dt.strftime('%Y-%m')
    serie_df = serie_df.rename(columns={'valor': f'valor_{codigo}'})
    serie_df = serie_df.set_index('data')
    series_bacen.append(serie_df)

series_bacen = pd.concat(series_bacen, axis=1).reset_index()


# In[12]:


series_bacen_limpo = series_bacen.dropna()


# In[13]:


series_bacen_limpo['data'] = pd.to_datetime(series_bacen_limpo['data'])


# In[14]:


series_bacen_limpo['data'] = series_bacen_limpo['data'].dt.strftime('%Y')


# In[15]:


for col in series_bacen_limpo.columns[1:]:
    series_bacen_limpo[col] = series_bacen_limpo[col].astype(float)



# In[197]:


df_analise_porte_pf = pd.merge(series_bacen_limpo,
                              df_pivot,
                              left_on="data",
                              right_on="data_base",
                              how = "inner")


# In[198]:


df_analise_porte_pf = df_analise_porte_pf.rename(columns={
    'data': "ano",
    'valor_24868': "Pontos atendimento",
    'valor_24881': "Bancos autorizados",
    'valor_25149': "Cart. créd. ativos",
    'valor_20716': "Tx. juros PF",
    'valor_29404': "Retorno sobre ativos IF"
})


# In[199]:


df_analise_porte_pf = df_analise_porte_pf.drop(columns = ["data_base"])


# In[215]:


df_analise_porte_pf_num = df_analise_porte_pf.drop(columns = {'ano',
                                                              'ativo_problematico_renda indisponível',
                                                              'ativo_problematico_renda média',
                                                              'carteira_ativa_renda indisponível',
                                                              'carteira_ativa_renda média'}, axis=1)


# In[221]:


df_analise_porte_pf_num.to_csv("df_corr_porte_pf.csv", index=False)


# In[216]:


# sns.set_theme(style="white")

# corr = df_analise_porte_pf_num.corr()

# # Generate a mask for the upper triangle
# mask = np.triu(np.ones_like(corr, dtype=bool))

# # Set up the matplotlib figure
# f, ax = plt.subplots(figsize=(11, 9))

# # Generate a custom diverging colormap
# cmap = sns.diverging_palette(230, 20, as_cmap=True)

# # Draw the heatmap with the mask and correct aspect ratio
# sns_heatmap = sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
#             square=True, linewidths=.5, cbar_kws={"shrink": .5}, annot = True)


# In[206]:


# df_scatter_plot = pd.merge(series_bacen_limpo,
#                               df_total,
#                               left_on="data",
#                               right_on="data_base",
#                               how = "inner")


# In[208]:


# df_scatter_plot = df_scatter_plot.rename(columns={
#     'data': "ano",
#     'valor_24868': "Pontos atendimento",
#     'valor_24881': "Bancos autorizados",
#     'valor_25149': "Cart. créd. ativos",
#     'valor_20716': "Tx. juros PF",
#     'valor_29404': "Retorno sobre ativos IF"
# })


# In[209]:


# df_scatter_plot = df_scatter_plot.drop(columns = ['ano', 'data_base', 'mes'])


# In[218]:


# # valores_excluir = ['ativo_problematico_renda indisponivel', 
#                    'ativo_problematico_renda média', 
#                    'carteira_ativa_renda indisponível', 
#                    'carteira_ativa_renda indisponível']

# df_scatter_plot = df_scatter_plot[~df_scatter_plot['categoria_renda'].isin(valores_excluir)]


# In[219]:


# import warnings
# warnings.filterwarnings('ignore')

# g = sns.FacetGrid(df_scatter_plot, col = 'categoria_renda')
# g.map_dataframe(sns.scatterplot, x="carteira_ativa", y="ativo_problematico", hue = "porte")
# g.add_legend()

