import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
import warnings
import datetime
import calendar
import json
import requests
from dash import Dash, dcc, html, Input, Output
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt, timedelta

warnings.filterwarnings('ignore')

st.set_page_config(page_title="Monitor endividamento", page_icon=":bar_chart:", layout="wide", initial_sidebar_state="collapsed", 
                   menu_items={'About': "Teste"})


#Desabilitar o hover no celular

# disable_hover_plotly_css = """
# <style>
# @media (hover: none), (pointer: coarse) {
#     /* Desativar hover nos elementos Plotly com a classe 'nsewdrag drag' */
#     .nsewdrag.drag {
#         pointer-events: none !important;
#     }
# }
# </style>
# """

#st.markdown(disable_hover_plotly_css, unsafe_allow_html=True)

#Início da página

st.title(":bar_chart: Monitor do endividamento dos brasileiros")

link = "https://sobremonitordoendividamento.readthedocs.io"

st.info(f'Para facilitar a sua análise, todos os valores já estão deflacionados!\n\n'
        f'Quer conferir mais detalhes sobre este projeto ou entrar em contato conosco? Clique [aqui]({link})',
        icon="👩‍💻")

#Fazer o filtro
@st.cache_data()
def load_data():
    data = pd.read_csv('analise_divida_tempo.csv')
    data['data_base'] = pd.to_datetime(data['data_base'])
    return data

df_intervalobase = load_data()

min_data = df_intervalobase['data_base'].min().replace(day=1).to_pydatetime()
max_data = df_intervalobase['data_base'].max().replace(day=1).to_pydatetime()

intervalo_data = st.slider(
    "Para qual intervalo você deseja visualizar as informações?",
    value=(min_data, max_data),
    format="MM/YYYY",
    min_value=min_data,
    max_value=max_data
)

data_inicio, data_fim = intervalo_data

date1 = data_inicio.strftime("%Y-%m")

date2 = data_fim.strftime("%Y-%m")

ano1 = data_inicio.strftime("%Y")

ano2 = data_fim.strftime("%Y")

def muda_ordem_data(data_y_m):
    ano, mes = data_y_m.split('-')
    return f'{mes}/{ano}'

st.write(f'Exibindo dados para o intervalo {muda_ordem_data(date1)} a {muda_ordem_data(date2)}.', unsafe_allow_html=True)


#Funções-chaves

#Carregar dados
@st.cache_data()
def load_data(arquivo, coluna_data):
    data = pd.read_csv(arquivo, encoding="UTF-8", delimiter=',', decimal='.')
    data[coluna_data] = pd.to_datetime(data[coluna_data], format='%Y-%m-%d')
    data[coluna_data] = data[coluna_data].dt.strftime("%Y-%m")
    return data

@st.cache_data()
def load_data_apenas_ano(arquivo, coluna_data):
    data = pd.read_csv(arquivo, encoding="UTF-8", delimiter=',', decimal='.')
    data[coluna_data] = pd.to_datetime(data[coluna_data], format='%Y')
    data[coluna_data] = data[coluna_data].dt.strftime("%Y")
    return data

@st.cache_data()
def load_data_ano_mes(arquivo, coluna_data):
    data = pd.read_csv(arquivo, encoding="UTF-8", delimiter=',', decimal='.')
    return data

#Filtrar dados
@st.cache_data()
def filter_data(data, coluna_data, filtro, coluna_filtro, data_inicio=None, data_fim=None):
    if data_inicio is None:
        data_inicio = date1
    if data_fim is None:
        data_fim = date2
    filtered_data = data[(data[coluna_data] >= data_inicio) & (data[coluna_data] <= data_fim)]
    if filtro is not None and coluna_filtro is not None:
        filtered_data = filtered_data[filtered_data[coluna_filtro] == filtro]
    return filtered_data

st.subheader("Como está o endividamento da população brasileira?")

st.markdown("""
<div style='text-align: center; color: #555555; font-size: 1.3em; margin-bottom: 20px;'>
    Endividamento dos brasileiros de acordo com a sua ocupação
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: left; color: #666666; font-size: 1em; background-color: #f0f0f0; padding: 10px; border-radius: 5px;margin-bottom: 20px;'>
    💡&nbsp;&nbsp;&nbsp;Nos gráficos abaixo, a lista de ocupações é proveniente do cadastro da Receita Federal e está vínculada natureza da ocupação principal do cliente que contrata a operação de crédito. Por sua vez, o endividamento total é a soma das parcelas de crédito contratadas para qualquer prazo de vencimento. Já a informação sobre o endividamento por Estado considera o CEP de residência do contratante da operação, enquanto o ativo problemático se refere à parcela de crédito em que há pouca expectativa de pagamento.
</div>
""", unsafe_allow_html=True)

pf_ocupacao_modalidade_endividamento = load_data(arquivo="pf_ocupacao_modalidade_endividamento.csv", 
                                                 coluna_data="data_base")

ocupacao = st.selectbox(
    'Para qual ocupação você deseja visualizar?',
    pf_ocupacao_modalidade_endividamento['ocupacao'].unique()
)

pf_ocupacao_modalidade_endividamento_filtrado = filter_data(
    data=pf_ocupacao_modalidade_endividamento, 
    coluna_data="data_base", 
    filtro=ocupacao, 
    coluna_filtro="ocupacao",
    data_inicio=date1,
    data_fim=date2
)

col1, col2 = st.columns((2))

