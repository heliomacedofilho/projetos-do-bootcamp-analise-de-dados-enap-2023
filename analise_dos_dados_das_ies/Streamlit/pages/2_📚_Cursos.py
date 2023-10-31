import os
import pandas as pd 
import numpy as np 
import matplotlib
import matplotlib.pyplot as plt 
import seaborn as sns 
import plotly
import plotly.express as px
import streamlit as st


# ------------------------------------------------------------------------
# PARTE 01 - Evolução da Oferta de Curso
# ------------------------------------------------------------------------
st.set_page_config(page_title='Analise Cursos', 
                    page_icon=':books:', 
				    layout='wide', 
                    initial_sidebar_state='expanded')

# st.set_page_config(page_title='Evolução Cursos', 
                   # page_icon=':chart_with_upwards_trend:', 
				   # layout='wide', 
                   # initial_sidebar_state='expanded')

st.title(':chart_with_upwards_trend: Evolução da Oferta de Cursos :flag-br:')
st.subheader('Escopo: Cursos Presenciais de Federais Públicas e Privadas')
st.subheader("Dados de 2012-2022")
st.markdown("---")


# ------------------------------------------------------------------------
# Parametros plots seaborn
# ------------------------------------------------------------------------
sns.set(style="darkgrid")

# ------------------------------------------------------------------------
# Carrega dados Cursos
# ------------------------------------------------------------------------
@st.cache_data
# carregar algumas colunas pois a carga do df é demorado
# dados_cursos_2012_2022.csv alterado para dados_cursos_2012_2022_reduzida01.csv

def carrega_df():
	df_all = pd.read_csv('./arquivos/dados_cursos_2012_2022_reduzida01.csv', sep='|', 
						low_memory=False, 
						usecols=['NU_ANO_CENSO','Tipo_Cat_Admn','Tipo_Org_Acad','Tipo_Org_Principal', 'Tipo_Grau_Acad','Tipo_Rede',
						'NO_CINE_AREA_GERAL', 'NO_CURSO','QT_CURSO','QT_MAT','QT_ING','QT_CONC'])
	return df_all
df_all = carrega_df()	

# ------------------------------------------------------------------------				  
# Prepara dataframes
# ------------------------------------------------------------------------

#plot01
evol_cursos = df_all.groupby(['NU_ANO_CENSO'])['NO_CURSO'].count().reset_index()
evol_cursos = evol_cursos.rename(columns={'NO_CURSO':'Total_cursos'})

#plot02
evol_cursos_cat = df_all.groupby(['NU_ANO_CENSO','Tipo_Cat_Admn'])['NO_CURSO'].count().reset_index()
evol_cursos_cat = evol_cursos_cat.rename(columns={'NO_CURSO':'Total_cursos'})

#plot03
evol_cursos_org = df_all.groupby(['NU_ANO_CENSO','Tipo_Org_Acad'])['NO_CURSO'].count().reset_index()
evol_cursos_org = evol_cursos_org.rename(columns={'NO_CURSO':'Total_cursos'})

#plot04
evol_cursos_grau = df_all.groupby(['NU_ANO_CENSO','Tipo_Grau_Acad'])['NO_CURSO'].count().reset_index()
evol_cursos_grau = evol_cursos_grau.rename(columns={'NO_CURSO':'Total_cursos'})

#plot05
evol_cursos_area = df_all.groupby(['NU_ANO_CENSO','NO_CINE_AREA_GERAL'])['NO_CURSO'].count().reset_index()
evol_cursos_area = evol_cursos_area.rename(columns={'NO_CURSO':'Total_cursos'})
evol_cursos_area = evol_cursos_area[evol_cursos_area['NO_CINE_AREA_GERAL']!='Programas básicos']


# ------------------------------------------------------------------------				  
# Plot01:  Evolução da Qtd de Cursos ofertados/ Categoria (linha)
# ------------------------------------------------------------------------

titulo_plot01 =  '<p style="font-family:Courier; color:Black; font-size: 23px;"><b>Visualização da Evolução da Qtd de Cursos PRESENCIAIS</b></p>'
st.markdown(titulo_plot01, unsafe_allow_html=True)

ano_min = evol_cursos['NU_ANO_CENSO'].min()
ano_max = evol_cursos['NU_ANO_CENSO'].max()

f, axes = plt.subplots(1, 1,  figsize=(22,12))

# Curva Total
axes = sns.pointplot(x='NU_ANO_CENSO', y='Total_cursos', 
            data=evol_cursos.sort_values(by=('NU_ANO_CENSO'), ascending=False),
            label="Total Cursos", markers='o', color='r')
for i in range(len(evol_cursos)):
        plt.text(i, evol_cursos['Total_cursos'][i]+600,
                 evol_cursos['Total_cursos'][i], color='r', fontsize=14)

data1 = evol_cursos_cat[evol_cursos_cat['Tipo_Cat_Admn']=='Privada com fins lucrativos'].reset_index()
axes = sns.pointplot(x='NU_ANO_CENSO', y='Total_cursos', 
            data=data1.sort_values(by=('NU_ANO_CENSO'), ascending=False),
            label="Privada com fins lucrativos", markers='o', color='green')
for i in range(len(data1)):
         plt.text(i, data1['Total_cursos'][i]-1000,
                  data1['Total_cursos'][i], color='green', fontsize=14)

data2 = evol_cursos_cat[evol_cursos_cat['Tipo_Cat_Admn']=='Privada sem fins lucrativos'].reset_index()
axes = sns.pointplot(x='NU_ANO_CENSO', y='Total_cursos',  
            data=data2.sort_values(by=('NU_ANO_CENSO'), ascending=False),
            label="Privada sem fins lucrativos", markers='o', color='b')
for i in range(len(data2)):
         plt.text(i, data2['Total_cursos'][i]+800,
                  data2['Total_cursos'][i], color='b', fontsize=14)

