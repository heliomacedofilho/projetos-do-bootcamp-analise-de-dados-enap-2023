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

warnings.filterwarnings('ignore')

st.set_page_config(page_title="Monitor endividamento", page_icon=":bar_chart:", layout="wide", initial_sidebar_state="collapsed", menu_items={"About": "Link ou descrição aqui"})

st.title(" :bar_chart: Monitor do endividamento dos brasileiros")

st.info('Para facilitar a sua análise, todos os valores já estão a valores presentes!\n\n'
        'Clique em "sobre" no canto superior direito da tela para conferir mais detalhes sobre este projeto', 
        icon="👩‍💻")

#Caixa para selecionar as datas

st.sidebar.header("Qual período você deseja consultar?")
diferentes_dividas = pd.read_csv("analise_divida_tempo.csv", encoding="UTF-8", delimiter=',', decimal='.')
diferentes_dividas["data_base"] = pd.to_datetime(diferentes_dividas["data_base"], format='%Y-%m-%d')

min_year = int(diferentes_dividas['data_base'].dt.year.min())
max_year = int(diferentes_dividas['data_base'].dt.year.max())

min_month = int(diferentes_dividas['data_base'].dt.month.min())
max_month = int(diferentes_dividas['data_base'].dt.month.max())

month_abbr = list(calendar.month_abbr) 

def select_month_and_year(name, min_year, max_year, default_month, default_year):
    with st.sidebar.expander(name):
        year = st.selectbox(f'{name} - Ano', range(max_year, min_year - 1, -1), index=max_year - default_year)
        month = st.selectbox(f'{name} - Mês', month_abbr[1:], index=default_month - 1) 
    return month, year

start_month, start_year = select_month_and_year('Data de Início', min_year, max_year, min_month, min_year)
end_month, end_year = select_month_and_year('Data Final', min_year, max_year, max_month, max_year)

date1 = datetime.datetime(start_year, month_abbr.index(start_month), 1)
last_day = calendar.monthrange(end_year, month_abbr.index(end_month))[1]
date2 = datetime.datetime(end_year, month_abbr.index(end_month), last_day)

st.sidebar.markdown(f'<p style="text-align: center">Exibindo dados para o intervalo {date1.strftime("%Y-%m")} a {date2.strftime("%Y-%m")}.</p>', unsafe_allow_html=True)

st.markdown("<div style='text-align: center; color: #555555; font-size: 1.3em;'>Evolução do endividamento dos brasileiros ao longo do tempo</div>", unsafe_allow_html=True)

st.markdown("<div style='text-align: center; color: #666666; font-size: 1em;'>As parcelas de crédito se referem à soma das operações de crédito contratadas pelos brasileiros, pessoas físicas e jurídicas, com o prazo de vencimento indicado.</div>", unsafe_allow_html=True)

#Gráfico diferentes dívidas ao longo do tempo

diferentes_dividas["data_base"] = diferentes_dividas["data_base"].dt.to_period('M').dt.to_timestamp()
diferentes_dividas = diferentes_dividas.sort_values(by="data_base")

diferentes_dividas = diferentes_dividas[(diferentes_dividas["data_base"] >= date1) & (diferentes_dividas["data_base"] <= date2)].copy()

fig = go.Figure()

for col in diferentes_dividas.columns[1:]:
    if col != 'carteira_ativa':
        fig.add_trace(go.Scatter(x=diferentes_dividas['data_base'], 
                                 y=diferentes_dividas[col], 
                                 mode='lines', 
                                 name=col,
                                yaxis='y2'))

# Adicionar barras para 'carteira_ativa'
fig.add_trace(go.Bar(x=diferentes_dividas['data_base'], 
                     y=diferentes_dividas['carteira_ativa'],
                    opacity=0.5,
                    showlegend=False))

# Atualizar o layout
fig.update_layout(
    title='Parcelas a vencer vs Carteira ativa',
    xaxis_title='Data',
    yaxis_title='Parcelas das operações de crédito',
    yaxis2=dict(
        title='Carteira ativa',
        overlaying='y',
        side='right'
    ),
    legend=dict(
        y=-0.2,
        traceorder='normal',
        orientation='h',
        font=dict(
            size=12,
            
        ),
    ),
    template='seaborn'
)

