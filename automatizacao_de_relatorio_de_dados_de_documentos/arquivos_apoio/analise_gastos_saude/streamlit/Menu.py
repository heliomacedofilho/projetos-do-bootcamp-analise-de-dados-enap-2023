from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
#from streamlit_option_menu import option_menu
from st_pages import Page, Section, add_page_title, show_pages
#"Projeto Final do Bootcamp de Análise de Dados - ENAP "

#with st.echo("below"):
from st_pages import Page, Section, add_page_title, show_pages
show_pages(
        [
        Page("pages/1_Home.py", "Home", "🏠"),
        # Can use :<icon-name>: or the actual icon
        #Page("pages/example_one.py", "Example One", ":books:"),
        # Since this is a Section, all the pages underneath it will be indented
        # The section itself will look like a normal page, but it won't be clickable
        #Section(name="Automação SEI", icon="📖"),
        #Page("pages/1_2_SEI_Exemplo.py", icon="📖"),
        # The pages appear in the order you pass them
        Page("pages/1_Projeto_SEI.py", "Projeto SEI", "📖"),
        Page("pages/2_SEI_Exemplo.py", "HTML para DataFrame", "📖"),
        Page("pages/3_SEI_Estados.py", "Mapa de Requisições", "📖"),
        Page("pages/4_SEI_Analise.py", "Análises da Requisições", "📖"),
        #Section(name="Gastos Saúde", icon=":hospital:"),
        # Will use the default icon and name based on the filename if you don't
        # pass them
        Page("pages/1_Projeto_Saude.py", icon=":hospital:"),
        Page("pages/2_Estados.py", icon=":hospital:"),
        Page("pages/3_Municipios.py", icon=":hospital:"),
        Page("pages/4_Correlacao.py", icon=":hospital:"),
        Page("pages/6_Regressao.py", icon=":hospital:"),
        # You can also pass in_section=False to a page to make it un-indented
        Page("pages/7_Equipe.py", "Equipe", "🧰", in_section=False)
        ]
    )
    
add_page_title()
st.header('Automatização de Relatório de dados de Documentos')
st.caption("Projeto Final do Bootcamp de Análise de Dados - ENAP :game_die::game_die::game_die:")
st.caption("Turma Exclusiva para Mulheres - Outubro/2023 :cherry_blossom:")
st.subheader(':blue[Automação de Relatório de dados de Documentos] :large_blue_square: :ok:')
st.subheader(':red[Gastos Hospitalares no Brasil] :hospital: :fire:', divider='rainbow')
