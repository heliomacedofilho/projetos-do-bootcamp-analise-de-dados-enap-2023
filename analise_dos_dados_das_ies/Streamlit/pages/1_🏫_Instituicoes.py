import os
import pandas as pd 
import numpy as np 
import matplotlib
import matplotlib.pyplot as plt 
import seaborn as sns 
import plotly
import plotly.express as px
import streamlit as st
import geobr
import geopandas as gpd

# ------------------------------------------------------------------------
# PARTE 01 - Analise IES - 2022
# ------------------------------------------------------------------------
st.set_page_config(page_title='Analise IES', 
                    page_icon=':school:', 
				    layout='wide', 
                    initial_sidebar_state='expanded')


st.title(':school: Mapa das Instituições de Ensino Superior :flag-br:')
st.subheader('Escopo: Todas as IES existentes no Brasil')
st.subheader("Dados de 2022")
st.markdown("---")


# ------------------------------------------------------------------------
# Parametros plots seaborn
# ------------------------------------------------------------------------
sns.set(style="darkgrid")


# ------------------------------------------------------------------------
# Carrega dados IES
# ------------------------------------------------------------------------
colunas_CO = ['CO_REGIAO_IES',  'CO_UF_IES', 'CO_MESORREGIAO_IES', 'CO_MICRORREGIAO_IES',
 'CO_MANTENEDORA', 'CO_IES', 'COD_IBGE', 'IN_CAPITAL_IES', 'NU_CEP_IES']
dict_dtype = {column : 'str'  for column in colunas_CO}
ies = pd.read_csv('./arquivos/dados_ies_consolidado.csv', sep='|', dtype = dict_dtype, low_memory=False)

# ------------------------------------------------------------------------
# Carrega dados IES agregados por UF
# ------------------------------------------------------------------------
ies_agg_UF = pd.read_csv('./arquivos/dados_IES_agg_UF.csv', sep='|', 
                   low_memory=False)

ies_agg_UF = ies_agg_UF.rename(columns={'Total_mun':'Total_mun_IES',
                                        'Total_Pop_IES':'Total_Pop_UF_IES',
                                        'Total_Pop_IBGE_2022':'Total_Pop_UF',
                                        'Total_Mun_IBGE_2022':'Total_Mun_UF',
                                        'Total_Meso':'Total_Meso_UF',
                                        'Total_Micro':'Total_Micro_UF',
                                        'Prop_Mun':'Cob_Mun_com_IES',
                                        'Cob_Meso':'Cob_Meso_com_IES',
                                        'Cob_Micro':'Cob_Micro_com_IES'})

ies_agg_UF = ies_agg_UF[['SG_UF_IES', 'Total_Pop_UF', 'Total_Mun_UF', 'Total_Meso_UF', 'Total_Micro_UF',
                         'Total_IES', 'Total_Priv', 'Total_Publ','Total_mun_IES', 'Total_Pop_UF_IES',
                         'Total_Meso_IES','Total_Micro_IES',
                         'Cob_Mun_com_IES','Cob_Meso_com_IES','Cob_Micro_com_IES']]

                         
#--------------------------------------------------------------------------------------------
# Carrega dados IES agregados por Região
#------------------------------------------------------------------------------------------
ies_agg_regiao = pd.read_csv('./arquivos/dados_IES_agg_Regiao.csv', sep='|', 
                   low_memory=False)

ies_agg_regiao = ies_agg_regiao.rename(columns={'Total_mun':'Total_mun_IES',
                                        'Total_Pop_IES':'Total_Pop_UF_IES',
                                        'Total_Pop_IBGE_2022':'Total_Pop_UF',
                                        'Total_Mun_IBGE_2022':'Total_Mun_UF',
                                        'Total_Meso':'Total_Meso_UF',
                                        'Total_Micro':'Total_Micro_UF',
                                        'Prop_Mun':'Cob_Mun_com_IES',
                                        'Cob_Meso':'Cob_Meso_com_IES',
                                        'Cob_Micro':'Cob_Micro_com_IES'})

