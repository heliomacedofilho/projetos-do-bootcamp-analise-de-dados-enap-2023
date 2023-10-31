import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
from plotly.offline import iplot
pd.options.display.float_format = '{:.1f}'.format

st.set_page_config(layout="wide")
st.markdown("### Patentes depositadas entre Jan/2018 e Jan/2023")

df = pd.read_csv('dados_patentes_longo_AM.csv')
df['data_deposito'] = pd.to_datetime(df['data_deposito'], format="%d/%m/%Y")
df['ifes'] = df['ifes'].astype('category')
df['regiao'] = df['regiao'].astype('category')
df['parceria'] = df['parceria'].astype('category')

# Extrair o ano, o mês e mês/ano
df['ano_dep'] = df['data_deposito'].dt.year
df['mes_dep'] = df['data_deposito'].dt.month
df['mes_ano_dep'] = df.apply(lambda x: f"{x['mes_dep']:02d}/{x['ano_dep']}", axis=1)
df['ano_dep'] = df['ano_dep'].astype('int')
df['mes_dep'] = df['mes_dep'].astype('int')
df['mes_ano_dep'] = df['mes_ano_dep'].astype('str')

st.sidebar.markdown('#### Localização Geográfica do Titular da Patente')
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

aba1, aba2, aba3, aba4 = st.tabs(['Todas instituições Federais de Ensino',
                                  'Institutos e Centros Federais',
                                  'Universidades Federais',
                                  'Outras instituições, empresas e organizações'])


def plot_line(counts):
    fig=px.line(counts,
    x='mes_ano_dep', y='ID',
    color='parceria', 
    markers=True,
    width=900, height=600,
    labels={ # replaces default labels by column name
                "ID": "Número absoluto de pantentes",  
                "mes_ano_dep": "Data de depósito",
                "parceria": "Tipo de participação"
            },
    color_discrete_map={ # replaces default color mapping by value
                "Titular": "lightgreen", "Parceiro": "darkgreen"
            },
    template="simple_white")
    fig.update_xaxes(tickangle=-90)
    st.plotly_chart(fig)

def plot_pie(counts):
    fig=px.pie(counts,
    values='ID',
    names='parceria',
    color='parceria',
    width=900, height=600,
    labels={ # replaces default labels by column name
                "ID": "Número absoluto de pantentes",  
                "mes_ano_dep": "Data de depósito",
                "parceria": "Tipo de participação"
            },
    color_discrete_map={"Titular": "lightgreen", "Parceiro": "darkgreen"})
    fig.update_traces(hoverinfo='label+percent', textfont_size=18,
                  marker=dict(line=dict(color='#000000', width=2)))
    st.plotly_chart(fig)

with aba1:

    st.markdown("#### Série temporal das patentes com participação de instituições federais de ensino por tipo de participação")
    data = IFE
    counts = data.loc[data['data_deposito'] >= '2018-01-01'].copy()
    counts = counts.groupby(['mes_dep', 'ano_dep', 'mes_ano_dep', 'parceria'], observed=True)['ID'].nunique().reset_index()
    counts = counts.sort_values(['ano_dep', 'mes_dep']).copy()
    plot_line(counts)

    st.markdown("#### Distribuição percentual do total de patentes com participação de instituições federais de ensino por tipo de participação")
    counts = data.groupby('parceria', observed=True)['ID'].nunique().reset_index()
    plot_pie(counts)


with aba2:
    
    st.markdown("#### Série temporal das patentes com participação de institutos e centros federais de ensino por tipo de participação")
    data = IF
    counts = data.loc[data['data_deposito'] >= '2018-01-01'].copy()
    counts = counts.groupby(['mes_dep', 'ano_dep', 'mes_ano_dep', 'parceria'], observed=True)['ID'].nunique().reset_index()
    counts = counts.sort_values(['ano_dep', 'mes_dep']).copy()
    plot_line(counts)

    st.markdown("#### Distribuição percentual do total de patentes com participação de institutos e centros federais de ensino por tipo de participação")
    counts = data.groupby('parceria', observed=True)['ID'].nunique().reset_index()
    plot_pie(counts)

    
with aba3:   

    st.markdown("#### Série temporal das patentes com participação de universidades federais  por tipo de participação")
    data = UV
    counts = data.loc[data['data_deposito'] >= '2018-01-01'].copy()
    counts = counts.groupby(['mes_dep', 'ano_dep', 'mes_ano_dep', 'parceria'], observed=True)['ID'].nunique().reset_index()
    counts = counts.sort_values(['ano_dep', 'mes_dep']).copy()
    plot_line(counts)

    st.markdown("#### Distribuição percentual do total de patentes com participação de universidades federais por tipo de participação")
    counts = data.groupby('parceria', observed=True)['ID'].nunique().reset_index()
    plot_pie(counts)


with aba4:

    st.markdown("#### Série temporal das patentes sem participação de instituições federais de ensino por tipo de participação")
    data = NIFE
    counts = data.loc[data['data_deposito'] >= '2018-01-01'].copy()
    counts = counts.groupby(['mes_dep', 'ano_dep', 'mes_ano_dep', 'parceria'], observed=True)['ID'].nunique().reset_index()
    counts = counts.sort_values(['ano_dep', 'mes_dep']).copy()
    plot_line(counts)

    st.markdown("#### Distribuição percentual do total de patentes sem participação de instituições federais de ensino por tipo de participação")
    counts = data.groupby('parceria', observed=True)['ID'].nunique().reset_index()
    plot_pie(counts)
