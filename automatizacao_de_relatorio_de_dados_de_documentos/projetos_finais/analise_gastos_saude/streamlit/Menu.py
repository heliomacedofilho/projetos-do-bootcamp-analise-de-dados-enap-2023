from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
#from streamlit_option_menu import option_menu
from st_pages import Page, Section, add_page_title, show_pages


from st_pages import Page, Section, add_page_title, show_pages
show_pages(
        [
        Page("pages/1_Home.py", "Início", "🏠"),
            
        Page("pages/1_Projeto_SEI.py", "Projeto SEI", "📖"),
        Page("pages/2_SEI_Exemplo.py", "HTML para DataFrame", "📖"),
        Page("pages/3_SEI_Estados.py", "Mapa de Requisições", "📖"),
        Page("pages/4_SEI_Analise.py", "Análises da Requisições", "📖"),
       
        Page("pages/1_Projeto_Saude.py", "Projeto Saúde", icon=":hospital:"),
        Page("pages/2_Estados.py", "Análise Descritiva por UF", icon=":hospital:"),
        Page("pages/3_Municipios.py", "Mapas Gastos Hospitalares por UF", icon=":hospital:"),
        Page("pages/4_Correlacao.py", "Correlações", icon=":hospital:"),
        Page("pages/6_Regressao.py", "Regressões", icon=":hospital:"),
       
        Page("pages/7_Equipe.py", "Equipe", "👩‍💻", in_section=False)
        ]
    )
    
add_page_title()
st.header('Automatização de Relatório de dados de Documentos SEI')
st.caption("Projeto Final do Bootcamp de Análise de Dados - ENAP :game_die::game_die::game_die:")
st.caption("Turma Exclusiva para Mulheres - Outubro/2023 :cherry_blossom:")
st.subheader(':blue[Automação de Relatório de dados de Documentos] :large_blue_square: :ok:')
st.subheader(':red[Gastos Hospitalares no Brasil] :hospital: :fire:', divider='rainbow')