ies_agg_regiao = ies_agg_regiao[['REGIAO', 'NOME_REGIAO', 'Total_Pop_UF', 'Total_Mun_UF', 'Total_Meso_UF', 'Total_Micro_UF',
                         'Total_IES', 'Total_Priv', 'Total_Publ','Total_mun_IES', 'Total_Pop_UF_IES',
                         'Total_Meso_IES','Total_Micro_IES',
                         ]]

                         
                       
# ------------------------------------------------------------------------
# Prepara dados IES agregados por campos especificos
# ------------------------------------------------------------------------				 

# Total IES
total_ies = ies['NO_IES'].count()

# total de IES por Categoria 
total_ies_cat_adm = ies['Tipo_Cat_Admn'].value_counts()
perc_ies_cat_adm = round(total_ies_cat_adm / total_ies * 100,2) 
distr_ies_cat_br = pd.DataFrame({'Total_IES'   : total_ies_cat_adm,
                                 'Total_IES_p':  perc_ies_cat_adm}).reset_index()

# total de IES por Organização e Categoria Adm
distr_cat_org_br = ies.groupby(['Tipo_Cat_Admn','Tipo_Org_Acad'])['CO_IES'].count().reset_index()
distr_cat_org_br = distr_cat_org_br.rename(columns={'CO_IES':'Total_IES'})


#--------------------------------------------------------------------------------------------
# Prepara dados IES agregados por UF
#------------------------------------------------------------------------------------------               

# total de IES por UF 
tot_ies_uf = ies.groupby('SG_UF_IES')['NO_IES'].count()
                  
# total de IES por UF e Organização 
tot_ies_org_uf = ies.groupby(['SG_UF_IES','Tipo_Org_Acad'])['NO_IES'].count()
perc_ies_org_uf = round(tot_ies_org_uf / tot_ies_uf *100,2)
distr_ies_org_uf = pd.DataFrame({'Total_Org'   : tot_ies_org_uf,
                                 'Total_Org_p': perc_ies_org_uf}).reset_index()

# total de IES por UF e Tipo Instituicao
tot_ies_tp_uf = ies.groupby(['SG_UF_IES','TIPO_INST'])['NO_IES'].count()
perc_ies_tp_uf = round(tot_ies_tp_uf / tot_ies_uf *100,2)
distr_ies_tp_uf = pd.DataFrame({'Total_IES'   : tot_ies_tp_uf,
                                'Total_IES_p': perc_ies_tp_uf}).reset_index()
                                
#--------------------------------------------------------------------------------------------
# Prepara dados IES agregados por Regiao
#------------------------------------------------------------------------------------------
tot_ies_regiao = ies.groupby('NO_REGIAO_IES')['NO_IES'].count()

# Total IES por Orgao
tot_ies_org_regiao = ies.groupby(['NO_REGIAO_IES','Tipo_Org_Acad'])['NO_IES'].count()
perc_ies_org_regiao = round(tot_ies_org_regiao / tot_ies_regiao *100,2)
distr_ies_org_regiao = pd.DataFrame({'Total_Org'   : tot_ies_org_regiao,
                                 'Total_Org_p': perc_ies_org_regiao}).reset_index()

# Total IES por Tipo Instituição                        
tot_ies_tp_regiao = ies.groupby(['NO_REGIAO_IES','TIPO_INST'])['NO_IES'].count()
perc_ies_tp_regiao = round(tot_ies_tp_regiao / tot_ies_regiao *100,2)
distr_ies_tp_regiao = pd.DataFrame({'Total_IES'   : tot_ies_tp_regiao,
                                'Total_IES_p': perc_ies_tp_regiao}).reset_index()                         
                         
# -----------------------------------------------------------------------------------
# Mapa 01:  Distribuição IES no Brasil - 2022
# -----------------------------------------------------------------------------------
titulo_map01 = '<p style="font-family:Courier; color:blue; font-size: 25px;"><b>Mapa do Brasil com todas as Instituições de Ensino Superior</b></p>'
st.markdown(titulo_map01, unsafe_allow_html=True)

# cria o dataframe das IES publicas e privadas
df_publica = ies[ies['TIPO_INST'] == 'Pública']
df_privada = ies[ies['TIPO_INST'] == 'Privada']
states = geobr.read_state(code_state='all')

