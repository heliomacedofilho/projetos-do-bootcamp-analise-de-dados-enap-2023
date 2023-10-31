from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
#from streamlit_option_menu import option_menu

#with st.echo("below"):
from st_pages import Page, Section, add_page_title, show_pages

"Projeto Final do Bootcamp de Análise de Dados - ENAP "

add_page_title()
st.header('Automação de Relatório de dados de Documentos','rainbow')
st.subheader(':blue[Automação de Relatório de dados de Documentos] :large_blue_square: :ok:')
st.subheader(':red[Gastos Hospitalares no Brasil] :hospital: :fire:')

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
        Page("pages/1_1_Dados_SEI.py", "Dados SEI", "📖"),
        Page("pages/1_2_SEI_Exemplo.py", "Exemplo SEI", "📖"),
        Page("pages/1_3_SEI_Estados.py", "Mapa de Requisições", "📖"),
        #Section(name="Gastos Saúde", icon=":hospital:"),
        # Will use the default icon and name based on the filename if you don't
        # pass them
        Page("pages/Gastos_Saude.py", icon=":hospital:"),
        Page("pages/2_Estados.py", icon=":hospital:"),
        Page("pages/3_Municipios.py", icon=":hospital:"),
        Page("pages/4_Dispersao.py", icon=":hospital:"),
        Page("pages/6_Regressao.py", icon=":hospital:"),
        # You can also pass in_section=False to a page to make it un-indented
        Page("pages/7_About.py", "About", "🧰", in_section=False)
    ]
)

#st.sidebar.success("Select a page")
# page_names_to_funcs = {
#     "Main Page": main_page,
#     "Page 2": page2,
#     "Page 3": page3,

# selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
# page_names_to_funcs[selected_page]()


# import dados, gastos

# st.set_page_config(
#     page_title="Menu",
#     #page_icon= ':large_blue_square:',
#     layout='wide',
# #    multi_app_icon='🎨'
#     initial_sidebar_state='auto'
#     )

# st.set_page_config(
#     page_title=“my app page 1”,
#     layout=“wide”,
#     initial_sidebar_state=“auto”,
#     multi_app_icon=*️⃣,
#     ordering=1
#     )



# class MultiApp:

#     def __init__(self):
#         self.apps = []

#     def add_app(self, title, func):

#         self.apps.append({
#             "title": title,
#             "function": func
#         })

#     def run():
#         with st.sidebar:
#             app = opition_menu(
#                 menu_title = ['Menu'],
#                 options = ['Dados SEI', 'Gastos'],
#                 icons = ['house-fill','trophy-pill'],
#                 menu_icons = 'chat-text-fill',
#                 default_index=1
#             )
#         if app == "Dados SEI":
#             dados.app()
#         if app == "Gastos":
#             gastos.app()

#     run()

# st.markdown(
#     f"""
#     <link
#         rel="stylesheet"
#         href="assets/styles.css"
#     >
#     """,
#     unsafe_allow_html=True
# )
# st.title("Projeto Final do Bootcamp de Análise de Dados - ENAP ")
# st.header('Automação de Relatório de dados de Documentos', divider='rainbow')
# st.subheader(':blue[Automação de Relatório de dados de Documentos] :large_blue_square: :ok:')
# st.subheader(':red[Gastos Hospitalares no Brasil] :hospital: :fire:')

        