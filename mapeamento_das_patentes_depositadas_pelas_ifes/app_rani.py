import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go
import plotly.offline as pyo
from plotly.offline import iplot
from datetime import timedelta
import numpy as np


st.set_page_config(page_title="Patentes Depositadas pelas IFES", layout="wide")
st.title("Patentes Depositadas pelas Instituições Federais de Ensino Superior")
st.markdown("---")
st.subheader("Análise das Patentes Depositadas pelas IFES como titulares")
st.sidebar.title('Titulares depositantes')

aba1, aba2 = st.tabs(['Gráfico e Tabela', 'Ranking'])
    
# Carregar os dados, transformar e agrupar
df_ifes = pd.read_csv('data_ifes.csv')
df_ifes['data_publicacao'] = pd.to_datetime(df_ifes['data_publicacao'], format='%d/%m/%Y')
df_ifes['data_deposito'] = pd.to_datetime(df_ifes['data_deposito'], format='%d/%m/%Y')
df_ifes['data_prioridade'] = pd.to_datetime(df_ifes['data_prioridade'], format='%d/%m/%Y')
df_ifes['ano_dep'] = df_ifes['data_deposito'].dt.year
df_ifes['mes_dep'] = df_ifes['data_deposito'].dt.month

with aba1:
    #Grafico 1
    st.write("### Número de Patentes depositadas por Mês e Ano (publicadas de 2020 a julho/2023)")
    # Agrupamentos necessarios
    df_mes = df_ifes.groupby(['ano_dep', 'mes_dep'])['titular_nome'].count().reset_index()
    df_mes['ano_mes_dep'] = df_mes.apply(lambda x: f"{x['ano_dep']}-{x['mes_dep']:02d}", axis=1)
    df_mes = df_mes.rename(columns={'titular_nome': 'Patentes', 'ano_dep': 'Ano', 'mes_dep': 'Mês', 'ano_mes_dep':'Ano_Mês'})
    df_mes_corte = df_mes[df_mes['Ano_Mês'] >= '2018-01']
    #Plotagem
    # Coordenadas dos picos (x e y)
    picos_x = ['2018-12','2019-12','2020-07','2021-12']
    picos_y = [132, 151, 124, 136 ]
    
    # Trace principal
    trace = go.Scatter(x=df_mes_corte['Ano_Mês'], y=df_mes_corte['Patentes'],
                        mode='lines+markers',
                        name='Números de Patentes depositadas pelas IFES',
                        line={'color': '#341f97', 'dash': 'dot'})
    
    # Traços dos picos com marcadores
    picos_trace = go.Scatter(x=picos_x, y=picos_y, mode='markers', marker=dict(size=10, color='red'),
                            name='Picos', text=['Pico 1', 'Pico 2', 'Pico 3', 'Pico 4'], textposition='top center')
    
    layout = go.Layout(yaxis=dict(range=[0, 160], showgrid=True),
                       xaxis=dict(range=['2018-01', df_mes_corte['Ano_Mês'].max()], title='Mês/Ano'),
                       width=800,  # Defina a largura do gráfico
                       height=600,  # Defina a altura do gráfico
                       legend=dict(orientation='h', y=-0.2))  # Reduza o tamanho da legenda
    
    fig2 = go.Figure(data=[trace, picos_trace], layout=layout)
    st.plotly_chart(fig2)

    
    #Tabela1
    
    # Obtenha a lista de instituições únicas
    instituicoes_unicas = df_ifes['titular_abv'].dropna().unique()  # Remova valores NaN e obtenha as instituições únicas
    
    # Classifique a lista em ordem alfabética
    instituicoes_unicas = sorted(instituicoes_unicas, key=str)
    
    # Crie um filtro selectbox
    selected_instituicao = st.selectbox('Selecione uma instituição', instituicoes_unicas)
    
    # Filtre os dados com base na instituição selecionada
    df_ifes_filtrado = df_ifes[df_ifes['titular_abv'] == selected_instituicao]

    # Formate a coluna "Data de Depósito" para mostrar apenas a data (dia/mês/ano)
    df_ifes_filtrado['data_deposito'] = df_ifes_filtrado['data_deposito'].dt.strftime('%d/%m/%Y')
    
    # Exiba a tabela com os dados filtrados
    st.write("### Tabela de IFES")
    df_ifes_display = df_ifes_filtrado[["titular_nome", "data_deposito", "numero", "numero_revista"]].rename(
        columns={"titular_nome": "Nome do Titular", "data_deposito": "Data de Depósito", "numero": "Natureza do depósito", "numero_revista": "Número da revista"}
    )
    st.write(df_ifes_display)

with aba2: 
    # GRAFICO RANKING
    df_ifes_rank = df_ifes.groupby('titular_abv').agg(contagem=('titular_abv', 'size')).reset_index()
    df_ifes_rank = df_ifes_rank.sort_values(by='contagem', ascending=False)
    
    fig = px.bar(df_ifes_rank.head(20), x='contagem', y='titular_abv',
                 labels={'titular_abv': 'Titular/Depositante', 'contagem': 'Número de Patentes'},
                 title='Ranking Geral das IFES Depositantes por Número de Patentes publicadas de 2020 a 2023 (julho)',
                 orientation='h',
                 text='contagem',
                color_discrete_sequence=['darkblue'])
    
    # Inverta o eixo Y e ajuste a ordem
    fig.update_yaxes(categoryorder='total ascending')
    
    # Ajuste a cor e tamanho da fonte das labels do eixo Y
    fig.update_layout(yaxis_title_font=dict(size=14, color='black'))
    
    # Remova a legenda
    fig.update_layout(showlegend=False)
    
    # Aumente o tamanho do gráfico
    fig.update_layout(width=900, height=600)
    
    # Exiba o gráfico interativo no Streamlit
    st.plotly_chart(fig)

    #GRAFICO 2 RANKING
    st.write("Ranking das IFES Depositantes por Ano")
    
    # Realize a análise e gere o gráfico
    df_ifes_ano_rank = df_ifes.groupby(['titular_abv', 'ano_dep']).agg(contagem=('titular_abv', 'size')).reset_index()
    df_ifes_ano_rank = df_ifes_ano_rank.sort_values(by=['ano_dep', 'contagem', 'titular_abv'], ascending=[True, False, True])
    df_ifes_ano_rank = df_ifes_ano_rank[df_ifes_ano_rank['ano_dep'] > 2017]
    
    # Filtrar dados para os anos desejados
    anos_desejados = [2019, 2020, 2021]
    
    # Criar subgráficos para os anos desejados
    fig, axs = plt.subplots(1, len(anos_desejados), figsize=(15, 5))
    
    for i, ano in enumerate(anos_desejados):
        df_ano_filtrado = df_ifes_ano_rank[df_ifes_ano_rank['ano_dep'] == ano]
        df_ano_filtrado = df_ano_filtrado.nlargest(10, 'contagem')
    
        axs[i].barh(df_ano_filtrado['titular_abv'], df_ano_filtrado['contagem'], color='skyblue')
        axs[i].set_title(f'Ranking de IFES Depositantes em {ano}')
        axs[i].set_xlabel('Patentes depositadas')
        axs[i].set_ylabel('Instituição Federal')
        axs[i].invert_yaxis()  # Inverter o eixo y para exibir do maior para o menor
    
    plt.tight_layout()
    
    # Exiba o gráfico no Streamlit
    st.pyplot(fig)   