fig, ax = plt.subplots(figsize=(6, 6))
states.boundary.plot(ax=ax, linewidth=0.4, color='black')
ax.scatter(df_privada['LNG'], df_privada['LAT'], color='#1b9e77', label='Instituição Privada', s=10, alpha=0.7)
ax.scatter(df_publica['LNG'], df_publica['LAT'], color='#d95f02', label='Instituição Pública', s=10, alpha=0.7)
ax.set_xlim(-75, -30)  # Ajuste os limites do mapa de acordo com a localização desejada
ax.set_ylim(-35, 5)
#ax.set_xlabel('Longitude')
#ax.set_ylabel('Latitude')
ax.tick_params(axis='y', labelsize=6)
ax.tick_params(axis='x', labelsize=6)
#ax.set_title('Mapa do Brasil com Instituições de Ensino Superior')
ax.legend(loc='best', fontsize=8)
st.pyplot(fig,  use_container_width=False)

# -------------------
# Analise
# -------------------
st.subheader('Análise:')

write_map01 = '<p style="font-family:Arial; color:black; font-size: 18px;">Nota-se, claramente em todo o país, a predominância de instituições privadas com relação às instituições públicas, com maior concentração das privadas nas Regiões Sul, Sudeste e Nordeste.</p>'

write_map02 = '<p style="font-family:Arial; color:black; font-size: 18px;">As instituições públicas, embora em menor quantidade total, se encontram fortemente concentradas no estado de São Paulo e Rio de Janeiro.</p>'

write_map03 = '<p style="font-family:Arial; color:black; font-size: 18px;">São pouquíssimas as instituições públicas nas Regiões Norte e Centro-Oeste.</p>'

st.markdown(write_map01, unsafe_allow_html=True)
st.markdown(write_map02, unsafe_allow_html=True)
st.markdown(write_map03, unsafe_allow_html=True)
st.markdown("---")

#--------------------------------------------------------------------------------------
# Plot 01 - Distribuição da Qtd de Instituições de Ensino Superior por Região 
#--------------------------------------------------------------------------------------
titulo_plot01 = '<p style="font-family:Courier; color:Blue; font-size: 25px;"><b>Distribuição da Qtd de IES por Região </b></p>'
st.markdown(titulo_plot01, unsafe_allow_html=True)

fig = px.bar(ies_agg_regiao.sort_values(by='Total_IES', ascending=False),
             x='NOME_REGIAO', 
             y='Total_IES', 
             color='Total_IES',
             color_continuous_scale='viridis_r',
             width=1100, height=600,
             text='Total_IES')
fig.update_traces(textfont_size=20, textangle=0, textposition="inside")
fig.update_layout(yaxis=dict(title='Total IES', titlefont_size=30, tickfont_size=12),
                  xaxis=dict(title='', tickfont_size=20),
                  coloraxis_showscale=False)
fig.update_xaxes(tickangle = 0)
fig.update_layout(plot_bgcolor='#dbe0f0') 
fig.update_layout(hoverlabel=dict(bgcolor="white", 
                                  font_size=18,
                                  font_family="Rockwell"))	

st.plotly_chart(fig, use_container_width=True)
st.markdown("---")                 

# -----------------------------------------------------------------------------------
# Plot 02:  Distribuição da Qtd de Instituições de Ensino Superior por UF
# -----------------------------------------------------------------------------------
titulo_plot02 = '<p style="font-family:Courier; color:blue; font-size: 25px;"><b>Distribuição da Qtd de IES por UF</b></p>'
st.markdown(titulo_plot02, unsafe_allow_html=True)

fig = px.bar(ies_agg_UF.sort_values(by='Total_IES', ascending=False),
             x='SG_UF_IES', 
             y='Total_IES', 
             color='Total_IES',
             color_continuous_scale='viridis_r',
             width=1100, height=600)
fig.update_layout(yaxis=dict(title='Total IES', titlefont_size=30, tickfont_size=12),
                  xaxis=dict(title='', tickfont_size=20),
                  coloraxis_showscale=False)
fig.update_xaxes(tickangle = -45)
fig.update_layout(plot_bgcolor='#dbe0f0') 
fig.update_layout(hoverlabel=dict(bgcolor="white", 
                                  font_size=22,
                                  font_family="Rockwell"))	
st.plotly_chart(fig, use_container_width=True)