st.plotly_chart(fig, use_container_width=True, height=200)

st.subheader("Como a população brasileira anda se endividando?")

st.markdown("<div style='text-align: center; color: #555555; font-size: 1.3em;'>Endividamento dos brasileiros pessoas físicas de acordo com a sua ocupação</div>", unsafe_allow_html=True)

pf_ocupacao_modalidade_endividamento = pd.read_csv("pf_ocupacao_modalidade_endividamento.csv", encoding="UTF-8", delimiter=',', decimal='.')

pf_ocupacao_modalidade_endividamento["data_base"] = pd.to_datetime(pf_ocupacao_modalidade_endividamento["data_base"], format='%Y-%m-%d')

pf_ocupacao_modalidade_endividamento_filtrado = pf_ocupacao_modalidade_endividamento[(pf_ocupacao_modalidade_endividamento["data_base"] >= date1) & (pf_ocupacao_modalidade_endividamento["data_base"] <= date2)].copy()

ocupacao = st.selectbox(
            'Para qual ocupação você deseja visualizar?',
            pf_ocupacao_modalidade_endividamento_filtrado['ocupacao'].unique()
        )
    
col1, col2 = st.columns((2))

with col1:
    
    st.markdown("<div style='text-align: center; color: #888888; font-size: 0.9em;'>Modalidades de crédito contratadas</div>", unsafe_allow_html=True)

    pf_ocupacao_modalidade_endividamento_filtrado = pf_ocupacao_modalidade_endividamento_filtrado[pf_ocupacao_modalidade_endividamento_filtrado['ocupacao'] == ocupacao]

    plot_pf_ocupacao_modalidade_endividamento = px.line(pf_ocupacao_modalidade_endividamento_filtrado, 
                 x='data_base',
                 y='carteira_ativa_deflacionada', 
                 color='modalidade')

    plot_pf_ocupacao_modalidade_endividamento.update_layout(
    title_text='',
    xaxis_title='',
    yaxis_title='Endividamento total',
    template="seaborn",
    legend=dict(
        x=0.5,
        y=-0.3,
        orientation='h',
        xanchor='center'
    ),
    xaxis=dict(showgrid=False),
    margin=dict(t=0, b=0, l=0, r=0)
)
    plot_pf_ocupacao_modalidade_endividamento.update_yaxes(showgrid=False)

    st.plotly_chart(plot_pf_ocupacao_modalidade_endividamento, use_container_width=True)

with col2:
    
    st.markdown("<div style='text-align: center; color: #888888; font-size: 0.9em;'>Estados federativos em que residem os tomadores de crédito com parcelas classificadas como ativo problemático, em que há pouca expectativa de pagamento</div>", unsafe_allow_html=True)
    
    df_ocupacao_pf_ativoproblematico = pd.read_csv("df_ocupacao_pf_ativoproblematico.csv", encoding="UTF-8", delimiter=',', decimal='.')

    url = "https://raw.githubusercontent.com/jonates/opendata/master/arquivos_geoespaciais/unidades_da_federacao.json" #Temos que dar os créditos
    response = requests.get(url)
    geojson_data = response.json()


    df_ocupacao_pf_ativoproblematico_filtered = df_ocupacao_pf_ativoproblematico[df_ocupacao_pf_ativoproblematico['ocupacao'] == ocupacao]


    plot_ocupacao_pf_ativoproblematico = px.choropleth_mapbox(df_ocupacao_pf_ativoproblematico_filtered, 
                               geojson=geojson_data, 
                               locations='Estado', 
                               color='ativo_problematico/pop',
                               color_continuous_scale="sunsetdark",
                               range_color=(0, max(df_ocupacao_pf_ativoproblematico_filtered['ativo_problematico/pop'])),
                               animation_frame='ano', 
                               mapbox_style="open-street-map",
                               zoom=1.9, 
                               center={"lat": -17.14, "lon": -57.33},
                               opacity=1,
                               labels={'ativo_problematico/pop':'Ativo problemático',
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
        title="ativo problemático/população",
        titleside = "bottom"
    ),
        margin=dict(t=0, b=0, l=0, r=0)
)

    
    st.plotly_chart(plot_ocupacao_pf_ativoproblematico,use_container_width=True, height = 200)

