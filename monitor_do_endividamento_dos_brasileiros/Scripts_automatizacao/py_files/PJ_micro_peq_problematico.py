#!/usr/bin/env python
# coding: utf-8

# In[1]:


#pip install deflateBR


# In[2]:


import zipfile
import os
import pandas as pd
import deflatebr as dbr
import plotly.express as px
import plotly.graph_objects as go


# In[3]:


def concatenar_csvs(diretorio):
    frames = []

    for arquivo in os.listdir(diretorio):
        if arquivo.endswith('.csv'):
            caminho_arquivo = os.path.join(diretorio, arquivo)
            
            df = pd.read_csv(caminho_arquivo, encoding='utf-8', delimiter=";", decimal=",")
            df = df.rename(columns={df.columns[0]: "data_base"})
            df['data_base'] = pd.to_datetime(df['data_base'], format="%Y-%m-%d")
            df['mes'] = df['data_base'].dt.month 
            df['ano'] = df['data_base'].dt.year
            #Filtros:
            df = df[df['mes'] == 12] 
            df = df[df['modalidade'] == "PJ - Capital de giro"]
            df['porte'] = df['porte'].str.replace(' ','')
            df = df[df['porte'] == "PJ-Micro"]
            df = df[['data_base', 'modalidade', 'porte', 'a_vencer_ate_90_dias','a_vencer_de_91_ate_360_dias', 'ativo_problematico']]        
            df['curto_prazo'] = df['a_vencer_ate_90_dias'] + df['a_vencer_de_91_ate_360_dias']
            df = df.drop(columns = ['a_vencer_ate_90_dias', 'a_vencer_de_91_ate_360_dias'], axis = 1)
            df['data_base'] = df['data_base'].dt.strftime('%Y-%m')
            #Agrupamentos para análise
            df = df.groupby(['data_base', 'modalidade', 'porte']).agg({
                'curto_prazo': 'sum',
                'ativo_problematico': 'sum'
            }).reset_index()
            
            frames.append(df)

    df_concatenado = pd.concat(frames, ignore_index=True)

    return df_concatenado


# In[4]:


anos = list(range(2012, 2023))
dataframes = []

for ano in anos:
    diretorio = f"planilha_{ano}"
    dataframe_ano = concatenar_csvs(diretorio)
    dataframes.append(dataframe_ano)

df_total_micro = pd.concat(dataframes, ignore_index=False)


# In[5]:


df_total_micro['data_base']=pd.to_datetime(df_total_micro['data_base'], format='%Y-%m')


# In[6]:


df_total_micro['curto_prazo_deflacionado'] = dbr.deflate(nominal_values=df_total_micro['curto_prazo'], nominal_dates=df_total_micro['data_base'], real_date='2022-12')


# In[7]:


df_total_micro['ativo_problematico_deflacionado'] = dbr.deflate(nominal_values=df_total_micro['ativo_problematico'], nominal_dates=df_total_micro['data_base'], real_date='2022-12')


# In[9]:


def concatenar_csvs(diretorio):
    frames = []

    for arquivo in os.listdir(diretorio):
        if arquivo.endswith('.csv'):
            caminho_arquivo = os.path.join(diretorio, arquivo)
            
            df = pd.read_csv(caminho_arquivo, encoding='utf-8', delimiter=";", decimal=",")
            df = df.rename(columns={df.columns[0]: "data_base"})
            df['data_base'] = pd.to_datetime(df['data_base'], format="%Y-%m-%d")
            df['mes'] = df['data_base'].dt.month 
            df['ano'] = df['data_base'].dt.year
            #Filtros:
            df = df[df['mes'] == 12] 
            df = df[df['modalidade'] == "PJ - Capital de giro"]
            df['porte'] = df['porte'].str.replace(' ','')
            df = df[df['porte'] == "PJ-Pequeno"]
            df = df[['data_base', 'modalidade', 'porte', 'a_vencer_ate_90_dias','a_vencer_de_91_ate_360_dias', 'ativo_problematico']]        
            df['curto_prazo'] = df['a_vencer_ate_90_dias'] + df['a_vencer_de_91_ate_360_dias']
            df = df.drop(columns = ['a_vencer_ate_90_dias', 'a_vencer_de_91_ate_360_dias'], axis = 1)
            df['data_base'] = df['data_base'].dt.strftime('%Y-%m')
            #Agrupamentos para análise
            df = df.groupby(['data_base', 'modalidade', 'porte']).agg({
                'curto_prazo': 'sum',
                'ativo_problematico': 'sum'
            }).reset_index()
            
            frames.append(df)

    df_concatenado = pd.concat(frames, ignore_index=True)

    return df_concatenado


