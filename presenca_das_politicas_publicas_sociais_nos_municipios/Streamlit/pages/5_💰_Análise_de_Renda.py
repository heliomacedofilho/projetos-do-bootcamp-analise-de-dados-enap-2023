# Importando as bibliotecas

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import locale
import plotly.io as pio
import json

st.set_page_config(layout="wide")

# criando título para página
st.write(
    """
    <div style="text-align: center;">
        <h1 style="color: black;">Análise de Renda</span>💰</h1>
    </div>
    """,
    unsafe_allow_html=True
)

#carregando os dados
df = pd.read_csv('resultado_tax_pob.csv')
df2 = pd.read_csv('mob_evolucao_pob_e_ext_pob_sum_01_mp2.csv')
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

            lista_municipios = df_filtrado['municipio_x'].unique().tolist()
            lista_municipios.insert(0, "Marcar Todos")
            municipio_selecionado = st.sidebar.selectbox("Selecione um município:", lista_municipios)

            if municipio_selecionado != "Marcar Todos":
                df_filtrado = df_filtrado[df_filtrado['municipio_x'] == municipio_selecionado]

 
st.write(
    """
    <div style="text-align: center;">
        <h2 style="color: black;">Análise da Taxa da Pobreza do <span style="color: blue;">CadÚnico</span> 💻</h2>
    </div>
    """,
    unsafe_allow_html=True)

#criando um espaço entre as visualizações
st.text("")

#criando o texto explicativo do programa
st.write(
    """
    <div style="text-align: justify">
<p>        O  <span style="color: blue;">Cadastro Único para Programas Sociais</span> é um instrumento que identifica e caracteriza as famílias de baixa renda, permitindo que o governo conheça melhor a realidade socioeconômica dessa população que reside em todo território nacional. Nele são registradas informações como: características da residência, identificação de cada pessoa da família, escolaridade, situação de trabalho e renda, entre outras. Isso facilita o diagnóstico para a criação de novos programas e a organização da oferta de serviços para essa população, além da seleção de público para esses programas e serviços.

<p>    O público-alvo são as famílias que vivem com renda mensal de até <b>meio salário-mínimo por pessoa</b>. As famílias com renda acima desse valor podem ser cadastradas para participar de programas ou serviços específicos. Destaca-se que o cadastramento leva em conta se as famílias fazem parte de povos e comunidades tradicionais ou de grupos específicos, entre eles, indígenas, quilombolas, ribeirinhos e população em situação de rua. 
    </div>
    """,
    unsafe_allow_html=True
)

#criando um espaço entre as visualizações
st.text("")

#criando o texto explicativo com a metodologia da análise da renda
st.divider()
st.write(
 """
    <div style="text-align: center;">
        <h2 style="color: black;">Metodologia da análise da Taxa da Pobreza 💠</h2>
    </div>
    """,
    unsafe_allow_html=True)
st.write(
    """
    <div style="text-align: justify">
<p>A partir dos dados do CadÚnico, de abril/2012 e de agosto/2023, foram feitas análises das taxas de pobreza do Cadastro Único, utilizando para tanto o total do número de pessoas nas faixas da pobreza e da extrema-pobreza, dividido pela população do Censo de 2010 e do Censo de 2023, respectivamente. O recorte de 2012 para calcular a taxa da pobreza com base na população do Censo de 2010 se deve ao fato de apenas a partir de abril/2012 constarem dados por faixa de renda. 

<p>Posteriormente, o resultado da diferença das taxas de pobreza de 2012 e 2023 foi dividido em classes de intervalos de diminuição ou aumento da taxa da pobreza, conforme apresentado no gráfico abaixo.


<p>Os valores de cada classe são: <b>Classe 1</b> - Aumento de até 20% da taxa da pobreza; <b>Classe 2</b> - Aumento entre 10% e 20% da taxa da pobreza; <b>Classe 3</b> - Aumento de até 10% data taxa da pobreza; <b>Classe 4</b> - Sem alteração da taxa da pobreza; <b>Classe 5</b> - Redução de até 10% da taxa de pobreza; <b>Classe 6</b> - Redução da Taxa da pobreza entre 10% a 20%; <b>Classe 7</b> - Redução da Taxa da pobreza entre 20% a 30%; <b>Classe 8</b> - Redução da Taxa da Pobreza em mais de 30%.
</div>
    """,
    unsafe_allow_html=True
)

#criando um espaço entre as visualizações
st.text("")

#criando os cartões com os valores totais das taxas de pobreza
col1, col2, col3= st.columns(3)

with col1 :
    st.write(
        """
        <h2 style="font-size: 24px;">Taxa da pobreza CadÚnico 04/2012 pelo Censo 2010</h2>
        """,
        unsafe_allow_html=True
    )
    st.write("{:,.3f}".format(df_filtrado['tx_pob_extpob_x'].mean()).replace(',', '.'))
with col2 :
    st.write(
        """
        <h2 style="font-size: 24px;">Taxa da pobreza CadÚnico 08/2023 pelo Censo 2022</h2>
        """,
        unsafe_allow_html=True
    )
    st.write("{:,.3f}".format(df_filtrado['tx_pob_extpob_y'].mean()).replace(',', '.'))

with col3 :
    st.write(
        """
        <h2 style="font-size: 24px;">Diferença da taxa da pobreza de 2012 e 2023</h2>
        """,
        unsafe_allow_html=True
    )
    st.write("{:,.3f}".format(df_filtrado['Dif_taxa_12_23'].mean()).replace(',', '.'))
    
    #criando um espaço entre as visualizações