st.markdown("<div style='text-align: center; color: #888888; font-size: 1.3em;'>Endividamento dos brasileiros pessoas físicas de acordo com a sua renda</div>", unsafe_allow_html=True)

pf_rendimento_modalidade_noperacoes_endividamento = pd.read_csv("pf_rendimento_modalidade_noperacoes_endividamento.csv", encoding="UTF-8", delimiter=',', decimal='.')

pf_rendimento_modalidade_noperacoes_endividamento["data_base"] = pd.to_datetime(pf_rendimento_modalidade_noperacoes_endividamento["data_base"], format='%Y-%m-%d')

pf_rendimento_modalidade_noperacoes_endividamento_filtrado = pf_rendimento_modalidade_noperacoes_endividamento[(pf_rendimento_modalidade_noperacoes_endividamento["data_base"] >= date1) & (pf_rendimento_modalidade_noperacoes_endividamento["data_base"] <= date2)].copy()

porte = st.selectbox(
    "Para qual faixa rendimento você deseja visualizar?",
    pf_rendimento_modalidade_noperacoes_endividamento_filtrado['porte'].unique()
)

col20, col21 = st.columns((2))

with col20:
    st.markdown("<div style='text-align: center; color: #888888; font-size: 0.9em;'>Endividamento com vencimento acima de 360 dias em relação às modalidades de crédito contratadas</div>", unsafe_allow_html=True)
    
    pf_rendimento_modalidade_noperacoes_endividamento_filtrado = pf_rendimento_modalidade_noperacoes_endividamento_filtrado[pf_rendimento_modalidade_noperacoes_endividamento_filtrado['porte'] == porte]

    plot_rendimento_modalidade_noperacoes = px.line(pf_rendimento_modalidade_noperacoes_endividamento_filtrado, 
                  x='data_base', 
                  y='longo_prazo_deflacionado', 
                  color='modalidade')

    plot_rendimento_modalidade_noperacoes.update_layout(
    title_text='',
    xaxis_title='',
    yaxis_title='Endividamento de longo prazo',
    template="seaborn",
    legend=dict(
        x=0.5,
        y=-0.3,
        orientation='h',
        xanchor='center'
    ),
    xaxis=dict(showgrid=False),
    yaxis=dict(
        showgrid=False, 
        title='Endividamento de longo prazo'
    ),
    margin=dict(t=0, b=0, l=0, r=0)
)

    st.plotly_chart(plot_rendimento_modalidade_noperacoes, use_container_width=True)

with col21:
    
    st.markdown("<div style='text-align: center; color: #888888; font-size: 0.9em;'>Quantidade de operações totais (para qualquer vencimento) em relação às modalidades de crédito contratadas</div>", unsafe_allow_html=True)

    pf_rendimento_modalidade_noperacoes_endividamento_filtrado = pf_rendimento_modalidade_noperacoes_endividamento_filtrado[pf_rendimento_modalidade_noperacoes_endividamento_filtrado['porte'] == porte]

    plot_rendimento_modalidade_noperacoes = px.line(pf_rendimento_modalidade_noperacoes_endividamento_filtrado, 
                  x='data_base', 
                  y='numero_de_operacoes', 
                  color='modalidade')

    plot_rendimento_modalidade_noperacoes.update_layout(
        title_text='',
        xaxis_title='',
        yaxis_title='Número de operações',
        template="seaborn",
        legend=dict(
            x=0.5,
            y=-0.3,
            orientation='h',
            xanchor='center'
        ),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        margin=dict(t=0, b=0, l=0, r=0)
    )

    st.plotly_chart(plot_rendimento_modalidade_noperacoes, use_container_width=True)

st.markdown("<div style='text-align: center; color: #555555; font-size: 1.3em;'>Inserindo dados macroeconômicos na análise</div>", unsafe_allow_html=True)

df_juros_inflacao_modalidade = pd.read_csv("df_juros_inflacao_modalidade.csv", encoding="UTF-8", delimiter=',', decimal='.')

df_juros_inflacao_modalidade["data_base"] = pd.to_datetime(df_juros_inflacao_modalidade["data_base"], format='%Y-%m')

