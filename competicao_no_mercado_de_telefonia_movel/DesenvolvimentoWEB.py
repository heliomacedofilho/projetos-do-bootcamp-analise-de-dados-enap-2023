### ************************************************************************************###
### Bibliotecas necessárias ###
### ************************************************************************************###

import streamlit as st
import pandas as pd
#import seaborn as sns
import matplotlib.pyplot as plt
#import numpy as np
import os
import webbrowser
from PIL import Image
from streamlit_option_menu import option_menu

# Defina a cor do background
#st.set_page_config(page_title="MERCADO REGULADO TELEFONIA MÓVEL", page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)

### ************************************************************************************###
### Configurações da página inicial ###
### ************************************************************************************###
st.set_page_config(
    page_title="Mercado Regulado Telefonia Móvel",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
   #menu_items={
   #    'Get Help': 'https://www.extremelycoolapp.com/help',
   #    'Report a bug': "https://www.extremelycoolapp.com/bug",
   #    'About': "# This is a header. This is an *extremely* cool app!"
   # }
)


### ************************************************************************************###
### Adicionando MENUS na página ###
### ************************************************************************************###
 
# Criando o MENU PRINCIPAL - BARRA
selected = option_menu(None, ["Projeto",  "Acesso a Informação", "Legislação", 'Acessibilidade'], 
        #icons=['house', "map", "bar-chart", 'book'], 
        icons=['house', "map", "bar-chart", 'book'], 
        menu_icon="cast", default_index=0, orientation="horizontal",
        styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "20px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "gray"},
        }
)


# Chame uma função do arquivo .py
#my_file.meu_codigo()

# O que acontece se clicarmos nos botões laterais
if selected == "Projeto":
        #webbrowser.open("https://www.gov.br/pt-br/orgaos-do-governo") 
        st.write(' ')
elif selected == "Acesso a Informação":
        webbrowser.open("https://www.gov.br/acessoainformacao/pt-br") 
elif selected == "Legislação":
        webbrowser.open("http://www4.planalto.gov.br/legislacao")
elif selected == "Acessibilidade":
        webbrowser.open("https://www.gov.br/governodigital/pt-br/acessibilidade-digital") 


### ************************************************************************************###
### Adicionando o título da página ###
### ************************************************************************************###

# escrevendo um título na página formato h1
st.markdown("<h1 style='text-align: center; color: grey;'>PROJETO BOOTCAMP</h1>", unsafe_allow_html=True)
#st.title("PROJETO BOOTCAMP", justify="center")

# escrevendo um subtítulo na página formato h2
st.markdown("<h2 style='text-align: center; color: blue;'>MERCADO REGULADO TELEFONIA MÓVEL</h2>", unsafe_allow_html=True)



### ************************************************************************************###
### Adicionando IMAGEM página ###
### ************************************************************************************###

# Importar a imagem
image = Image.open("image.png")
left_co, cent_co,last_co = st.columns(3)
with cent_co:
    st.image(image, width=400)



### ************************************************************************************###
### Adicionando texto no corpo da página ###
st.markdown("-------------------")
st.markdown("<h3 style='text-align: justify; color: green;'> SOBRE O PROJETO</h3>", unsafe_allow_html=True)
st.markdown("-------------------")# ************************************************************************************###


st.markdown("<h6 style='text-align: justify; color: black;font-weight: normal,'>Esta página objetiva divulgar o Projeto desenvolvido durante o Bootcamp em Análise de Dados (turma exclusiva para mulheres) – 2023, promovido pela Escola Nacional de Administração Pública - Enap. </h6>", unsafe_allow_html=True)

# Crie um link de página
link0 = "https://www.enap.gov.br/pt/cursos/coding-bootcamp"
# Exiba o link de página
st.markdown(f"[Link para a página do BootCamp]({link0})")

st.markdown("")