with col1:
    
    st.markdown("<div style='text-align: center; color: #888888; font-size: 0.9em;margin-bottom: 20px;margin-top: 20px;'>Endividamento por modalidade da operação de crédito e ocupação dos contratantes</div>", unsafe_allow_html=True)
    
    # Criação do gráfico
    plot_pf_ocupacao_modalidade_endividamento = px.line(pf_ocupacao_modalidade_endividamento_filtrado, 
                                                        x='data_base',
                                                        y='carteira_ativa_deflacionada', 
                                                        color='modalidade')

    plot_pf_ocupacao_modalidade_endividamento.update_layout(template="seaborn",
        legend=dict(
            x=0.5,  
            y=-0.2,
            traceorder='normal',
            orientation='h',
            xanchor='center',  
            yanchor='top',
            title="Modalidade da operação de crédito"
        ),
        yaxis=dict(
            showgrid=False,
            title="Endividamento total"
        ),
        xaxis=dict(showgrid=False,
                  title="Ano"),
        margin=dict(t=0, b=0, l=0, r=0),
        dragmode=False
    )
        
    st.plotly_chart(plot_pf_ocupacao_modalidade_endividamento, use_container_width=True)

with col2:
    
    st.markdown("<div style='text-align: center; color: #888888; font-size: 0.9em;margin-bottom: 20px;margin-top: 20px;'>Distribuição geográfica do ativo problemático por Estado de residência e ocupação dos contratantes</div>", unsafe_allow_html=True)

    @st.cache_data()
    def load_geojson_data():
        url = "https://raw.githubusercontent.com/jonates/opendata/master/arquivos_geoespaciais/unidades_da_federacao.json"
        response = requests.get(url)
        return response.json()
    
    
    df_ocupacao_pf_ativoproblematico = load_data_apenas_ano(arquivo = "df_ocupacao_pf_ativoproblematico.csv",
                                                coluna_data = "ano")
    
    df_ocupacao_pf_ativoproblematico_filtered = filter_data(data = df_ocupacao_pf_ativoproblematico,
                                                            coluna_data = "ano",
                                                            filtro = ocupacao,
                                                            coluna_filtro = "ocupacao",
                                                            data_inicio = ano1,
                                                            data_fim = ano2)

    geojson_data = load_geojson_data()

    plot_ocupacao_pf_ativoproblematico = px.choropleth_mapbox(df_ocupacao_pf_ativoproblematico_filtered, 
                                   geojson=geojson_data, 
                                   locations='Estado', 
                                   color='ativo_problematico/pop',
                                   color_continuous_scale="YlOrRd",
                                   range_color=(0, max(df_ocupacao_pf_ativoproblematico_filtered['ativo_problematico/pop'])),
                                   animation_frame='ano', 
                                   mapbox_style="open-street-map",
                                   zoom=2.2, 
                                   center={"lat": -15, "lon": -57.33},
                                   opacity=1,
                                   labels={'ativo_problematico/pop':'Ativo problemático/População',
                                           'uf': 'Unidade da Federação do Brasil'},
                                   featureidkey="properties.NM_ESTADO")

    plot_ocupacao_pf_ativoproblematico.update_layout(
        coloraxis_colorbar=dict(
            len=1, 
            y=-0.25,  
            yanchor='bottom',  
            xanchor='center',
            x=0.5,   
            orientation='h',  
            title="Ativo problemático/População",
            titleside = "bottom"
        ),
            margin=dict(t=0, b=0, l=0, r=0))
    
    st.plotly_chart(plot_ocupacao_pf_ativoproblematico,use_container_width=True)

