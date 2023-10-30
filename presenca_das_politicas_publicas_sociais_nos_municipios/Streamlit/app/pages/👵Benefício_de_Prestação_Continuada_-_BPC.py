#importando as bibliotecas
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import locale
import plotly.io as pio

#carregando os dados
df = pd.read_csv('data\df_bpc_fpm_completa.csv')
georreferenciamento_df = pd.read_csv('https://raw.githubusercontent.com/kelvins/Municipios-Brasileiros/main/csv/municipios.csv')

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
    <div style="text-align: center;">
        <h1 style="color: black;">Benefício de Prestação Continuada <br> <span style="color: blue;">BPC</span> &#x1F475;</h1>
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
        O  <span style="color: blue;">BPC</span> garante um salário mínimo mensal à pessoa com deficiência e ao idoso com 65 anos ou mais que não tenham condições de prover a própria subsistência. Aqui, analisaremos o peso do benefício nos municípios brasileiros no ano de 2022 e, para tanto, utilizaremos como base o Fundo de Participação dos Municípios -  <span style="color: blue;">FPM</span> que é a maneira como a União repassa verbas para as cidades, cujo percentual, dentre outros fatores, é determinado principalmente pela proporção do número de habitantes estimado anualmente pelo IBGE. Isso significa que quanto maior o índice (a relação entre o BPC e o FPM), maior é o peso do benefício no município.
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
        <h2 style="font-size: 24px;">Valor total pago do BPC</h2>
        """,
        unsafe_allow_html=True
    )
    st.write("R${:,.2f}".format(df_filtrado['bpc_val'].sum()))
with col2 :
    st.write(
        """
        <h2 style="font-size: 24px;">Repasse total do FPM</h2>
        """,
        unsafe_allow_html=True
    )
    st.write("R${:,.2f}".format(df_filtrado['repasse_fpm'].sum()))

with col3 :
    st.write(
        """
        <h2 style="font-size: 24px;">Total de beneficiados</h2>
        """,
        unsafe_allow_html=True
    )
    st.write("{:,}".format(df_filtrado['bpc_ben'].sum()))

#criando um espaço entre as visualizações
st.text("")

#criando o gráfico do índice
df_filtrado = df_filtrado.sort_values(by='Classe')
    # Adicionando uma coluna formatada com os rótulos de dados
df_filtrado['rótulo_dados'] = df_filtrado['count']
    # Criando o gráfico
fig = px.bar(df_filtrado, x='Classe', y='count')
    # Personalizando o gráfico
fig.update_traces(texttemplate='%{customdata}', customdata=df_filtrado['rótulo_dados'], textposition='outside')  # Adicionar rótulos de dados
fig.update_yaxes(showticklabels=False,  # Remover marcações do eixo y
                title_text='Nº de municípios')
fig.update_xaxes(
    title_text='Índice',
    tickvals=[1, 2,3,4,5,6,7,8,9,10,11],  # Valores reais
    ticktext=['0-10%', '11-20%', '21-30%', '31-40%', '41-50%', '51-60%', '61-70%', '71-80%', '81-90%', '91-100%', '>100%'],  # Rótulos personalizados
    tickangle=90,  # Rotação dos rótulos
    tickfont=dict(size=12)# Tamanho da fonte
)
    # Exibir o gráfico no Streamlit
st.header("Relação entre o valor pago do BPC e o FPM")
st.plotly_chart(fig, use_container_width=True)

#criando um espaço entre as visualizações
st.text("")

#criando o mapa
    #criando uma cópia segura dos dados
resultados_df = df_filtrado.copy()
    #criando dataframe com informações de georreferenciamento de municípios
    #os dados de georreferenciamento tem 7 dígitos (vamos remover o dígito verificador e atualizar o dataframe)
georreferenciamento_df['codigo_ibge'] = georreferenciamento_df['codigo_ibge'].astype('str').map(lambda x: x[:-1]).astype('int')
    #cruzamento do dataframe resultados com as informações de georreferenciamento
resultados_df = pd.merge(df_filtrado[['ibge_6', 'Classe']],
                         georreferenciamento_df[['codigo_ibge', 'nome', 'latitude', 'longitude']],
                         left_on='ibge_6',
                         right_on='codigo_ibge',
                         how='inner')
    #puxar a malha geográfica do brasil a nível de município
import requests
geojson = requests.get(f'http://servicodados.ibge.gov.br/api/v3/malhas/paises/BR?formato=application/vnd.geo+json&qualidade=minima&intrarregiao=municipio').json()
    #a malha geográfica do ibge tem 7 dígitos (vamos remover o dígito verificador e atualizar a malha)
from geojson_rewind import rewind
for feature in geojson['features']:
    feature['properties']['codarea'] = feature['properties']['codarea'][:-1]
geojson = rewind(geojson, rfc7946=False)
    #construir o mapa choroplético 
pio.renderers.default = 'iframe'
fig2 = px.choropleth(resultados_df,
                    geojson=geojson,
                    scope='south america',
                    color='Classe',
                    color_continuous_scale="Blues",
                    locations='ibge_6',
                    featureidkey='properties.codarea',
                    hover_name='nome').update_layout(height=800, width=1000, autosize=False)
fig2.update_traces(marker_line_width=0)
    # Exibir o gráfico no Streamlit
st.header("Mapa com o impacto do BPC em relação ao FPM nos municípios ")
st.plotly_chart(fig2, use_container_width = True)