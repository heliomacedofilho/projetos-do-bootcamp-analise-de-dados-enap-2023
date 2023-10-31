# pages/page1.py
import streamlit as st


st.set_page_config(
page_title="Home",
page_icon=":home:",
layout='wide',
initial_sidebar_state='auto')

st.title("Projeto Final do Bootcamp de Análise de Dados - ENAP")
st.caption("Turma Exclusiva para Mulheres - Outubro/2023")
#st.markdown('# Gastos Hospitalares no Brasil')
st.markdown(divider = 'rainbow')
st.subheader(':blue[Automação de Relatório de dados de Documentos SEI] :large_blue_square: :ok:')
st.subheader(':red[Gastos Hospitalares no Brasil] :hospital: :fire:')
st.sidebar.success("Select a page")


# st.markdown(
#     """
#     Escrever em resumo o objetivo do trabalho
#     ### Fontes dos Dados
#     - Escrever sobre DATASUS
#     - API Portal da Transparência
#     - IBGE - População
#     ### Ferramentas Utilizadas
#     Programa desenvolvido em linguagem Python e com o uso das bibliotecas streamlit, pandas, plotly express
    
# """
#     )
