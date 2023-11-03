#importando as bibliotecas
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import locale
import plotly.io as pio
import json 

st.set_page_config(layout="wide")

#carregando os dados
df = pd.read_csv('df_bpc_fpm_completa.csv')
georreferenciamento_df = pd.read_csv('georreferenciamento_df.csv')

with open('geojson', 'r') as geojson_file:
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
        <p>O  <span style="color: blue;">BPC</span> é o pagamento de um salário mínimo mensal ao idoso com 65 anos ou mais ou à pessoa com deficiência de qualquer idade com impedimentos de natureza física, mental, intelectual ou sensorial de longo prazo que comprovem não possuir meios de prover à própria manutenção ou tê-la provida por sua família. E cuja renda por pessoa do grupo familiar menor ou igual a 1/4 do salário-mínimo per capita vigente. </p>
  """,
    unsafe_allow_html=True
)

#criando um espaço entre as visualizações
st.text("")

#criando os cartões com os valores totais pagos do BPC e o total de beneficiados

col1, col2 = st.columns(2)

with col1 :
    st.write(
        """
        <h2 style="font-size: 18px;">Valor total pago do BPC em 2022</h2>
        """,
        unsafe_allow_html=True
    )
    st.write("R${:,.2f}".format(df_filtrado['bpc_val'].sum()).replace(',', ' ').replace('.', ',').replace(' ', '.'))


with col2 :
    st.write(
        """
        <h2 style="font-size: 18px;">Total de beneficiados em dez/2022</h2>
        """,
        unsafe_allow_html=True
    )
    st.write("{:,}".format(df_filtrado['bpc_ben'].sum()).replace(',', '.'))

#criando um espaço entre as visualizações
st.text("")

st.divider()

st.write(
    """
    <div style="text-align: center">
        <h2 style="color: black">Metodologia de cálculo da presença do BPC nos municípios</h2>
    </div>
    """,
    unsafe_allow_html=True
)

st.write(
    """
    <div style="text-align: justify">
        <p>Aqui, analisaremos o peso do benefício nos municípios brasileiros no ano de 2022 e, para tanto, utilizaremos como base o Fundo de Participação dos Municípios -  <span style="color: blue;">FPM</span> que é a maneira como a União repassa verbas para as cidades, cujo percentual, dentre outros fatores, é determinado principalmente pela proporção do número de habitantes estimado anualmente pelo IBGE. </p>
        <p> Isso significa que quanto maior o índice (a relação entre o BPC e o FPM), maior é o peso do benefício no município.</p>
        <p> Os índices foram divididos em 11 classes: <b>Classe 1</b> - Índice de 0 a 10%; <b>Classe 2</b> - Índice de 11 a 20%; <b>Classe 3</b> - Índice de 21 a 30%; <b>Classe 4</b> - Índice de 31 a 40%; <b>Classe 5</b> - Índice de 41 a 50%; <b>Classe 6</b> - Índice de 51 a 60%; <b>Classe 7</b> - Índice de 61 a 70%; <b>Classe 8</b> - Índice de 71 a 80%; <b>Classe 9</b> - Índice de 81 a 90%; <b>Classe 10</b> - Índice de 91 a 100%; <b>Classe 11</b> - Índice maior que 100%.<p>        
  """,
    unsafe_allow_html=True
)


#criando um espaço entre as visualizações
st.text("")

#criando os cartões com os valores totais do repasse do FPM e a média do índice
col3, col4= st.columns(2)


with col3 :
    st.write(
        """
        <h2 style="font-size: 18px;">Repasse total do FPM</h2>
        """,
        unsafe_allow_html=True
    )
    st.write("R${:,.2f}".format(df_filtrado['repasse_fpm'].sum()).replace(',', ' ').replace('.', ',').replace(' ', '.'))

with col4 :
    st.write(
        """
        <h2 style="font-size: 18px;">Índice Médio</h2>
        """,
        unsafe_allow_html=True
    )
    st.write("{:,.2f}%".format(df_filtrado['fpm_bpc'].mean()).replace('.', ','))

#criando um espaço entre as visualizações
st.text("")

col5, col6 = st.columns(2)

#criando o gráfico do índice
with col5:
    df_filtrado = df_filtrado.sort_values(by='Classe')
    df_filtrado2 = df_filtrado.groupby('Classe').agg({'count':'sum'}).reset_index()
    # Adicionando uma coluna formatada com os rótulos de dados
    fig = px.bar(df_filtrado2, x='Classe', y='count', text_auto=True, title = 'Relação entre o valor pago do BPC e o FPM')
    # Personalizando o gráfico
    fig.update_yaxes(title_text='Nº de municípios')
    fig.update_xaxes(
        title_text='Índice',
        tickvals=[1,2,3,4,5,6,7,8,9,10,11],
        ticktext=['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81-90', '91-100', '>100'], 
        tickangle=90, 
        tickfont=dict(size=12))
    fig.update_layout(height=600, width=45, autosize=False, title_x=0.2, title_y=0.93)
    # Exibindo o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)


#criando um espaço entre as visualizações
st.text("")

#criando o mapa
with col6 :
    #criando uma cópia segura dos dados
    resultados_df = df_filtrado.copy() 
    resultados_df = pd.merge(df_filtrado[['ibge_6', 'Classe']],
                             georreferenciamento_df[['codigo_ibge', 'nome', 'latitude', 'longitude']],
                             left_on='ibge_6',
                             right_on='codigo_ibge',
                             how='inner')
    #construindo o mapa choroplético 
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
    fig2.update_layout(title_text = 'Mapa com o impacto do BPC em relação ao FPM nos municípios', title_y = 0.95)
        # Exibindo o gráfico no Streamlit
    st.plotly_chart(fig2, use_container_width = True)
