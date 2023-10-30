import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import plotly.graph_objs as go
import plotly.offline as pyo
from plotly.offline import iplot
from datetime import timedelta
import numpy as np


st.set_page_config(page_title="Patentes Depositadas pelas Intituições Federais de Ensino", layout="wide")

st.markdown('# Mapeamento das IFES e Institutos Federais')
st.markdown("---")
st.sidebar.title('Áreas Tecnológicas')
#st.sidebar.selectbox('Área Tecnologica',('Nacional','Por Região e Estado'))

aba1, aba2 = st.tabs(['Nacional', 'Região e Estado'])

    

@st.cache_data    

def carregar_dados():
        
    dados=pd.read_csv("area_tecnologica.csv")
    return dados

dados_tratado=carregar_dados()

data_analise_IF = dados_tratado[
    dados_tratado['titular_1'].str.contains('^INSTITUTO|^CENTRO FEDERAL') |
    dados_tratado['titular_parceiros1'].str.contains('^INSTITUTO|^CENTRO FEDERAL') |
    dados_tratado['titular_parceiros2'].str.contains('^INSTITUTO|^CENTRO FEDERAL')
]

data_analise_UV = dados_tratado[
    dados_tratado['titular_1'].str.contains('UNIVER') |
    dados_tratado['titular_parceiros1'].str.contains('^UNIVER') |
    dados_tratado['titular_parceiros2'].str.contains('^UNIVER')
]
data_analise_total=pd.concat([data_analise_IF, data_analise_UV])

with aba1:
       
   
    def plot_graph(grouped):
       
        
        fig, ax = plt.subplots(figsize=(8, 6))

        # Crie o gráfico de barras usando seaborn
        sns.barplot(x="contagem", y="Area", 
                    hue="contagem", data=grouped.head(5), 
                    palette=pallete, ax=ax)

        # Ajuste os rótulos e o título
        ax.set_ylabel("Área Tecnológica", size=14) 
        ax.set_xlabel("Contagem", size=14) 
        ax.set_title(title, size=16)
        
        plt.subplots_adjust(top=0.9,right = 0.9)
        
        # Ajuste a figura
        plt.tight_layout()

        # Mostre a figura no Streamlit
        st.pyplot(fig)

    option = st.selectbox(
    'Escolha o grupo de dados:',
    ('Todas Instituições','Institutos e Centros Federais', 'Universidades'),key='unique_key_1' )

    # Filtragem de dados baseada na seleção
    if option == 'Todas Instituições':
        data_analise = data_analise_total
        pallete="Wistia"
        title = "Área Tecnológica: Todas Instituições"
        
    elif option == 'Institutos e Centros Federais':
        data_analise =data_analise_IF
        pallete="YlGn_d"
        title = "Área Tecnológica: Institutos e Centros Federais"
    elif option == 'Universidades':
        data_analise = data_analise_UV
        pallete="YlGnBu_d"
        title = "Área Tecnológica: Universidades"
        

    # Agrupe os dados filtrados
    grouped_data = data_analise.groupby('Area').agg(contagem=('Area','count')).sort_values(by='contagem',ascending=False)

    # Mostre o gráfico
    plot_graph(grouped_data)

with aba2:
    
    
    def generate_treemap(data):
        grouped_regiao = data.groupby(['Regiao', 'titular_uf1', 'Area']).agg(contagem=('Area', 'count'))
        grouped_regiao_sorted = grouped_regiao.sort_values(by=['titular_uf1', 'contagem'], ascending=[True, False])
        top_5_per_state = grouped_regiao_sorted.groupby('titular_uf1').head(5).reset_index()

        fig = px.treemap(top_5_per_state, 
                         path=[px.Constant("Brasil"),'Regiao', 'titular_uf1', 'Area'], 
                         values='contagem', 
                         color='Area',
                         color_continuous_scale='RdBu')
        fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))

        st.plotly_chart(fig)

          
    option = st.selectbox(
    'Escolha o grupo de dados:',
    ('Todas Instituições','Institutos e Centros Federais', 'Universidades'),key='unique_key_2' )
    
    if option == 'Todas Instituições':
        generate_treemap(data_analise_total)
    elif option == 'Institutos e Centros Federais':
        generate_treemap(data_analise_IF)
    elif option == 'Universidades':
        generate_treemap(data_analise_UV)



    


