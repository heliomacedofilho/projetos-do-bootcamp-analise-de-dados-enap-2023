# pages/page3.py
import streamlit as st
import pandas as pd

st.set_page_config(page_icon=":large_blue_square:",
                   layout="wide")
st.header(':blue[Automação de Relatório de dados de Documentos]', divider='rainbow')
st.title('De arquivo em HTML para DataFrame')
st.caption("Projeto Final do Bootcamp de Análise de Dados - ENAP :game_die::game_die::game_die:")
st.caption("Turma Exclusiva para Mulheres - Outubro/2023 :cherry_blossom:")

st.subheader( 'Exemplo de HTML' , divider='rainbow')
st.image('./data/exemple.png', caption = "Exemplo de um documento SEI em HTML")

rema =  pd.read_excel('./data/rema.xlsx', engine='openpyxl')
st.subheader( 'Exemplo do DataFrame' , divider='rainbow')
st.dataframe(rema.head())

st.subheader('Visualizando o programa em funcionamento')
video_sei = 'https://youtu.be/adiF0AfB4Iw?si=d8lUhlsHwakTTKVO'
st.video(video_sei)
