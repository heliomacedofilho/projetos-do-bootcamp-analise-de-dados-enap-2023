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
df = pd.read_csv('df_RMA_completa.csv')
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
    <div style="text-align: center;">
        <h1 style="color: black;">Registro Mensal de Atendimentos - RMA nos Centro de Referência de Assistência Social - CRAS <br> <span style="color: blue;">RMA</span> &#x1f4cb;</h1>
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
        <p>O <b>Registro Mensal de Atendimentos - RMA </b> é um sistema onde são registradas mensalmente as informações relativas aos serviços ofertados e o volume de atendimentos nos Centros de Referência da Assistência Social (CRAS), Centros de Referência Especializados de Assistência Social (CREAS) e Centro de Referência Especializado para População em Situação de Rua (Centros POP). </p>
        <p>O Centro de Referência de Assistência Social - CRAS é uma unidade pública de atendimento à população que oferece diversos serviços de Assistência Social. No CRAS, as pessoas podem fazer o Cadastro Único, ter orientação sobre os benefícios sociais, ter acesso a serviços, benefícios e projetos de assistência social, orientação sobre direitos e serviços públicos.</p>    
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
        <h2 style="font-size: 22px;">Média de atendimentos por mês em 2022</h2>
        """,
        unsafe_allow_html=True
    )
    st.write("{:,.0f}".format(df_filtrado['media_c1'].sum()).replace(',', '.'))
with col2 :
    st.write(
        """
        <h2 style="font-size: 22px;">Total de atendimentos em 2022</h2>
        """,
        unsafe_allow_html=True
    )
    st.write("{:,.0f}".format(df_filtrado['soma_c1'].sum()).replace(',', '.'))

with col3 :
    st.write(
        """
        <h2 style="font-size: 22px;">Número de pessoas na faixa de pobreza e extrema pobreza (Cadastro Único - Dez/2022)</h2>
        """,
        unsafe_allow_html=True
    )
    st.write("{:,.0f}".format(df_filtrado['Dez_tot_pes_pob_e_ext_pob'].sum()).replace(',', '.'))

with col4 :
    st.write(
        """
        <h2 style="font-size: 22px;">Número de Centro de Referência de Assistência Social - CRAS</h2>
        """,
        unsafe_allow_html=True
    )
    st.write("{:,.0f}".format(df_filtrado['total_max_cras'].sum()).replace(',', '.'))

st.divider()
#criando um espaço entre as visualizações
st.text("")
st.write(
       """
    <div style="text-align: center;">
        <h2 style="color: black;">Metodologia para avaliação do número de atendimentos - RMA nos municípios<br> </h2>
        <br>    
    </div>
    <div style="text-align: justify">
        <p> A avaliação do número de atendimentos nos CRAS foi calculada por meio da média de atendimento mensal dos municípios dividida pelo número de pessoas do cadastro único de dezembro de 2022 classificadas na faixa de pobreza e extrema pobreza multiplicado por 100. </p>      
        <p> Desta forma, foi obtido o atendimento médio (RMA médio) para cada 100 pessoas classificadas na faixa de pobreza e extrema pobreza. </p>
        <p> O resultado do cálculo foi dividido em classes e cada município foi classificado de acordo com a sua faixa de atendimento. Quanto maior o valor encontrado, maior é o número de atendimentos efetuado pelo município à população que necessita da assistência social. </p>
<p> As classes definidas foram: <b>classe 0</b> - sem informação, <b>classe 1</b> - atendimento maior que 0 a 5, <b>classe 2</b> - atendimento maior que 5 a 10, <b>classe 3</b> - atendimento maior que 10 a 15, <b>classe 4</b> - atendimento maior que 15 a 20, <b>classe 5</b> - atendimento maior que 20 a 25, <b>classe 6</b> - atendimento maior que 25 a 30, <b>classe 7</b> - atendimento maior que 30 a 35, <b>classe 8</b> - atendimento maior que 35 a 40, <b>classe 9</b> - atendimento maior que 40 a 45, <b>classe 10</b>- atendimento maior que 45 a 50, <b>classe 11</b>- atendimento maior que 50.</p> 
           </div>
    """,
    unsafe_allow_html=True
)

col5, col6= st.columns(2)

with col5 :
    #criando o gráfico do índice
    # Adicionando uma coluna formatada com os rótulos de dados
    contagem_valores = df_filtrado['Classe'].value_counts()
    df_contagem_valores = pd.DataFrame(contagem_valores)
    df_contagem_valores.sort_values(by='Classe')
    df_contagem_valores.reset_index(inplace=True)
    df_contagem_valores.rename(columns={'count':'Quantidade'}, inplace=True)
        # Criando o gráfico
    fig = px.bar(df_contagem_valores, x='Classe', y='Quantidade', text_auto=True,
                title='Número médio de atendimentos mensal a cada 100 pessoas')
   
    fig.update_layout(height=600, width=45, autosize=False, title_x=0.2)
           
    # PERSONALIZAR o gráfico
    fig.update_yaxes(title_text='Nº de municípios',
                    # title_textfont =dict(size=20),
                    tickfont=dict(size=16) # Tamanho da fonte 
                    )

    fig.update_traces(text=df_contagem_valores['Quantidade'], texttemplate='%{text}', textposition='outside', textfont=dict(size=12) )
    
    fig.update_xaxes(
        title_text='',
        tickvals=[0,1,2,3,4,5,6,7,8,9,10,11],  # Valores reais
        ticktext=['0','> 0-5', '>5-10', '>10-15', '>15-20', '>20-25', '>25-30', '>30-35', '>35-40', '>40-45', '>45-50', '>50'],  # Rótulos personalizados
        tickangle=-45,  # Rotação dos rótulos
        tickfont=dict(size=16)# Tamanho da fonte
    )
    fig.update_layout(
    yaxis=dict(
        fixedrange=False,  # Permitir rolagem na direção y
        range=[0, max(df_contagem_valores['Quantidade']) * 1.1]  # Ajustar a faixa do eixo y conforme necessário
    ))  
    
    # EXIBIR o gráfico  
    
    st.plotly_chart(fig, use_container_width=True)


#criando um espaço entre as visualizações
#st.text("")
with col6 :
    #criando o mapa
        #criando uma cópia segura dos dados
    resultados_df = df_filtrado.copy()
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
                        color_continuous_midpoint = 5.5,
                        locations='ibge_6',
                        featureidkey='properties.codarea',
                        hover_name='nome').update_layout(height=800, width=1000, autosize=False)
    
    fig2.update_traces(marker_line_width=0)
    
    fig2.update_geos(fitbounds="locations", visible=False) #só aparece Brasil

    fig2.update_layout(
    title_text='Mapa de atendimento médio (RMA médio) a cada 100 pessoas',   title_x=0.15,  title_y=0.95)
   
            # Exibir o gráfico no Streamlit
    st.plotly_chart(fig2, use_container_width = True)


