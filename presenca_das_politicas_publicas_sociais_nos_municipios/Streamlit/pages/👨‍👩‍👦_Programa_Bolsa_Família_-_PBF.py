#importando as bibliotecas

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import locale
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

escolha = st.sidebar.selectbox("Deseja filtrar os resultados?", ['Não', 'Sim'])

df_filtrado = df
if escolha == 'Sim':
    lista_regioes = df['Regiao'].unique().tolist()
    lista_regioes.insert(0, "Marcar Todos")
    regiao_selecionada = st.sidebar.selectbox("Selecione uma região:", lista_regioes)

    if regiao_selecionada != "Marcar Todos":
        df_filtrado = df[df['Regiao'] == regiao_selecionada]

        lista_estados = df_filtrado['ufSigla'].unique().tolist()
        lista_estados.insert(0, "Marcar Todos")
        estado_selecionado = st.sidebar.selectbox("Selecione um estado:", lista_estados)

        if estado_selecionado != "Marcar Todos":
            df_filtrado = df_filtrado[df_filtrado['ufSigla'] == estado_selecionado]

            lista_municipios = df_filtrado['Município_UF'].unique().tolist()
            lista_municipios.insert(0, "Marcar Todos")
            municipio_selecionado = st.sidebar.selectbox("Selecione um município:", lista_municipios)

            if municipio_selecionado != "Marcar Todos":
                df_filtrado = df_filtrado[df_filtrado['Município_UF'] == municipio_selecionado]

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
<p> O  <span style="color: blue;">PBF</span>  é um programa de transferência de renda para famílias em situação de pobreza e extrema pobreza. O mapeamento das famílias que atendem aos requisitos para obter o auxílio é feito no Cadastro Único. Para este trabalho, utilizamos os dados do PBF de <strong>Setembro de 2023</strong> e os dados do Cadastro Único de <strong>Agosto de 2023</strong>, posto que a folha de pagamento do PBF se baseia no Cadastro Único do mês anterior. </p>
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

st.text("")
st.text("")
st.text("")

st.write(
        """
        <div style="text-align: justify">
    <p> A presença do Bolsa Família em cada município foi mensurada a partir da porcentagem de famílias beneficiárias em relação ao total de famílias cadastradas na faixa de pobreza ou extrema pobreza. De acordo com a porcentagem de famílias atendidas, foi atribuído um índice para o município (IPBF), que varia de 0 a 6, sendo que 6 é quando mais de 100% das famílias elegíveis foram beneficiadas. </p>  
    </div>    
        """,
        unsafe_allow_html=True
    )
st.text("")
st.text("")
st.text("")
st.text("")


col4, col5= st.columns(2)

with col4 :
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
        ticktext=['<=80', '80-85', '85-90', '90-95', '95-100', '>100'],  # Rótulos personalizados
        tickangle=0,  # Rotação dos rótulos
        tickfont=dict(size=14)# Tamanho da fonte
    )
    # EXIBIR o gráfico
    # st.header("Famílias elegíveis beneficiadas em cada município")
    st.plotly_chart(fig, use_container_width=True)
    
    
with col5 :
    st.write(
        """
        <div style="text-align: justify">
        <p> Classes do IPBF:</p>  
        <p> 0: 0 % de famílias atendidas</p>  
        <p> 1: < 80 % de famílias atendidas</p>  
        <p> 2: 80-85 % de famílias atendidas</p>  
        <p> 3: 85-90 % de famílias atendidas</p>  
        <p> 4: 90-95 % de famílias atendidas</p>  
        <p> 5: 95-100 % de famílias atendidas</p>  
        <p> 6: >100 % de famílias atendidas</p>  

    </div>    
        """,
        unsafe_allow_html=True
    )
   
#criando um espaço entre as visualizações
st.text("")
  
# MAPA
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
                    color_continuous_midpoint = 3, 
                    locations='ibge_6',
                    featureidkey='properties.codarea',
                    hover_name='nome').update_layout(height=800, width=1000, autosize=False)

fig2.update_traces(marker_line_width=0)
fig2.update_geos(fitbounds="locations", visible=False)

# Exibir o gráfico no Streamlit
st.header("IPBF por Município")
st.plotly_chart(fig2, use_container_width = True)