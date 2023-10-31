### ************************************************************************************###
### Bibliotecas necessárias ###
### ************************************************************************************###
import streamlit as st
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt

import plotly.express as px
#import plotly.io as pio

import numpy as np

import os
from geojson_rewind import rewind
import requests

#A biblioteca pickle é uma biblioteca Python padrão que permite serializar e desserializar objetos Python. Serializar um objeto significa converter o objeto em uma representação binária que pode ser armazenada em um arquivo ou transmitida por uma rede. Desserializar um objeto significa converter a representação binária de volta para o objeto Python.
#Faz com que a exibição dos gráficos fique mais rapida
import pickle 

### ************************************************************************************###
### Adicionando o título da página ###
### ************************************************************************************###
st.markdown("-------------------")
st.markdown("<h3 style='text-align: justify; color: black;'> REPRESENTAÇÃO BIDIMENSIONAL - MAPAS</h3>", unsafe_allow_html=True)
st.markdown("-------------------")

### ************************************************************************************###
### Adicionando  texto no corpo da página ###
### ************************************************************************************###
st.markdown("<h5 style='text-align: justify; color: black;'>Esse projeto resultou em um conjunto de mapas/gráficos visando facilitar as análises e entendimento dos resultados pelos interessados: </h5>", unsafe_allow_html=True)
st.markdown("-------------------")


# arquivo = './Bootcamp Enap/projeto-smp/df_tec_geracao.csv'

### ************************************************************************************###
### Orientação do Bruno para melhorar a performance da exibição dos dados ###
### ************************************************************************************###
#Adicionar o comando @st.cache_data antes de cada função


### ************************************************************************************###
### Função de carga dos dados ###
### ************************************************************************************###
@st.cache_data
def load_data(arquivo):
    # Carregue os dados do arquivo CSV
    #data = pd.read_csv(arquivo, sep=';')
    data = pd.read_csv(arquivo, sep=';',encoding='utf-8')

    # Retorne os dados
    return data

@st.cache_data
def abre_url():
    return requests.get(f'http://servicodados.ibge.gov.br/api/v3/malhas/paises/BR?formato=application/vnd.geo+json&qualidade=minima&intrarregiao=municipio').json()
    

    
### ************************************************************************************###
### Inicio do Código da Bia para criar o MAPA
### ************************************************************************************###

# Chame a função de carga dos dados
arquivo = './dadospublicos/df_tec_geracao.csv'
df = load_data(arquivo)


#print(len(df))
#print(df.shape)

df.head()

# vemos que os decimais estao com virgula, e nao com ponto (que é o default do python)

# retirando a coluna 'Unnamed: 0'

df = df.drop(columns = ['Unnamed: 0'])

print(df['percentual'].dtype)
print(df['media_ano'].dtype)

# o tipo do dado que vou manipular('percentual') está em formato string, e não float

df['media_ano'] = df['media_ano'].str.replace(',', '.', regex=True).astype(float)
df['percentual'] = df['percentual'].str.replace(',', '.', regex=True).astype(float)

# estamos aplicando a substituição do caracter ',' por '.' em cada coluna ('percentual' e 'media_ano') 
# individualmente; e depois usamos o método astype(float) para converter os valores para o tipo de dados float


# restringindo o numero de casas decimais da coluna percentual a 2 casas decimais

df['percentual'] = df['percentual'].round(2)

print(df['percentual'].dtype)
print(df['media_ano'].dtype)

# agora ambas as colunas são do tipo float e são manipuláveis em operações matemáticas

df.head(20)

# vendo a tabela mais ampla
# temos 2 casas decimais na coluna 'percentual'

# vendo quais tipos de tecnologia tivemos ao longo dos últimos 15 anos: foram 7

print(df['Tecnologia Geração'].unique())
print(len(df['Tecnologia Geração'].unique()))

tec_1g = df.query('`Tecnologia Geração` == "1G"')
tec_2g = df.query('`Tecnologia Geração` == "2G"')
tec_3g = df.query('`Tecnologia Geração` == "3G"')
tec_4g = df.query('`Tecnologia Geração` == "4G"')
tec_m2m = df.query('`Tecnologia Geração` == "M2M"')
tec_5g = df.query('`Tecnologia Geração` == "5G"')
#tec_5g_nsa = df.query('`Tecnologia Geração` == "5G Non Stand Alone"')

