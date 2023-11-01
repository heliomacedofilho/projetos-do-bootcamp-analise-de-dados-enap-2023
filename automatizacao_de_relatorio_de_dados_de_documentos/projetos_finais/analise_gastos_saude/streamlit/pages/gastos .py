# pages/page1.py
import streamlit as st

def app():

    st.set_page_config(
    page_title="Gastos Hospitalares",
    page_icon="🏥",
    layout='wide',
    initial_sidebar_state='expanded')

    st.title('Gastos Hospitalares no Brasil')
    #st.markdown('# Gastos Hospitalares no Brasil')
    #st.markdown("---")
    st.write("## Projeto Final do Bootcamp de Análise de Dados - ENAP")
    st.write("### Turma Exclusiva para Mulheres - Outubro/2023")
    st.sidebar.success("Select a page")


    st.markdown(
        """
        Escrever em resumo o objetivo do trabalho
        ### Fontes dos Dados
        - Escrever sobre DATASUS
        - API Portal da Transparência
        - IBGE - População
        ### Ferramentas Utilizadas
        Programa desenvolvido em linguagem Python e com o uso das bibliotecas streamlit, pandas, plotly express
        
    """
        )
