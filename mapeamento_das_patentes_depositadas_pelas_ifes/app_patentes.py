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
with st.container():
    st.markdown('# Mapeamento das IFES e Institutos Federais')
    st.markdown("---")
    st.sidebar.title('Áreas Tecnológicas')
    st.sidebar.selectbox('Área Tecnologica',('Nacional','Por Região e Estado'))
    
    

@st.cache_data    

def carregar_dados():
        
    dados=pd.read_csv("area_tecnologica.csv")
    return dados

        
with st.container():
    
    dados_tratado=carregar_dados()
    #grouped=dados.groupby('Area').agg(contagem=('Area','count')).sort_values(by='contagem',ascending=False)
    
    #opcoes=st.selectbox("Selecione a Opção",["Todas Instituições", "Universidades","Institutos Federais"])
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
    ('Todas Instituições','Institutos e Centros Federais', 'Universidades'))

    # Filtragem de dados baseada na seleção
    if option == 'Todas Instituições':
        data_analise = dados_tratado
        pallete="Wistia"
        title = "Área Tecnológica: Todas Instituições"
        
    elif option == 'Institutos e Centros Federais':
        data_analise = dados_tratado[
            dados_tratado['titular_1'].str.contains('^INSTITUTO|^CENTRO FEDERAL') |
            dados_tratado['titular_parceiros1'].str.contains('^INSTITUTO|^CENTRO FEDERAL') |
            dados_tratado['titular_parceiros2'].str.contains('^INSTITUTO|^CENTRO FEDERAL')
        ]
        pallete="YlGn"
        title = "Área Tecnológica: Institutos e Centros Federais"
    elif option == 'Universidades':
        data_analise = dados_tratado[
            dados_tratado['titular_1'].str.contains('UNIVER') |
            dados_tratado['titular_parceiros1'].str.contains('^UNIVER') |
            dados_tratado['titular_parceiros2'].str.contains('^UNIVER')
        ]
        pallete="YlGnBu"
        title = "Área Tecnológica: Universidades"
        

    # Agrupe os dados filtrados
    grouped_data = data_analise.groupby('Area').agg(contagem=('Area','count')).sort_values(by='contagem',ascending=False)

    # Mostre o gráfico
    plot_graph(grouped_data)


