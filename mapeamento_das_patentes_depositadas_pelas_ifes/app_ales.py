import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
from plotly.offline import iplot
pd.options.display.float_format = '{:.1f}'.format

st.set_page_config(page_title="Período de depósitos das patentes: 01/2018 a 01/2023", layout="wide")
st.title('Patentes depositadas entre 01/2018 e 01/2023')

df = pd.read_excel('dados_patentes_longo_AM.xlsx')
df['data_deposito'] = pd.to_datetime(df['data_deposito'], format="%d/%m/%Y")
df['ifes'] = df['ifes'].astype('category')
df['area'] = df['area'].astype('category')
df['regiao'] = df['regiao'].astype('category')
df['ipc'] = df['ipc'].astype('category')
df['parceria'] = df['parceria'].astype('category')

# Extrair o ano, o mês e mês/ano
df['ano_dep'] = df['data_deposito'].dt.year
df['mes_dep'] = df['data_deposito'].dt.month
df['mes_ano_dep'] = df.apply(lambda x: f"{x['mes_dep']:02d}/{x['ano_dep']}", axis=1)
df['ano_dep'] = df['ano_dep'].astype('int')
df['mes_dep'] = df['mes_dep'].astype('int')
df['mes_ano_dep'] = df['mes_ano_dep'].astype('str')

st.sidebar.title('Localização Geográfica do Titular da Patente')
filtro = st.sidebar.radio('Selecione uma opção' ,
                          ['Tudo', 'Brasil', 'Norte do Brasil', 'Nordeste do Brasil',
                           'Centro-Oeste do Brasil', 'Sudeste do Brasil', 'Sul do Brasil'])

if filtro == 'Brasil':
    df = df.loc[df['titular_pais'] == 'BR'].copy()
    st.title('Brasil')
elif filtro == 'Norte do Brasil':
    df = df.loc[df['regiao'] == 'Norte'].copy()
    st.title('Norte/BR')
elif filtro == 'Nordeste do Brasil':
    df = df.loc[df['regiao'] == 'Nordeste'].copy()
    st.title('Nordeste/BR')
elif filtro == 'Centro-Oeste do Brasil':
    df = df.loc[df['regiao'] == 'Centro-Oeste'].copy()
    st.title('Centro-Oeste/BR')
elif filtro == 'Sudeste do Brasil':
    df = df.loc[df['regiao'] == 'Sudeste'].copy()
    st.title('Sueste/BR')
elif filtro == 'Sul do Brasil':
    df = df.loc[df['regiao'] == 'Sul'].copy()
    st.title('Sul/BR')
    st.title('Todas')

IF = df[(df['ifes'] == 'Sim') & (df['responsavel'].str.contains('^INSTITUTO|^CENTRO'))].copy()
UV = df[(df['ifes'] == 'Sim') & (df['responsavel'].str.contains('^UNIVER'))].copy()
IFE = df[df['ifes'] == 'Sim'].copy()
NIFE = df[df['ifes'] == 'Não'].copy()

total_geral = df[df['data_deposito'] >= '2018-01-01']['ID'].nunique()
total_ifes = df.loc[(df['ifes'] == 'Sim') & (df['data_deposito'] >= '2018-01-01')]['ID'].nunique()
total_nifes = NIFE[(~NIFE['ID'].isin(IFE['ID'])) & (NIFE['data_deposito'] >= '2018-01-01')]['ID'].nunique()
    
st.metric('Quantidade de Patentes (geral)', total_geral)
st.metric('Quantidade de Patentes com participação de IFEs', total_ifes)
st.metric('Quantidade de Patentes sem paricipação de IFEs', total_nifes)

aba1, aba2, aba3, aba4 = st.tabs(['Todas instituições Federais de Ensino',
                                  'Institutos e Centros Federais',
                                  'Universidades Federais',
                                  'Outras instituições, empresas e organizações'])


def plot_graph(counts):
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.lineplot(x='mes_ano_dep', y='ID', data=counts)
    plt.xticks(rotation=90)  # Rotacionar os rótulos no eixo x para melhor legibilidade
    plt.xlabel('\nData de depósito da patente')
    plt.ylabel('Número absoluto de patentes depositadas\n')
    #plt.subplots_adjust(top=0.9,right = 0.9)
    # Ajuste a figura
    plt.tight_layout()
    # Mostre a figura no Streamlit
    st.pyplot(fig)

def plot_graph(counts):
    fig = px.line(counts,
                  x='mes_ano_dep', y='ID',
                  markers=True,
                  width=900, height=600,
                  labels={"ID": "Número absoluto de pantentes",
                          "mes_ano_dep": "Data de depósito"
                          },
                  template="simple_white")
    fig.update_xaxes(tickangle=-90)
    st.write(fig)


with aba1:

    st.title("Patentes com participação de instituições federais de ensino")
    data = IFE
    counts = data.loc[data['data_deposito'] >= '2018-01-01'].copy()
    counts = counts.groupby(['mes_dep', 'ano_dep', 'mes_ano_dep', 'ifes'], observed=True)['ID'].nunique().reset_index()
    counts = counts.sort_values(['ano_dep', 'mes_dep']).copy()
    plot_graph(counts)

with aba2:
    
    st.title("Patentes dcom participação de institutos e centros federais de ensino")
    data = IF
    counts = data.loc[data['data_deposito'] >= '2018-01-01'].copy()
    counts = counts.groupby(['mes_dep', 'ano_dep', 'mes_ano_dep', 'ifes'], observed=True)['ID'].nunique().reset_index()
    counts = counts.sort_values(['ano_dep', 'mes_dep']).copy()
    plot_graph(counts)
    
with aba3:   

    st.title("Patentes com participação de universidades federais de ensino")
    data = UV
    counts = data.loc[data['data_deposito'] >= '2018-01-01'].copy()
    counts = counts.groupby(['mes_dep', 'ano_dep', 'mes_ano_dep', 'ifes'], observed=True)['ID'].nunique().reset_index()
    counts = counts.sort_values(['ano_dep', 'mes_dep']).copy()
    plot_graph(counts)

with aba4:

    st.title('Patentes sem participação de instituições federais de ensino')
    data = NIFE
    counts = data.loc[data['data_deposito'] >= '2018-01-01'].copy()
    counts = counts.groupby(['mes_dep', 'ano_dep', 'mes_ano_dep', 'ifes'], observed=True)['ID'].nunique().reset_index()
    counts = counts.sort_values(['ano_dep', 'mes_dep']).copy()
    plot_graph(counts)