# -------------------
# Analise
# -------------------
st.subheader('Análise:')
write_plot01 = '<p style="font-family:Arial; color:black; font-size: 18px;">As IES estão presentes em todos os estados do território nacional, em maior número nos estados da região sudeste do país (1.098 IES, 42,31%), condizente com a proporção populacional da região que é de aproximadamente 40% da população total do país.</p>'
st.markdown(write_plot01, unsafe_allow_html=True)
st.markdown("---")

# ------------------------------------------------------------------------
# Plot 03: Distribuição da Qtd de IES por Org Acadêmica e Cat Administrativa 
# Brasil 
# ------------------------------------------------------------------------
titulo_plot03 = '<p style="font-family:Courier; color:Blue; font-size: 25px;"><b>Distribuição da Qtd de IES por  Org. Acadêmica e Categ. Administrativa - Brasil</b></p>'
st.markdown(titulo_plot03, unsafe_allow_html=True)

fig = px.bar(distr_cat_org_br,
             y='Tipo_Cat_Admn', 
             x='Total_IES', 
             color='Tipo_Org_Acad',
             color_discrete_sequence=px.colors.sequential.Viridis_r,
             barmode = 'stack', width=1100, height=700,
             labels=dict(Tipo_Org_Acad = 'Organização Acadêmica'))
fig.update_layout(yaxis=dict(title='', titlefont_size=30, tickfont_size=20),
                  xaxis=dict(title='', tickfont_size=20),      
                  legend=dict(x=0.1,y=-0.6, font = dict(size = 18))) 
fig.update_xaxes(tickangle=0)
fig.update_layout(plot_bgcolor='#dbe0f0') 
fig.update_layout(hoverlabel=dict(bgcolor="white", 
                                  font_size=22,
                                  font_family="Rockwell"))	
st.plotly_chart(fig, use_container_width=True) 

# -------------------
# Analise
# -------------------
st.subheader('Análise:')
write_plot03 = '<p style="font-family:Arial; color:black; font-size: 18px;">Observa-se a predominância de organizações privadas no país, tendo as públicas 11% do total de IES. Das 2.595 Instituições de Ensino Superior (IES) do Brasil, há uma predominância de Faculdades (75,84%) e Centros Universitários (14,68%), totalizando 2.349 IES, ou seja, 90,52% do total de instituições no país. Ainda que dentre essas organizações estejam algumas públicas, o resultado é condizente com o encontrado na distribuição das IES por categoria administrativa, em que as instituições privadas (com e sem fim lucrativo) ocupam a proporção de 87,98% do total de IES no Brasil.</p>'
st.markdown(write_plot03, unsafe_allow_html=True)
st.markdown("---")


# -----------------------------------------------------------------------------------
# Plot 04:  Proporção de IES por Organização Acadêmica - Regioes
# -----------------------------------------------------------------------------------
titulo_plot04 = '<p style="font-family:Courier; color:Blue; font-size: 25px;"><b>Distribuição da Proporção de IES por Organização Acadêmica - Regiões</b></p>'
st.markdown(titulo_plot04, unsafe_allow_html=True)
   
fig = px.bar(distr_ies_org_regiao.sort_values(by='Total_Org_p', ascending=False),
             x='NO_REGIAO_IES', 
             y='Total_Org_p', 
             color='Tipo_Org_Acad',
             color_discrete_sequence=px.colors.qualitative.Dark2,
             barmode = 'group', width=1000, height=800)
fig.update_layout(yaxis=dict(title='Proporção %', titlefont_size=25, tickfont_size=20),
                  xaxis=dict(title='', tickfont_size=20),      
                  legend=dict(x=0.25,y=-0.4, font = dict(size = 18))) 
                  
fig.update_layout(plot_bgcolor='#dbe0f0') 
fig.update_layout(hoverlabel=dict(bgcolor="white", 
                                  font_size=22,
                                  font_family="Rockwell"))
st.plotly_chart(fig, use_container_width=True)