st.markdown("<h6 style='text-align: justify; color: black;'> - Carga Horária: 150 horas (132 horas síncronas e 18 horas assíncronas) </h6>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: justify; color: black;'> - Período: 02 outubro a 31 de outubro de 2023 </h6>", unsafe_allow_html=True)

st.markdown("")
st.markdown("<h6 style='text-align: justify; color: black;'> O setor de telecomunicações está sofrendo muitas mudanças no Brasil. Além de muitas expectativas com a chegada da tecnologia 5G, o mercado da telecom passa por expansões constantes. O projeto MERCADO REGULADO TELEFONIA MÓVEL aborda esse contexto histórico apresentando uma série temporal de acessos no mercado de telefonia móvel, identificando  padrões e tendências nesse mercado e analisando a qualidade do serviço a partir de dados sobre o uso das tecnologias: 4G, 3G e 2G.</h6>", unsafe_allow_html=True)           

st.markdown("<h6 style='text-align: justify; color: black;'>Dentre os principais objetivos desta página, podemos destacar: o acesso interativo (às vezes em tempo real) aos dados pertinentes a telefonia móvel; permitir a manipulação de dados e oferecer aos gestores organizacionais, analistas e à sociedade em geral a capacidade de conduzir suas próprias análises sobre a temática da telefonia móvel no contexto brasileiro.</h6>", unsafe_allow_html=True)


st.markdown("-------------------")
# escrevendo um subtítulo na página formato h3
st.markdown("<h3 style='text-align: justify; color: black;'>Análise de Política Pública de Concorrência </h3>", unsafe_allow_html=True)

# escrevendo os textos na página com markdown
st.markdown("A análise de dados sobre o Mercado Regulado de Telefonia Móvel contempla dados agrupados por Grupo Econômico, DDD e Unidade Federativa.")

st.write('A documentação completa sobre as analises realizadas com os dados de Telefonia Móvel podem ser acessadas no Menu Documentação')

st.markdown("<h4 style='text-align: left; color: blue;'>Período da Análise: </h4>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: left; color: black;'> - 2005 a 2008 </h5>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: left; color: black;'> - 2009 a 2023 </h5>", unsafe_allow_html=True)

# Crie um ícone
st.markdown("<h4 style='text-align: left; color: blue;'>Indicadores: </h4>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: left; color: black;'>- Market Share </h5>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: left; color: black;'>- HHI </h5>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: left; color: black;'>- Tecnologia de Geração </h5>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: left; color: black;'>- Tecnologia 5G </h5>", unsafe_allow_html=True)

st.markdown("-------------------")
st.markdown("<h4 style='text-align: left; color: black;'>Fonte de Dados </h4>", unsafe_allow_html=True)
st.markdown("Os dados utilizados nesse projeto são disponibilizados pela Agência Nacional de Telecomunicações - Anatel no Portal Brasileiro de Dados Abertos e no Portal da Agência Telefonia Móvel da Anatel, conforme acessos de Telefonia Móvel (Serviço Móvel Pessoal – SMP) enviados pelas prestadoras do serviço")

## LINKS ###
# Crie um link de página
link1 = "https://informacoes.anatel.gov.br/paineis/acessos/telefonia-movel"
# Exiba o link de página
st.markdown(f"[Link para a página do Anatel]({link1})")

link2 = "https://www.gov.br/anatel/pt-br/dados/qualidade/qualidade-dos-servicos/cobertura-da-telefonia-movel"
# Exiba o link de página
st.markdown(f"[Link para a página Dados Abertos]({link2})")

link3 = "https://agenciabrasil.ebc.com.br/geral/noticia/2021-04/numero-de-acessos-moveis-no-brasil-cresce-e-fecha-2020-com-234-milhoes"
# Exiba o link de página
st.markdown(f"[Link para a EBC]({link3})")


