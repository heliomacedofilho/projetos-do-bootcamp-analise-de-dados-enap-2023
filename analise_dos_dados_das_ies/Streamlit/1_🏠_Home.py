import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import plotly.express as px
import os


########## CONFIGURAÇÃO DA PÁGINA########
st.set_page_config(
    page_title='Analise IES Brasil',
    page_icon='📊',
    layout='wide',
    initial_sidebar_state='expanded',
    menu_items={
        'Get Help': 'http://www.meusite.com.br',
        'Report a bug': "http://www.meuoutrosite.com.br",
        'About': "Esse app foi desenvolvido no curso ENAP ."
    }
)

header_left, header_mid, header_right = st.columns([1, 3, 1], gap="large")
##############################################################################
#######LOGO INICIAL#################
logo = Image.open('./Midia/logo.png')
st.image(logo, width=800)
st.markdown('---')

#######################################LOAD HTML ##############################################
###########PLOTE MAPA HTML
with st.container():
    
    w01 = '<p style="font-family:Arial; color:black; font-size: 18px;">Este trabalho é resultado do Bootcamp <b>\"Análise de Dados para Mulheres\"</b>, promovido pela ENAP. Como resultado foi gerado este Dashboard, que trata da <b>Análise das Instituições de Ensino Superior do Brasil</b>.</p>'
    st.markdown(w01, unsafe_allow_html=True)
    
    w02 = '<p style="font-family:Arial; color:black; font-size: 18px;">Este Dashboard está dividido em cinco seções principais - cada seção apresenta mapas, tabelas, gráficos e um resumo de constatações encontradas nas análises realizadas sobre: Instituições, Cursos, Docentes, Discentes e Técnicos Administrativos.</p>'
    st.markdown(w02, unsafe_allow_html=True)
    
    w03 = '<p style="font-family:Arial; color:black; font-size: 18px;">Na seção <b>\"Projeto\"</b>, detalhamos o processo de desenvolvimento deste projeto.</p>'
    st.markdown(w03, unsafe_allow_html=True)
    
    w04 = '<p style="font-family:Arial; color:black; font-size: 18px;">Em <b>\"Quem Somos\"</b>, vocês encontrarão informações de contato sobre o nosso grupo.</p>'
    st.markdown(w04, unsafe_allow_html=True)
    
    
    st.markdown('---')

    st.subheader('Mapa da Distribuição de Instituições de Ensino Públicas e Privadas nos Estados do Brasil')
    st.subheader('Uma Análise Comparativa')
   
###############################################################################################
    # Carrega o arquivo HTML
    with open('./data/ies_interativo.html', 'r', encoding='utf-8') as file:
        html_code = file.read()

    # Exibe o conteúdo HTML
    st.components.v1.html(html_code, height=800, scrolling=True)


 #######################################################################################################