# -------------------
# Analise
# -------------------
st.subheader('Análise:')
write_plot04 = '<p style="font-family:Arial; color:black; font-size: 18px;">Quando analisa-se a distribuição das IES pelas regiões do país, em função do tipo de organização acadêmica, é possível observar que a maior prevalência de faculdades e centros universitários está presente em todas as regiões. Quando estratifica-se a análise retirando as faculdades, pode-se observar que a região sul possui, entre os tipos, a maior proporção de universidades que as demais regiões do país. Ainda assim, em todas as regiões a ordem proporcional é sempre a mesma: faculdades, centro-universitários, universidades, Institutos Federais e Cefet.</p>'
st.markdown(write_plot04, unsafe_allow_html=True)
st.markdown("---")


# -----------------------------------------------------------------------------------
# Plot 05:  Proporção de IES por Organização Acadêmica - UFS
# -----------------------------------------------------------------------------------
titulo_plot05 = '<p style="font-family:Courier; color:Blue; font-size: 25px;"><b>Distribuição da Proporção de IES por Organização Acadêmica - UF </b></p>'
st.markdown(titulo_plot05, unsafe_allow_html=True)

fig = px.bar(distr_ies_org_uf.sort_values(by='Total_Org_p', ascending=False),
             x='SG_UF_IES', 
             y='Total_Org_p', 
             color='Tipo_Org_Acad',
             color_discrete_sequence=px.colors.qualitative.Dark2,
             barmode = 'group', width=1000, height=800,
            )

fig.update_layout(yaxis=dict(title='Proporção %', titlefont_size=25, tickfont_size=20),
                 xaxis=dict(title='', tickfont_size=20),      
                 legend=dict(x=0.3,y=-0.4, font = dict(size = 18)))
fig.update_layout(plot_bgcolor='#dbe0f0') 
fig.update_layout(hoverlabel=dict(bgcolor="white", 
                                  font_size=22,
                                  font_family="Rockwell"))
st.plotly_chart(fig, use_container_width=True)
             
# -------------------
# Analise
# -------------------
st.subheader('Análise:')
write_plot05a = '<p style="font-family:Arial; color:black; font-size: 18px;">A distribuição das IES nos estados, por tipo de organização, segue o mesmo padrão encontrado nos dados agrupados em nível nacional, com predominância significativa de instituições do tipo faculdade. Contudo, essa proporção tem variação entre os estados: enquanto a maioria dos estados possuem majoritariamente faculdades e centros universitários; os estados de Roraima, Rio Grande do Sul, Mato Grosso do Sul e Amapá destacam-se por possuir universidades como o segundo tipo de IES mais prevalente.</p>'
write_plot05b = '<p style="font-family:Arial; color:black; font-size: 18px;">Amapá, curiosamente, é o unico Estado sem a existência de centro universitário, enquanto que apenas os estados de RJ e MG possuem CEFETs federais.</p>'
st.markdown(write_plot05a, unsafe_allow_html=True)
st.markdown(write_plot05b, unsafe_allow_html=True)
st.markdown("---")

# -----------------------------------------------------------------------------------
# Plot 06: Distribuição da Qtd de IES por Categoria - Regiao
# Plot 07: Proporção de IES por Categoria - Regiao
# -----------------------------------------------------------------------------------             

# Inserir titulos 
col1, col2 = st.columns(2)
with col1:
    titulo_plot06 = '<p style="font-family:Courier; color:blue; font-size: 25px;"><b>Distribuição da Qtd de IES por Categoria - Região</b></p>'
    st.markdown(titulo_plot06, unsafe_allow_html=True)
with col2:
    titulo_plot07 = '<p style="font-family:Courier; color:Blue; font-size: 25px;"><b>Distribuição da Proporção de IES por Categoria - Região</b></p>'
    st.markdown(titulo_plot07, unsafe_allow_html=True)
        