# ChatCPT me ajudando na sintaxe:
# O erro no código que você forneceu está relacionado à forma como o nome da coluna 'Tecnologia Geração' é 
# especificado na consulta. O espaço no nome da coluna requer que você o coloque entre colchetes ou aspas.
# Neste código corrigido, usamos as crases (``) para cercar o nome da coluna 'Tecnologia Geração' porque ele 
# contém espaços. Também usamos as aspas duplas ("2G") para comparar com o valor "2G" na coluna.

# vendo os dataframes por tecnologia

#tec_5g_nsa

df['Tecnologia Geração'].unique()

## comandos para plotar um gráfico do pyplot do matplotlib

grafico_1 = plt.figure(figsize=(6,5))
plt.plot(tec_1g["ano"], tec_1g["percentual"], label = "1G", linewidth = 2.5, color = "cyan") #argumentos são eixo x e eixo y
plt.plot(tec_2g["ano"], tec_2g["percentual"], label = "2G", linewidth = 2.5, color = "green")
plt.plot(tec_3g["ano"], tec_3g["percentual"], label = "3G", linewidth = 2.5, color = "purple")
plt.plot(tec_m2m["ano"], tec_m2m["percentual"], label = "M2M", linewidth = 2.5, color = "gold")
plt.plot(tec_4g["ano"], tec_4g["percentual"], label = "4G", linewidth = 2.5, color = "red")
plt.plot(tec_5g["ano"], tec_5g["percentual"], label = "5G", linewidth = 2.5, color = "magenta")
#plt.plot(tec_5g_nsa["ano"], tec_5g_nsa["percentual"], label = "5G-NSA", linewidth = 2.5, color = "blue")
plt.title("Evolução das Tecnologias de Geração \n Anos 2009 a 2023", fontweight='bold')
plt.xlabel("Período")
plt.ylabel("Acessos no ano (%)")
plt.annotate('Ápice do 3G', (2015,60), xytext=(2015 + 1, 60 + 6),
             arrowprops=dict(facecolor='black', shrink=0.05))
plt.annotate('4G é a tecnologia mais utilizada atualmente', (2023,80), xytext=(2015, 80 + 10),
             arrowprops=dict(facecolor='black', shrink=0.05))
plt.ticklabel_format(style="plain", axis="y")
plt.grid()
plt.legend()
#plt.show()
st.pyplot(grafico_1)

#plt.savefig('grafico_tecnologia_estatico.png')

### ************************************************************************************###
### Inicio do Código da Bia para criar o 2o MAPA
### ************************************************************************************###

st.markdown("-------------------")
st.markdown("<h5 style='text-align: justify; color: black;'> O Gráfico abaixo exibe a tecnologia de geração dos telefones móveis usados pelos brasileiros</h5>", unsafe_allow_html=True)
st.markdown("-------------------")

# Chame a função de carga dos dados
arquivo = './dadospublicos/tec_2023_modalidade.csv'
modalidade = load_data(arquivo)

#modalidade = pd.read_csv('./dadospublicos/tec_2023_modalidade.csv', sep = ';')

modalidade['percentual'] = modalidade['percentual'].str.replace(',', '.', regex=True).astype(float)
modalidade['media_ano'] = modalidade['media_ano'].str.replace(',', '.', regex=True).astype(float)


# import plotly.express as px

fig = px.treemap(modalidade, path=[px.Constant("Tecnologia de Geração de Telefonia Móvel - Ano 2023"), 'Tecnologia Geração', 'Modalidade de Cobrança', 'percentual'], values='media_ano',           color='percentual', hover_data=['media_ano'], color_continuous_scale='YlGnBu')
fig.update_traces(root_color="lightgrey")
fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
#fig.show()
#st.pyplot(fig)
st.plotly_chart(fig)


### ************************************************************************************###
### Inicio do Código da Graciele para criar o MAPA
### ************************************************************************************###

# Chame a função de carga dos dados
#arquivo = './dadospublicos/uf_5g.csv'
#df = load_data(arquivo)
#
###**Ler o df de dados de 5g por UF**
#tec_2023_5g_por_estado = pd.read_csv('./tec_2023_5g_por_estado.csv',sep =';')
#tec_2023_5g_por_estado.head()
#
#tec_2023_5g_por_estado.rename(columns=str.lower, inplace=True) #renomear as colunas para minúsculas