data3 = evol_cursos_cat[evol_cursos_cat['Tipo_Cat_Admn']=='Pública Federal'].reset_index()
axes = sns.pointplot(x='NU_ANO_CENSO', y='Total_cursos',  
            data=data3.sort_values(by=('NU_ANO_CENSO'), ascending=False),
            label="Pública Federal", markers='o', color='orange')
for i in range(len(data3)):
         plt.text(i, data3['Total_cursos'][i]+600,
                  data3['Total_cursos'][i], color='orange', fontsize=14)

#axes.set_title("Evolução do Total de Cursos PRESENCIAIS por Ano", fontsize=20)
axes.set_xticklabels(axes.get_xticklabels(), rotation=0, ha="right", fontsize=16)
axes.set(xlabel=''); axes.set_ylabel('Total Cursos', fontsize=18)
axes.tick_params(axis='y', labelsize=14)

axes.grid(color='gray', linestyle='--', linewidth=1.2, axis='y', alpha=.2)

axes.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=2,
           fontsize='x-large')

st.pyplot(f)

# ------------------------------------------------------------------------
# Plot01: Análise
# ------------------------------------------------------------------------
st.subheader("Principais Resultados")
st.write("Ao analisarmos a série temporal que abrange o período de 2012 a 2022, notamos distintos comportamentos entre as entidades públicas e as privadas, seja com fins lucrativos ou sem fins lucrativos.")
st.write("As entidades públicas mantiveram um padrão de crescimento constante, caracterizado por um aumento pequeno, gradual e linear ao longo dos anos. Por outro lado, as instituições privadas, tanto com fins lucrativos quanto sem fins lucrativos, apresentaram uma dinâmica mais variada.")
st.write("Entre os anos de 2017 e 2018, observamos uma inversão no padrão de crescimento dessas entidades privadas. Nesse período, houve uma significativa inflexão, marcando o início de um declínio, enquanto as entidades privadas iniciaram um notável avanço. Este movimento representa uma mudança substancial na dinâmica educacional, onde as instituições privadas passaram a ocupar um espaço de destaque no cenário educacional, impulsionando o crescimento do setor.")
st.write("Esse contraste na evolução entre as entidades públicas e privadas nos oferece uma visão abrangente da complexa dinâmica do sistema educacional ao longo dos anos analisados.")
st.markdown("---")

# ------------------------------------------------------------------------
# Prepara pagina para 2 colunas
# ------------------------------------------------------------------------
col1, col2 = st.columns(2)


# ------------------------------------------------------------------------
# Plot02: Evolução da Qtd de Cursos ofertados/ Categoria (barra)
# ------------------------------------------------------------------------	
with col1:
	titulo_plot02 =  '<p style="font-family:Courier; color:Black; font-size: 23px;"><b>Evolução da Quantidade de Cursos por Categoria</b></p>'
	st.markdown(titulo_plot02, unsafe_allow_html=True)
	
	fig = px.bar(evol_cursos_cat,
             y='Total_cursos', 
             x='NU_ANO_CENSO', 
             color='Tipo_Cat_Admn',
             color_discrete_sequence=px.colors.qualitative.G10,
             barmode = 'stack', width=800, height=900,
             #title='Evolução da Quantidade de Cursos por Categoria',
             labels=dict(Tipo_Cat_Admn = 'Categoria'),
             text='Total_cursos')
			 
	fig.update_layout(yaxis=dict(title='', titlefont_size=22, tickfont_size=18),
                  xaxis=dict(title='', titlefont_size=22, tickfont_size=18),  
                  legend=dict(x=0.1,y=-0.30, font = dict(size = 18))) 
				  
	fig.update_layout(hoverlabel=dict(bgcolor="white", 
                                  font_size=16,
                                  font_family="Rockwell"))				  
				  
	fig.update_xaxes(tickangle=0)
	fig.update_traces(textposition='inside', insidetextfont=dict(color='white', size=16,family='Times New Roman'))

	st.plotly_chart(fig, use_container_width=True)


# ------------------------------------------------------------------------
# Plot03: Evolução da Qtd de Cursos ofertados/ Organizacao Academica (linha)
# ------------------------------------------------------------------------	

with col2:
	titulo_plot03 =  '<p style="font-family:Courier; color:Black; font-size: 23px;"><b>Evolução da Quantidade de Cursos por Org. Acadêmica</b></p>'
	st.markdown(titulo_plot03, unsafe_allow_html=True)
	
	fig = px.bar(evol_cursos_org,
             y='Total_cursos', 
             x='NU_ANO_CENSO', 
             color='Tipo_Org_Acad',
             color_discrete_sequence=px.colors.qualitative.G10,
             barmode = 'stack', width=800, height=900,
             #title='Evolução da Quantidade de Cursos por Organização Academica',
             labels=dict(Tipo_Org_Acad = 'Organização'),
             text='Total_cursos')
			 
	fig.update_layout(yaxis=dict(title='', titlefont_size=22, tickfont_size=18),
                  xaxis=dict(title='', titlefont_size=22, tickfont_size=18),      
                  legend=dict(x=0.1,y=-0.3, font = dict(size = 18))) 
				  
	fig.update_layout(hoverlabel=dict(bgcolor="white", 
                                  font_size=16,
                                  font_family="Rockwell"))		
	
	fig.update_xaxes(tickangle=0)
	
	fig.update_traces(textposition='inside', insidetextfont=dict(color='white', size=16,family='Times New Roman'))
	
	st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------------------------
# Plot03: Análise
# ------------------------------------------------------------------------
st.subheader("Principais Resultados")
st.write("Podemos notar uma tendência de crescimento contínuo na oferta de cursos. Esse crescimento experimentou um notável impulso por volta de 2017, seguido por uma estabilização em uma escala ligeiramente menor.")