col1, col2 = st.columns(2)
with col1:
    fig = px.bar(distr_ies_tp_regiao.sort_values(by='Total_IES', ascending=False),
    x='NO_REGIAO_IES', 
    y='Total_IES', 
    color='TIPO_INST',
    color_discrete_sequence=px.colors.qualitative.Dark2,
    barmode = 'group', width=1000, height=800,
    text='Total_IES')
    fig.update_traces(textfont_size=20, textangle=0, textposition="inside")
    fig.update_layout(yaxis=dict(title='Total IES', titlefont_size=25, tickfont_size=22),
    xaxis=dict(title='', tickfont_size=20),      
    legend=dict(x=0.65,y=0.9, font = dict(size = 20)))
    fig.update_layout(plot_bgcolor='#dbe0f0') 
    fig.update_layout(hoverlabel=dict(bgcolor="white", font_size=22,font_family="Rockwell"))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.bar(distr_ies_tp_regiao.sort_values(by='Total_IES_p', ascending=False),
    x='NO_REGIAO_IES', 
    y='Total_IES_p', 
    color='TIPO_INST',
    color_discrete_sequence=px.colors.qualitative.Dark2,
    barmode = 'group', width=1000, height=800,
    text='Total_IES_p')
    fig.update_traces(textfont_size=20, textangle=0, textposition="inside")
    fig.update_layout(yaxis=dict(title='Proporção %', titlefont_size=25, tickfont_size=22),
    xaxis=dict(title='', titlefont_size=30, tickfont_size=22),      
    #legend=dict(x=0.25,y=-0.2, font = dict(size = 20))    
    ) 
    fig.update_layout(plot_bgcolor='#dbe0f0') 
    fig.update_layout(showlegend=False)
    fig.update_layout(hoverlabel=dict(bgcolor="white", font_size=22,font_family="Rockwell"))
    st.plotly_chart(fig, use_container_width=True)

# -------------------
# Analise
# -------------------
st.subheader('Análise:')
write_plot06 = '<p style="font-family:Arial; color:black; font-size: 18px;">Em números absolutos, quando analisado por categoria administrativa, o que se observa é o mesmo comportamento da distribuição geral das IES nas regiões do país. Uma hierarquização em que a região Sudeste apresenta o maior número de instituições, tanto públicas quanto privadas, seguido das regiões Nordeste, Sul, Centro-Oeste e Norte.</p>'
write_plot07 = '<p style="font-family:Arial; color:black; font-size: 18px;">Mas números absolutos podem enganar. O gráfico a seguir, com as mesmas informações do ponto de vista proporcional em cada região, demonstra que o Sudeste passa a ser a região com a menor proporção de IES privadas e, consequentemente, a maior proporção de IES públicas. Ou seja, ainda que em termos absolutos a região apresente o maior número de IES privadas do país, também é a região com a menor proporção. Isso provavelmente se explica pelos estados do RJ e SP, que possuem uma proporção de IES públicas mais alta do que a maioria dos estados.</p>'
st.markdown(write_plot06, unsafe_allow_html=True)
st.markdown(write_plot07, unsafe_allow_html=True)
st.markdown("---")



# -----------------------------------------------------------------------------------
# Plot 08:  Distribuição da Qtd de IES por Categoria  - UF
# ----------------------------------------------------------------------------------- 
titulo_plot08 = '<p style="font-family:Courier; color:blue; font-size: 25px;"><b>Distribuição da Qtd de IES por Categoria - UF</b></p>'
st.markdown(titulo_plot08, unsafe_allow_html=True)

fig = px.bar(distr_ies_tp_uf.sort_values(by='Total_IES', ascending=False),
             x='SG_UF_IES', 
             y='Total_IES', 
             color='TIPO_INST',
             color_discrete_sequence=px.colors.qualitative.Dark2,
             barmode = 'group', width=1000, height=600)
fig.update_layout(yaxis=dict(title='Total IES', titlefont_size=25, tickfont_size=22),
                  xaxis=dict(title='', tickfont_size=20),      
                  legend=dict(x=0.35,y=0.9, font = dict(size = 24)))
fig.update_layout(plot_bgcolor='#dbe0f0') 
fig.update_layout(hoverlabel=dict(bgcolor="white", 
                                  font_size=22,
                                  font_family="Rockwell"))
st.plotly_chart(fig, use_container_width=True)
st.markdown("---")

# -----------------------------------------------------------------------------------
# Plot 09: Proporção de IES por Categoria - UF
# -----------------------------------------------------------------------------------  
titulo_plot09 = '<p style="font-family:Courier; color:Blue; font-size: 25px;"><b>Distribuição da Proporção de IES por Categoria - UF</b></p>'
st.markdown(titulo_plot09, unsafe_allow_html=True)

