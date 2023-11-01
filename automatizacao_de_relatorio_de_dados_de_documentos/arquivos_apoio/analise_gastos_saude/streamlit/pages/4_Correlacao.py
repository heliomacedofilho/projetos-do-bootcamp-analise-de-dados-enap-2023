import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="Correlação", page_icon="🏥", layout="wide")

st.title('_Análise de Correlação_ :hospital:')
st.markdown("---")


@st.cache_data
def gerar_df():
    df = pd.read_excel('./data/variaveis_uf_ano.xlsx',
                       engine='openpyxl',
                       usecols='A:F',
                       nrows=244)
    return df


df = gerar_df()
nomes_originais = ['Gastos Hospitalares', 'Gastos Hosp. per capita']

anos = ['Escolha o ano', '2014', '2015', '2016',
        '2017', '2018', '2019', '2020', '2021', '2022']


with st.sidebar:
    st.sidebar.header("Nível de Agregação: UF")
    st.subheader('Seleção de Filtros')
    fvariavel = st.selectbox('Selecione a Variável:', options=nomes_originais)
    fano = st.selectbox('Selecione o Ano:', options=anos)

# filtrando a variável desejada
nomes_alvo = ['gastos', 'gastos_percapita', 'mortalidade', 'valor_emendas']
mapeamento = dict(zip(nomes_originais, nomes_alvo))
nome_alvo = mapeamento.get(fvariavel, fvariavel)
df_filtro = df[nome_alvo]

# filtrando ano
# filtrando ano
if fano != anos[0]:
    dados_usuario = df.loc[(df['ano'] == int(fano))]
else:
    dados_usuario = df.loc[(df['ano'] == 2022)]

dados_usuario['text'] = dados_usuario['uf']

fig_scatter_mortalidade = px.scatter(dados_usuario, x='mortalidade', y=nome_alvo, title=fvariavel, template='plotly_dark', text='text').update_layout(
    title_x=0.5).update_xaxes(title='Mortalidade', showgrid=False).update_yaxes(
    title=fvariavel, showgrid=False)
st.plotly_chart(fig_scatter_mortalidade, theme=None, use_container_width=True)

fig_scatter_emendas = px.scatter(dados_usuario, x='valor_emendas', y=nome_alvo, title=fvariavel, template='plotly_dark', text='text').update_layout(
    title_x=0.5).update_xaxes(title='Emendas Parlamentares', showgrid=False).update_yaxes(
    title=fvariavel, showgrid=False)
st.plotly_chart(fig_scatter_emendas, theme=None, use_container_width=True)
