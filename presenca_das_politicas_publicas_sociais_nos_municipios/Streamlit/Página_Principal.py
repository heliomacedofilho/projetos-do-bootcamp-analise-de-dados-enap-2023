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
from PIL import Image

#carregando os dados
df = pd.read_csv('df_indice_pps_streamlit.csv')
georreferenciamento_df = pd.read_csv('georreferenciamento_df.csv')
with open('geojson', 'r') as geojson_file:
    geojson = json.load(geojson_file)

st.set_page_config(
    page_title='Presença das Políticas Públicas Sociais nos municípios brasileiros :earth_americas:',
    page_icon='📊',
    layout='wide',
    initial_sidebar_state='expanded',
    menu_items={
        'Get Help': 'http://www.meusite.com.br',
        'Report a bug': "http://www.meuoutrosite.com.br",
        'About': "Esse app foi desenvolvido no curso ENAP ."
    }
)

st.markdown('# Presença das políticas públicas sociais nos municípios brasileiros :earth_americas:')


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


#criando um espaço entre as visualizações
st.text("")

#criando o texto explicativo
st.write(
    """
    <div style="text-align: justify">
<p> Para a avaliação da presença das Políticas Públicas Sociais (PPS) nos municípios brasileiros, foram selecionadas políticas de responsabilidade do Ministério do Desenvolvimento e Assistência Social, Família e Combate à Fome (MDS), que fossem universais e cujos dados estivessem disponibilizados no Portal de Dados Abertos. 

</p> Desta forma, foram selecionadas três políticas e um indicador: Programa Bolsa Família (PBF), Benefício de Prestação Continuada (BPC), Registro Mensal de Atendimentos dos  Centros de Referência da Assistência Social (CRAS) e o Índice de Gestão Descentralizada Municipal (IGD-M), o qual mede a qualidade da gestão do Cadastro Único e do PBF. 

</p> Para avaliar a presença das PPS selecionadas em cada um dos municípios brasileiros, foi definido um índice composto pelo resultado da análise da presença de cada uma das políticas, cujo detalhamento consta nas páginas específicas das políticas. 

</p> Cada município poderia pontuar de 0 a 10 pontos, de acordo com o resultado do Índice da presença das PPS nos municípios brasileiros, conforme apresentado nos gráficos abaixo. </p>
</div>    
    """,
    unsafe_allow_html=True
)


#criando um espaço entre as visualizações
st.text("")

#criando os cartões com os valores totais do BPC, FPM e total de beneficiados
#col1, col2= st.columns(2)

# #with col1 :
#     st.write(
#         """
#         <h2 style="font-size: 24px;">XXX</h2>
#         """,
#         unsafe_allow_html=True
#     )
#     #st.write("{:,}".format(df_filtrado['qtd_fam_beneficiadas'].sum()))
# with col2:
## GRÁFICO do índice
# AJUSTA o dataframe
contagem_valores = df_filtrado['indice_pps'].value_counts()
df_contagem_valores = pd.DataFrame(contagem_valores)
df_contagem_valores.reset_index(inplace = True)
    
# CRIA o gráfico
fig = px.bar(df_contagem_valores, x='indice_pps', y='count',
            title="Índice da Presença de Políticas Públicas Sociais nos Municípios")
    
# PERSONALIZAR o gráfico
fig.update_yaxes(title_text='Nº de municípios',
                    # title_textfont =dict(size=20),
                    tickfont=dict(size=18) # Tamanho da fonte 
    )
    
fig.update_xaxes(
        title_text='Índice Presença de Políticas Públicas',
        tickvals=[1,2,3,4,5,6,7,8,9,10],  # Valores reais
        ticktext=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],  # Rótulos personalizados
        tickangle=0,  # Rotação dos rótulos
        tickfont=dict(size=18)# Tamanho da fonte
    )
# EXIBIR o gráfico
#st.header("Índice de Presença de Políticas Públicas nos Municípios (1-10)")
fig.update_layout(title_x=0.3)
st.plotly_chart(fig, use_container_width=True)
    
#criando um espaço entre as visualizações
st.text("")
    

# MAPA
# cópia segura
resultados_df = df_filtrado.copy()
# dataframe info geográficas dos municípios
resultados_df = pd.merge(df_filtrado[['ibge_6', 'indice_pps']],
                         georreferenciamento_df[['codigo_ibge', 'nome', 'latitude', 'longitude']],
                         left_on='ibge_6',
                         right_on='codigo_ibge',
                         how='inner')

# COROPLÉTICO 
#pio.renderers.default = 'iframe'
fig2 = px.choropleth(resultados_df,
                    geojson=geojson,
                    title="Índice da Presença de Políticas Públicas Sociais nos Municípios",
                    scope='south america',
                    color='indice_pps',
                    color_continuous_scale="Reds",
                    locations='ibge_6',
                    featureidkey='properties.codarea',
                    hover_name='nome').update_layout(height=800, width=1000, autosize=False)

fig2.update_layout(title_x=0.3, title_y=0.9)
fig2.update_traces(marker_line_width=0)
fig2.update_geos(fitbounds="locations", visible=False)

# Exibir o gráfico no Streamlit
#st.header("Índice de Presença de Políticas Públicas nos Municípios (0-10)")
st.plotly_chart(fig2, use_container_width = True)

#criando um espaço entre as visualizações
st.text("")

st.subheader('**Autoras do projeto**') 

st.write(
    """
    <div style="text-align: justify">
<p> - Aline Oliveira Moura
<p> - Camila Abuassi de Faro Passos 
<p> - Cristiane Lopes de Assis 
<p> - Juliana Pierrobon Lopez 
<p> - Mariana Nogueira de Resende Sousa   
    """,
    unsafe_allow_html=True
)