st.text("")

col4, col5= st.columns(2)

with col4 :
 
# GRÁFICO do índice
# AJUSTA o dataframe
    contagem_valores = df_filtrado['Classe_dif_taxa_12_23'].value_counts()
    df_contagem_valores = pd.DataFrame(contagem_valores)
    df_contagem_valores.reset_index(inplace = True)

# CRIA o gráfico
    fig = px.bar(df_contagem_valores, x='Classe_dif_taxa_12_23', y='count', text_auto=True,
                title='Diferença das taxas de pobreza do CadÚnico 2012 e 2023')

# PERSONALIZAR o gráfico
    fig.update_yaxes(title_text='Nº de municípios',
                #title_textfont =dict(size=20),
                tickfont=dict(size=18)) # Tamanho da fonte 


    fig.update_xaxes(
        title_text='Aumento ou diminuição das taxas de pobreza em %',
        tickvals=[1,2,3,4,5,6,7,8],  # Valores reais
        ticktext=['Aum <20', 'Aum 10a20','Aum <10', 'Igual', 'Dim <10', 'Dim 10a20', 'Dim 20a30', 'Dim >30'],
        # Rótulos personalizados
        tickangle=-45,  # Rotação dos rótulos
        tickfont=dict(size=18))# Tamanho da fonte
   
    #fig.update_layout(title_y=0.9)
    fig.update_layout(height=600, width=150, autosize=False)
    
# EXIBIR o gráfico
    #st.header("Diferença das taxas de pobreza do CadÚnico 2012 e 2023")
    st.plotly_chart(fig, use_container_width=True)


with col5 :
# MAPA
# cópia segura
    resultados_df = df_filtrado.copy()
# dataframe info geográficas dos municípios
    resultados_df = pd.merge(df_filtrado[['ibge_6', 'Dif_taxa_12_23']],
                         georreferenciamento_df[['codigo_ibge', 'nome', 'latitude', 'longitude']],
                         left_on='ibge_6',
                         right_on='codigo_ibge',
                         how='inner')

# COROPLÉTICO 
#pio.renderers.default = 'iframe'
    fig2 = px.choropleth(resultados_df,
                    geojson=geojson,
                    title="Diferença das taxas de pobreza do CadÚnico 2012 e 2023",
                    scope='south america',
                    color='Dif_taxa_12_23',
                    color_continuous_scale="RdBu_r",
                    color_continuous_midpoint = 0.0,
                    locations='ibge_6',
                    featureidkey='properties.codarea',
                    hover_name='nome').update_layout(height=800, width=1000, autosize=False)
    
    #fig2.update_layout(title_y=0.9)
    fig2.update_traces(marker_line_width=0)
    fig2.update_geos(fitbounds="locations", visible=False)

# Exibir o gráfico no Streamlit
    #st.header("Diferença das taxas de pobreza do CadÚnico 2012 e 2023")
    st.plotly_chart(fig2, use_container_width = True)
    

#criando o texto explicativo sobre a evolução do tamanhos da faixa da pobreza ao longo do tempo
st.divider()
st.write(
 """
    <div style="text-align: center;">
        <h2 style="color: black;">Variação do nº de famílias na faixa da pobreza no <span style="color: blue;">CadÚnico</span> ao longo do tempo💸</h2>
    </div>
    """,
    unsafe_allow_html=True)
#criando um espaço entre as visualizações
st.text("")
st.write(
    """
    <div style="text-align: justify">
A partir dos dados do CadÚnico, de 2012 a 2023, foram feitas análises da variação do número total de famílias em situação de pobreza e de extrema-pobreza, ou seja, que se encontram na faixa da pobreza. Para tanto, foram utilizados os dados do mês de agosto de cada ano, e o resultado da análise está representado no mapa abaixo.

</div>
    """,
    unsafe_allow_html=True
)



#criando um espaço entre as visualizações
st.text("")

# MAPA evolução da faixa da pobreza
# AJUSTA o dataframe
contagem_valores2 = df2['valor'].value_counts()
df_contagem_valores2 = pd.DataFrame(contagem_valores2)
df_contagem_valores2.reset_index(inplace = True)

# cópia segura
resultados_df2 = df2.copy()
# dataframe info geográficas dos municípios
resultados_df2 = pd.merge(df2[['ibge_6','ano', 'valor']],
                        georreferenciamento_df[['codigo_ibge', 'nome', 'latitude', 'longitude']],
                        left_on='ibge_6',
                        right_on='codigo_ibge',
                        how='inner')

# COROPLÉTICO 
#pio.renderers.default = 'iframe'
fig3 = px.choropleth(resultados_df2,
                    geojson=geojson,
                    scope='south america',
                    color='valor',
                    color_continuous_scale="Oryel",
                    locations='ibge_6',
                    featureidkey='properties.codarea',
                    hover_name='nome',
                    animation_frame='ano').update_layout(height=800, width=1000, autosize=False)

fig3.update_layout(
    title_text='Variação do nº de famílias do CadÚnico na faixa da pobreza ao longo do tempo',
    title_x=0.2,  title_y=0.9)  # Define o título no centro horizontal do gráfico

fig3.update_traces(marker_line_width=0)
fig3.update_geos(fitbounds="locations", visible=False)

# Exibir o gráfico no Streamlit
#st.header("Evolução da faixa da pobreza das famílias do CadÚnico")
st.plotly_chart(fig3, use_container_width = True)
    
