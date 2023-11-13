import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import plotly.express as px
import os


# Configuração Página
# ----------------- 
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

logo = Image.open('./Midia/logo.png')
st.image(logo, width=800)
st.markdown('---')


with st.container():
    
    w01 = '<p style="font-family:Arial; color:black; font-size: 18px;">Este Dashboard trata da <b>Análise das Instituições de Ensino Superior do Brasil</b>, sendo resultado do Bootcamp <b>\"Análise de Dados para Mulheres\"</b>, promovido pela ENAP.</p>'
    st.markdown(w01, unsafe_allow_html=True)
    
    w02 = '<p style="font-family:Arial; color:black; font-size: 18px;">Este Dashboard está dividido em cinco seções principais: Instituições, Cursos, Docentes, Discentes e Técnicos Administrativos. Cada seção apresenta mapas, tabelas, gráficos e constatações encontradas nas análises realizadas.</p>'
    st.markdown(w02, unsafe_allow_html=True)
    
        
    
    st.markdown('---')

   