st.write("Ao analisamos as categorias, fica evidente que a maioria dos cursos é ofertada por entidades privadas. Além disso, as Faculdades e Universidades se destacam como as organizações que são as que mais oferecem cursos. Por outro lado, os Institutos Federais apresentam um número menor de ofertas em comparação com as outras categorias.")

st.write("Essa análise demonstra a dinâmica da evolução da oferta de cursos ao longo do tempo e ressalta o papel significativo desempenhado pelas instituições privadas, pelas Faculdades e Universidades no cenário educacional brasileiro.")

st.markdown("---")

# ------------------------------------------------------------------------
# Plot04: Evolução da Qtd de Cursos ofertados/ Grau Academico (linha) 
# ------------------------------------------------------------------------	
titulo_plot04 =  '<p style="font-family:Courier; color:Black; font-size: 23px;"><b>Evolução da Quantidade de Cursos por Grau Academico</b></p>'
st.markdown(titulo_plot04, unsafe_allow_html=True)
	
fig = px.bar(evol_cursos_grau,
             y='Total_cursos', 
             x='NU_ANO_CENSO', 
             color='Tipo_Grau_Acad',
             color_discrete_sequence=px.colors.qualitative.G10,
             barmode = 'stack', width=800, height=900,
             labels=dict(Tipo_Grau_Acad = 'Grau Academico'),
             text='Total_cursos')
			 
fig.update_layout(yaxis=dict(title='', titlefont_size=22, tickfont_size=18),
                  xaxis=dict(title='', titlefont_size=22, tickfont_size=18),  
                  legend=dict(x=0.1,y=-0.30, font = dict(size = 18))) 
				  
fig.update_layout(hoverlabel=dict(bgcolor="white", 
                                  font_size=16,
                                  font_family="Rockwell"))				  
				  
fig.update_xaxes(tickangle=0)
fig.update_traces(textposition='inside', insidetextfont=dict(color='white', size=16,family='Times New Roman'))

st.plotly_chart(fig, use_container_width=True)
st.markdown("---")	

# ------------------------------------------------------------------------
# Plot05: Evolução da Qtd de Cursos ofertados/ Area Geral (linha) 
# ------------------------------------------------------------------------	
titulo_plot05 =  '<p style="font-family:Courier; color:Black; font-size: 23px;"><b>Evolução da Quantidade de Cursos por Area Geral</b></p>'
st.markdown(titulo_plot05, unsafe_allow_html=True)

ano_min = evol_cursos_area['NU_ANO_CENSO'].min()
ano_max = evol_cursos_area['NU_ANO_CENSO'].max()

# necessidade de criar paleta de cores
palette_11cores = ["#F72585", "#7209B7", "#3A0CA3", "#4361EE", "#4CC9F0", #rosa escuro, roxo, roxo escuro, azul escuro, azul agua
                   '#00cc00', # verde claro
                   '#00661a', # verde escuro
                   '#ffbf00',  # laranja
                   '#cc0000', # vermelho
                   '#66001a', # vermelho vinho
                   '#ffff66' # amarelo
                   ]

f, axes = plt.subplots(1, 1,  figsize=(20,8))

axes = sns.pointplot(x='NU_ANO_CENSO', y='Total_cursos', hue='NO_CINE_AREA_GERAL',
            data=evol_cursos_area.sort_values(by=('NU_ANO_CENSO'), ascending=False),
            label="Total Cursos", markers='o', palette=palette_11cores)

#axes.set_title(" ", fontsize=20)
axes.set_xticklabels(axes.get_xticklabels(), rotation=0, ha="right", fontsize=16)
axes.set(xlabel=''); axes.set_ylabel('Total Cursos', fontsize=18)
axes.tick_params(axis='y', labelsize=14)

axes.grid(color='gray', linestyle='--', linewidth=1.2, axis='y', alpha=.2)

#axes.legend(loc='best', fontsize=18)
axes.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=2,
           fontsize='x-large')
		   
st.pyplot(f)
st.markdown("---")		   

# ------------------------------------------------------------------------
# PARTE 02 - Evolução da Oferta de Curso X Matriculas
# ------------------------------------------------------------------------
# import os
# import pandas as pd 
# import numpy as np 
# import matplotlib
# import matplotlib.pyplot as plt 
# import seaborn as sns 
# import plotly
# import plotly.express as px
# import streamlit as st


# st.set_page_config(page_title='Cursos e Matriculas', 
                   # page_icon=':computer:', 
                   # layout='wide', 
                   # initial_sidebar_state='expanded')

st.title(':computer: :female-student: Evolução da Oferta de Cursos e Qtd de Matriculas :flag-br:')
st.subheader('Escopo: Cursos Presenciais de Federais Públicas e Privadas')
st.subheader("Dados de 2012-2022")
st.markdown("---")

# ------------------------------------------------------------------------
# Funcoes
# ------------------------------------------------------------------------
def formata_area_geral(x):
    if x == 'Engenharia, produção e construção': return 'Eng, Produção e <br>construção'                  
    elif x == 'Educação': return 'Educação'  
    elif x == 'Negócios, administração e direito': return 'Negócios, <br>admin. e<br>direito'             
    elif x == 'Saúde e bem-estar': return 'Saúde e<br> bem-estar'  
    elif x == 'Ciências sociais, comunicação e informação': return  'Ciênc. sociais, comunicação<br>e informação' 
    elif x == 'Computação e Tecnologias da Informação e Comunicação (TIC)': return  'Computação <br>e TIC' 
    elif x == 'Agricultura, silvicultura, pesca e veterinária': return  'Agric., <br>silvicultura, <br>pesca e veterinária'         
    elif x == 'Ciências naturais, matemática e estatística': return  'Ciênc. naturais, <br>matem. e <br>estatística' 
    elif x == 'Artes e humanidades': return  'Artes e <br>humanidades' 
    elif x == 'Serviços': return  'Serviços' 
    elif x == 'Programas básicos': return  'Progr. <br> básicos' 
    else: return 'não informado'