# In[10]:


anos = list(range(2012, 2023))
dataframes = []

for ano in anos:
    diretorio = f"planilha_{ano}"
    dataframe_ano = concatenar_csvs(diretorio)
    dataframes.append(dataframe_ano)

df_total_pequeno = pd.concat(dataframes, ignore_index=False)


# In[11]:


df_total_pequeno['data_base']=pd.to_datetime(df_total_pequeno['data_base'], format='%Y-%m')


# In[12]:


df_total_pequeno['curto_prazo_deflacionado'] = dbr.deflate(nominal_values=df_total_pequeno['curto_prazo'], nominal_dates=df_total_pequeno['data_base'], real_date='2022-12')


# In[13]:


df_total_pequeno['ativo_problematico_deflacionado'] = dbr.deflate(nominal_values=df_total_pequeno['ativo_problematico'], nominal_dates=df_total_micro['data_base'], real_date='2022-12')


# In[24]:


df_micro_peq_problematico = pd.concat([df_total_micro, df_total_pequeno])


# In[29]:


# # Criar a figura
# fig = go.Figure()

# # Adicionar as barras empilhadas
# fig.add_trace(go.Bar(x=df_total_micro['data_base'], y=df_total_micro['curto_prazo_deflacionado'], name='curto_prazo_deflacionado'))
# fig.add_trace(go.Bar(x=df_total_micro['data_base'], y=df_total_micro['ativo_problematico_deflacionado'], name='ativo_problematico_deflacionado'))

# # Atualizar as configurações das barras para empilhamento
# fig.update_traces(marker_line_width=0, opacity=0.7)

# # Configurar o layout do gráfico
# fig.update_layout(barmode='group', xaxis_title='Ano', yaxis_title='Valores em reais', title='Endividamento das Micro Empresas X Ativo Problemático - Anos 2012 a 2023')

# # Mostrar o gráfico
# fig.show()


# # In[22]:


# # Criar a figura
# fig = go.Figure()

# # Adicionar as barras empilhadas
# fig.add_trace(go.Bar(x=df_total_pequeno['data_base'], y=df_total_pequeno['curto_prazo_deflacionado'], name='curto_prazo_deflacionado'))
# fig.add_trace(go.Bar(x=df_total_pequeno['data_base'], y=df_total_pequeno['ativo_problematico_deflacionado'], name='ativo_problematico_deflacionado'))

# # Atualizar as configurações das barras para empilhamento
# fig.update_traces(marker_line_width=0, opacity=0.7)

# # Configurar o layout do gráfico
# fig.update_layout(barmode='group', xaxis_title='Ano', yaxis_title='Valores em reais', title='Endividamento das Pequenas Empresas X Ativo Problemático - Anos 2012 a 2023')

# # Mostrar o gráfico
# fig.show()


# In[30]:


df_micro_peq_problematico = df_micro_peq_problematico.rename(columns={
    'curto_prazo_deflacionado': 'Endividamento de Curto Prazo',
    'ativo_problematico_deflacionado': 'Ativo Problemático'
})


# In[31]:


# fig = px.bar(df_micro_peq_problematico, 
#              x='data_base', 
#              y=['Endividamento de Curto Prazo', 'Ativo Problemático'],
#              facet_col='porte', 
#              labels={'data_base': ''},
#              template="seaborn")

# fig.update_layout(
#     barmode='group',
#     yaxis_title="Endividamento de curto prazo e ativo problemático, em que há pouca expectativa de pagamento",
#     legend_title_text='tipo de endividamento',
#     legend=dict(x=0.5, y=-0.15, xanchor='center', yanchor='top', orientation = 'h'),
#         xaxis=dict(dtick="M24"),
#         xaxis2=dict(dtick="M24")
# )

# fig.show()


# In[32]:


df_micro_peq_problematico.to_csv("df_micro_peq_problematico.csv")