df_juros_inflacao_modalidade_filtrado = df_juros_inflacao_modalidade[(df_juros_inflacao_modalidade["data_base"] >= date1) & (df_juros_inflacao_modalidade["data_base"] <= date2)].copy()

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
        yaxis2=dict(
            overlaying='y',
            side='right',
            showgrid=False,
            title=""
        ),
        template="seaborn",
        legend=dict(
            x=0.5,
            y=-0.2,
            orientation='h',
            xanchor='center'
        ),
        xaxis=dict(showgrid=False),
        yaxis=dict(
            showgrid=False,
            title=yaxis_column_name
        ),
        margin=dict(t=0, l=0, r=0, b=0)
    )

    return plot_juros_inflacao_modalidade

option = st.selectbox(
        'Selecione o indicador macroeconômico que você deseja adicionar à série',
        ('IPCA', 'Taxa média mensal de juros - PF')
    )
    
st.markdown("<div style='text-align: center; color: #888888; font-size: 0.9em;'>Distribuição do endividamento com parcelas acima de 360 dias por modalidades de contratação</div>", unsafe_allow_html=True)

st.plotly_chart(create_figure(option), use_container_width=True)


col30, col31 = st.columns((2))

with col30:
    
    st.markdown("<div style='text-align: center; color: #888888; font-size: 0.9em;'>Endividamento por faixa de renda em comparação à taxa de desocupação</div>", unsafe_allow_html=True)
    
    desemprego_divida_lp = pd.read_csv("df_desemprego_divida_grupo.csv", encoding="UTF-8", delimiter=',', decimal='.')
    
    desemprego_divida_lp["data"] = pd.to_datetime(desemprego_divida_lp["data"], format='%Y-%m')

    desemprego_divida_lp_filtrado = desemprego_divida_lp[(desemprego_divida_lp["data"] >= date1) & (desemprego_divida_lp["data"] <= date2)].copy()

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
        yaxis2=dict(
            overlaying='y',
            side='right',
            showgrid=False,
            title="Endividamento de longo prazo"
        ),
        template="seaborn",
        legend=dict(
            y=-0.2,
            traceorder='normal',
            orientation='h',
            font=dict(
                size=12
            )
        ),  
        xaxis=dict(showgrid=False),
        yaxis=dict(
            showgrid=False,
            title="Taxa de desocupação"
        ),
        showlegend = True,
        margin=dict(t=0, b=0, l=0, r=0)
    )

    st.plotly_chart(plot_desemprego_divida_lp_filtrado, use_container_width=True)

    
with col31:
    
    st.markdown("<div style='text-align: center; color: #888888; font-size: 0.9em;'>Correlação entre indicadores macroeconômicos e as parcelas do endividamento total e parcelas com pouca expectativa de pagamento</div>", unsafe_allow_html=True)
    
    df_corr_porte_pf = pd.read_csv("df_corr_porte_pf.csv", encoding="UTF-8", delimiter=',', decimal='.')

    sns.set_theme(style="white")
    corr = df_corr_porte_pf.corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    plot_corr_porte_pf, ax = plt.subplots(figsize=(11, 9))
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    sns_heatmap = sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
                          square=True, linewidths=.5, annot=True, annot_kws={"size": 15},
                          cbar=True)
    ax.tick_params(axis='both', which='major', labelsize=15, color='#666666')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)

    st.pyplot(plot_corr_porte_pf)

st.markdown("<div style='text-align: center; color: #888888; font-size: 0.9em;'>Endividamento com prazo de vencimento acima de 360 dias em comparação ao índice de preços ao consumidor amplo (inflação)</div>", unsafe_allow_html=True)

pf_porte_endividamentolp_inflacao = pd.read_csv("pf_porte_endividamentolp_inflacao.csv", encoding="UTF-8", delimiter=',', decimal='.')

pf_porte_endividamentolp_inflacao["data"] = pd.to_datetime(desemprego_divida_lp["data"], format='%Y-%m')

pf_porte_endividamentolp_inflacao_filtrado = pf_porte_endividamentolp_inflacao[(pf_porte_endividamentolp_inflacao["data"] >= date1) & (pf_porte_endividamentolp_inflacao["data"] <= date2)].copy()

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
        showgrid=False
    ),
    legend=dict(
        y=-0.2,
        traceorder='normal',
        orientation='h',
        font=dict(size=12)
    ),
    template="seaborn",
    showlegend = True,
)