fig = px.bar(distr_ies_tp_uf.sort_values(by='Total_IES_p', ascending=False),
             x='SG_UF_IES', 
             y='Total_IES_p', 
             color='TIPO_INST',
             color_discrete_sequence=px.colors.qualitative.Dark2,
             barmode = 'stack', width=1000, height=600)
fig.update_layout(yaxis=dict(title='Proporção %', titlefont_size=20, tickfont_size=22),
                  xaxis=dict(title='', titlefont_size=25, tickfont_size=22),    
                  legend=dict(x=0.35,y=0.5, font = dict(size = 24))) # 
fig.update_layout(plot_bgcolor='#dbe0f0') 
fig.update_layout(hoverlabel=dict(bgcolor="white", 
                                  font_size=22,
                                  font_family="Rockwell"))
st.plotly_chart(fig, use_container_width=True)


# -------------------
# Analise
# -------------------
st.subheader('Análise:')
write_plot09a = '<p style="font-family:Arial; color:black; font-size: 18px;">Em nível nacional, as instituições privadas (com e sem fins lucrativos) ocupam a proporção de 87,98% do total de IES no Brasil. Pode-se observar um cenário aproximado com predominância de instituições privadas quando analisado por UF, destacando-se o estado de MT com a maior proporção de instituições privadas (94,44%) e Roraima com a menor proporção (66.67%).</p>'
write_plot09b = '<p style="font-family:Arial; color:black; font-size: 18px;">Observa-se que a proporção entre IES público e privadas em cada estado possui um variação, como por exemplo, as IES públicas que tem uma prevalência entre 5,56%  em MT e 33,33% em RR. Ainda assim, é possível identificar que na maioria dos estados (67%) a proporção de IES públicas não chega a 10%.</p>'
st.markdown(write_plot09a, unsafe_allow_html=True)
st.markdown(write_plot09b, unsafe_allow_html=True)
st.markdown("---")


# -----------------------------------------------------------------------------------
# Plot 10: Cobertura de Municipios 
# -----------------------------------------------------------------------------------  
titulo_plot10 = '<p style="font-family:Courier; color:Blue; font-size: 25px;"><b>Cobertura de Municipios com existência de IES</b></p>'
st.markdown(titulo_plot10, unsafe_allow_html=True)

fig = plt.figure(figsize=(20, 15))
axes = fig.add_subplot(111)

cores = sns.color_palette("mako", 27) # magma
interval_x = np.arange(0,625,25) # intervalo eixos população
interval_y = np.arange(0,60000000,5000000) # intervalo eixos população

g = sns.barplot(x='SG_UF_IES', 
                y='Total_IES', 
                data=ies_agg_UF.sort_values(by='Total_IES', ascending=False),
                palette = cores, 
                label='Total_IES')

axes.set_ylabel('Total IES', fontsize=18)
axes.yaxis.set_ticks(interval_x)
axes.set(xlabel='') 

ax2 = axes.twinx()
ax2.plot(ies_agg_UF.sort_values(by='Total_IES', ascending=False)['SG_UF_IES'], 
         ies_agg_UF.sort_values(by='Total_IES', ascending=False)['Total_Pop_UF_IES'],
        color='#ffff00', label='Total_Pop_IES')
ax2.set_ylabel("População dos municipios com IES", fontsize=20)

ax3 = axes.twinx()
ax3.plot(ies_agg_UF.sort_values(by='Total_IES', ascending=False)['SG_UF_IES'], 
         ies_agg_UF.sort_values(by='Total_IES', ascending=False)['Total_Pop_UF'],
        color='#ff8000', label='Total_Pop_IBGE')
#ax3.set_ylabel("População total da UF")

axes.grid(visible=False)

ax2.grid(visible=True, linestyle = "dashed", color='white')
ax2.yaxis.set_ticks(interval_y)
#ax2.yaxis.set_visible(False) # remove yticks

ax3.grid(visible=False)
ax3.yaxis.set_ticks(interval_y)
ax3.yaxis.set_visible(True) # remove yticks

lines1, labels1 = axes.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
lines3, labels3 = ax3.get_legend_handles_labels()
ax3.legend(lines1 + lines2 + lines3, labels1 + labels2 + labels3, loc="upper center", fontsize=18)