# ------------------------------------------------------------------------
# Carrega dados Cursos
# ------------------------------------------------------------------------
# st.cache_data
# carregar algumas colunas pois a carga do df é demorado
# def carrega_df():
	# df_all = pd.read_csv('./arquivos/dados_cursos_2012_2022.csv', sep='|', 
						# low_memory=False, 
						# usecols=['NU_ANO_CENSO','NO_CINE_AREA_GERAL','QT_CURSO','QT_MAT','QT_ING','QT_CONC'])
	# return df_all

# df_all = carrega_df()	

# ------------------------------------------------------------------------				  
# Prepara df: Distribuição dos cursos
# ------------------------------------------------------------------------
distr_cursos = df_all[df_all['NO_CINE_AREA_GERAL']!='Programas básicos']
distr_cursos = distr_cursos.groupby(['NU_ANO_CENSO','NO_CINE_AREA_GERAL']).\
                                        agg({'QT_CURSO':'sum',
                                             'QT_MAT':'sum',                                             
                                             'QT_ING':'sum',
                                             'QT_CONC':'sum'
                                             }).reset_index()

distr_cursos['AREA_GERAL'] = distr_cursos['NO_CINE_AREA_GERAL'].apply(lambda x: formata_area_geral(x))

# ------------------------------------------------------------------------
# Plot 01: Treemap de Cursos e Matriculas
# ------------------------------------------------------------------------	
l_anos = range(2012,2023,1)

## para exibir todos os TreeMaps - todos os anos
# for ano in l_anos:
	# titulo_plot01 =  '<p style="font-family:Courier; color:Black; font-size: 23px;"><b>Treemap de Cursos e Matriculas para o ano de ' + str(ano) + '</b></p>'
	# st.markdown(titulo_plot01, unsafe_allow_html=True)
    
	# fig = px.treemap(distr_cursos[distr_cursos['NU_ANO_CENSO']==ano], 
	# path = [px.Constant('Area Geral'), 'AREA_GERAL'], 
	# values = 'QT_CURSO',  
	# color_continuous_scale='RdBu', 
	# color = 'QT_MAT', 
	# width=400, height=500)
    
	# fig.update_layout(margin = dict(t=20, l=25, r=25, b=25))
	# fig.update_traces(textposition='middle left', textfont_size=18)
	# fig.update_traces(textposition='middle left', textfont_size=18)
	
	# st.plotly_chart(fig, use_container_width=True)

# para exibir conforme o ano selecionado

col1, col2, col3 = st.columns(3)
with col1:
    label01 = '<p style="font-family:Courier; color:#992600; font-size: 20px;"><b>Selecione um ano específico:</b></p>'
    st.markdown(label01, unsafe_allow_html=True) 
    
with col2:
    ano_selecionado = st.selectbox(label="Selecione um ano específico:", options=l_anos, label_visibility="collapsed")
    
with col3:    
    st.subheader(':date:')


if ano_selecionado:
    titulo_plot01 =  f'<p style="font-family:Courier; color:Black; font-size: 23px;"><b>Treemap de Cursos e Matriculas para o ano de {ano_selecionado}</b></p>'
    st.markdown(titulo_plot01, unsafe_allow_html=True)
    
    fig = px.treemap(distr_cursos[distr_cursos['NU_ANO_CENSO']==ano_selecionado], 
    path = [px.Constant('Area Geral'), 'AREA_GERAL'], 
    values = 'QT_CURSO', color_continuous_scale='RdBu', color = 'QT_MAT', width=400, height=500)
    
    fig.update_layout(margin = dict(t=20, l=25, r=25, b=25))
    fig.update_traces(textposition='middle left', textfont_size=18)
    fig.update_traces(textposition='middle left', textfont_size=18)
    
    st.plotly_chart(fig, use_container_width=True)
    
# ------------------------------------------------------------------------
# Plot01: Análise
# ------------------------------------------------------------------------
st.subheader("Principais Resultados")
st.write("O mapa de calor nos revela como as tendências no mercado de trabalho exercem influência sobre as preferências acadêmicas nas universidades.")

st.write("Podemos observar uma notável mudança nos cursos mais procurados ao longo dos anos. Em 2012, a grande área predominante era 'Negócios, Administração e Direito'. Contudo, ao chegarmos em 2022, percebemos uma transição marcante, com 'Saúde e Bem-Estar' emergindo como a área de maior destaque.")

st.write("Essa análise demonstra claramente a dinâmica do mercado e sua capacidade de moldar as preferências dos estudantes, bem como a adaptabilidade das instituições de ensino para atender a essas demandas em constante evolução.")
st.markdown('---')    

# ------------------------------------------------------------------------
# PARTE 03 - Analise Cursos - Ano Atual: 2022 
# ------------------------------------------------------------------------
# import os
# import pandas as pd 
# import numpy as np 
# import matplotlib
# import matplotlib.pyplot as plt 
# import seaborn as sns 
# import plotly
# import plotly.express as px
# import streamlit as st

# st.set_page_config(page_title='Analise Cursos', 
                   # page_icon=':books:', 
                   # layout='wide', 
                   # initial_sidebar_state='expanded')

st.title(':books: Oferta de Cursos :flag-br: :classical_building:')
st.subheader('Escopo: Cursos Presenciais de Federais Públicas e Privadas')
st.subheader("Dados de 2022")
st.markdown("---")


