
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import locale

df = pd.read_csv('df_bpc_fpm_completa.csv')
georreferenciamento_df = pd.read_csv('https://raw.githubusercontent.com/kelvins/Municipios-Brasileiros/main/csv/municipios.csv')

lista_regioes = df['Região'].unique().tolist()
regioes = st.sidebar.selectbox("Selecione uma região:", lista_regioes)
df_filtrado = df[df['Região']==regioes]
estados = st.sidebar.selectbox("Selecione um estado:", df_filtrado['ufSigla'].unique())
df_filtrado = df[df['ufSigla']==estados]
municipios = st.sidebar.selectbox("Selecione um município:", df_filtrado['Município_UF'].unique())
df_filtrado = df[df['Município_UF']==municipios]

st.title('_Benefício de Prestação Continuada_ :blue[BPC] :older_woman:')

col1, col2= st.columns(2)

with col1 :
    st.header("Valor pago do BPC")
    st.write("R${:,.2f}".format(df_filtrado['bpc_val'].sum()))

with col2 :
    st.header("Repasse do FPM")
    st.write("R${:,.2f}".format(df_filtrado['repasse_fpm'].sum()))


col4, col5 = st.columns(2)

# Crie o gráfico de barras
fig = px.bar(df_filtrado, x='indice_bpc', y='count', title='Relação entre o BPC e o FPM')
col4.header("Relação entre o valor pago em BPC e o FPM")
fig.show()
col4.plotly_chart(fig, use_container_width = True)

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

#construir o mapa choroplético com timeline no campo de ano
import plotly.express as px
import plotly.io as pio
pio.renderers.default = 'iframe'

fig2 = px.choropleth(resultados_df,
                    geojson=geojson,
                    scope='south america',
                    color='Classe',
                    color_continuous_scale="Reds",
                    locations='ibge_6',
                    featureidkey='properties.codarea',
                    hover_name='nome').update_layout(height=800, width=1000, autosize=False)

fig2.update_traces(marker_line_width=0)

col5.header("Mapa dos municípios com o impacto do BPC em relação ao FPM")
# Mostre o gráfico
fig2.show()
col5.plotly_chart(fig2, use_container_width = True)