st.plotly_chart(plot_pf_porte_endividamentolp_inflacao, use_container_width=True)

#Mapa endividamento PF e PJ
st.subheader('Como as empresas andam se financiando?')

st.markdown("<div style='text-align: center; color: #555555; font-size: 1.3em;'>Endividamento das empresas brasileiras por Estado de atuação</div>", unsafe_allow_html=True)

col5, col6 = st.columns((2))

with col6:
    
    st.markdown("<div style='text-align: center; color: #888888; font-size: 0.9em;'>Estados federativos em que estão localizadas as empresas tomadoras de crédito com parcelas classificadas como ativo problemático, em que há pouca expectativa de pagamento</div>", unsafe_allow_html=True)

    df_cnae_pj_ativoproblematico = pd.read_csv("df_cnae_pj_ativoproblematico.csv", encoding="UTF-8", delimiter=',', decimal='.')

    cnae_secao = st.selectbox(
        'Para qual setor de atuação você deseja visualizar?',
        df_cnae_pj_ativoproblematico['cnae_secao'].unique()
    )

    df_cnae_pj_ativoproblematico_filtered = df_cnae_pj_ativoproblematico[df_cnae_pj_ativoproblematico['cnae_secao'] == cnae_secao]


    plot_cnae_pj_ativoproblematico = px.choropleth_mapbox(df_cnae_pj_ativoproblematico_filtered, 
                               geojson=geojson_data, 
                               locations='Estado', 
                               color='ativo_problematico/pop',
                               color_continuous_scale="sunsetdark",
                               range_color=(0, max(df_cnae_pj_ativoproblematico_filtered['ativo_problematico/pop'])),
                               animation_frame='ano', 
                               mapbox_style="open-street-map",
                               zoom=1.9, 
                               center={"lat": -17.14, "lon": -57.33},
                               opacity=1,
                               labels={'ativo_problematico/pop':'Ativo problemático',
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
        title="ativo problemático/população",
        titleside = "bottom"
    ),
        margin=dict(t=0, b=0, l=0, r=0)
)

    
    st.plotly_chart(plot_cnae_pj_ativoproblematico,use_container_width=True, height = 200)

st.markdown("<div style='text-align: center; color: #555555; font-size: 1.3em;'>Por dentro das micro e pequenas empresas</div>", unsafe_allow_html=True)
    
st.markdown("<div style='text-align: center; color: #888888; font-size: 0.9em;'>Modalidades de crédito contratadas pelas micro e pequenas empresas com parcelas cujo vencimento é inferior a 360 dias</div>", unsafe_allow_html=True)

pj_porte_modalidade_endividamentocp = pd.read_csv("pj_porte_modalidade_endividamentocp.csv", encoding="UTF-8", delimiter=',', decimal='.')

pj_porte_modalidade_endividamentocp["data_base"] = pd.to_datetime(pj_porte_modalidade_endividamentocp["data_base"], format='%Y-%m')

pj_porte_modalidade_endividamentocp_filtrado = pj_porte_modalidade_endividamentocp[(pj_porte_modalidade_endividamentocp["data_base"] >= date1) & (pj_porte_modalidade_endividamentocp["data_base"] <= date2)].copy()

plot_pj_porte_modalidade_endividamentocp = px.line(pj_porte_modalidade_endividamentocp_filtrado, 
             x='data_base', 
             y='curto_prazo_deflacionado',
              color = 'modalidade',
             facet_col='porte',
             title='',
             labels={'data_base': '', 'curto_prazo_deflacionado': 'Endividamento de curto prazo'},
             template="seaborn",
             category_orders={"porte": ["Empresa de pequeno porte", "Microempresa"]})

plot_pj_porte_modalidade_endividamentocp.update_layout(
    yaxis_title="Endividamento de curto prazo",
    legend_title_text='modalidade',
    legend=dict(x=0.5, y=-0.17, xanchor='center', yanchor='top', orientation = 'h')
)

st.plotly_chart(plot_pj_porte_modalidade_endividamentocp, use_container_width=True)

st.markdown("<div style='text-align: center; color: #888888; font-size: 0.9em;'>Micro e pequenas empresas: endividamento para capital de giro versus ativo problemático, em que há pouca expectativa de pagamento</div>", unsafe_allow_html=True)

