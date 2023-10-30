#importando as bibliotecas

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
import requests
from geojson_rewind import rewind
import json

#carregando os dados
df = pd.read_csv('data\df_pbf_cadunico_streamlit.csv')
georreferenciamento_df = pd.read_csv('data\georreferenciamento_df.csv')
with open('data/geojson', 'r') as geojson_file:
    geojson = json.load(geojson_file)


#criando as caixas de seleção
#escolha = st.sidebar.selectbox("Deseja filtrar os resultados?", ['Não', 'Sim'])
df_filtrado = df
#if escolha == 'Sim':
#    lista_regioes = df['Região'].unique().tolist()
#    lista_regioes.insert(0, "Marcar Todos")
#    regiao_selecionada = st.sidebar.selectbox("Selecione uma região:", lista_regioes)
#
#    if regiao_selecionada != "Marcar Todos":
#        df_filtrado = df[df['Região'] == regiao_selecionada]
#
#        lista_estados = df_filtrado['ufSigla'].unique().tolist()
#        lista_estados.insert(0, "Marcar Todos")
#        estado_selecionado = st.sidebar.selectbox("Selecione um estado:", lista_estados)
#
#        if estado_selecionado != "Marcar Todos":
#            df_filtrado = df_filtrado[df_filtrado['ufSigla'] == estado_selecionado]
#
#            lista_municipios = df_filtrado['Município_UF'].unique().tolist()
#            lista_municipios.insert(0, "Marcar Todos")
#            municipio_selecionado = st.sidebar.selectbox("Selecione um município:", lista_municipios)
#
#            if municipio_selecionado != "Marcar Todos":
#                df_filtrado = df_filtrado[df_filtrado['Município_UF'] == municipio_selecionado]

# criando título para página
st.write(
    """
    <div style="text-align: center;">
        <h1 style="color: black;">Programa Bolsa Família <br> <span style="color: blue;">PBF</span> \U0001F46A</h1>
    </div>
    """,
    unsafe_allow_html=True
)



#criando um espaço entre as visualizações
st.text("")

#criando o texto explicativo
st.write(
    """
    <div style="text-align: justify">
<p> O  <span style="color: blue;">PBF</span>  é um programa de transferência de renda para famílias em situação de pobreza e extrema pobreza. O mapeamento das famílias de baixa renda que atendem os requisitos para obter o auxílio é feito pelo Cadastro Único. Para este trabalho, utilizamos os dados do PBF de <strong>Setembro de 2023</strong>. </p>
</div>    
    """,
    unsafe_allow_html=True
)

#criando um espaço entre as visualizações
st.text("")

#criando os cartões com os valores totais do BPC, FPM e total de beneficiados
col1, col2, col3= st.columns(3)

with col1 :
    st.write(
        """
        <h2 style="font-size: 24px;">Número de famílias beneficiadas</h2>
        """,
        unsafe_allow_html=True
    )
    st.write("{:,}".format(df_filtrado['qtd_fam_beneficiadas'].sum()))
with col2 :
    st.write(
        """
        <h2 style="font-size: 24px;">Repasse total do PBF</h2>
        """,
        unsafe_allow_html=True
    )
    st.write("R${:,.2f}".format(df_filtrado['valor_repassado_bolsa_familia_s'].sum()))

with col3 :
    st.write(
        """
        <h2 style="font-size: 24px;">Valor médio do benefício por família</h2>
        """,
        unsafe_allow_html=True
    )
    st.write("R${:,.2f}".format(df_filtrado['pbf_vlr_medio_benef_f'].mean()))

#criando um espaço entre as visualizações
st.text("")

st.write(
    """
    <div style="text-align: justify">
<p> O   <span style="color: blue;">Cadastro Único</span> é um  mapa das famílias de baixa renda no Brasil, mostrando ao governo quem essas famílias são, como elas vivem e do que elas precisam para melhorar suas vidas. Atualmente,  considera-se "baixa renda" como aquele em a renda per capita familiar (rpcf) é menor do que 1/2 salário mínimo, dentro desta faixa, a *Pobreza* compreende a faixa em que rpcf está entre R$ 89,01 e R$ 178,00 e a *Extrema pobreza* quando a rpcf é <= R$ 89 reais. </p>
<p> Para este trabalho, utilizamos os dados do Cadastro Único de <strong>Agosto de 2023</strong>, posto que o pagamento do PBF baseia-se no Cadastro Único do mês anterior. </p>

 
</div>    
    """,
    unsafe_allow_html=True
)

