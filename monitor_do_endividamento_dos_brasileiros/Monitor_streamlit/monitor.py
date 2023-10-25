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

warnings.filterwarnings('ignore')

st.set_page_config(page_title="Monitor endividamento", page_icon=":bar_chart:",layout="wide")

st.title(" :bar_chart: Monitor do endividamento dos brasileiros")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

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


#Gráfico diferentes dívidas ao longo do tempo

diferentes_dividas["data_base"] = diferentes_dividas["data_base"].dt.to_period('M').dt.to_timestamp()
diferentes_dividas = diferentes_dividas.sort_values(by="data_base")

diferentes_dividas = diferentes_dividas[(diferentes_dividas["data_base"] >= date1) & (diferentes_dividas["data_base"] <= date2)].copy()

st.subheader("Prazo da dívida")

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

# Exibir o gráfico
st.plotly_chart(fig, use_container_width=True, height=200)

st.subheader("Renda vs Endividamento de longo prazo")
    
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

plot_desemprego_divida_lp_filtrado.update_layout(yaxis2=dict(overlaying='y',
                              side='right',
                             showgrid=False,
                             title = "Endividamento de longo prazo"),
                 template="seaborn",
                  legend=dict(x = 0.5,
                              y = -0.3,
                              orientation='h',
                              xanchor='center'),
                 xaxis=dict(showgrid=False),
                 yaxis=dict(showgrid=False,
                           title = "Taxa de desocupação"))

st.plotly_chart(plot_desemprego_divida_lp_filtrado, use_container_width=True)

divida_uf = pd.read_csv("analise_divida_uf.csv", encoding="UTF-8", delimiter=',', decimal='.')
divida_uf["ano"] = pd.to_datetime(divida_uf["ano"], format='%Y')
divida_uf_filtrado = divida_uf[(divida_uf["ano"] >= date1) & (divida_uf["ano"] <= date2)].copy()

divida_uf_filtrado['ano'] = divida_uf_filtrado['ano'].dt.year

divida_uf_filtrado['ano'] = divida_uf_filtrado['ano'].astype('object')

plot_divida_uf = px.bar(divida_uf_filtrado, 
                        x='uf', 
                        y='carteira_ativa',
                        title='Carteira Ativa por UF e Ano',
                        labels={'carteira_ativa':'Carteira Ativa', 'uf_ano':'UF e Ano'},
                        color='ano',
                        barmode = 'group',
                        template="seaborn")
plot_divida_uf.update_layout(
    legend=dict(
        y = -0.2,
        traceorder='normal',
        orientation='h',
        font=dict(
            size=12,
        ),
    )
)

st.plotly_chart(plot_divida_uf, use_container_width=True)

#Mapa endividamento PF e PJ
st.title('Análise dos ativos problemáticos')

col3, col4 = st.columns((2))

with col3:
    
    df_ocupacao_pf_ativoproblematico = pd.read_csv("df_ocupacao_pf_ativoproblematico.csv", encoding="UTF-8", delimiter=',', decimal='.')


    url = "https://raw.githubusercontent.com/jonates/opendata/master/arquivos_geoespaciais/unidades_da_federacao.json" #Temos que dar os créditos
    response = requests.get(url)
    geojson_data = response.json()

    

    ocupacao = st.selectbox(
        'Selecione uma ocupação:',
        df_ocupacao_pf_ativoproblematico['ocupacao'].unique()
    )

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
        title="Ativo problemático deflacionado / População (2022)",
        titleside = "bottom"
    ),
        margin=dict(t=0, b=0, l=0, r=0)
)

    
    st.plotly_chart(plot_ocupacao_pf_ativoproblematico,use_container_width=True, height = 200)

with col4:

    df_cnae_pj_ativoproblematico = pd.read_csv("df_cnae_pj_ativoproblematico.csv", encoding="UTF-8", delimiter=',', decimal='.')

    cnae_secao = st.selectbox(
        'Selecione um setor de atuação:',
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
        title="Ativo problemático deflacionado / População (2022)",
        titleside = "bottom"
    ),
        margin=dict(t=0, b=0, l=0, r=0)
)

    
    st.plotly_chart(plot_cnae_pj_ativoproblematico,use_container_width=True, height = 200)