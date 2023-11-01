# pages/page3.py
import streamlit as st
import pandas as pd
#from pytube import YouTube


# st.set_page_config(
#     page_title="De arquivos em HTML para DataFrame",
#     page_icon= ':large_blue_square:',
#     layout='wide',
#     initial_sidebar_state='expanded')

st.header(':blue[Automação de Relatório de dados de Documentos]', divider='rainbow')
st.title('De arquivo em HTML para DataFrame')
st.caption("Projeto Final do Bootcamp de Análise de Dados - ENAP :game_die::game_die::game_die:")
st.caption("Turma Exclusiva para Mulheres - Outubro/2023 :cherry_blossom:")

st.subheader( 'Exemplo de HTML' , divider='rainbow')
st.image('./data/exemple.png', caption = "Exemplo de um documento SEI em HTML")

rema =  pd.read_excel('./data/rema.xlsx', engine='openpyxl')
st.subheader( 'Exemplo do DataFrame' , divider='rainbow')

st.dataframe(rema.head())
#  st.(divider='rainbow')
#     """
#     Escrever em resumo o objetivo do trabalho
#     ### Fontes dos Dados
#     - Documentos SEI em html 
#     - Manual da Rede de Litoteca
#     ### Ferramentas Utilizadas
#     Programa desenvolvido em linguagem Python e com o uso das bibliotecas
#     # Request
#     # Selenium
#     # BeautifulSoup
#     # Streamlit
#     # Pandas
#     # Plotly express
#     """
#     )

#video_file = open('https://youtu.be/adiF0AfB4Iw?si=d8lUhlsHwakTTKVO')
video_sei = 'https://youtu.be/adiF0AfB4Iw?si=d8lUhlsHwakTTKVO'

#video_sei = video_file.read()
st.video(video_sei)
