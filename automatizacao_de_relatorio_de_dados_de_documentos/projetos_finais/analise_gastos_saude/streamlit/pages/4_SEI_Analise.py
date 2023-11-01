import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Analise dos dados do SEI",
                   page_icon=":large_blue_square:",
                   layout="wide")

st.header(':blue[Automação de Relatório de dados de Documentos]', divider='rainbow')
st.title("Análise dos dados do SEI")
st.caption("Projeto Final do Bootcamp de Análise de Dados - ENAP :game_die::game_die::game_die:")
st.caption("Turma Exclusiva para Mulheres - Outubro/2023 :cherry_blossom:")

@st.cache_data
def gerar_df():
    df = pd.read_excel('./data/rema.xlsx',
                       engine='openpyxl')
                    
    return df

df_metodos = gerar_df()

st.header("Métodos Utilizados para os Empréstimos", divider='rainbow')
st.bar_chart(df_metodos
            .reset_index()
            .melt(id_vars=["index"], value_vars=df_metodos.columns[6:22],var_name = 'Métodos Analíticos')
            .query('value == True')
            .loc[:, 'Métodos Analíticos']
            .value_counts(ascending=True))
            
st.header("Finalidade dos Empréstimos", divider='rainbow')
st.line_chart(df_metodos
            .reset_index()
            .melt(id_vars=["index"], value_vars=df_metodos.columns[22:32],var_name = 'Finalidade')
            .query('value == True')
            .loc[:, 'Finalidade']
            .value_counts(ascending=True)) 
            

st.header("Tipo de Solicitantes", divider='rainbow')
fig = px.pie(df_metodos.iloc[:, 2].value_counts().reset_index(), values= 'count', names='Tipo de Solicitante', title='Tipo de Usuário')

st.plotly_chart(fig)