df_micro_peq_problematico = pd.read_csv("df_micro_peq_problematico.csv", encoding="UTF-8", delimiter=',', decimal='.')

df_micro_peq_problematico["data_base"] = pd.to_datetime(df_micro_peq_problematico["data_base"], format='%Y-%m-%d')

df_micro_peq_problematico_filtrado = df_micro_peq_problematico[(df_micro_peq_problematico["data_base"] >= date1) & (df_micro_peq_problematico["data_base"] <= date2)].copy()

df_micro_peq_problematico = df_micro_peq_problematico.rename(columns={
    'curto_prazo_deflacionado': 'Endividamento de Curto Prazo',
    'ativo_problematico_deflacionado': 'Ativo Problemático'
})

plot_micro_peq_problematico = px.bar(df_micro_peq_problematico, 
             x='data_base', 
             y=['Endividamento de Curto Prazo', 'Ativo Problemático'],
             facet_col='porte', 
             labels={'data_base': ''},
             template="seaborn")

plot_micro_peq_problematico.update_layout(
    yaxis_title="Endividamento de curto prazo e ativo problemático, em que há pouca expectativa de pagamento",
    legend_title_text='',
    legend=dict(x=0.5, y=-0.15, xanchor='center', yanchor='top', orientation = 'h'),
        xaxis=dict(dtick="M24"),
        xaxis2=dict(dtick="M24")
)

st.plotly_chart(plot_micro_peq_problematico, use_container_width=True)

st.markdown("<div style='text-align: center; color: #555555; font-size: 1.3em;'>Por dentro do setor de agricultura, pecuária, produção florestal, pesca e aquicultura</div>", unsafe_allow_html=True)

st.markdown("<div style='text-align: center; color: #888888; font-size: 0.9em;'>Distribuição do endividamento nas principais áreas de atuação das empresas do setor de agricultura, pecuária, produção florestal, pesca e aquicultura em dezembro-2022</div>", unsafe_allow_html=True)

pj_cnaesecao_cnaesubclasse_endividamento = pd.read_csv("pj_cnaesecao_cnaesubclasse_endividamento.csv", encoding="UTF-8", delimiter=',', decimal='.')

pj_cnaesecao_cnaesubclasse_endividamento["data_base"] = pd.to_datetime(pj_cnaesecao_cnaesubclasse_endividamento["data_base"], format='%Y-%m')

pj_cnaesecao_cnaesubclasse_endividamento_filtrado = pj_cnaesecao_cnaesubclasse_endividamento[(pj_cnaesecao_cnaesubclasse_endividamento["data_base"] >= date1) & (pj_cnaesecao_cnaesubclasse_endividamento["data_base"] <= date2)].copy()

plot_pj_cnaesecao_cnaesubclasse_endividamento = px.treemap(pj_cnaesecao_cnaesubclasse_endividamento_filtrado, 
                 path=['cnae_secao', 'cnae_subclasse'],
                 values='valor_deflacionado')

plot_pj_cnaesecao_cnaesubclasse_endividamento.update_layout(title='',
                  margin=dict(t=0, l=0, r=0, b=0),
                 template = "seaborn")

plot_pj_cnaesecao_cnaesubclasse_endividamento.update_traces(textinfo='label+percent entry',
                 marker_line_width = 1,
                 hovertemplate='%{label} <br> $%{value:,.2f} <br> Percentual: %{percentRoot:.2%}',
                 textposition="top left",
                 textfont_size = 12,
                 textfont_color = 'white')

st.plotly_chart(plot_pj_cnaesecao_cnaesubclasse_endividamento,use_container_width=True, height = 200)

st.subheader("Como esse assunto vem sendo tratado pelos legisladores?")

st.markdown("<div style='text-align: center; color: #888888; font-size: 0.9em;'>Palavras em destaque nos projetos leis da Câmara dos Deputados - 2013 a 2023</div>", unsafe_allow_html=True)

col10, col11, col12 = st.columns([1, 3, 1])

with col10:
    st.write(' ')

with col11:
    st.image("nuvem_palavras_projetos_leis_2012_2023.svg", caption='', use_column_width=True)

with col12:
    st.write(' ')