st.markdown("<div style='text-align: center; color: #555555; font-size: 1.3em;margin-bottom: 20px;'>Endividamento dos brasileiros de acordo com a sua renda</div>", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: left; color: #666666; font-size: 1em; background-color: #f0f0f0; padding: 10px; border-radius: 5px;margin-bottom: 20px;'>
    💡&nbsp;&nbsp;&nbsp; Nos gráficos abaixo, a faixa de rendimento dos tomadores de crédito se refere ao porte do cliente conforme classificação do Sistema de Operações de Crédito. Para o cálculo do endividamento de longo prazo foram consideradas todas as parcelas com prazo de vencimento acima de 360 dias. Quanto ao cálculo da quantidade de operações, foram desconsideradas as séries agregadas em que o número de operações é inferior ou igual a 15.
</div>
""", unsafe_allow_html=True)

pf_rendimento_modalidade_noperacoes_endividamento = load_data(arquivo = "pf_rendimento_modalidade_noperacoes_endividamento.csv",
                                                              coluna_data = "data_base")

porte = st.selectbox(
    "Para qual faixa rendimento você deseja visualizar?",
    pf_rendimento_modalidade_noperacoes_endividamento['porte'].unique()
)

pf_rendimento_modalidade_noperacoes_endividamento_filtrado = filter_data(
                                                             data=pf_rendimento_modalidade_noperacoes_endividamento, 
                                                             coluna_data="data_base", filtro=porte, 
                                                             coluna_filtro="porte",
                                                             data_inicio=date1,
                                                             data_fim=date2)


col20, col21 = st.columns((2))

with col20:
    st.markdown("<div style='text-align: center; color: #888888; font-size: 0.9em;margin-bottom: 20px;margin-top: 20px;'>Endividamento de longo prazo por modalidade da operação de crédito e renda dos contratantes</div>", unsafe_allow_html=True)

    plot_rendimento_modalidade_noperacoes = px.line(pf_rendimento_modalidade_noperacoes_endividamento_filtrado, 
                  x='data_base', 
                  y='longo_prazo_deflacionado', 
                  color='modalidade')

    plot_rendimento_modalidade_noperacoes.update_layout(
    title_text='',
    template="seaborn",
    legend=dict(
        x=0.5,
        y=-0.2,
        orientation='h',
        xanchor='center',
        traceorder='normal', 
        title='Modalidade da operação de crédito'
    ),
    xaxis=dict(showgrid=False, title='Ano'),
    yaxis=dict(
        showgrid=False, 
        title='Endividamento de longo prazo'
    ),
    margin=dict(t=0, b=0, l=0, r=0),
    dragmode=False
    ) 
        
    st.plotly_chart(plot_rendimento_modalidade_noperacoes, use_container_width=True)

with col21:
    
    st.markdown("<div style='text-align: center; color: #888888; font-size: 0.9em;margin-bottom: 20px;margin-top: 20px;'>Quantidade de operações de crédito por modalidade e renda dos contrantantes</div>", unsafe_allow_html=True)

    plot_rendimento_modalidade_noperacoes = px.line(pf_rendimento_modalidade_noperacoes_endividamento_filtrado, 
                  x='data_base', 
                  y='numero_de_operacoes', 
                  color='modalidade')

    plot_rendimento_modalidade_noperacoes.update_layout(
        title_text='',
        template="seaborn",
        legend=dict(
            x=0.5,
            y=-0.2,
            orientation='h',
            xanchor='center',
            traceorder='normal', 
            title="Modalidade da operação de crédito"
        ),
        xaxis=dict(showgrid=False, title = 'Ano'),
        yaxis=dict(showgrid=False, title = 'Quantidade de operações'),
        margin=dict(t=0, b=0, l=0, r=0),
        dragmode=False
    )
            
    st.plotly_chart(plot_rendimento_modalidade_noperacoes, use_container_width=True)

st.markdown("<div style='text-align: center; color: #555555; font-size: 1.3em;margin-bottom: 20px;margin-bottom: 20px;'>Relação do endividamento dos brasileiros com dados macroeconômicos</div>", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: left; color: #666666; font-size: 1em; background-color: #f0f0f0; padding: 10px; border-radius: 5px;margin-bottom: 20px;margin-bottom: 20px;'>
    💡&nbsp;&nbsp;&nbsp;Nos gráficos abaixo são apresentadas a relação do endividamento dos brasileiros com os principais indicadores da atividade econômica do país. O Índice Nacional de Preços ao Consumidor Amplo (IPCA) mensura a variação do custo de vida médio das famílias, enquanto a taxa de de desocupação é o percentual de pessoas na força de trabalho que estão desempregados. Ambos são calculados pelo IBGE. Já a taxa média mensal de juros se refere à taxa contratada pelas pessoas físicas nas instituições financeiras e é disponibilizada pelo Banco Central do Brasil. Por sua vez, no cálculo do endividamento de longo prazo foram consideradas as parcelas de crédito com vencimento maior do que 360 dias, enquanto o endividamento total considera todas as operações. 
<br>
<br>
Conforme classificação adotada pela Fundação Getúlio Vargas, considerou-se baixa renda os contrantes com rendimento de até dois salários mínimos e alta renda os contratantes com rendimento acima de cinco salários mínimos.
</div>
""", unsafe_allow_html=True)

df_juros_inflacao_modalidade = load_data_ano_mes(arquivo = "df_juros_inflacao_modalidade.csv", coluna_data = "data_base")

indicador_macro = st.selectbox(
        'Selecione o indicador macroeconômico que você deseja visualizar na série',
        ('IPCA', 'Taxa média mensal de juros - PF')
    )

df_juros_inflacao_modalidade_filtrado = filter_data(data = df_juros_inflacao_modalidade,
                                                    coluna_data = "data_base",
                                                    filtro=indicador_macro,
                                                    coluna_filtro=None,
                                                    data_inicio=date1,
                                                    data_fim=date2)

def create_figure(yaxis_column_name):
    plot_juros_inflacao_modalidade = go.Figure()

    for modalidade in df_juros_inflacao_modalidade_filtrado['modalidade'].unique():
        subset = df_juros_inflacao_modalidade_filtrado[df_juros_inflacao_modalidade_filtrado['modalidade'] == modalidade]
        plot_juros_inflacao_modalidade.add_trace(go.Scatter(x=subset['data_base'],
                                     y=subset['longo_prazo_deflacionado'],
                                     mode='lines',
                                     name=f'{modalidade}',
                                     yaxis='y2',
                                     opacity=0.7,
                                     line=dict(width=2)))

    plot_juros_inflacao_modalidade.add_trace(go.Scatter(x=df_juros_inflacao_modalidade_filtrado['data_base'],
                                 y=df_juros_inflacao_modalidade_filtrado[yaxis_column_name],
                                 mode='lines',
                                 opacity=1,
                                 name=yaxis_column_name,
                                 line=dict(color='dimgray', width=2, dash='dot')))

    plot_juros_inflacao_modalidade.update_layout(
        title_text='',
        yaxis2=dict(
            overlaying='y',
            side='right',
            showgrid=False,
            title="Endividamento de longo prazo"
        ),
        template="seaborn",
        legend=dict(
            x=0.5,
            y=-0.2,
            orientation='h',
            xanchor='center',
            traceorder='normal',
            yanchor='top',
            title = 'Modalidade da operação de crédito'
            ),
        xaxis=dict(showgrid=False, title = 'Ano'),
        yaxis=dict(
            showgrid=False,
            title=yaxis_column_name
        ),
        margin=dict(t=0, l=0, r=0, b=0),
        dragmode=False
    )
        
    return plot_juros_inflacao_modalidade


    
st.markdown("<div style='text-align: center; color: #888888; font-size: 0.9em;margin-bottom: 20px;margin-top: 20px;'>Endividamento de longo prazo por modalidades de contratação</div>", unsafe_allow_html=True)

