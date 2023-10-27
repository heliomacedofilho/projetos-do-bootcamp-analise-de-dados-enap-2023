import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

df = pd.read_csv('df_bpc_fpm_completa.csv')

st.set_page_config(page_title="Presença das políticas públicas sociais nos municípios brasileiros :earth_americas:", layout="wide")
st.markdown('# Presença das políticas públicas sociais nos municípios brasileiros :earth_americas:')
st.markdown("---")
regioes = st.sidebar.selectbox("Selecione uma região:", df['Região'].unique())
estados = st.sidebar.selectbox("Selecione um estado:", df['ufSigla'].unique())
municipios = st.sidebar.selectbox("Selecione um município:", df['Município_UF'].unique())

df_filtro_regioes = df[df['Região']==regioes]
df_filtro_estados = df[df['ufSigla']==estados]
df_filtro_municipios = df[df['Município_UF']==municipios]

st.title('_Benefício de Prestação Continuada_ :blue[BPC] :older_woman:')

col1, col2 = st.columns(2)

#criando uma cópia segura dos dados
resultados_df = df.copy()

#criando dataframe com informações de georreferenciamento de municípios
georreferenciamento_df = pd.read_csv('https://raw.githubusercontent.com/kelvins/Municipios-Brasileiros/main/csv/municipios.csv')

#os dados de georreferenciamento tem 7 dígitos (vamos remover o dígito verificador e atualizar o dataframe)
georreferenciamento_df['codigo_ibge'] = georreferenciamento_df['codigo_ibge'].astype('str').map(lambda x: x[:-1]).astype('int')

#cruzamento do dataframe resultados com as informações de georreferenciamento
resultados_df = pd.merge(df[['ibge_6', 'Classe']],
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

fig2.show()
col2.plotly_chart(fig2, use_container_width = True)

# Crie o gráfico de barras
fig = px.bar(df, x='Classe', y='count', title='Relação entre o BPC e o FPM')

# Mostre o gráfico
fig.show()
col1.plotly_chart(fig, use_container_width = True)
