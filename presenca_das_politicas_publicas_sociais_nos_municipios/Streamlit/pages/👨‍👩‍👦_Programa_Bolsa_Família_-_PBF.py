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

st.set_page_config(layout="wide")

#carregando os dados
df = pd.read_csv('df_pbf_cadunico_streamlit.csv')
georreferenciamento_df = pd.read_csv('georreferenciamento_df.csv')
with open('geojson', 'r') as geojson_file:    
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
<p> O  <span style="color: blue;">PBF</span>  é um programa de transferência de renda para famílias em situação de pobreza e extrema pobreza que estão no Cadastro Único e atendem os demais critérios definidos na legislação. Para avaliar a presença do PBF em cada município, utilizamos os dados do PBF de <strong>Setembro de 2023</strong> e os dados do Cadastro Único de <strong>Agosto de 2023</strong>, posto que a folha de pagamento do PBF se baseia no Cadastro Único do mês anterior. </p>
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
    st.write("{:,}".format(df_filtrado['qtd_fam_beneficiadas'].sum()).replace(',', '.'))
    
with col2 :
    st.write(
        """
        <h2 style="font-size: 24px;">Repasse total do PBF</h2>
        """,
        unsafe_allow_html=True
    )
    st.write("R${:,.2f}".format(df_filtrado['valor_repassado_bolsa_familia_s'].sum()).replace(',', ' ').replace('.', ',').replace(' ', '.'))

with col3 :
    st.write(
        """
        <h2 style="font-size: 24px;">Valor médio do benefício por família</h2>
        """,
        unsafe_allow_html=True
    )
    st.write("R${:,.2f}".format(df_filtrado['pbf_vlr_medio_benef_f'].mean()).replace('.', ','))

st.text("")
#criando divisão na página
st.divider()

st.write(
 """
    <div style="text-align: center;">
        <h2 style="color: black;">Metodologia da avaliação da presença do Bolsa Família nos municípios 💠</h2>
    </div>
    """,
    unsafe_allow_html=True)

st.write(
        """
        <div style="text-align: justify">
    <p> A presença do Bolsa Família em cada município foi mensurada a partir da porcentagem de famílias beneficiárias em relação ao total de famílias cadastradas na faixa de pobreza ou extrema pobreza. De acordo com o resultado da porcentagem de famílias elegíveis que foram  beneficiadas, o município foi incluído em uma classe do <b>Índice Programa Bolsa Família (IPBF)</b>: <b>Classe 1</b> - menos de 80 % de famílias elegíveis beneficiadas; <b>Classe 2</b> - entre 80 e 85 % de famílias elegíveis beneficiadas; <b>Classe 3</b> - entre 85 e 90 % de famílias elegíveis beneficiadas; <b>Classe 4</b> - entre 90 e 95 % de famílias elegíveis beneficiadas; <b>Classe 5</b> - entre 95 e 100 % de famílias elegíveis beneficiadas; <b>Classe 6</b> - mais de 100 % de famílias elegíveis beneficiadas</p>  
    </div>    
        """,
    unsafe_allow_html=True
)
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
    fig = px.bar(df_contagem_valores, x='cl_indice_bf', y='count', text_auto=True,
                title='Contagem de municípios por classe do IPBF')
    
    # PERSONALIZAR o gráfico
    fig.update_yaxes(title_text='Nº de municípios',
                    # title_textfont =dict(size=20),
                    tickfont=dict(size=18) # Tamanho da fonte 
    )
    
    fig.update_xaxes(
        title_text='% de famílias elegíveis beneficiadas',
        tickvals=[1,2,3,4,5,6],  # Valores reais
        ticktext=['<=80', '80-85', '85-90', '90-95', '95-100', '>100'],  # Rótulos personalizados
        tickangle=0,  # Rotação dos rótulos
        tickfont=dict(size=14)# Tamanho da fonte
    )
    # EXIBIR o gráfico
    # st.header("Famílias elegíveis beneficiadas em cada município")
    fig.update_layout(title_x=0.2, title_y=0.9)
    fig.update_layout(height=600, width=60, autosize=False)
    st.plotly_chart(fig, use_container_width=True)
    
    
with col5 :
    # MAPA
    # dataframe info geográficas dos municípios
    resultados_df = pd.merge(df_filtrado[['ibge_6', 'cl_indice_bf']],
                             georreferenciamento_df[['codigo_ibge', 'nome', 'latitude', 'longitude']],
                             left_on='ibge_6',
                             right_on='codigo_ibge',
                             how='inner')
    resultados_df.rename(columns={'cl_indice_bf': 'Classe'}, inplace = True)
    # COROPLÉTICO 
    #pio.renderers.default = 'iframe'
    fig2 = px.choropleth(resultados_df,
                        geojson=geojson,
                        scope='south america',
                        color='Classe',
                        color_continuous_scale="Blues",
                        color_continuous_midpoint = 3, 
                        locations='ibge_6',
                        featureidkey='properties.codarea',
                        hover_name='nome')
    
    fig2.update_layout(height=600, width=60, autosize=False)
    fig2.update_layout(
    title_text='IPBF em cada Município',
    title_x=0.3, title_y=0.9)  # Define o título no centro horizontal do gráfico
    fig2.update_traces(marker_line_width=0)
    fig2.update_geos(fitbounds="locations", visible=False)
    
    # Exibir o gráfico no Streamlit
    #st.header("IPBF por Município")
    
    st.plotly_chart(fig2, use_container_width = True)