# ------------------------------------------------------------------------
# Funcoes
# ------------------------------------------------------------------------
def formata_area_geral2(x):
    if x == 'Engenharia, produção e construção': return 'Eng, Produção e construção'                  
    elif x == 'Educação': return 'Educação'  
    elif x == 'Negócios, administração e direito': return 'Negócios, admin. e direito'             
    elif x == 'Saúde e bem-estar': return 'Saúde e bem-estar'  
    elif x == 'Ciências sociais, comunicação e informação': return  'Ciências sociais, comunicação e info' 
    elif x == 'Computação e Tecnologias da Informação e Comunicação (TIC)': return  'Computação e TIC' 
    elif x == 'Agricultura, silvicultura, pesca e veterinária': return  'Agric., silvicultura, pesca e veterinária'         
    elif x == 'Ciências naturais, matemática e estatística': return  'Ciências naturais, mat. e estat.' 
    elif x == 'Artes e humanidades': return  'Artes e humanidades' 
    elif x == 'Serviços': return  'Serviços' 
    elif x == 'Programas básicos': return  'Programas básicos' 
    else: return 'não informado'

# ------------------------------------------------------------------------
# Carrega dados Cursos
# ------------------------------------------------------------------------
colunas_CO = ['CO_REGIAO', 'CO_UF', 'CO_MUNICIPIO', 'CO_IES', 'CO_CURSO', 
			  'CO_CINE_ROTULO', 'CO_CINE_AREA_GERAL', 'CO_CINE_AREA_ESPECIFICA', 
			  'CO_CINE_AREA_DETALHADA', 'IN_CAPITAL', 'IN_GRATUITO']
dict_dtype = {column : 'str'  for column in colunas_CO}


@st.cache_data
def carrega_df():
	cursos = pd.read_csv('./arquivos/dados_cursos_escopo_consolidado.csv', sep='|', 
                  dtype = dict_dtype, 
                  low_memory=False)			  
	return cursos
cursos = carrega_df()

# retirada Programas básicos
cursos = cursos[cursos['NO_CINE_AREA_GERAL']!='Programas básicos']
cursos['AREA_GERAL2'] = cursos['NO_CINE_AREA_GERAL'].apply(lambda x: formata_area_geral2(x))
	
# ------------------------------------------------------------------------				  
# Prepara df: Top 10 cursos - Brasil
# ------------------------------------------------------------------------
tot_cursos = cursos.shape[0]
tot_cursos_br = cursos.groupby(['NO_CURSO'])['QT_CURSO'].count()
perc_cursos_br = round((tot_cursos_br / tot_cursos * 100),2)
distr_cursos_br = pd.DataFrame({'Total_Cursos' : tot_cursos_br,
                                'Total_Cursos_p_BR': perc_cursos_br}).reset_index()
								
top10_BR = distr_cursos_br.sort_values(by='Total_Cursos', ascending=False).head(10)
top10_BR['Perc_top10'] = top10_BR['Total_Cursos'] / (top10_BR['Total_Cursos'].sum()) * 100								
								
# ------------------------------------------------------------------------
# Prepara df: Top 5 cursos - UF
# ------------------------------------------------------------------------
no_cursos_uf = cursos.groupby(['SG_UF','NO_CURSO'])['QT_CURSO'].count().\
reset_index().rename(columns={'QT_CURSO':'Total'})						
top5 = no_cursos_uf.sort_values(['SG_UF','Total'], ascending=[True, False]).groupby('SG_UF').head(5)		

# ------------------------------------------------------------------------
# Prepara df: Total de Cursos Presenciais por UF/ Tipo Rede
# ------------------------------------------------------------------------
tot_cursos_uf = cursos.groupby('SG_UF')['QT_CURSO'].sum()
tot_cursos_uf_rede = cursos.groupby(['SG_UF','Tipo_Rede'])['QT_CURSO'].sum()
perc_cursos_uf_rede = round((tot_cursos_uf_rede/tot_cursos_uf*100),2)
distr_cursos_uf_rede = pd.DataFrame({'Total_Cursos'   : tot_cursos_uf_rede,
                                     'Total_Cursos_p': perc_cursos_uf_rede}).reset_index()
									 
# ------------------------------------------------------------------------
# Prepara df: Total de Cursos Presenciais por UF/ Org Academica
# ------------------------------------------------------------------------
#tot_cursos_uf = cursos.groupby('SG_UF')['QT_CURSO'].sum()
tot_cursos_uf_org = cursos.groupby(['SG_UF','Tipo_Org_Acad'])['QT_CURSO'].sum()
perc_cursos_uf_org = round((tot_cursos_uf_org/tot_cursos_uf*100),2)
distr_cursos_uf_org = pd.DataFrame({'Total_Cursos'   : tot_cursos_uf_org,
                                   'Total_Cursos_p': perc_cursos_uf_org}).reset_index()

# ------------------------------------------------------------------------
# Prepara df: Total de Cursos Presenciais por UF/ Grau Academico
# ------------------------------------------------------------------------
#tot_cursos_uf = cursos.groupby('SG_UF')['QT_CURSO'].sum()
tot_cursos_uf_ga = cursos.groupby(['SG_UF','Tipo_Grau_Acad'])['QT_CURSO'].sum()
perc_cursos_uf_ga = round((tot_cursos_uf_ga/tot_cursos_uf*100),2)
distr_cursos_uf_ga = pd.DataFrame({'Total_Cursos'   : tot_cursos_uf_ga,
                                   'Total_Cursos_p': perc_cursos_uf_ga}).reset_index()
								   
		   
titulo_secao01 =  '<p style="font-family:Courier; color:Black; font-size: 25px;"><b>Top 10 cursos mais oferecidos no Brasil</b></p>'
st.markdown(titulo_secao01, unsafe_allow_html=True)		
								   
# ------------------------------------------------------------------------
# Prepara pagina para 2 colunas
# ------------------------------------------------------------------------
col1, col2 = st.columns(2)
						
# ------------------------------------------------------------------------
# Exibir dataframe dos 10 Top cursos - Brasil
# ------------------------------------------------------------------------
display_df = top10_BR.copy()
display_df = display_df.rename(columns={'NO_CURSO':'Nome do Curso', 
                                     'Total_Curso':'Oferta', 
                                     'Total_Cursos_p_BR':'Oferta (% Total)',
                                     'Perc_top10': 'Oferta (% Top10)'})                                     
									 
