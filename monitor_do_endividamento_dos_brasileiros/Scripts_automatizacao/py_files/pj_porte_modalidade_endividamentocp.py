#!/usr/bin/env python
# coding: utf-8

# In[1]:


import zipfile
import os
import pandas as pd
import plotly.express as px
import deflatebr as dbr

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

              #Filtros:
            df = df[df['mes'] == 12] #trocar para o ano que você quer filtrar
            df['porte'] = df['porte'].str.replace(' ','')
            filtro1 = df['porte'] == "PJ-Micro"
            filtro2 = df['porte'] == "PJ-Pequeno"
            df = df.loc[filtro1 | filtro2]
            df['porte']=df['porte'].str.replace('PJ-','')
            df['modalidade']=df['modalidade'].str.replace('PJ - ','')
            df = df[['data_base', 'modalidade', 'porte', 'a_vencer_ate_90_dias','a_vencer_de_91_ate_360_dias']]
            
            #Nova coluna para endividamento de curto prazo
            df['curto_prazo'] = df['a_vencer_ate_90_dias'] + df['a_vencer_de_91_ate_360_dias']
            df = df.drop(columns = ['a_vencer_ate_90_dias', 'a_vencer_de_91_ate_360_dias'], axis = 1)
            df['data_base'] = df['data_base'].dt.strftime('%Y-%m')
            
            #Agrupamentos para análise
            df = df.groupby(['data_base','modalidade','porte'])['curto_prazo'].sum().reset_index()
            
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


# In[7]:


df_total['curto_prazo_deflacionado'] = dbr.deflate(nominal_values=df_total['curto_prazo'], nominal_dates=df_total['data_base'], real_date='2022-12') 


# In[43]:


df_total['porte'] = df_total['porte'].replace({
    'Pequeno': 'Empresa de pequeno porte',
    'Micro': 'Microempresa'
})


# In[44]:


df_total.to_csv("pj_porte_modalidade_endividamentocp.csv")


# In[11]:


df_total_micro=df_total[df_total['porte']=='Micro']


# In[28]:


# fig = px.line(df_total_micro, 
#              x='data_base',
#              y='curto_prazo_deflacionado', 
#              color='modalidade')

# fig.update_layout(title_text='Endividamento de Curto Prazo de Microempresas por Modalidade de Crédito',
#              xaxis_title='Ano',
#              yaxis_title='Endividamento de Curto Prazo',
#              legend_orientation="h",
#              legend=dict(y=-0.2, x=0.5, xanchor='center'))

# fig.show()


# In[22]:


df_total_pequeno=df_total[df_total['porte']=='Pequeno']


# # In[27]:


# fig = px.line(df_total_pequeno, 
#              x='data_base',
#              y='curto_prazo_deflacionado', 
#              color='modalidade')

# fig.update_layout(title_text='Endividamento de Curto Prazo de Pequenas Empresas por Modalidade de Crédito',
#              xaxis_title='Ano',
#              yaxis_title='Endividamento de Curto Prazo',
#              legend_orientation="h",
#              legend=dict(y=-0.2, x=0.5, xanchor='center'))

# fig.show()


# In[56]:


# fig = px.line(df_total, 
#              x='data_base', 
#              y='curto_prazo_deflacionado',
#               color = 'modalidade',
#              facet_col='porte',
#              title='Curto Prazo Deflacionado por Porte ao Longo do Tempo',
#              labels={'data_base': '', 'curto_prazo_deflacionado': 'Endividamento de curto prazo deflacionado'},
#               height=600,
#              width=1000,
#              template="seaborn",
#              category_orders={"porte": ["Empresa de pequeno porte", "Microempresa"]})

# fig.update_layout(
#     yaxis_title="",
#     legend_title_text='',
#     legend=dict(x=0.5, y=-0.17, xanchor='center', yanchor='top', orientation = 'h'),
#     yaxis_title_standoff=0
# )

# fig.show()