st.text("")

#criando os cartões com os valores totais do BPC, FPM e total de beneficiados
col4, col5, col6= st.columns(3)

with col4 :
    st.write(
        """
        <h2 style="font-size: 24px;">Número de famílias de baixa renda</h2>
        """,
        unsafe_allow_html=True
    )
    st.write("{:,}".format(df_filtrado['cadunico_tot_fam_rpc_ate_meio_sm'].sum()))
with col5 :
    st.write(
        """
        <h2 style="font-size: 24px;">Número de famílias na faixa da pobreza</h2>
        """,
        unsafe_allow_html=True
    )
    st.write("{:,}".format(df_filtrado['cadunico_tot_fam_pob'].sum()))

with col6 :
    st.write(
        """
        <h2 style="font-size: 24px;">Número de famílias na faixa da extrema pobreza</h2>
        """,
        unsafe_allow_html=True
    )
    st.write("{:,}".format(df_filtrado['cadunico_tot_fam_ext_pob'].sum()))

#criando um espaço entre as visualizações
st.text("")

st.write(
    """
    <div style="text-align: justify">
<p> A Presença do Bolsa Família em cada município foi mensurada a partir da porcentagem de famílias atendidas pelo programa em relação ao total de famílias cadastradas como a faixa de pobreza ou extrema pobreza. 
<p> Considerando que o pagamento do benefício no mês baseia-se no Cadastro Único do mês anterior, utilizamos os dados do Cadastro Único de <strong>Agosto de 2023</strong>. </p>
  
</div>    
    """,
    unsafe_allow_html=True
)

## GRÁFICO do índice

# AJUSTA o dataframe
contagem_valores = df_filtrado['cl_indice_bf'].value_counts()
df_contagem_valores = pd.DataFrame(contagem_valores)
df_contagem_valores.reset_index(inplace = True)

# CRIA o gráfico
fig = px.bar(df_contagem_valores, x='cl_indice_bf', y='count')

# PERSONALIZAR o gráfico
fig.update_yaxes(title_text='Nº de municípios',
                # title_textfont =dict(size=20),
                tickfont=dict(size=18) # Tamanho da fonte 
)

fig.update_xaxes(
    title_text='% de famílias',
    tickvals=[1,2,3,4,5,6],  # Valores reais
    ticktext=['<=80%', '80-85%', '85-90%', '90-95%', '95-100%', '>100%'],  # Rótulos personalizados
    tickangle=0,  # Rotação dos rótulos
    tickfont=dict(size=18)# Tamanho da fonte
)
# EXIBIR o gráfico
st.header("Porcentagem de famílias abaixo da linha da pobreza que receberam o Bolsa Família em Setembro de 2023")
st.plotly_chart(fig, use_container_width=True)

#criando um espaço entre as visualizações
st.text("")


# MAPA
# cópia segura
resultados_df = df_filtrado.copy()
# dataframe info geográficas dos municípios
resultados_df = pd.merge(df_filtrado[['ibge_6', 'cl_indice_bf']],
                         georreferenciamento_df[['codigo_ibge', 'nome', 'latitude', 'longitude']],
                         left_on='ibge_6',
                         right_on='codigo_ibge',
                         how='inner')

# COROPLÉTICO 
#pio.renderers.default = 'iframe'
fig2 = px.choropleth(resultados_df,
                    geojson=geojson,
                    scope='south america',
                    color='cl_indice_bf',
                    color_continuous_scale="Reds",
                    locations='ibge_6',
                    featureidkey='properties.codarea',
                    hover_name='nome').update_layout(height=800, width=1000, autosize=False)

fig2.update_traces(marker_line_width=0)
fig2.update_geos(fitbounds="locations", visible=False)

# Exibir o gráfico no Streamlit
st.header("Índice Bolsa Família nos Municípios")
st.plotly_chart(fig2, use_container_width = True)