with col1: 
	titulo_df1 =  '<p style="text-align: left; font-family:Courier; color:Blue; font-size: 20px;"><b>Lista cursos</b></p>'
	st.markdown(titulo_df1, unsafe_allow_html=True)
	st.dataframe(display_df, hide_index=True, use_container_width=True)  
	
	write01 = '<p style="font-family:Courier; color:Black; font-size: 18px;">Total de todos os cursos: ' + str(tot_cursos) + '</p>'
	
	tot_cursos_top10 = top10_BR['Total_Cursos'].sum()
	write02 = '<p style="font-family:Courier; color:Black; font-size: 18px;">Total de cursos considerando-se top 10: ' + str(tot_cursos_top10) + '</p>'
	
	st.markdown(write01, unsafe_allow_html=True)
	st.markdown(write02, unsafe_allow_html=True)
	

# ------------------------------------------------------------------------
# Plot01: Top 10 cursos mais oferecidos no Brasil
# ------------------------------------------------------------------------						
fig = plt.figure(figsize =(8, 6))

labels = top10_BR['NO_CURSO'].values
data = top10_BR['Total_Cursos'].values

fracs = top10_BR['Perc_top10'].values
total = sum(fracs)
explode = (0.30, 0.15, 0.20, 0.18, 0.15, 0.13, 0.12, 0.1, 0.1, 0.1)

#plt.title("Top 10 cursos mais oferecidos no Brasil", fontsize=16, loc = 'center', color='b')
plt.pie(fracs, 
        explode=explode, 
        labels=labels,
        autopct=lambda p: '{:.0f}%'.format(p * total / 100),
        shadow=True, 
        startangle=90)
		
with col2: 
	titulo_plot01 =  '<p style="text-align: center; font-family:Courier; color:Blue; font-size: 20px;"><b>Top 10 cursos presenciais (quantidade)</b></p>'
	st.markdown(titulo_plot01, unsafe_allow_html=True)
	st.pyplot(fig, use_container_width=True)
	
# ------------------------------------------------------------------------
# Plot01: Análise
# ------------------------------------------------------------------------
st.subheader("Principais Resultados")
st.write("Os dados foram analisados de forma a identificar os cursos ofertados pelas IES do Brasil, o que em 2022 era de 35.765. Analisando apenas os 10 cursos mais frequentes, identificou-se um total de 12.866 cursos ofertados. Destacaram-se nesse rank aqueles ligados a área geral de negócios, administração e direito, com os cursos de Administração, Direito e Ciências Contábeis (14,03% do total de cursos do país e 38,98% do cursos do TOP 10). Em segundo lugar no rank dos Top 10 estão os cursos da área de saúde e bem-estar, como Educação Física, Enfermagem e Fisioterapia (9,73% do total de cursos do país e 27,05% dos cursos TOP 10).")
st.markdown('---')

# ------------------------------------------------------------------------
# Plot02: Top 5 cursos mais oferecidos em cada UF
# ------------------------------------------------------------------------						
titulo_plot02 =  '<p style="font-family:Courier; color:Black; font-size: 25px;"><b>Top 5 cursos presenciais mais oferecidos em cada UF</b></p>'
st.markdown(titulo_plot02, unsafe_allow_html=True)

fig = px.bar(top5.sort_values(by='Total', ascending=False),
             x='SG_UF', 
             y='Total', 
             color='NO_CURSO',
             color_discrete_sequence= px.colors.diverging.Spectral_r,
             barmode = 'stack', 
             width=1000, height=600,
             #title='Top 5 Cursos Presenciais (em quantidade) por UF - 2022',
             hover_data = {'NO_CURSO','Total'})

fig.update_layout(yaxis=dict(title='Total Cursos', titlefont_size=22, tickfont_size=18),
                  xaxis=dict(title='', tickfont_size=18),      
                  legend=dict(x=0.6,y=0.9, font = dict(size = 18))) # deslocar legenda para dentro do plot
				  
fig.update_layout(hoverlabel=dict(bgcolor="white", 
                                  font_size=16,
                                  font_family="Rockwell"))				  

st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------------------------
# Plot02: Análise
# ------------------------------------------------------------------------

st.subheader("Principais Resultados")
st.write("Enquanto a análise dos TOP 5 cursos de cada UF permitiu identificar 10 diferentes cursos distribuídos entre os estados. A análise dos Top 5 de cada região do país foi mais uniforme, resultando em 6 diferentes cursos mais prevalentes: Administração, Direito, Educação Física, Pedagogia, Ciências Contábeis e Enfermagem.") 
st.write("Assim como na avaliação por estados, os cursos de Administração e Direito estão presentes nos TOP 5 de todas as regiões, associados agora também à presença do curso de Pedagogia.") 
st.write("Os cursos de Educação Física só não estão presente no TOP 5 da região Norte e os de Ciências Contábeis no Nordeste. A Enfermagem, por sua vez, aparece no TOP 5 apenas nas regiões Norte e Nordeste, em substiuição aos outros dois cursos.")
st.markdown('---')

# ------------------------------------------------------------------------
# Plot03: Total de Cursos Presenciais por UF/ Tipo Rede
# ------------------------------------------------------------------------		
titulo_plot03 =  '<p style="font-family:Courier; color:Black; font-size: 25px;"><b>Distribuição da Qtd de Cursos Presenciais por UF e Rede</b></p>'
st.markdown(titulo_plot03, unsafe_allow_html=True)

fig = px.bar(distr_cursos_uf_rede.sort_values(by='Total_Cursos', ascending=True),
             y='SG_UF', 
             x='Total_Cursos', 
             color='Tipo_Rede',
             color_discrete_sequence=px.colors.qualitative.Dark2,
             barmode = 'stack', #stack=empilhado; group=barras separadas
             width=1000, height=800,
             #title='Distribuição Cursos Presenciais (IES)  no Brasil por UF e Tipo Rede - 2022',
             hover_data = {'SG_UF','Tipo_Rede','Total_Cursos',
                           'Total_Cursos_p'})