#import streamlit as st
from streamlit.components.v1 import html

# Carregue o arquivo HTML do mapa
with open('./mapas/mapa_estados_5g_com_tooltip.html', 'r') as f:
    mapa_html = f.read()

# Insira o mapa HTML em seu aplicativo Streamlit
st.markdown('*Mapa 5G com Tooltip*')
html(mapa_html, height=600)


### ************************************************************************************###
### Inicio do Código da FERNANDA para criar o GRAFICO DINÂMICO
### ************************************************************************************###

st.markdown("-------------------")
st.markdown("<h5 style='text-align: justify; color: black;'> O Gráfico abaixo permite ao usuário interagir selecionando a Operadora e visualizando a concentração de telefones móveis por municípios brasileiros</h5>", unsafe_allow_html=True)
st.markdown("-------------------")

import time

resultados = st.selectbox('Qual a operadora gostaria de ver a concentração de dados por Municípios?', ('TELECOM AMERICAS','TELEFONICA', 'TELECOM ITALIA', 'OI','OUTROS'))

import gzip

# Nome do arquivo Pickle compactado
#pickle_file = './mapas/mapa_Telefonica_Vivo.pkl.gz'

# Use gzip para abrir o arquivo compactado em modo leitura binária ('rb')
#with gzip.open(pickle_file, 'rb') as f:
 #   loaded_data = pickle.load(f)

#print('Dados descompactados:')
#print(loaded_data)

# Open the zip file

###INICIA AQUI

#@st.cache_data
#def carrega_mapa():
#    start_time = time.time()
#    file_names =['mapa_Telefonica_Vivo.pkl.gz']
#    #file_names=['mapa_oi.pkl','mapa_TelecomAmericas_Claro.pkl','mapa_TelecomItalia_Tim.pkl','mapa_Telefonica_Vivo.pkl','mapa_Outros.pkl']
#    mapas = {}
#    #url = 'https://raw.githubusercontent.com/rislamiranda/projeto-smp/main/mapas/'
#
#    for arquivo_mapa in file_names:
#        with gzip.GzipFile('./mapas/' + arquivo_mapa, 'r') as archive:
#            mapas[arquivo_mapa[:-3]] = pickle.load(archive)
#            print("--- %s seconds ---" % (time.time() - start_time))
#    return mapas
#    
#start_time = time.time()
#mapas = carrega_mapa()
#print("--- carrega mapa %s seconds ---" % (time.time() - start_time))
#
#def cor_grupos(escolha_grupo):
#    if escolha_grupo == 'TELECOM AMERICAS':
#        result = 'mapa_TelecomAmericas_Claro.pkl'
#    elif escolha_grupo == 'TELECOM ITALIA':
#        result = 'mapa_TelecomItalia_Tim.pkl'
#    elif escolha_grupo == 'TELEFONICA':
#        result = 'mapa_Telefonica_Vivo.pkl'
#    elif escolha_grupo == 'OI':
#        result = 'mapa_oi.pkl'
#    else:
#        result = 'mapa_Outros.pkl'     
#    return result
#
##st.write(cor_grupos(resultados))
#print("--- Iniciando o plotly %s seconds ---" % (time.time() - start_time))
#st.plotly_chart(mapas[cor_grupos(resultados)])  
#print("--- finalizando o plotly %s seconds ---" % (time.time() - start_time))

###FINALIZA AQUI

### ************************************************************************************###
### Código EXTRA ###
### ************************************************************************************###
## Dar preferência a usar os comandos do streamlit ao inves do plotly


#criando um gráfico de linhas responsivo
##grafico_2 = px.line(df, x = "ano", y = "percentual", color="Tecnologia Geração").update_layout(
#xaxis_title = "Período",
#yaxis_title = "Acessos no ano (%)",
#title = "Evolução das Tecnologias de Geração - Anos 2009 a 2023",
#title_font_color = "blue",
#title_font_size = 24,
#title_x = 0.05,
#title_y = 0.93,
#xaxis_color = "blue",
#yaxis_color = "blue",
#xaxis_title_font=dict(size=16),
#yaxis_title_font=dict(size=16))

#o title_x pode varia de 0 a 1, e é a centralização do título em relação ao eixo x (ajuste na horizontal)
#o title_y é o ajuste na vertical (varia de 0 a 1)

#grafico_2

#grafico_2.write_html('grafico_tecnologia_dinamico.html')