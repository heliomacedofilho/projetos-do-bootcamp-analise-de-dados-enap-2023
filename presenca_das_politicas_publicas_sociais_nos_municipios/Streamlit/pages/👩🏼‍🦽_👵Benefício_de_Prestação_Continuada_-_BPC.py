#importando as bibliotecas
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import locale
import plotly.io as pio
import json 

#carregando os dados
df = pd.read_csv('data\df_bpc_fpm_completa.csv')
georreferenciamento_df = pd.read_csv('data\georreferenciamento_df.csv')

with open('data\geojson', 'r') as geojson_file:
    geojson = json.load(geojson_file)

#criando as caixas de seleção
escolha = st.sidebar.selectbox("Deseja filtrar os resultados?", ['Não', 'Sim'])
df_filtrado = df
if escolha == 'Sim':
    lista_regioes = df['Região'].unique().tolist()
    lista_regioes.insert(0, "Marcar Todos")
    regiao_selecionada = st.sidebar.selectbox("Selecione uma região:", lista_regioes)

    if regiao_selecionada != "Marcar Todos":
        df_filtrado = df[df['Região'] == regiao_selecionada]

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

#criando um título para a página
st.write(
    """
    <div style="text-align: center">
        <h1 style="color: black">Benefício de Prestação Continuada <br> 👩🏼‍🦽  <span style="color: blue">BPC</span>  &#x1F475 </h1>
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
        <p>O  <span style="color: blue;">BPC</span> garante um salário mínimo mensal à pessoa com deficiência e ao idoso com 65 anos ou mais que não tenham condições de prover a própria subsistência. </p>
        <p>Aqui, analisaremos o peso do benefício nos municípios brasileiros no ano de 2022 e, para tanto, utilizaremos como base o Fundo de Participação dos Municípios -  <span style="color: blue;">FPM</span> que é a maneira como a União repassa verbas para as cidades, cujo percentual, dentre outros fatores, é determinado principalmente pela proporção do número de habitantes estimado anualmente pelo IBGE. </p>
        <p> Isso significa que quanto maior o índice (a relação entre o BPC e o FPM), maior é o peso do benefício no município.</p>
    </div>
    """,
    unsafe_allow_html=True
)

#criando um espaço entre as visualizações
st.text("")

#criando os cartões com os valores totais do BPC, FPM e total de beneficiados
col1, col2, col3, col4= st.columns(4)

with col1 :
    st.write(
        """
        <h2 style="font-size: 18px;">Valor total pago do BPC</h2>
        """,
        unsafe_allow_html=True
    )
    st.write("R${:,.2f}".format(df_filtrado['bpc_val'].sum()))
with col2 :
    st.write(
        """
        <h2 style="font-size: 18px;">Repasse total do FPM</h2>
        """,
        unsafe_allow_html=True
    )
    st.write("R${:,.2f}".format(df_filtrado['repasse_fpm'].sum()))

with col3 :
    st.write(
        """
        <h2 style="font-size: 18px;">Total de beneficiados</h2>
        """,
        unsafe_allow_html=True
    )
    st.write("{:,}".format(df_filtrado['bpc_ben'].sum()))

with col4 :
    st.write(
        """
        <h2 style="font-size: 18px;">Índice Médio</h2>
        """,
        unsafe_allow_html=True
    )
    st.write("{:,.2f}%".format(df_filtrado['fpm_bpc'].mean()))

#criando um espaço entre as visualizações
st.text("")

col5, col6 = st.columns(2)

#criando o gráfico do índice
with col5:
    
    df_filtrado = df_filtrado.sort_values(by='Classe')
    df_filtrado2 = df_filtrado.groupby('Classe').agg({'count':'sum'}).reset_index()
    #    # Adicionando uma coluna formatada com os rótulos de dados
    fig = px.bar(df_filtrado2, x='Classe', y='count', text_auto=True)
        # Personalizando o gráfico
    fig.update_yaxes(title_text='Nº de municípios')
    fig.update_xaxes(
        title_text='Índice',
        tickvals=[1,2,3,4,5,6,7,8,9,10,11],  # Valores reais
        ticktext=['0-10%', '11-20%', '21-30%', '31-40%', '41-50%', '51-60%', '61-70%', '71-80%', '81-90%', '91-100%', '>100%'],          # Rótulos personalizados
        tickangle=90,  # Rotação dos rótulos
        tickfont=dict(size=12))# Tamanho da fonte
        # Exibir o gráfico no Streamlit
    st.write(
        """
        <h2 style="font-size: 22px; ">Relação entre o valor pago do BPC e o FPM</h2>
        """,
        unsafe_allow_html=True
    )
    st.plotly_chart(fig, use_container_width=True)
#criando um espaço entre as visualizações
st.text("")

with col6 :
    #criando o mapa
    resultados_df = df_filtrado.copy() #criando uma cópia segura dos dados
    resultados_df = pd.merge(df_filtrado[['ibge_6', 'Classe']],
                             georreferenciamento_df[['codigo_ibge', 'nome', 'latitude', 'longitude']],
                             left_on='ibge_6',
                             right_on='codigo_ibge',
                             how='inner')
    #construir o mapa choroplético 
    fig2 = px.choropleth(resultados_df,
                        geojson=geojson,
                        scope='south america',
                        color='Classe',
                        color_continuous_scale="Blues",
                        color_continuous_midpoint = 5.5,
                        locations='ibge_6',
                        featureidkey='properties.codarea',
                        hover_name='nome').update_layout(height=800, width=1000, autosize=False)
    fig2.update_traces(marker_line_width=0)
    fig2.update_geos(fitbounds="locations", visible=False) #só aparece Brasil
        # Exibir o gráfico no Streamlit
    st.write(
        """
        <h2 style="font-size: 22px;  ">Mapa com o impacto do BPC em relação ao FPM nos municípios</h2>
        """,
        unsafe_allow_html=True
    )
    st.plotly_chart(fig2, use_container_width = True)