fig.update_layout(xaxis=dict(title='Total Cursos', titlefont_size=22, tickfont_size=18),
                  yaxis=dict(title='', tickfont_size=18),      
                  legend=dict(x=0.5,y=0.5, font = dict(size = 25))) 

fig.update_layout(hoverlabel=dict(bgcolor="white", 
                                  font_size=16,
                                  font_family="Rockwell"))
				  
st.plotly_chart(fig, use_container_width=True)
st.markdown("---")


# ------------------------------------------------------------------------
# Plot04: Total de Cursos Presenciais por UF/ Org Acadêmica 
# ------------------------------------------------------------------------		

titulo_plot04 =  '<p style="font-family:Courier; color:Black; font-size: 25px;"><b>Distribuição da Qtd de Cursos Presenciais por UF e Org. Acadêmica</b></p>'
st.markdown(titulo_plot04, unsafe_allow_html=True)

fig = px.bar(distr_cursos_uf_org.sort_values(by='Total_Cursos', ascending=True),
             y='SG_UF', 
             x='Total_Cursos', 
             color='Tipo_Org_Acad',
             color_discrete_sequence=px.colors.qualitative.Dark2,
             barmode = 'stack', #stack=empilhado; group=barras separadas
             width=1000, height=800,
             #title='',
             hover_data = {'SG_UF','Tipo_Org_Acad','Total_Cursos',
                           'Total_Cursos_p'})
fig.update_layout(xaxis=dict(title='Total Cursos', titlefont_size=22, tickfont_size=18),
                  yaxis=dict(title='', tickfont_size=18),      
                  legend=dict(x=0.5,y=0.5, font = dict(size = 25))) 

fig.update_layout(hoverlabel=dict(bgcolor="white", 
                                  font_size=16,
                                  font_family="Rockwell"))
				  
st.plotly_chart(fig, use_container_width=True)
st.markdown("---")

# ------------------------------------------------------------------------
# Plot 05: Total de Cursos Presenciais por UF/Grau Academico
# ------------------------------------------------------------------------		

titulo_plot05 =  '<p style="font-family:Courier; color:Black; font-size: 25px;"><b>Distribuição da Qtd de Cursos Presenciais por UF e Grau Academico</b></p>'
st.markdown(titulo_plot05, unsafe_allow_html=True)

fig = px.bar(distr_cursos_uf_ga.sort_values(by='Total_Cursos', ascending=True),
             y='SG_UF', 
             x='Total_Cursos', 
             color='Tipo_Grau_Acad',
             color_discrete_sequence=px.colors.qualitative.Dark2,
             barmode = 'stack', 
             width=1000, height=800,
            # title='Distribuição Cursos Presenciais (IES)  no Brasil por UF e Grau Academico - 2022',
             hover_data = {'SG_UF','Tipo_Grau_Acad','Total_Cursos', 'Total_Cursos_p'})
fig.update_layout(xaxis=dict(title='Total Cursos', titlefont_size=22, tickfont_size=18),
                  yaxis=dict(title='', tickfont_size=18),      
                  legend=dict(x=0.5,y=0.5, font = dict(size = 25))) 
				  
fig.update_layout(hoverlabel=dict(bgcolor="white", 
                                  font_size=16,
                                  font_family="Rockwell"))				  

st.plotly_chart(fig, use_container_width=True)		

# ------------------------------------------------------------------------
# Plot05: Análise
# ------------------------------------------------------------------------
st.subheader("Principais Resultados")
st.write("A distribuição da quantidade de cursos presenciais por estado e tipo de instituição revela alguns padrões. Como podemos observar, São Paulo se destaca como o estado com o maior número de instituições privadas de ensino em todo o Brasil. Enquanto isso, Minas Gerais lidera na quantidade de entidades públicas.")

st.write("Além disso, nota-se uma alta concentração de institutos federais também em São Paulo, o que também se reflete nas faculdades e centros universitários. Isso indica a presença robusta dessas instituições no estado.")

st.write("Outro ponto notável é a preferência dos paulistas por cursos de bacharelado e tecnólogos, sugerindo uma inclinação específica nas escolhas educacionais dessa população.")
st.markdown("---")

# ------------------------------------------------------------------------
# Plot 06: Total de Cursos Presenciais por Regiao e Area Geral
# ------------------------------------------------------------------------	

titulo_plot06 =  '<p style="font-family:Courier; color:Black; font-size: 25px;"><b>Distribuição da Qtd de Cursos Presenciais por Região e Area Geral </b></p>'
st.markdown(titulo_plot06, unsafe_allow_html=True)

distr_cursos_reg_area = cursos.groupby(['NU_ANO_CENSO','NO_REGIAO', 'NO_CINE_AREA_GERAL','AREA_GERAL2'])['NO_CURSO'].count().reset_index()
distr_cursos_reg_area = distr_cursos_reg_area.rename(columns={'NO_CURSO':'Total_Cursos'})

distr_cursos_reg_area_SE = distr_cursos_reg_area[distr_cursos_reg_area['NO_REGIAO']=='Sudeste']
distr_cursos_reg_area_NE = distr_cursos_reg_area[distr_cursos_reg_area['NO_REGIAO']=='Nordeste']
distr_cursos_reg_area_S = distr_cursos_reg_area[distr_cursos_reg_area['NO_REGIAO']=='Sul']
distr_cursos_reg_area_N = distr_cursos_reg_area[distr_cursos_reg_area['NO_REGIAO']=='Norte']
distr_cursos_reg_area_CO = distr_cursos_reg_area[distr_cursos_reg_area['NO_REGIAO']=='Centro-Oeste']

