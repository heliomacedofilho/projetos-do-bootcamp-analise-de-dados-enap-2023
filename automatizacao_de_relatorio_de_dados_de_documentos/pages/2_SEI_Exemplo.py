# pages/page3.py
import streamlit as st



st.set_page_config(
    page_title="Arquivos em HTML para DataFrame",
    page_icon= ':large_blue_square:',
    layout='wide',
    initial_sidebar_state='auto')

st.title('Arquivos em HTML para DataFrame :large_blue_square:')
    #st.markdown("---")
st.caption("Projeto Final do Bootcamp de Análise de Dados - ENAP")
st.subheader("Turma Exclusiva para Mulheres - Outubro/2023 :cherry_blossom: ", divider = 'rainbow')
st.sidebar('expanded')
#st.sidebar.success("Select a page")
st.image('\data\exemple.png', caption = "Exemplo de um documento SEI em HTML")

st.markdown(
    """
    Escrever em resumo o objetivo do trabalho
    ### Fontes dos Dados
    - Documentos SEI em html 
    - Manual da Rede de Litoteca
    ### Ferramentas Utilizadas
    Programa desenvolvido em linguagem Python e com o uso das bibliotecas
    # Request
    # Selenium
    # BeautifulSoup
    # Streamlit
    # Pandas
    # Plotly express
    """
    )