st.plotly_chart(create_figure(indicador_macro), use_container_width=True)

st.markdown("<div style='text-align: center; color: #888888; font-size: 0.9em;margin-bottom: 20px;margin-top: 20px;'>Endividamento de longo prazo por renda dos contratantes</div>", unsafe_allow_html=True)


pf_porte_endividamentolp_inflacao = load_data_ano_mes(arquivo = "pf_porte_endividamentolp_inflacao.csv", coluna_data = "data")


pf_porte_endividamentolp_inflacao_filtrado = filter_data(data = pf_porte_endividamentolp_inflacao,
                                                        coluna_data = "data",
                                                        filtro = None,
                                                        coluna_filtro = None,
                                                        data_inicio = date1,
                                                        data_fim = date2)

plot_pf_porte_endividamentolp_inflacao = go.Figure()

for porte in pf_porte_endividamentolp_inflacao_filtrado['porte'].unique():
    subset = pf_porte_endividamentolp_inflacao_filtrado[pf_porte_endividamentolp_inflacao_filtrado['porte'] == porte]
    
    plot_pf_porte_endividamentolp_inflacao.add_trace(go.Scatter(
        x=subset['data_divida'],
        y=subset['valor_deflacionado'],
        mode='lines',
        opacity=0.7,
        name=f'{porte}',
        yaxis='y2'
    ))

plot_pf_porte_endividamentolp_inflacao.add_trace(go.Scatter(
    x=pf_porte_endividamentolp_inflacao_filtrado['data_divida'],
    y=pf_porte_endividamentolp_inflacao_filtrado['valor'],
    opacity=1,
    line=dict(color='dimgray', width=2, dash='dot'),
    mode='lines',
    name='IPCA'
))

plot_pf_porte_endividamentolp_inflacao.update_layout(
    title='',
    yaxis=dict(
        title="IPCA",
        showgrid=False
    ),
    yaxis2=dict(
        title="Endividamento de longo prazo",
        overlaying='y',
        side='right',
        showgrid=False
    ),
    xaxis=dict(
        showgrid=False,
        title='Ano'
    ),
    legend=dict(
        x=0.5,
        y=-0.2,
        traceorder='normal',
        orientation='h',
        xanchor='center',
        yanchor='top',
        title='Faixa de rendimento'
    ),
    template="seaborn",
    dragmode=False
)
    
st.plotly_chart(plot_pf_porte_endividamentolp_inflacao, use_container_width=True)

st.markdown("<div style='text-align: center; color: #888888; font-size: 0.9em;margin-bottom: 20px;margin-top: 20px;'>Endividamento de longo prazo por categoria de renda dos contratantes</div>", unsafe_allow_html=True)

desemprego_divida_lp = load_data_ano_mes(arquivo = "df_desemprego_divida_grupo.csv", coluna_data = "data")

desemprego_divida_lp_filtrado = filter_data(data = desemprego_divida_lp,
                                            coluna_data = "data",
                                            filtro = None,
                                            coluna_filtro = None,
                                            data_inicio = date1,
                                            data_fim = date2)

filtro1 = desemprego_divida_lp_filtrado['categoria_renda'] == "alta renda"
filtro2 = desemprego_divida_lp_filtrado['categoria_renda'] == "baixa renda"
desemprego_divida_lp_filtrado=  desemprego_divida_lp_filtrado.loc[filtro1 | filtro2]

plot_desemprego_divida_lp_filtrado = go.Figure()

for categoria_renda in desemprego_divida_lp_filtrado['categoria_renda'].unique():
    subset = desemprego_divida_lp_filtrado[desemprego_divida_lp_filtrado['categoria_renda'] == categoria_renda]
    plot_desemprego_divida_lp_filtrado.add_trace(go.Scatter(x=subset['data'],
                             y=subset['longo_prazo_deflacionado'],
                             mode='lines',
                             name=f'{categoria_renda}',
                             yaxis='y2',
                             opacity=0.7))

plot_desemprego_divida_lp_filtrado.add_trace(go.Scatter(x=desemprego_divida_lp_filtrado['data'],
                         y=desemprego_divida_lp_filtrado['valor'], 
                         mode='lines',
                         name='taxa de desocupação',
                         opacity=1,
                        line=dict(color='dimgray', width=2, dash='dot')))

plot_desemprego_divida_lp_filtrado.add_shape(
    go.layout.Shape(
        type="line",
        x0="2017-07-01",
        x1="2017-07-01",
        y0=0,
        y1=1,
        yref='paper',
        line=dict(color="black", width=2)
    )
)

plot_desemprego_divida_lp_filtrado.add_annotation(
    go.layout.Annotation(
        text="Reforma Trabalhista",
        x="2017-07-01",
        y=0,
        yref='paper',
        showarrow=False,
        font=dict(color="black", size=12),
        textangle = 90,
        xshift=10
    )
)

plot_desemprego_divida_lp_filtrado.update_layout(
    title_text='',
    yaxis2=dict(
        overlaying='y',
        side='right',
        showgrid=False,
        title="Endividamento de longo prazo"
    ),
    template="seaborn",
    legend=dict(
        x=0.5,  
        y=-0.2,
        traceorder='normal',
        orientation='h',
        xanchor='center',  
        yanchor='top',
        title='Categorias de faixas de rendimento'
    ),  
    xaxis=dict(showgrid=False, title = 'Ano'),
    yaxis=dict(
        showgrid=False,
        title="Taxa de desocupação"
    ),
    margin=dict(t=0, b=0, l=0, r=0),
    dragmode=False
)

st.plotly_chart(plot_desemprego_divida_lp_filtrado, use_container_width=True)