size=15
fig_NE = px.bar(distr_cursos_reg_area_NE.sort_values(by='NO_CINE_AREA_GERAL', ascending=True),
             x='NO_REGIAO', y='Total_Cursos', color='AREA_GERAL2',
             color_discrete_sequence=px.colors.diverging.Spectral,
             barmode = 'group', width=1000, height=700)
fig_NE.update_layout(yaxis=dict(title='Total Cursos', titlefont_size=20, tickfont_size=12),
                  xaxis=dict(title=''), legend=dict(x=0.03,y=0.98, font = dict(size = size))) 
fig_NE.update_layout(plot_bgcolor='#dbe0f0')
                  
fig_SE = px.bar(distr_cursos_reg_area_SE.sort_values(by='NO_CINE_AREA_GERAL', ascending=True),
             x='NO_REGIAO', y='Total_Cursos', color='AREA_GERAL2',
             color_discrete_sequence=px.colors.diverging.Spectral, 
             barmode = 'group', width=1000, height=700)
fig_SE.update_layout(yaxis=dict(title='Total Cursos', titlefont_size=20, tickfont_size=12),
                  xaxis=dict(title=''), legend=dict(x=0.03,y=0.98, font = dict(size = size)))     
fig_SE.update_layout(plot_bgcolor='#dbe0f0')                  
                  
fig_S = px.bar(distr_cursos_reg_area_S.sort_values(by='NO_CINE_AREA_GERAL', ascending=True),
             x='NO_REGIAO', y='Total_Cursos', color='AREA_GERAL2',
             color_discrete_sequence=px.colors.diverging.Spectral,
             barmode = 'group', width=1000, height=700)
fig_S.update_layout(yaxis=dict(title='Total Cursos', titlefont_size=20, tickfont_size=12),
                  xaxis=dict(title=''), legend=dict(x=0.03,y=0.98, font = dict(size = size))) 
fig_S.update_layout(plot_bgcolor='#dbe0f0')
                  
fig_N = px.bar(distr_cursos_reg_area_N.sort_values(by='NO_CINE_AREA_GERAL', ascending=True),
             x='NO_REGIAO', y='Total_Cursos', color='AREA_GERAL2',
             color_discrete_sequence=px.colors.diverging.Spectral,
             barmode = 'group', width=1000, height=700)
fig_N.update_layout(yaxis=dict(title='Total Cursos', titlefont_size=20, tickfont_size=12),
                  xaxis=dict(title=''), legend=dict(x=0.03,y=0.98, font = dict(size = size)))    
fig_N.update_layout(plot_bgcolor='#dbe0f0')

fig_CO = px.bar(distr_cursos_reg_area_CO.sort_values(by='NO_CINE_AREA_GERAL', ascending=True),
             x='NO_REGIAO', y='Total_Cursos', color='AREA_GERAL2',
             color_discrete_sequence=px.colors.diverging.Spectral,
             barmode = 'group', width=1000, height=700)
fig_CO.update_layout(yaxis=dict(title='Total Cursos', titlefont_size=20, tickfont_size=12),
                  xaxis=dict(title=''), legend=dict(x=0.03,y=0.98, font = dict(size = size)))
fig_CO.update_layout(plot_bgcolor='#dbe0f0')                  
                  
                  
# ------------------------------------------------------------------------
# Prepara pagina para 2 colunas
# ------------------------------------------------------------------------

col1, col2 = st.columns(2)
with col1: 
	titulo_plot06a =  '<p style="text-align: center; font-family:Courier; color:Blue; font-size: 20px;"><b>Regiao Nordeste</b></p>'
	st.markdown(titulo_plot06a, unsafe_allow_html=True)
	st.plotly_chart(fig_NE, use_container_width=True)

with col2: 
	titulo_plot06b =  '<p style="text-align: center; font-family:Courier; color:Blue; font-size: 20px;"><b>Regiao Norte</b></p>'
	st.markdown(titulo_plot06b, unsafe_allow_html=True)
	st.plotly_chart(fig_N, use_container_width=True)

col1, col2 = st.columns(2)
with col1: 
	titulo_plot06c =  '<p style="text-align: center; font-family:Courier; color:Blue; font-size: 20px;"><b>Regiao Sul</b></p>'
	st.markdown(titulo_plot06c, unsafe_allow_html=True)
	st.plotly_chart(fig_S, use_container_width=True)

with col2: 
	titulo_plot06d =  '<p style="text-align: center; font-family:Courier; color:Blue; font-size: 20px;"><b>Regiao Centro-Oeste</b></p>'
	st.markdown(titulo_plot06d, unsafe_allow_html=True)
	st.plotly_chart(fig_CO, use_container_width=True)

titulo_plot06e =  '<p style="text-align: center; font-family:Courier; color:Blue; font-size: 20px;"><b>Regiao Sudeste</b></p>'
st.markdown(titulo_plot06e, unsafe_allow_html=True)
st.plotly_chart(fig_SE, use_container_width=True)

# ------------------------------------------------------------------------
# Plot07: Análise
# ------------------------------------------------------------------------
st.subheader("Principais Resultados")
st.write("Assim como, de forma geral, o Brasil possui uma grande quantidade de instituições privadas de ensino superior, totalizando 88% do total de IES; a análise por cursos também indica uma superioridade numérica e proporcional daqueles ofertados por IES privadas. Em números absolutos, a região sudeste destaca-se com uma grande concentração de cursos ofertados, principalmente nos estados de São Paulo, Minas Gerais e Rio de Janeiro.")

st.write("Além disso, a região Sudeste lidera em quantidade de cursos nas áreas de 'Negócios, Administração e Direito' e 'Saúde e Bem-Estar'. Em segundo lugar, o Nordeste também apresenta uma quantidade significativa de cursos nessas mesmas áreas. Observa-se uma tendência consistente em todas as regiões: os cursos menos ofertados estão nas áreas de serviços, com exceção do Nordeste, onde a menor oferta é na categoria de 'Ciências Naturais, Matemática e Estatística'.")
st.markdown('---')