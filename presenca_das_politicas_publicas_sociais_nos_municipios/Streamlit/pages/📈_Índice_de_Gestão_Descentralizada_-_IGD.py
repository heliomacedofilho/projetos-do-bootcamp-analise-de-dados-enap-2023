import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import locale
import plotly.io as pio
import  json

st.set_page_config(layout="wide")

#carregando os dados
df = pd.read_csv('df_idg_completo_2.csv', encoding='utf-8', sep=';')
georreferenciamento_df = pd.read_csv('georreferenciamento_df.csv')

#criando as caixas de seleção
escolha = st.sidebar.selectbox("Deseja filtrar os resultados?", ['Não', 'Sim'])
df_filtrado = df
if escolha == 'Sim':
    lista_regioes = df['Região'].unique().tolist()

    print(lista_regioes)
    lista_regioes.insert(0, "Marcar Todos")
    print(lista_regioes)
    regiao_selecionada = st.sidebar.selectbox("Selecione uma região:", lista_regioes)
    

    if regiao_selecionada != "Marcar Todos":
        df_filtrado = df[df['Região'] == regiao_selecionada]

        lista_estados = df_filtrado['ufSigla'].unique().tolist()
        lista_estados.insert(0, "Marcar Todos")
        estado_selecionado = st.sidebar.selectbox("Selecione um estado:", lista_estados)

        if estado_selecionado != "Marcar Todos":
            df_filtrado = df_filtrado[df_filtrado['ufSigla'] == estado_selecionado]

            lista_municipios = df_filtrado['municipio'].unique().tolist()
            lista_municipios.insert(0, "Marcar Todos")
            municipio_selecionado = st.sidebar.selectbox("Selecione um município:", lista_municipios)

            if municipio_selecionado != "Marcar Todos":
                df_filtrado = df_filtrado[df_filtrado['municipio'] == municipio_selecionado]

                df_filtrado = df_filtrado[df_filtrado['municipio'] == municipio_selecionado]
                
#criando um título para a página
st.write(
    """
    <div style="text-align: center;">
        <h1 style="color: black;">Índice de Gestão Descentralizada do município <br> <span style="color: blue;">IGD-M</span> &#x1f4cb;</h1>
    </div>
    """,
    unsafe_allow_html=True
)

#criando um espaço entre as visualizações
st.text("")

# Texto introdutório
introduction_text = """
O Índice de Gestão Descentralizada é um indicador que mede a quantidade de ações realizadas pelo município nas ações de cadastramento, atualização cadastral e de acompanhamento das condicionalidades de educação e saúde.
Também verifica se o município aderiu ao Sistema Único de Assistência Social (Suas) e se as gestões e os Conselhos Municipais registraram, no Sistema SuasWeb, as informações relativas à prestação de contas.

O cálculo do IGD-M é composto por quatro fatores de operação: 1) taxa de atualização cadastral e taxas de acompanhamento das condicionalidades da saúde e educação; 2) adesão ao Sistema Único de Assistência Social (Suas); 3) prestação de contas; e 4) parecer das contas do uso dos recursos.

Foram utilizados para esta analise apenas os dados do Fator de Operação 1, cujo cálculo envolce as seguintes variáveis:

- **TAC** - Taxa de Atualização Cadastral, calculada pela divisão total de cadastros válidos de famílias com renda "per capita" até meio salário mínimo atualizados nos últimos dois anos no Cadastro Único no município.
- **TAFE** - Taxa de Acompanhamento da Frequência Escolar, calculada pela divisão do somatório do número de crianças e adolescentes pertencentes às famílias beneficiárias do Programa Bolsa Família com perfil educação no município e com informações da frequência escolar, pelo número total de crianças e adolescentes pertencentes a famílias beneficiárias do Programa Bolsa Família com perfil educação no município.
- **TAAS** - Taxa de Acompanhamento da Agenda de Saúde, calculada pela divisão do público com perfil saúde no município e com informações de acompanhamento de condicionalidade de saúde, pelo número total do público com perfil de saúde no município.
"""

# Exibir o texto formatado
st.write(introduction_text)


st.text("")


# Exibindo o valor de 'igd_m' formatado

# Criar uma caixa informativa
# Definir o tamanho da fonte e centralizar o texto
html_content = "<div style='text-align: center;'>"
html_content += "<p style='font-size: 32px;'><strong>IGD-M da área selecionada:</strong></p>"
html_content += "<p style='font-size: 24px;'>{:.2f}</p>".format(df_filtrado['igd_m'].mean())
html_content += "</div>"