st.markdown("""
<div style='text-align: left; color: #666666; font-size: 1em; background-color: #f0f0f0; padding: 10px; border-radius: 5px;margin-bottom: 20px;margin-bottom: 20px;'>
    💡&nbsp;&nbsp;&nbsp;A correlação é a medida estatística que indica o quanto as variáveis apresentadas estão relacionadas. Valores mais próximos de 1 indicam uma relação forte e positiva, enquanto valores mais próximos de -1 indicam uma relação forte e negativa. Por sua vez, valores mais próximos de 0 indicam relação fraca.
<br>
<br>
Pontos de atendimento indicam as unidades físicas de instituições financeiras (I.F) autorizadas a funcionar no Brasil; bancos autorizados apontam a quantidade de I.F. com autorização para funcionar no sistema financeira nacional; cartões de crédito mostram a quantidade de cartões de crédito ativos; taxa de juros pessoa física é a taxa média contratada pelas pessoas físicas nas instituições financeiras; retorno sobre ativos das I.F. reflete o resultado contábil dessas instituições; ativo problemático designa a parcela das operações de crédito em que há pouca expectativa de pagamento; por fim, carteira ativa é o endividamento total das pessoas físicas. Todos esses indicadores foram obtidos no Sistema Gerenciador de Séries Temporais do Banco Central do Brasil.
<br>
<br>
Atenção: em dispositivos móveis a visualização a seguir pode ficar prejudicada devido às dimensões do gráfico.
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='text-align: center; color: #888888; font-size: 0.9em;margin-bottom: 20px;margin-top: 20px;'>Mapa de calor da correlação entre variáveis de endividamento e de inclusão financeira</div>", unsafe_allow_html=True)

@st.cache_data()
def load_df_corr_porte_pf():
    df = pd.read_csv("df_corr_porte_pf.csv", encoding="UTF-8", delimiter=',', decimal='.')
    return df

df_corr_porte_pf = load_df_corr_porte_pf()

corr = df_corr_porte_pf.corr()

rename_columns = {
'carteira_ativa_baixa renda': 'Carteira ativa <br> baixa renda',
'carteira_ativa_alta renda': 'Carteira ativa <br> alta renda',
'ativo_problematico_baixa renda': 'Ativo problemático <br> baixa renda',
'ativo_problematico_alta renda': 'Ativo problemático <br> alta renda',
'Cart. créd. ativos': 'Cartões de crédito <br> ativos',
'Retorno sobre ativos IF': 'Retorno sobre ativos <br> das I.F.'}

corr.rename(columns=rename_columns, index=rename_columns, inplace=True)

mask = np.triu(np.ones_like(corr, dtype=bool))
corr_masked = corr.mask(mask)

fig = go.Figure(data=go.Heatmap(
z=corr_masked,
x=corr.columns,
y=corr.index,
zmin=-1, 
zmax=1, 
showscale=True,
colorbar=dict(
    orientation='h',
    x=0.5, 
    y=-0.2, 
    xanchor='center',
    yanchor='bottom',
    len=0.75,
    thickness=15
    )))

for i, row in enumerate(corr_masked.to_numpy()):
    for j, value in enumerate(row):
        if not np.isnan(value):  
            fig.add_annotation(dict(
                font=dict(size=12),
                x=corr.columns[j],
                y=corr.index[i],
                showarrow=False,
                text=f"{value:.2f}",
                xref="x",
                yref="y"
            ))
fig.update_xaxes(side="top", tickangle=360, showgrid=False)
fig.update_yaxes(side="left", tickangle=0, showgrid=False)

fig.update_layout(margin=dict(t=0, b=50, l=0, r=0),
template = "seaborn",
dragmode=False
)

st.plotly_chart(fig, use_container_width=True)

#PESSOAS JURÍDICAS
st.subheader('Como está o endividamento das empresas brasileiras?')

st.markdown("<div style='text-align: center; color: #555555; font-size: 1.3em;margin-bottom: 20px;'>Endividamento das empresas brasileiras</div>", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: left; color: #666666; font-size: 1em; background-color: #f0f0f0; padding: 10px; border-radius: 5px;margin-bottom: 20px;'>
    💡&nbsp;&nbsp;&nbsp;Nos gráficos abaixo, o setor de atuação (CNAE) se refere à atividade econômica da empresa, conforme classificação do IBGE. O primeiro gráfico (gráfico de dispersão) representa a relação entre duas variáveis: a proporção de empresas que saíram da atividade e o ativo problemático do respectivo setor. O segundo gráfico demonstra a distribuição geográfica do ativo problemático e considera o Estado ao qual o CNPJ da empresa contratante da operação está vinculado. O ativo problemático indica as parcelas de crédito em que há poucas expectativas de pagamento.
    
</div>
""", unsafe_allow_html=True)

@st.cache_data()
def load_df_corr_ibge_scr_pj():
    df = pd.read_csv("df_corr_ibge_scr_pj.csv", encoding="UTF-8", delimiter=',', decimal='.')
    return df

df_corr_ibge_scr_pj = load_df_corr_ibge_scr_pj()

cnae_secao = st.selectbox(
        'Qual setor de atuação você deseja visualizar?',
        df_corr_ibge_scr_pj['cnae_secao'].unique(), 
        index=14
    )
    
col5, col6 = st.columns((2))