st.markdown("-------------------")
st.markdown("<h4 style='text-align: justify; color: black;'>Ferramentas de TI e Biblicotecas</h4>", unsafe_allow_html=True)
st.markdown("As ferramentas de tecnologia utilizadas no projeto são:")
st.markdown("<h5 style='text-align: left; color: black;'>-  Python </h5>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: left; color: black;'>- Numpy </h5>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: left; color: black;'>- Pandas </h5>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: left; color: black;'>- MatPlotLib </h5>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: left; color: black;'>- Plotly </h5>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: left; color: black;'>- Seaborn </h5>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: left; color: black;'>- StreamLit </h5>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: left; color: black;'>- Power BI </h5>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: left; color: black;'>- Folium </h5>", unsafe_allow_html=True)

### ************************************************************************************###
### Código EXTRA ###
### ************************************************************************************###


#st.header("LINKS")    


## Incorporando e centralizando  a figura


# Carrega a imagem
#st.image('image.png')

# Importar a imagem
#image = Image.open("fig/image.png")

#left_co, cent_co,last_co = st.columns(3)
#with cent_co:
 #   st.image(image, width=500)


#st.markdown("<h1 style='text-align: center; color: blue;'>TELEFONIA MÓVEL</h1>", unsafe_allow_html=True)
#st.title('** MERCADO REGULADO DE TELEFONIA MÓVEL **')


# Clique no botão
#if btn_painel:
 #   webbrowser.open("https://www.gov.br/mec/pt-br/assuntos/paineis-de-monitoramento-e-indicadores")


### ************************************************************************************###
### Adicionando MENUS na página ###
### ************************************************************************************###

# Criando o MENU LATERAL
#with st.sidebar:
 #   selected = option_menu(None, ["O Projeto", 'Sobre Nós'], icons=['house', 'people'], menu_icon="cast", default_index=1, styles={
  #      "container": {"padding": "0!important", "background-color": "#fafafa"},
   #     "icon": {"color": "orange", "font-size": "20px"}, 
    #    "nav-link": {"font-size": "15px", "text-align": "left", "margin":"auto", "--hover-color": "#eee"},
     #    "nav-link-selected": {"background-color": "green"},
    #}
#)

### ************************************************************************************###
### Página SOBRE ###
### ************************************************************************************###
# Criando a página sobre
#def sobre():
 #   stsobrenos = st.empty()
 #   stsobrenos.title("Sobre")
 #   stsobrenos.write("Nesse projeto apresentamos uma série temporal de acessos no mercado de telefonia móvel, identificando  padrões e tendências nesse mercado e analisando a qualidade do serviço a partir do uso de tecnologias (4G, 3G e 2G)")


# O que acontece se clicarmos nos botões laterais
#if selected == "O Projeto":
#       st.write(' ')
#elif selected == "Sobre Nós":
        #webbrowser.open("/sobre_nos.py")
#        st.write(' ')
        #sobre()
#else:
    #    st.write(' ')
      # st.redirect("/sobre.py")


### ************************************************************************************###
### Adicionando botões ao final da página e colocando link ###
### ************************************************************************************###
# Coloca os botões lado a lado
#col1, col2 = st.columns(2)

# Criando os botões
#btn_documentacao = st.button("Documentação")
#btn_painel = st.button("Painel")

# Adiciona os botões às colunas e dá nome aos botões
#col1.write(btn_documentacao)
#col2.write(btn_painel)

# Clique no botão
#if btn_documentacao:
 #   webbrowser.open("https://www.gov.br/mec/pt-br/assuntos/paineis-de-monitoramento-e-indicadores")
#elif btn_painel:
 #   webbrowser.open("https://www.gov.br/mec/pt-br/assuntos/paineis-de-monitoramento-e-indicadores")

#st.header("CONTEXTUALIZANDO")

#st.markdown("Política de concorrência em mercado regulado")
#st.markdown("Mercado de telefonia móvel")
#st.markdown("Papel do CADE na defesa da concorrência")
#st.markdown("Política que impacta diretamente nossa rotina como consumidores")