# Criar uma caixa informativa com o conteúdo formatado
st.write(html_content, unsafe_allow_html=True)

#criando um espaço entre as visualizações
st.text("")


#criando o gráfico do índice
# Adicionando uma coluna formatada com os rótulos de dados
contagem_valores = df_filtrado['Classe'].value_counts()
df_contagem_valores = pd.DataFrame(contagem_valores)
df_contagem_valores.sort_values(by='Classe')
df_contagem_valores.reset_index(inplace=True)
df_contagem_valores.rename(columns={'count':'Quantidade'}, inplace=True)
        
# Criando o gráfico
fig = px.bar(df_contagem_valores, x='Classe', y='Quantidade')
    
# PERSONALIZAR o gráfico
fig.update_yaxes(title_text='Nº de municípios',
                   
                # title_textfont =dict(size=20),
                tickfont=dict(size=16) # Tamanho da fonte 
                    )
fig.update_traces(text=df_contagem_valores['Quantidade'], texttemplate='%{text}', textposition='outside', textfont=dict(size=12))
    
fig.update_xaxes(
        title_text='',
        #tickvals=[-1, 1, 70, 75, 80, 85, 90, 95, 100],  # Valores reais
        tickvals=[0, 1, 2, 3, 4, 5, 6, 7],  # Valores reais
        ticktext=['0','até 70', '> 70 até 75', '> 75 até 80', '> 80 até 85', '> 85 até 90', '> 90 até 95', '> 95 até 100'],  # Rótulos personalizados
        tickangle=-75,  # Rotação dos rótulos
        tickfont=dict(size=16)# Tamanho da fonte
    )
fig.update_layout(
    yaxis=dict(
        fixedrange=False,  # Permitir rolagem na direção y
        range=[0, max(df_contagem_valores['Quantidade']) * 1.2]  # Ajustar a faixa do eixo y conforme necessário
    )
)
    # EXIBIR o gráfico
st.header("Quantidade de municípios agrupados de acordo com a taxa de IGD-M")
st.plotly_chart(fig, use_container_width=True)

#criando um espaço entre as visualizações
#st.text("")
 #criando o mapa
        #criando uma cópia segura dos dados
# Copiar o DataFrame df_filtrado para resultados_df
import requests
#from geojson_rewind import rewind
import json
resultados_df = df_filtrado.copy()

# Puxar a malha geográfica do Brasil a nível de município
with open('data/geojson', 'r') as geojson_file:
    geojson = json.load(geojson_file)

# Remover o dígito verificador dos códigos IBGE
#resultados_df['ibge_6'] = resultados_df['ibge_6'].astype(str).str[:-1].astype(int)

# Carregar os dados de georreferenciamento
georreferenciamento_df = pd.read_csv('georreferenciamento_df.csv')  # Substitua "seuarquivo.csv" pelo caminho do seu arquivo

# Cruzamento do DataFrame resultados com as informações de georreferenciamento
resultados_df = pd.merge(resultados_df[['ibge_6', 'Classe']],
                         georreferenciamento_df[['codigo_ibge', 'nome', 'latitude', 'longitude']],
                         left_on='ibge_6',
                         right_on='codigo_ibge',
                         how='inner')




# Remover o dígito verificador dos códigos de área na malha geográfica
#for feature in geojson['features']:
    #feature['properties']['codarea'] = feature['properties']['codarea'][:-1]

# Corrigir a malha geográfica com geojson_rewind
#geojson = rewind(geojson, rfc7946=False)

# Configurar renderizador padrão para Plotly
pio.renderers.default = 'iframe'

# Criar o mapa choroplético
fig2 = px.choropleth(resultados_df,
                    geojson=geojson,
                    scope='south america',
                    color='Classe',
                    color_continuous_scale="Reds",
                    locations='ibge_6',
                    featureidkey='properties.codarea',
                    hover_name='nome')
fig2.update_layout(height=800, width=1000, autosize=False)
fig2.update_geos(fitbounds="locations", visible=False)
fig2.update_traces(marker_line_width=0)


        # Exibir o gráfico no Streamlit
st.header("Distribuição da classificação de IGD-M nos municípios no mapa do Brasil ")
st.plotly_chart(fig2, use_container_width = True)