with col5:

    st.markdown("<div style='text-align: center; color: #888888; font-size: 0.9em;margin-bottom: 20px;margin-top: 20px;'>Gráfico de dispersão os ativos problemáticos e a proporção de saída das empresas do setor</div>", unsafe_allow_html=True)
    
    df_corr_ibge_scr_pj_filtered = df_corr_ibge_scr_pj[df_corr_ibge_scr_pj['cnae_secao'] == cnae_secao]

    plot_corr_ibge_scr_pj = px.scatter(df_corr_ibge_scr_pj_filtered, x="ativo_problematico", y="Saída de atividade/Total", color="cnae_secao", hover_data=["Seção CNAE e ano"])
    
    plot_corr_ibge_scr_pj.update_layout(showlegend=False,
                                       title='',
                                       margin=dict(t=0, l=0, r=0, b=0),
                                       template = "seaborn",
                                       xaxis=dict(showgrid=False, title = 'Ativo problemático'), 
                                       yaxis=dict(showgrid=False, title='Qtde. empresas que saíram da atividade/Total'),
                                       dragmode=False)
    
    plot_corr_ibge_scr_pj.update_yaxes(showgrid=False)
    
    st.plotly_chart(plot_corr_ibge_scr_pj, use_container_width=True)
    

with col6:
    
    st.markdown("<div style='text-align: center; color: #888888; font-size: 0.9em;margin-bottom: 20px;margin-top: 20px;'>Distribuição geográfica do ativo problemático por Estado e setor de atuação das empresas contratantes</div>", unsafe_allow_html=True)
    
    df_cnae_pj_ativoproblematico = load_data_apenas_ano(arquivo = "df_cnae_pj_ativoproblematico.csv",
                                                coluna_data = "ano")
    
    df_cnae_pj_ativoproblematico_filtered = filter_data(data = df_cnae_pj_ativoproblematico,
                                                            coluna_data = "ano",
                                                            filtro = cnae_secao,
                                                            coluna_filtro = "cnae_secao",
                                                            data_inicio = ano1,
                                                            data_fim = ano2)

    plot_cnae_pj_ativoproblematico = px.choropleth_mapbox(df_cnae_pj_ativoproblematico_filtered, 
                               geojson=geojson_data, 
                               locations='Estado', 
                               color='ativo_problematico/pop',
                               color_continuous_scale="YlOrRd",
                               range_color=(0, max(df_cnae_pj_ativoproblematico_filtered['ativo_problematico/pop'])),
                               animation_frame='ano', 
                               mapbox_style="open-street-map",
                               zoom=2, 
                               center={"lat": -15, "lon": -57.33},
                               opacity=1,
                               labels={'ativo_problematico/pop':'Ativo problemático/População',
                                       'uf': 'Unidade da Federação do Brasil'},
                               featureidkey="properties.NM_ESTADO")
    
    plot_cnae_pj_ativoproblematico.update_layout(
    coloraxis_colorbar=dict(
        len=1,
        y=-0.25,  
        yanchor='bottom',  
        xanchor='center',
        x=0.5,   
        orientation='h',  
        title="Ativo problemático/População",
        titleside = "bottom"
    ),
        margin=dict(t=0, b=0, l=0, r=0)
)
    
    st.plotly_chart(plot_cnae_pj_ativoproblematico,use_container_width=True)

