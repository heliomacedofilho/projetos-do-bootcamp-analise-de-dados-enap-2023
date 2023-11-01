import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

from st_pages import Page, Section, add_page_title, show_pages

"## Declaring the pages in your app:"

show_pages(
    [
        Page("example_app/streamlit_app_sections.py", "Home", "🏠"),
        # Can use :<icon-name>: or the actual icon
        Page("example_app/example_one.py", "Example One", ":books:"),
        # Since this is a Section, all the pages underneath it will be indented
        # The section itself will look like a normal page, but it won't be clickable
        Section(name="Cool apps", icon=":pig:"),
        # The pages appear in the order you pass them
        Page("example_app/example_four.py", "Example Four", "📖"),
        Page("example_app/example_two.py", "Example Two", "✏️"),
        Section(name="Other apps", icon=":horse:"),
        # Will use the default icon and name based on the filename if you don't
        # pass them
        Page("example_app/example_three.py"),
        # You can also pass in_section=False to a page to make it un-indented
        Page("example_app/example_five.py", "Example Five", "🧰", in_section=False),
    ]
)

add_page_title()



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

        