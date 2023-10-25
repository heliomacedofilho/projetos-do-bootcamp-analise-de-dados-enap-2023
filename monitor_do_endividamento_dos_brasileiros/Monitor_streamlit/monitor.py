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

st.set_page_config(page_title="Monitor endividamento", page_icon=":bar_chart:", layout="centered", initial_sidebar_state="collapsed", menu_items={"About": "Link ou descrição aqui"})

st.title(" :bar_chart: Monitor do endividamento dos brasileiros")

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

st.subheader("Os dados")

st.caption('Sistema de Informações de Crédito (SCR)')

st.caption('O que são operações de crédito?')

st.caption('Prazo das operações de crédito')

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

pf_ocupacao_modalidade_endividamento = pd.read_csv("pf_ocupacao_modalidade_endividamento.csv", encoding="UTF-8", delimiter=',', decimal='.')

pf_ocupacao_modalidade_endividamento["data_base"] = pd.to_datetime(pf_ocupacao_modalidade_endividamento["data_base"], format='%Y-%m-%d')

pf_ocupacao_modalidade_endividamento_filtrado = pf_ocupacao_modalidade_endividamento[(pf_ocupacao_modalidade_endividamento["data_base"] >= date1) & (pf_ocupacao_modalidade_endividamento["data_base"] <= date2)].copy()

ocupacao = st.selectbox(
            'Selecione uma ocupação:',
            pf_ocupacao_modalidade_endividamento_filtrado['ocupacao'].unique()
        )
    
col1, col2 = st.columns((2))

with col1:
    
    st.markdown("<div style='text-align: center; color: #888888; font-size: 0.8em;'>Distribuição do endividamento das pessoas físicas pelas modalidades de crédito</div>", unsafe_allow_html=True)

    pf_ocupacao_modalidade_endividamento_filtrado = pf_ocupacao_modalidade_endividamento_filtrado[pf_ocupacao_modalidade_endividamento_filtrado['ocupacao'] == ocupacao]

    plot_pf_ocupacao_modalidade_endividamento = px.line(pf_ocupacao_modalidade_endividamento_filtrado, 
                 x='data_base',
                 y='carteira_ativa_deflacionada', 
                 color='modalidade')

    plot_pf_ocupacao_modalidade_endividamento.update_layout(
        xaxis_title='anos',
        yaxis_title='carteira ativa deflacionada',
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

    st.plotly_chart(plot_pf_ocupacao_modalidade_endividamento, use_container_width=True)

with col2:
    
    st.markdown("<div style='text-align: center; color: #888888; font-size: 0.8em;'>Distribuição do endividamento das pessoas físicas pelos Estados brasileiros</div>", unsafe_allow_html=True)
    
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
        title="Ativo problemático deflacionado/População (2022)",
        titleside = "bottom"
    ),
        margin=dict(t=0, b=0, l=0, r=0)
)

    
    st.plotly_chart(plot_ocupacao_pf_ativoproblematico,use_container_width=True, height = 200)
    
st.caption('Distribuição do endividamento por faixas de renda')
    
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

st.caption('Distribuição do endividamento pelos Estados')

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
st.subheader('Como anda o pagamento das dívidas?')

col5, col6 = st.columns((2))



with col6:

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
        title="Ativo problemático deflacionado/População (2022)",
        titleside = "bottom"
    ),
        margin=dict(t=0, b=0, l=0, r=0)
)

    
    st.plotly_chart(plot_cnae_pj_ativoproblematico,use_container_width=True, height = 200)