st.markdown("<div style='text-align: center; color: #555555; font-size: 1.3em;margin-bottom: 20px;'>Endividamento das micro e pequenas empresas</div>", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: left; color: #666666; font-size: 1em; background-color: #f0f0f0; padding: 10px; border-radius: 5px;margin-bottom: 20px;'>
    💡&nbsp;&nbsp;&nbsp;Nos gráficos abaixo, microempresa é aquela cuja receita bruta anual é de até R$ 360 mil por ano e pequena empresa é aquela cuja receita bruta anual está entre R$ 360 mil e R$ 4,8 milhões, conforme classificação da Receita Federal em janeiro de 2022. Para o cálculo do endividamento de curto prazo foram consideradas as operações de crédito com parcelas de vencimento em até 360 dias. O capital de giro se refere aos recursos utilizados para manter o equilíbrio do caixa e é utilizado para cobrir despesas correntes.
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='text-align: center; color: #888888; font-size: 0.9em;margin-bottom: 20px;margin-top: 20px;'>Modalidades de crédito de curto prazo contratadas pelas micro e pequenas empresas</div>", unsafe_allow_html=True)

pj_porte_modalidade_endividamentocp = load_data_ano_mes(arquivo = "pj_porte_modalidade_endividamentocp.csv",
                                                        coluna_data = "data_base")

pj_porte_modalidade_endividamentocp_filtrado = filter_data(data = pj_porte_modalidade_endividamentocp,
                                             coluna_data = "data_base",
                                             filtro = None,
                                             coluna_filtro = None,
                                             data_inicio = date1,
                                             data_fim = date2)

pj_porte_modalidade_endividamentocp_filtrado['modalidade'] = pj_porte_modalidade_endividamentocp['modalidade'].replace('Financiamento de infraestrutura/desenvolvimento/projeto e outros créditos', 'Financiamento de infraestrutura')

plot_pj_porte_modalidade_endividamentocp = px.line(pj_porte_modalidade_endividamentocp_filtrado, 
             x='data_base', 
             y='curto_prazo_deflacionado',
             color = 'modalidade',
             facet_col='porte',
             title='',
             labels={'data_base': '', 'curto_prazo_deflacionado': 'Endividamento de curto prazo'},
             category_orders={"porte": ["Microempresa", "Empresa de pequeno porte"]})

plot_pj_porte_modalidade_endividamentocp.update_layout(
    title='',
    legend=dict(x=0.5, 
                y=-0.4, 
                xanchor='center', 
                yanchor='top', 
                orientation = 'h',
                traceorder='normal',
               title = "Modalidade da operação de crédito"),
    xaxis=dict(title="Anos"),
    xaxis2=dict(title="Anos"),
    dragmode=False,
    yaxis=dict(showgrid=False),
    template="seaborn",
)

plot_pj_porte_modalidade_endividamentocp.update_yaxes(showgrid=False)

st.plotly_chart(plot_pj_porte_modalidade_endividamentocp, use_container_width=True)

st.markdown("<div style='text-align: center; color: #888888; font-size: 0.9em;margin-bottom: 20px;margin-top: 20px;'>Endividamento para capital de giro e ativo problemático das micro e pequenas empresas</div>", unsafe_allow_html=True)

df_micro_peq_problematico = load_data(arquivo = "df_micro_peq_problematico.csv",
                                      coluna_data = "data_base")

df_micro_peq_problematico_filtrado = filter_data(data = df_micro_peq_problematico,
                                             coluna_data = "data_base",
                                             filtro = None,
                                             coluna_filtro = None,
                                             data_inicio = date1,
                                             data_fim = date2)

df_micro_peq_problematico_filtrado = df_micro_peq_problematico_filtrado.rename(columns={
    'curto_prazo_deflacionado': 'Endividamento de Curto Prazo',
    'ativo_problematico_deflacionado': 'Ativo Problemático'
})

plot_micro_peq_problematico = px.bar(df_micro_peq_problematico_filtrado, 
             x='data_base', 
             y=['Endividamento de Curto Prazo', 'Ativo Problemático'],
             facet_col='porte', 
             labels={'data_base': 'data_base'},
             template="seaborn",
            category_orders={"porte": ["Microempresa", "Empresa de pequeno porte"]})

plot_micro_peq_problematico.update_layout(
    barmode='group',
    legend_title_text='tipo de endividamento',
    legend=dict(x=0.5, 
                y=-0.2, 
                xanchor='center', 
                yanchor='top', 
                orientation = 'h',
                traceorder='normal',
                title= 'Tipo de parcela de crédito'),
    xaxis=dict(title="Anos"),
    xaxis2=dict(title="Anos"),
    dragmode=False,
    yaxis=dict(showgrid=False, title="Endividamento para capital de giro <br> e ativo problemático")
)

plot_micro_peq_problematico.update_yaxes(showgrid=False)

st.plotly_chart(plot_micro_peq_problematico, use_container_width=True)

st.markdown("<div style='text-align: center; color: #555555; font-size: 1.3em;margin-bottom: 20px;'>Endividamento do setor de agricultura, pecuária, produção florestal, pesca e aquicultura</div>", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: left; color: #666666; font-size: 1em; background-color: #f0f0f0; padding: 10px; border-radius: 5px;margin-bottom: 20px;'>
    💡&nbsp;&nbsp;&nbsp;Pela classificação do IBGE, o setor de agricultura, pecuária, produção florestal, pesca e aquicultura possui subclasses, que fornecem informações mais detalhadas sobre a atividade econômica da empresa. A visualização abaixo considera as subclasses que tem participação de até 80% no setor.
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='text-align: center; color: #888888; font-size: 0.9em;margin-bottom: 20px;margin-top: 20px;'>Distribuição do endividamento no setor de agricultura, pecuária, produção florestal, pesca e aquicultura em dezembro-2022</div>", unsafe_allow_html=True)


@st.cache_data()
def load_pj_cnaesecao_cnaesubclasse_endividamento():
    df = pd.read_csv("pj_cnaesecao_cnaesubclasse_endividamento.csv", encoding="UTF-8", delimiter=',', decimal='.')
    df["data_base"] = pd.to_datetime(df["data_base"], format='%Y-%m')
    return df

pj_cnaesecao_cnaesubclasse_endividamento = load_pj_cnaesecao_cnaesubclasse_endividamento()

plot_pj_cnaesecao_cnaesubclasse_endividamento = px.treemap(pj_cnaesecao_cnaesubclasse_endividamento, 
                 path=['cnae_secao', 'cnae_subclasse'],
                 values='valor_deflacionado')

plot_pj_cnaesecao_cnaesubclasse_endividamento.update_layout(title='',
                  margin=dict(t=0, l=0, r=0, b=0),
                template = "seaborn",
                  dragmode=False)

plot_pj_cnaesecao_cnaesubclasse_endividamento.update_traces(textinfo='label+percent entry',
                 marker_line_width = 1,
                 hovertemplate='%{label} <br> $%{value:,.2f} <br> Percentual: %{percentRoot:.2%}',
                 textposition="top left",
                 textfont_size = 12,
                 textfont_color = 'white')

st.plotly_chart(plot_pj_cnaesecao_cnaesubclasse_endividamento,use_container_width=True)

st.subheader("Endividamento em pauta no Congresso Nacional")

st.markdown("<div style='text-align: center; color: #555555; font-size: 1.3em;margin-bottom: 20px;'>Proposições legislativas que se referem à endividamento com tramitação nos últimos 180 dias</div>", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: left; color: #666666; font-size: 1em; background-color: #f0f0f0; padding: 10px; border-radius: 5px;margin-bottom: 20px;'>
    💡&nbsp;&nbsp;&nbsp;A busca utiliza a base de dados da Câmara dos Deputados e se refere aos projetos de lei e medidas provisórias que tenham como palavras-chave termos relacionados ao endividamento da população e das empresas brasileiras. Os resultados são atualizados em tempo real.
</div>
""", unsafe_allow_html=True)

#API Camara dos deputados

@st.cache_data(ttl=3600)
def fetch_projetos(data_inicio, data_fim, palavras_chave):
    url = "https://dadosabertos.camara.leg.br/api/v2/proposicoes"
    params = {
        "dataInicio": data_inicio,
        "dataFim": data_fim,
        "ordenarPor": "id",
        "itens": 100,
        "pagina": 1,
        "siglaTipo": ["PL", "PLP", "MPV"],
        "keywords": palavras_chave
    }

    projetos = []
    while True:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            dados = response.json()["dados"]
            if len(dados) == 0:
                break
            projetos.extend(dados)
            params["pagina"] += 1
        else:
            print("Erro ao fazer requisição para a API:", response.status_code)
            break
    return projetos

@st.cache_data(ttl=3600)
def fetch_tramitacoes(id_proposicao, token):
    url_tramitacoes = f"https://dadosabertos.camara.leg.br/api/v2/proposicoes/{id_proposicao}/tramitacoes"
    response_tramitacoes = requests.get(url_tramitacoes, headers={"Authorization": f"Bearer {token}"})
    if response_tramitacoes.status_code == 200:
        tramitacoes = response_tramitacoes.json()['dados']
        ultima_tramitacao = tramitacoes[-1] if tramitacoes else None
        return ultima_tramitacao['descricaoSituacao'] if ultima_tramitacao else "Sem tramitações"
    else:
        print(f"Erro ao obter as tramitações da proposição {id_proposicao}: {response_tramitacoes.status_code}")
        return "Erro na tramitação"

def create_dataframe(projetos, token):
    for proposicao in projetos:
        id_proposicao = proposicao['id']
        situacao_tramitacao = fetch_tramitacoes(id_proposicao, token)
        proposicao['situacaoTramitacao'] = situacao_tramitacao

    colunas = ['siglaTipo', 'numero', 'ano', 'ementa', 'situacaoTramitacao']
    df = pd.DataFrame(projetos, columns=colunas)
    df['situacaoTramitacao'] = df['situacaoTramitacao'].astype('str')
    df['situacaoTramitacao'] = df['situacaoTramitacao'].replace(to_replace='None', value='Não informado')
    
    df['ano'] = df['ano'].astype('int')
    df['numero'] = df['numero'].astype('int')

    df.columns = ["Tipo", "Número", "Ano", "Ementa", "Situação"]
    return df

token = "seu_token_de_acesso_aqui"
data_inicio = (datetime.datetime.now() - datetime.timedelta(days=180)).strftime("%Y-%m-%d")
data_fim = datetime.datetime.now().strftime("%Y-%m-%d")
palavras_chave = [ 
"superendividamento",
"inadimplimento das obrigações", 
"mínimo existencial",   
"repactuação de dívidas",
"taxa de juros"
"crédito ao consumidor",
"parcelamento de dívidas",
"renegociação de dívidas"
"rotativo"
"cartão de crédito",
"crédito rural",
"crédito habitacional",
"empréstimo consignado"
"capital de giro",
"crédito para investimento",
"sistemas de informação de crédito",
"ativo problemático",
"crédito a vencer"
]

projetos = fetch_projetos(data_inicio, data_fim, palavras_chave)

df = create_dataframe(projetos, token)

def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    # Inicializar os estados dos filtros apenas uma vez
    if 'filter_initialized' not in st.session_state:
        st.session_state.filter_tipo = df['Tipo'].unique().tolist()
        st.session_state.filter_ano = (int(df['Ano'].min()), int(df['Ano'].max()))
        st.session_state.filter_situacao = df['Situação'].unique().tolist()
        st.session_state.filter_initialized = True

    modify = st.checkbox("Filtrar o resultado")

    if not modify:
        return df

    with st.container():
        # Filtro para o Tipo
        selected_tipo = st.multiselect(
            "Tipo de proposição",
            df['Tipo'].unique(),
            default=st.session_state.filter_tipo
        )

        # Filtro para o Ano
        _min, _max = int(df['Ano'].min()), int(df['Ano'].max())
        selected_ano = st.slider(
            "Ano",
            min_value=_min,
            max_value=_max,
            value=st.session_state.filter_ano,
            step=1
        )

        # Filtro para a Situação
        selected_situacao = st.multiselect(
            "Situação",
            df['Situação'].unique(),
            default=st.session_state.filter_situacao
        )

    # Aplicar filtros
    if selected_tipo != st.session_state.filter_tipo:
        df = df[df['Tipo'].isin(selected_tipo)]
        st.session_state.filter_tipo = selected_tipo

    if selected_ano != st.session_state.filter_ano:
        df = df[df['Ano'].between(*selected_ano)]
        st.session_state.filter_ano = selected_ano

    if selected_situacao != st.session_state.filter_situacao:
        df = df[df['Situação'].isin(selected_situacao)]
        st.session_state.filter_situacao = selected_situacao

    return df

filtered_df = filter_dataframe(df)

def formatar_numero(valor):
    return f"{valor}"

dados_formatados = filtered_df.style.format({'Número': formatar_numero,
                                            'Ano': formatar_numero})

st.dataframe(dados_formatados, use_container_width=True, hide_index=True, height=500)

#Última atualização

url = "https://api.github.com/repos/brunagmoura/SiteMonitorEndividamento/commits"

@st.cache_data
def get_last_commit_date(url):
    response = requests.get(url)
    last_commit = response.json()[0]
    return last_commit['commit']['committer']['date']

last_update = get_last_commit_date(url)
if last_update != "Não foi possível obter as informações":
    last_update = dt.fromisoformat(last_update[:-1]) - timedelta(hours=3)
    last_update = last_update.strftime("%d/%m/%Y %H:%M:%S")

# Exibe no Streamlit
st.warning(f"Esse site é atualizado automaticamente de acordo com a disponibilização de informações no Painel de Operações de Crédito, do Banco Central do Brasil. A última atualização foi em {last_update}.", icon = "🤖")