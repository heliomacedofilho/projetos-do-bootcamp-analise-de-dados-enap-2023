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
import sidrapy


# In[2]:


def concatenar_csvs(diretorio):
    frames = []

    for arquivo in os.listdir(diretorio):
        if arquivo.endswith('.csv'):
            caminho_arquivo = os.path.join(diretorio, arquivo)
            
            df = pd.read_csv(caminho_arquivo, encoding='utf-8', delimiter=";", decimal=",")
            df = df.rename(columns={df.columns[0]: "data_base"})
            df = df.rename(columns={df.columns[6]: "cnae_secao"})
            df = df[df['cliente'] == "PJ"]
            df['cnae_secao']=df['cnae_secao'].str.replace('PJ - ','')
            df = df.iloc[:, [0, 6, 20, 22]]
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


df_total_group = df_total.groupby(['data_base', 'cnae_secao'])[['carteira_ativa', 'ativo_problematico']].sum().reset_index()


# In[6]:


df_total_group['data_base'] = df_total_group['data_base'].dt.strftime('%Y') #Converti apenas para o ano porque as séries que vou usar do ibge são anuais


# In[10]:


df_total_group['Seção CNAE e ano'] = df_total_group['cnae_secao'] + ' (' + df_total_group['data_base'] + ')'


# In[13]:


#Extraindo informações do IBGE via api

empresas = sidrapy.table.get_table(
    table_code="2718",
    territorial_level="1",
    ibge_territorial_code="all",
    period="last 9",
    variable="630",
    classifications={"12762": "all", "370": "9504", "369": "all"},
    
)

empresas.columns = empresas.iloc[0] #troca a primeira linha para o nome da coluna
empresas = empresas.iloc[1:, :]


# In[14]:


empresas = empresas.drop(columns = ['Nível Territorial', 'Unidade de Medida', 'Nível Territorial (Código)', 'Unidade de Medida (Código)',
                                    'Brasil (Código)', 'Brasil', 'Variável (Código)', 
                                    'Classificação Nacional de Atividades Econômicas (CNAE 2.0) (Código)',
                                    'Faixas de pessoal ocupado assalariado (Código)',
                                    'Faixas de pessoal ocupado assalariado',
                                    'Tipo de evento da empresa (Código)',
                                    'Ano (Código)',
                                   'Variável'])


# In[15]:


empresas = empresas.rename(columns={"Classificação Nacional de Atividades Econômicas (CNAE 2.0)": "cnae_secao",
                                     "Tipo de evento da empresa": "evento",
                                    "Valor": "qtde_empresas"}) 


# In[16]:


empresas['qtde_empresas'] = empresas['qtde_empresas'].replace("-", np.nan)


# In[17]:


empresas['qtde_empresas'] = empresas['qtde_empresas'].astype("float")


# In[18]:


empresas_pivot = empresas.pivot_table(index=['Ano', 'cnae_secao'], 
                                      columns='evento', 
                                      values='qtde_empresas').reset_index()


# In[19]:


empresas_pivot['cnae_secao'] = empresas_pivot['cnae_secao'].str.slice(start=2)


# In[22]:


df_corr_ibge_scr_pj = pd.merge(empresas_pivot,
                               df_total_group,
                               left_on = ["Ano", "cnae_secao"],
                               right_on = ["data_base", "cnae_secao"])


# In[23]:


df_corr_ibge_scr_pj['Saída de atividade/Total'] = df_corr_ibge_scr_pj['Saída de atividade'] / df_corr_ibge_scr_pj['Total de empresas ativas']


# In[25]:


df_corr_ibge_scr_pj_num = df_corr_ibge_scr_pj.drop(columns = {'Ano',
                                                              'cnae_secao',
                                                             'data_base',
                                                             'Seção CNAE e ano'}, axis=1)


# In[26]:


sns.set_theme(style="white")

corr = df_corr_ibge_scr_pj_num.corr()

# Generate a mask for the upper triangle
mask = np.triu(np.ones_like(corr, dtype=bool))

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))

# Draw the heatmap with the mask and correct aspect ratio
sns_heatmap = sns.heatmap(corr, mask=mask, cmap="Spectral", #possíveis parâmetros para o cmap: https://matplotlib.org/stable/users/explain/colors/colormaps.html
            square=True, linewidths=.5, cbar_kws={"shrink": .5}, annot = True)


# In[36]:


df_scatter_plot = df_corr_ibge_scr_pj.drop(columns = ['Ano'], axis=1)


# In[44]:


# palette = sns.color_palette("tab20", 19) #possíveis palettes

# sns.scatterplot(data = df_scatter_plot, x="ativo_problematico", y="Saída de atividade/Total", hue = 'Seção CNAE e ano', palette=palette)
# plt.legend(title='cnae_secao', loc='right', bbox_to_anchor=(3, 3), ncol=3)
# plt.tight_layout()
# plt.show()


# In[45]:


df_scatter_plot.to_csv("df_corr_ibge_scr_pj.csv", index=False)