valores_prop_mun =  ies_agg_UF.sort_values(by='Total_IES', ascending=False)['Cob_Mun_com_IES'].values
for i, p in enumerate(axes.patches):
        axes.annotate('{:,.0f}%'.format(valores_prop_mun[i]), 
                      (p.get_x()+0.1, p.get_height()+10) , 
                     fontsize=16, weight='bold', color='#730099')

st.pyplot(fig)

# -------------------
# Analise
# -------------------
st.subheader('Análise:')
write_plot10 = '<p style="font-family:Arial; color:black; font-size: 18px;">O gráfico acima mostra o percentual de municipios com a existência de pelo menos uma instituição de ensino. Desta forma, embora SP tenha o maior número de instituições, é o estado do Rio de Janeiro que possui a maior cobertura de IES (32% dos seus municípios com alguma instituição), seguido pelos estados do Espírito Santo e São Paulo, ambos com cobertura de 24%. Na PB e RN, apenas 4 a 5% dos municípios possuem algum tipo de IES</p>'
st.markdown(write_plot10, unsafe_allow_html=True)
st.markdown("---")


# -----------------------------------------------------------------------------------
# Plot 11: Cobertura de Microregioes 
# -----------------------------------------------------------------------------------  
titulo_plot11 = '<p style="font-family:Courier; color:Blue; font-size: 25px;"><b>Cobertura de Microrregiões com existência de IES</b></p>'
st.markdown(titulo_plot11, unsafe_allow_html=True)


# prepara dados
colunas_int = ['SG_UF_IES','Total_IES', 'Cob_Mun_com_IES','Cob_Meso_com_IES','Cob_Micro_com_IES']
df_coberturas = ies_agg_UF[colunas_int]
df_coberturas_m = df_coberturas.melt(id_vars=['SG_UF_IES'])

f, axes = plt.subplots(1, 1,  figsize=(20, 10))
cores = sns.color_palette("Paired")

dados = df_coberturas_m[df_coberturas_m['variable'].isin(['Cob_Mun_com_IES','Cob_Micro_com_IES'])]

# ordem das UFs no eixo x
my_order = list(df_coberturas.sort_values(by='Total_IES', ascending=False)['SG_UF_IES'])

sns.barplot(x='SG_UF_IES', y='value', hue='variable', 
            data=dados,
            ax=axes, 
            palette=cores, 
            order=my_order,
            hue_order=['Cob_Micro_com_IES','Cob_Mun_com_IES'])

#axes.set_title('Distribuição IES no Brasil - Cobertura Microrregiões (2022)', fontsize=20)
axes.set_xlabel('')
axes.set_ylabel("Percentual (%)", fontsize = 20)
xlocs, xlabels = plt.xticks()
ylocs, ylabels = plt.yticks()
plt.setp(xlabels, rotation=0, fontsize=15)
plt.setp(ylabels, fontsize=15)

dados2 = df_coberturas[['SG_UF_IES','Total_IES']].sort_values(by='Total_IES', ascending=False)
x=dados2['SG_UF_IES']
y=dados2['Total_IES']
axes2 = axes.twinx()
axes2.plot(x, y, color='#cc0000', label='Total IES')
axes2.set_ylabel("Total de IES na UF", fontsize = 20)
axes2.grid(visible=False)

for i, j in zip(x, y):
    axes2.text(i,j, str(j), ha='center', va='bottom', color='#cc0000', fontsize=14)

    axes.legend(loc='best', fontsize=18)
st.pyplot(f)

# -------------------
# Analise
# -------------------
st.subheader('Análise:')
write_plot11 = '<p style="font-family:Arial; color:black; font-size: 18px;">O gráfico acima mostra a cobertura de municípios em microrregiões com a existência de pelo menos uma instituição de ensino. Desta forma, se tem uma razoável cobertura de IES em boa parte dos estados, ao se considerar esta perspectiva de microrregiões.</p>'
write_plot11b = '<p style="font-family:Arial; color:red; font-size: 18px;">Obs. a linha vermelha representa o total de instituições de ensino em cada UF.</p>'

st.markdown(write_plot11, unsafe_allow_html=True)
st.markdown(write_plot11b, unsafe_allow_html=True)
st.markdown("---")


