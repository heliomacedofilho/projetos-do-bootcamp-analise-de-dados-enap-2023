import os
import pandas as pd 
import numpy as np 
import matplotlib
import matplotlib.pyplot as plt 
import seaborn as sns 
import plotly
import plotly.express as px

import json
import requests

import streamlit as st

# https://emec.mec.gov.br/emec/educacao-superior/cursos


# ------------------------------------------------------------------------
# Evolução da Oferta de Curso
# ------------------------------------------------------------------------
st.set_page_config(page_title='Analise Cursos', 
                    page_icon=':books:', 
				    layout='wide', 
                    initial_sidebar_state='expanded')

st.title(':chart_with_upwards_trend: Evolução e Situação Atual - Oferta de Cursos :flag-br:')
st.subheader('Escopo: Cursos Presenciais de Federais Públicas e Privadas')
st.subheader("Dados de 2012-2022")
st.markdown("---")


# Cabeçalho
titulo_map =  '<p style="font-family:Arial; color:Black; font-size: 18px;">Esta aba apresenta informações consolidadas sobre a oferta de cursos pelas Instituições de Ensino Superior. <br><br>É importante enfatizar que estão sendo considerados neste estudo apenas os cursos de graduação presenciais (nos graus de bacharelado, licenciatura e tecnólogo) de instituições públicas federais e de todas as instituições privadas.</p>'
st.markdown(titulo_map, unsafe_allow_html=True)

texto = '<p style="font-family:Arial; color:Black; font-size: 14px;">Nota: Para iniciar a oferta de um curso de graduação, a IES depende de autorização do Ministério da Educação. A exceção são as universidades e centros universitários que, por terem autonomia, independem de autorização para funcionamento de curso superior. No entanto, essas instituições devem informar à Secretaria competente os cursos abertos para fins de supervisão, avaliação e posterior reconhecimento, conforme disposto no art. 28 do Decreto nº 5.773/2006.</p>'
st.markdown(texto, unsafe_allow_html=True)



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
    
@st.cache_data
# dados_cursos_2012_2022.csv alterado para dados_cursos_2012_2022_reduzida01.csv
def carrega_cursos_2012_2022():
	df_all = pd.read_csv('./arquivos/dados_cursos_2012_2022_reduzida01.csv', sep='|', 
						low_memory=False, 
						usecols=['NU_ANO_CENSO', 'NO_UF','Tipo_Cat_Admn','Tipo_Org_Acad','Tipo_Org_Principal', 'Tipo_Grau_Acad','Tipo_Rede',
						'NO_CINE_AREA_GERAL', 'NO_CURSO','QT_CURSO','QT_MAT','QT_ING','QT_CONC'])
	return df_all
    
@st.cache_data
def carrega_cursos():
    colunas_CO = ['CO_REGIAO', 'CO_UF', 'CO_MUNICIPIO', 'CO_IES', 'CO_CURSO', 
    'CO_CINE_ROTULO', 'CO_CINE_AREA_GERAL', 'CO_CINE_AREA_ESPECIFICA', 
    'CO_CINE_AREA_DETALHADA', 'IN_CAPITAL', 'IN_GRATUITO']
    dict_dtype = {column : 'str'  for column in colunas_CO}
    
    cursos = pd.read_csv('./arquivos/dados_cursos_escopo_consolidado.csv', sep='|', 
                  dtype = dict_dtype, 
                  low_memory=False)			  
    
    # retirada Programas básicos
    cursos = cursos[cursos['NO_CINE_AREA_GERAL']!='Programas básicos']
    cursos['AREA_GERAL2'] = cursos['NO_CINE_AREA_GERAL'].apply(lambda x: formata_area_geral2(x))
    return cursos
    


# Carrega dados IES agregados por UF
# ------------------------------------------------------------------------
@st.cache_data
def carrega_ies_agg_uf():
    ies_agg_UF = pd.read_csv('./arquivos/dados_IES_agg_UF.csv', sep='|', 
                   low_memory=False) 
    # renomear colunas para nomes mais intuitivos
    ies_agg_UF = ies_agg_UF.rename(columns={'Total_mun':'Total_mun_IES',
                                            'Total_Pop_IES':'Total_Pop_UF_IES',
                                            'Total_Pop_IBGE_2022':'Total_Pop_UF',
                                            'Total_Mun_IBGE_2022':'Total_Mun_UF',
                                            'Total_Meso':'Total_Meso_UF',
                                            'Total_Micro':'Total_Micro_UF',
                                            'Prop_Mun':'Cob_Mun_com_IES',
                                            'Cob_Meso':'Cob_Meso_com_IES',
                                            'Cob_Micro':'Cob_Micro_com_IES'})
    # ordenar as colunas
    ies_agg_UF = ies_agg_UF[['SG_UF_IES', 'Total_Pop_UF', 'Total_Mun_UF', 'Total_Meso_UF',
    'Total_Micro_UF','Total_IES', 'Total_Priv', 'Total_Publ','Total_mun_IES', 'Total_Pop_UF_IES',
     'Total_Meso_IES','Total_Micro_IES','Cob_Mun_com_IES','Cob_Meso_com_IES','Cob_Micro_com_IES']]
                   
    return ies_agg_UF                   
    

# ------------------------------------------------------------------------
# Parametros plots seaborn
# ------------------------------------------------------------------------
sns.set(style="darkgrid")

# ------------------------------------------------------------------------
# Carrega dados Cursos
# ------------------------------------------------------------------------
df_all = carrega_cursos_2012_2022()	
cursos = carrega_cursos()
ies_agg_UF = carrega_ies_agg_uf()

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


#--------------------------------------------------------------------------------------------
# Prepara tabs
#------------------------------------------------------------------------------------------          
t_evol_red_org_gr, t_evol_area, t_evol_matr, t_sit_br, t_sit_reg, t_sit_uf  = st.tabs([
                'Evolução Rede e Grau',
                'Evolução Área',
                'Evolução com Matriculas',
                'Situação Atual - BR',
                'Situação Atual - Regiões',
                'Situação Atual - UF',
                    ])
css = '''
<style>
.stTabs [data-baseweb="tab-list"] {
        color:#1221c4;
		gap: 20px; } # afastamento entre as tabs

	.stTabs [data-baseweb="tab"] {
		height: 50px;
        white-space: pre-wrap;
		background-color: white;
		border-radius: 4px 4px 4px 4px;
		gap: 10px;
		padding-top: 10px;
		padding-bottom: 10px;
    }

	.stTabs [aria-selected="true"] {
        color:#e63212;
  		background-color: #f7eb0a; #cor de fundo da tab selecionada;
        border-radius: 4px 4px 4px 4px;
        gap: 10px;
	}   
</style>
'''              
st.markdown(css, unsafe_allow_html=True)
              

# ------------------------------------------------------------------------				  
# Tab 01 - Evolução por Rede Ensino
# Plot01:  Evolução da Qtd de Cursos ofertados/ Categoria (linha) - Brasil
# Plot02:  Evolução da Qtd de Cursos ofertados/ Categoria (linha) - UF
# Plot03: Evolução da Qtd de Cursos ofertados/ Categoria (barra): Brasil e UF
# Plot04: Evolução da Qtd de Cursos ofertados/ Organizacao Academica (linha): Brasil e UF
# Plot05: Evolução da Qtd de Cursos ofertados/ Grau Academico (linha): Brasil e UF 
# ------------------------------------------------------------------------


with t_evol_red_org_gr:

    # ------------------------------------------------------------------------
    # Plot01: Evolução da Qtd de Cursos ofertados/ Categoria
    # Brasil 
    # ------------------------------------------------------------------------	  
    titulo_plot01 =  '<p style="font-family:Courier; color:Blue; font-size: 20px;"><b>Evolução da Quantidade de Cursos PRESENCIAIS por Rede de Ensino</b></p>'
    st.markdown(titulo_plot01, unsafe_allow_html=True)

    ano_min = evol_cursos['NU_ANO_CENSO'].min()
    ano_max = evol_cursos['NU_ANO_CENSO'].max()

    f, axes = plt.subplots(1, 1,  figsize=(22,8))

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
    axes.set_xticklabels(axes.get_xticklabels(), rotation=0, ha="right", fontsize=16)
    axes.set(xlabel=''); axes.set_ylabel('Total Cursos', fontsize=18)
    axes.tick_params(axis='y', labelsize=14)

    axes.grid(color='gray', linestyle='--', linewidth=1.2, axis='y', alpha=.2)

    axes.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=2,
               fontsize='x-large')

    st.pyplot(f)
    plt.close()

    # ------------------------------------------------------------------------
    # Plot01: Análise
    # ------------------------------------------------------------------------
    st.subheader("Análise:")
    st.write("Ao longo dos últimos 10 anos, há claramente uma tendência de crescimento contínuo na oferta de cursos das Instituições de Ensino Superior. Nota-se, entretanto, distintos comportamentos de oferta de cursos presenciais entre as entidades públicas e as privadas.")
    st.write("Enquanto as entidades públicas mantiveram o padrão de apresentar um pequeno aumento de oferta de cursos ao longo dos anos, as privadas apresentaram uma dinâmica mais variada.")
    st.write("Entre os anos de 2017 e 2018, pode-se notar claramente uma inversão no padrão de oferta de cursos  das entidades privadas: um aumento da oferta de cursos nas privadas com fins lucrativos, em contraste com o declínio dessa mesma oferta nas privadas sem fins lucrativos. Desta forma, as instituições privadas passaram a ocupar um espaço de maior destaque no setor educacional.")
    st.markdown("---")

    # ------------------------------------------------------------------------
    # Plot02: Evolução da Qtd de Cursos ofertados/ Categoria
    # select UF 
    # ------------------------------------------------------------------------	

    # Evolução da Quantidade de Cursos PRESENCIAIS por Rede de Ensino - Para uma UF específica
    # escolher uma UF 
    titulo_plot02_uf =  '<p style="font-family:Courier; color:Blue; font-size: 20px;"><b>Evolução da Quantidade de Cursos PRESENCIAIS por Rede de Ensino - Para uma UF específica</b></p>'
    st.markdown(titulo_plot02_uf, unsafe_allow_html=True)
    
    # preparar dados
    evol_cursos_uf = df_all.groupby(['NU_ANO_CENSO','NO_UF'])['NO_CURSO'].count().reset_index()
    evol_cursos_uf = evol_cursos_uf.rename(columns={'NO_CURSO':'Total_cursos'})
    evol_cursos_cat_uf = df_all.groupby(['NU_ANO_CENSO','NO_UF', 'Tipo_Cat_Admn'])['NO_CURSO'].count().reset_index()
    evol_cursos_cat_uf = evol_cursos_cat_uf.rename(columns={'NO_CURSO':'Total_cursos'})
    
    # prepara lista de opções de UFs
    l_UF = list(evol_cursos_cat_uf['NO_UF'].unique())
    col1, col2, col3 = st.columns(3)
    with col1:
        label01 = '<p style="font-family:Courier; color:#992600; font-size: 16px;"><b>Selecione uma UF:</b></p>'
        st.markdown(label01, unsafe_allow_html=True) 
    with col2:
        UF_selected = st.selectbox(label="Selecione uma UF:", options=l_UF, label_visibility="collapsed")
    with col3:    
        st.subheader(':classical_building:')

    if UF_selected:
        ano_min = evol_cursos_cat_uf['NU_ANO_CENSO'].min()
        ano_max = evol_cursos_cat_uf['NU_ANO_CENSO'].max()
        f, axes = plt.subplots(1, 1,  figsize=(22,8))

        # Curva Total
        data = evol_cursos_uf[evol_cursos_uf['NO_UF']==UF_selected].reset_index(drop=True)
        axes = sns.pointplot(x='NU_ANO_CENSO', y='Total_cursos', 
                    data=evol_cursos_uf[evol_cursos_uf['NO_UF']==UF_selected].reset_index(drop=True),
                    label="Total Cursos", markers='o', color='r')
        for i in range(len(data)):
                plt.text(i, data['Total_cursos'][i]*1.02,
                         data['Total_cursos'][i], color='r', fontsize=12)
        data1 = evol_cursos_cat_uf[
                (evol_cursos_cat_uf['Tipo_Cat_Admn']=='Privada com fins lucrativos') & 
                (evol_cursos_cat_uf['NO_UF']==UF_selected)].reset_index()
        axes = sns.pointplot(x='NU_ANO_CENSO', y='Total_cursos', 
                    data=data1.sort_values(by=('NU_ANO_CENSO'), ascending=False),
                    label="Privada com fins lucrativos", markers='o', color='green')
        for i in range(len(data1)):
                 plt.text(i, data1['Total_cursos'][i]*1.02,
                          data1['Total_cursos'][i], color='green', fontsize=12)

        data2 = evol_cursos_cat_uf[
                    (evol_cursos_cat_uf['Tipo_Cat_Admn']=='Privada sem fins lucrativos') & 
                    (evol_cursos_cat_uf['NO_UF']==UF_selected)].reset_index()
        axes = sns.pointplot(x='NU_ANO_CENSO', y='Total_cursos',  
                    data=data2.sort_values(by=('NU_ANO_CENSO'), ascending=False),
                    label="Privada sem fins lucrativos", markers='o', color='b')
        for i in range(len(data2)):
                 plt.text(i, data2['Total_cursos'][i]*1.02,
                          data2['Total_cursos'][i], color='b', fontsize=12)

        data3 = evol_cursos_cat_uf[
                    (evol_cursos_cat_uf['Tipo_Cat_Admn']=='Pública Federal') &
                    (evol_cursos_cat_uf['NO_UF']==UF_selected)
                    ].reset_index()
        axes = sns.pointplot(x='NU_ANO_CENSO', y='Total_cursos',  
                    data=data3.sort_values(by=('NU_ANO_CENSO'), ascending=False),
                    label="Pública Federal", markers='o', color='orange')
        for i in range(len(data3)):
                 plt.text(i, data3['Total_cursos'][i]*1.02,
                          data3['Total_cursos'][i], color='orange', fontsize=12)

        axes.set_xticklabels(axes.get_xticklabels(), rotation=0, ha="right", fontsize=16)
        axes.set(xlabel=''); axes.set_ylabel('Total Cursos', fontsize=18)
        axes.tick_params(axis='y', labelsize=14)

        axes.grid(color='gray', linestyle='--', linewidth=1.2, axis='y', alpha=.2)

        axes.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=2,
                   fontsize='x-large')
                   
        st.pyplot(f)
        plt.close()
        
    # ------------------------------------------------------------------------
    # Plot02: Análise
    # ------------------------------------------------------------------------
    st.subheader("Análise:")
    st.write("Em cada UF percebe-se comportamentos distintos na oferta de cursos das diferentes redes das Instituições de Ensino Superior, não sendo possível generalizar para todos os Estados. Nos estados de Santa Catarina e Rio Grande do Sul, por exemplo, há predominância de oferta de cursos  das entidades privadas sem fins lucrativos, diferente do que foi percebido ao verificar-se as curvas para todo o país.")
    st.markdown("---")
    
    
    # ------------------------------------------------------------------------
    # Plot03: Evolução da Qtd de Cursos ofertados/ Categoria (barra)
    # Brasil e UFs
    # ------------------------------------------------------------------------	   
    titulo_plot03 =  '<p style="font-family:Courier; color:Blue; font-size: 20px;"><b>Evolução da Quantidade de Cursos PRESENCIAIS por Categoria</b></p>'
    st.markdown(titulo_plot03, unsafe_allow_html=True)
    
    # ------------------------------------------------------------------------
    # Prepara pagina para 2 colunas
    # ------------------------------------------------------------------------
    col1, col2 = st.columns(2)

    # ------------------------------------------------------------------------
    # Brasil
    # ------------------------------------------------------------------------	
    with col1:
        titulo_plot02 =  '<p style="font-family:Courier; color:#992600; font-size: 16px;text-align:center"><b>Brasil</b></p>'
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
        fig.update_layout(yaxis=dict(title='', titlefont_size=18, tickfont_size=16),
                      xaxis=dict(title='', titlefont_size=18, tickfont_size=14),  
                      legend=dict(x=0.1,y=-0.30, font = dict(size = 18))) 
        fig.update_layout(hoverlabel=dict(bgcolor="white", 
                                      font_size=16,
                                      font_family="Rockwell"))				  
        #fig.update_xaxes(tickangle=0)
        fig.update_traces(textposition='inside', insidetextfont=dict(color='white', size=16,family='Times New Roman'))
        st.plotly_chart(fig, use_container_width=True)
        plt.close()
        
    # ------------------------------------------------------------------------
    # Escolher UF
    # ------------------------------------------------------------------------	
    with col2:    
        # titulo
        #titulo_plot02 =  '<p style="font-family:Courier; color:Black; font-size: 20px;text-align:center"><b>Para uma UF específica</b></p>'
        #st.markdown(titulo_plot02, unsafe_allow_html=True)
        
        # prepara dados 
        evol_cursos_cat_uf = df_all.groupby(['NU_ANO_CENSO','NO_UF', 'Tipo_Cat_Admn'])['NO_CURSO'].count().reset_index()
        evol_cursos_cat_uf = evol_cursos_cat_uf.rename(columns={'NO_CURSO':'Total_cursos'})
        
        # prepara lista de opções de UFs
        # l_UF = list(evol_cursos_cat_uf['NO_UF'].unique()) # ja tem
        col1, col2, col3 = st.columns(3)
        with col1:
            label01 = '<p style="font-family:Courier; color:#992600; font-size: 16px;"><b>Selecione uma UF:</b></p>'
            st.markdown(label01, unsafe_allow_html=True) 
        with col2:
            UF_selected = st.selectbox(label="Selecione uma UF2:", options=l_UF, label_visibility="collapsed")
        with col3:    
            st.subheader(':classical_building:')
        
        if UF_selected:
            data = evol_cursos_cat_uf[evol_cursos_cat_uf['NO_UF']==UF_selected]
            fig = px.bar(data,
                         y='Total_cursos', 
                         x='NU_ANO_CENSO', 
                         color='Tipo_Cat_Admn',
                         color_discrete_sequence=px.colors.qualitative.G10,
                         barmode = 'stack', width=800, height=900,
                         labels=dict(Tipo_Cat_Admn = 'Categoria'),
                         text='Total_cursos')
            fig.update_layout(yaxis=dict(title='', titlefont_size=18, tickfont_size=16),
                              xaxis=dict(title='', titlefont_size=18, tickfont_size=14),  
                              legend=dict(x=0.1,y=-0.3, font = dict(size = 18))) 
            fig.update_xaxes(tickangle=0)
            fig.update_traces(textposition='inside', insidetextfont=dict(color='white', size=16,family='Times New Roman'))
            st.plotly_chart(fig, use_container_width=True)
            plt.close()

    # ------------------------------------------------------------------------
    # Plot03: Análise
    # ------------------------------------------------------------------------
    st.subheader("Análise:")
    st.write("Na visão consolidada (todos os cursos no país), observa-se que a maioria dos cursos é ofertada por entidades privadas (com e sem fins lucrativos, respectivamente). Entretanto, a realidade pode ser diferente em alguns estados, como no Acre e Amapá (maioria dos cursos são de entidades públicas) e no Rio Grande do Sul e Santa Catarina (maioria dos cursos são de entidades privadas sem fins lucrativos). Pode-se, desta forma, visualizar outros Estados e compará-los com o país.")
    st.markdown("---")
            

    # ------------------------------------------------------------------------
    # Plot04: Evolução da Qtd de Cursos ofertados/ Organizacao Academica (barra)
    # Brasil e UFs
    # ------------------------------------------------------------------------	   
    titulo_plot04 =  '<p style="font-family:Courier; color:Blue; font-size: 20px;"><b>Evolução da Quantidade de Cursos PRESENCIAIS por Org. Acadêmica</b></p>'
    st.markdown(titulo_plot04, unsafe_allow_html=True)
    
    # ------------------------------------------------------------------------
    # Prepara pagina para 2 colunas
    # ------------------------------------------------------------------------
    col1, col2 = st.columns(2)

    # ------------------------------------------------------------------------
    # Brasil
    # ------------------------------------------------------------------------	
    with col1:
        titulo_plot03 =  '<p style="font-family:Courier; color:#992600; font-size: 16px;text-align:center"><b>Brasil</b></p>'
        st.markdown(titulo_plot03, unsafe_allow_html=True)
        fig = px.bar(evol_cursos_org,
                 y='Total_cursos', 
                 x='NU_ANO_CENSO', 
                 color='Tipo_Org_Acad',
                 color_discrete_sequence=px.colors.qualitative.G10,
                 barmode = 'stack', width=800, height=900,
                 labels=dict(Tipo_Org_Acad = 'Organização'),
                 text='Total_cursos')
        fig.update_layout(yaxis=dict(title='', titlefont_size=18, tickfont_size=16),
                      xaxis=dict(title='', titlefont_size=18, tickfont_size=14),  
                      legend=dict(x=0.1,y=-0.30, font = dict(size = 18))) 
        fig.update_layout(hoverlabel=dict(bgcolor="white", 
                                      font_size=16,
                                      font_family="Rockwell"))				  
        #fig.update_xaxes(tickangle=0)
        fig.update_traces(textposition='inside', insidetextfont=dict(color='white', size=16,family='Times New Roman'))
        st.plotly_chart(fig, use_container_width=True)
        plt.close()
        
    # ------------------------------------------------------------------------
    # Escolher UF
    # ------------------------------------------------------------------------	
    with col2:    
        # prepara dados 
        evol_cursos_org_uf = df_all.groupby(['NU_ANO_CENSO','NO_UF', 'Tipo_Org_Acad'])['NO_CURSO'].count().reset_index()
        evol_cursos_org_uf = evol_cursos_org_uf.rename(columns={'NO_CURSO':'Total_cursos'})
        
        # prepara lista de opções de UFs
        l_UF = list(evol_cursos_org_uf['NO_UF'].unique()) 
        col1, col2, col3 = st.columns(3)
        with col1:
            label01 = '<p style="font-family:Courier; color:#992600; font-size: 16px;"><b>Selecione uma UF:</b></p>'
            st.markdown(label01, unsafe_allow_html=True) 
        with col2:
            UF_selected = st.selectbox(label="Selecione uma UF3:", options=l_UF, label_visibility="collapsed")
        with col3:    
            st.subheader(':classical_building:')
        
        if UF_selected:
            data = evol_cursos_org_uf[evol_cursos_org_uf['NO_UF']==UF_selected]
            fig = px.bar(data,
                         y='Total_cursos', 
                         x='NU_ANO_CENSO', 
                         color='Tipo_Org_Acad',
                         color_discrete_sequence=px.colors.qualitative.G10,
                         barmode = 'stack', width=800, height=900,
                         labels=dict(Tipo_Org_Acad = 'Organização'),
                         text='Total_cursos')
            fig.update_layout(yaxis=dict(title='', titlefont_size=18, tickfont_size=16),
                              xaxis=dict(title='', titlefont_size=18, tickfont_size=14),  
                              legend=dict(x=0.1,y=-0.3, font = dict(size = 18))) 
            fig.update_xaxes(tickangle=0)
            fig.update_traces(textposition='inside', insidetextfont=dict(color='white', size=16,family='Times New Roman'))
            st.plotly_chart(fig, use_container_width=True)
            plt.close()            
            
            
    # ------------------------------------------------------------------------
    # Plot04: Análise
    # ------------------------------------------------------------------------
    st.subheader("Análise:")
    st.write("Na visão consolidada (todos os cursos no país), observa-se que a maioria dos cursos é ofertada por Faculdades e Universidades. Os Institutos Federais apresentam um número bem menor de ofertas em comparação com as outras organizações. Mais uma vez, há Estados que apresentam configurações diferentes, como Amazonas, que possui Centros Universitários como a organização predominante.")
    st.markdown("---")
                        
    
    # ------------------------------------------------------------------------
    # Plot05: Evolução da Qtd de Cursos ofertados/ Grau Academico (linha) 
    # Brasil e UF
    # ------------------------------------------------------------------------	
    titulo_plot05 =  '<p style="font-family:Courier; color:Blue; font-size: 20px;"><b>Evolução da Quantidade de Cursos PRESENCIAIS por Grau Academico</b></p>'
    st.markdown(titulo_plot05, unsafe_allow_html=True)
    
    # ------------------------------------------------------------------------
    # Prepara pagina para 2 colunas
    # ------------------------------------------------------------------------
    col1, col2 = st.columns(2)

    # ------------------------------------------------------------------------
    # Brasil
    # ------------------------------------------------------------------------	
    with col1:
        titulo_plot03 =  '<p style="font-family:Courier; color:#992600; font-size: 16px;text-align:center"><b>Brasil</b></p>'
        st.markdown(titulo_plot03, unsafe_allow_html=True)
        fig = px.bar(evol_cursos_grau,
                         y='Total_cursos', 
                         x='NU_ANO_CENSO', 
                         color='Tipo_Grau_Acad',
                         color_discrete_sequence=px.colors.qualitative.G10,
                         barmode = 'stack', width=800, height=900,
                         labels=dict(Tipo_Grau_Acad = 'Grau Academico'),
                         text='Total_cursos')
        fig.update_layout(yaxis=dict(title='', titlefont_size=18, tickfont_size=16),
                              xaxis=dict(title='', titlefont_size=18, tickfont_size=14),  
                              legend=dict(x=0.1,y=-0.30, font = dict(size = 18))) 
        fig.update_layout(hoverlabel=dict(bgcolor="white", 
                                              font_size=16,
                                              font_family="Rockwell"))				  
        fig.update_xaxes(tickangle=0)
        fig.update_traces(textposition='inside', insidetextfont=dict(color='white', size=16,family='Times New Roman'))
        st.plotly_chart(fig, use_container_width=True)
        plt.close()
        
        
    # ------------------------------------------------------------------------
    # Escolher UF
    # ------------------------------------------------------------------------	
    with col2:
        
        # prepara dados 
        evol_cursos_grau_uf = df_all.groupby(['NU_ANO_CENSO','NO_UF', 'Tipo_Grau_Acad'])['NO_CURSO'].count().reset_index()
        evol_cursos_grau_uf = evol_cursos_grau_uf.rename(columns={'NO_CURSO':'Total_cursos'})
        
        # prepara lista de opções de UFs
        l_UF = list(evol_cursos_grau_uf['NO_UF'].unique()) 
        col1, col2, col3 = st.columns(3)
        with col1:
            label01 = '<p style="font-family:Courier; color:#992600; font-size: 16px;"><b>Selecione uma UF:</b></p>'
            st.markdown(label01, unsafe_allow_html=True) 
        with col2:
            UF_selected = st.selectbox(label="Selecione uma UF4:", options=l_UF, label_visibility="collapsed")
        with col3:    
            st.subheader(':classical_building:')
        
        if UF_selected:
            data = evol_cursos_grau_uf[evol_cursos_grau_uf['NO_UF']==UF_selected]
            fig = px.bar(data,
                         y='Total_cursos', 
                         x='NU_ANO_CENSO', 
                         color='Tipo_Grau_Acad',
                         color_discrete_sequence=px.colors.qualitative.G10,
                         barmode = 'stack', width=800, height=900,
                         labels=dict(Tipo_Grau_Acad = 'Grau Acadêmico'),
                         text='Total_cursos')
            fig.update_layout(yaxis=dict(title='', titlefont_size=18, tickfont_size=16),
                              xaxis=dict(title='', titlefont_size=18, tickfont_size=14),  
                              legend=dict(x=0.1,y=-0.3, font = dict(size = 18))) 
            fig.update_xaxes(tickangle=0)
            fig.update_traces(textposition='inside', insidetextfont=dict(color='white', size=16,family='Times New Roman'))
            st.plotly_chart(fig, use_container_width=True)
            plt.close()        

    # ------------------------------------------------------------------------
    # Plot05: Análise
    # ------------------------------------------------------------------------
    st.subheader("Análise:")
    st.write("Na visão consolidada (todos os cursos no país), observa-se que a maioria dos cursos é de Bacharelado, com tendência de crescimento ao longo dos anos. Por outro lado, os cursos de Licenciatura estão em queda. Este padrão se repete na maioria dos estados. Algumas exceções são o estado do CE e GO, no qual há aumento do número de cursos de Licenciatura")
    st.markdown("---")            

    
# ------------------------------------------------------------------------
# Tab 02
# Plot01: Evolução da Qtd de Cursos ofertados/ Area Geral (linha) - Brasil 
# Plot02: Evolução da Qtd de Cursos ofertados/ Area Geral (linha) - UF
# ------------------------------------------------------------------------	
with t_evol_area:


    # Plot01: Evolução da Qtd de Cursos ofertados/ Area Geral - Brasil
    # -----------------------------------------------------------------------
    titulo_plot01 =  '<p style="font-family:Courier; color:Blue; font-size: 20px;"><b>Evolução da Quantidade de Cursos PRESENCIAIS por Area Geral</b></p>'
    st.markdown(titulo_plot01, unsafe_allow_html=True)

    ano_min = evol_cursos_area['NU_ANO_CENSO'].min()
    ano_max = evol_cursos_area['NU_ANO_CENSO'].max()

    # necessidade de criar paleta de cores
    palette_11cores = ["#F72585", "#7209B7", "#3A0CA3", "#4361EE", "#4CC9F0", #rosa escuro, roxo, roxo escuro, azul escuro, azul agua
                       '#00cc00', # verde claro
                       '#00661a', # verde escuro
                       '#ffbf00',  # laranja
                       '#cc0000', # vermelho
                       '#66001a', # vermelho vinho
                       '#ffff66'] # amarelo
                       
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
    plt.close()
        
    
    # ------------------------------------------------------------------------
    # Plot01: Análise
    # ------------------------------------------------------------------------
    st.subheader("Análise:")
    st.write("Considerando-se a área geral do cursos, pode-se afirmar que a quantidade de cursos em algumas áreas tem se mantido relativamente constante (como as áreas de Agricultura, Ciências Naturais e Serviços).")
    st.write("A área de Saúde apresenta um aumento de cursos desde 2012, de forma a passar as áreas tradicionais de Engenharia e Educação.")
    st.write("Interessante notar que as áreas de Negócios, Administração, Direito, Engenharia e Educação passaram a reduzir a oferta de cursos desde 2019, ao mesmo tempo em que houve aumento de oferta de cursos na área de Saúde.")
    st.markdown("---")  
    
    
    # Plot02: Evolução da Qtd de Cursos ofertados/ Area Geral - UF
    # -----------------------------------------------------------------------
    titulo_plot02 =  '<p style="font-family:Courier; color:Blue; font-size: 20px;"><b>Evolução da Quantidade de Cursos PRESENCIAIS por Area Geral - Para uma UF específica</b></p>'
    st.markdown(titulo_plot02, unsafe_allow_html=True)
    
    # prepara dados
    evol_cursos_area_uf = df_all.groupby(['NU_ANO_CENSO','NO_UF', 'NO_CINE_AREA_GERAL'])['NO_CURSO'].count().reset_index()
    evol_cursos_area_uf = evol_cursos_area_uf.rename(columns={'NO_CURSO':'Total_cursos'})
    evol_cursos_area_uf = evol_cursos_area_uf[evol_cursos_area_uf['NO_CINE_AREA_GERAL']!='Programas básicos']
    # usar a mesma paleta de cores
    
    # prepara lista de opções de UFs
    l_UF = list(evol_cursos_area_uf['NO_UF'].unique())
    col1, col2, col3 = st.columns(3)
    with col1:
        label01 = '<p style="font-family:Courier; color:#992600; font-size: 16px;"><b>Selecione uma UF:</b></p>'
        st.markdown(label01, unsafe_allow_html=True) 
    with col2:
        UF_selected = st.selectbox(label="Selecione uma UF5:", options=l_UF, label_visibility="collapsed")
    with col3:    
        st.subheader(':classical_building:')

    if UF_selected:
        ano_min = evol_cursos_area_uf['NU_ANO_CENSO'].min()
        ano_max = evol_cursos_area_uf['NU_ANO_CENSO'].max()
        f, axes = plt.subplots(1, 1,  figsize=(22,8))    
        axes = sns.pointplot(x='NU_ANO_CENSO', y='Total_cursos', hue='NO_CINE_AREA_GERAL',
                data=evol_cursos_area_uf[evol_cursos_area_uf['NO_UF']==UF_selected].sort_values(by=('NU_ANO_CENSO'), ascending=False),
                label="Total Cursos", markers='o', palette=palette_11cores)
        axes.set_title("Evolução do Total de Cursos PRESENCIAIS por Ano", fontsize=20)
        axes.set_xticklabels(axes.get_xticklabels(), rotation=0, ha="right", fontsize=16)
        axes.set(xlabel=''); axes.set_ylabel('Total Cursos', fontsize=18)
        axes.tick_params(axis='y', labelsize=14)
        axes.grid(color='gray', linestyle='--', linewidth=1.2, axis='y', alpha=.2)
        #axes.legend(loc='best', fontsize=18)
        axes.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=2,
                   fontsize='x-large')
        st.pyplot(f)
        plt.close()
        st.markdown("---")
    
        
    
# ------------------------------------------------------------------------
# Tab 03
# Evolução da Oferta de Curso X Matriculas
# ------------------------------------------------------------------------    

    
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
# TreeMap de Cursos e Matriculas
# ------------------------------------------------------------------------    
with t_evol_matr:
    titulo_plot06 =  '<p style="font-family:Courier; color:Blue; font-size: 20px;"><b>Comparativo da Oferta de Cursos e Quantidade de Matriculas</b></p>'
    st.markdown(titulo_plot06, unsafe_allow_html=True)
    
    l_anos = range(2012,2023,1)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        label01 = '<p style="font-family:Courier; color:#992600; font-size: 16px;"><b>Selecione um ano específico:</b></p>'
        st.markdown(label01, unsafe_allow_html=True) 
        
    with col2:
        ano_selecionado = st.selectbox(label="Selecione um ano específico:", options=l_anos, label_visibility="collapsed")
        
    with col3:    
        st.subheader(':date:')


    if ano_selecionado:
        titulo_plot01 =  f'<p style="font-family:Courier; color:Blue; font-size: 16px;"><b>Treemap de Cursos e Matriculas para o ano de {ano_selecionado}</b></p>'
        st.markdown(titulo_plot01, unsafe_allow_html=True)
        
        fig = px.treemap(distr_cursos[distr_cursos['NU_ANO_CENSO']==ano_selecionado], 
        path = [px.Constant('Area Geral'), 'AREA_GERAL'], 
        values = 'QT_CURSO', color_continuous_scale='RdBu', color = 'QT_MAT', width=400, height=500)
        
        fig.update_layout(margin = dict(t=20, l=25, r=25, b=25))
        fig.update_traces(textposition='middle left', textfont_size=18)
        fig.update_traces(textposition='middle left', textfont_size=18)
        
        st.plotly_chart(fig, use_container_width=True)
        plt.close()
        
        
    # Análise
    # ------------------
    st.subheader("Análise:")
    st.write("A oferta de cursos é resultado das tendências no mercado de trabalho e, desta forma, exercem influência sobre as preferências acadêmicas nas universidades (quantidade de matrículas.")

    st.write("Há uma notável mudança nos cursos mais procurados ao longo dos anos. Nos anos de 2012 a 2020, cursos na área de 'Negócios, Administração e Direito' são os de maior oferta de cursos e também os de maior quantidade de matrículas. Contudo, ao chegarmos em 2021-2022, percebe-se uma transição marcante: a área de 'Saúde e Bem-Estar' passa a ser a área de maior destaque nas matrículas realizadas.")

    st.markdown('---')    
    

# ------------------------------------------------------------------------				  
# Tab 04
# Situação atual: 2022
# ------------------------------------------------------------------------   

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

# ------------------------------------------------------------------------
# Prepara mapa com Total Cursos presenciais por UF
# info geograficas - Ufs 
# ------------------------------------------------------------------------
url = "https://raw.githubusercontent.com/jonates/opendata/master/arquivos_geoespaciais/unidades_da_federacao.json"
response = requests.get(url).json()
geojson_data = response

# Total Cursos presenciais por UF
total_cursos = cursos['CO_CURSO'].count()
qtd_cursos_uf = cursos.groupby(['NO_REGIAO', 'CO_REGIAO', 'NO_UF', 'SG_UF'])['CO_CURSO'].nunique().reset_index()
qtd_cursos_uf = qtd_cursos_uf.rename(columns={'CO_CURSO':'Tot_cursos'})
qtd_cursos_uf['NO_UF_M'] = qtd_cursos_uf['NO_UF'].str.upper()
qtd_cursos_uf['Tot_cursos_p'] = round((qtd_cursos_uf['Tot_cursos'] / total_cursos * 100),1)

# com info de populacao do EStado para o mapa (hab/ curso)
qtd_cursos_uf_pop = pd.merge(
    qtd_cursos_uf,
    ies_agg_UF,
    left_on = ['SG_UF'],
    right_on = ['SG_UF_IES'],
    how='inner',
    indicator=True)
qtd_cursos_uf_pop['Hab_Cursos'] = qtd_cursos_uf_pop['Total_Pop_UF'] / qtd_cursos_uf_pop['Tot_cursos'] 
    
    
# ------------------------------------------------------------------------
# Tab 04: Plots
# ------------------------------------------------------------------------                               

with t_sit_br:

    # mapas em colunas
    col1, col2  = st.columns(2)
    
    with col1:
        titulo_secao01 =  '<p style="text-align: center; font-family:Courier; color:Blue; font-size: 16px;"><b>Distribuição do Total de Cursos presenciais - Brasil</b></p>'
        st.markdown(titulo_secao01, unsafe_allow_html=True)
        
        mapa = px.choropleth_mapbox(qtd_cursos_uf,       
                                    geojson=geojson_data,
                                    locations='NO_UF_M',        
                                    color='Tot_cursos',
                                    color_continuous_scale="viridis_r",
                                    range_color=(0, max(qtd_cursos_uf['Tot_cursos'])),
                                    mapbox_style="open-street-map",
                                    zoom=3, 
                                    center={"lat": -15, "lon": -57.33},
                                    opacity=1,
                                    labels={'NO_UF_M': 'Estado', 
                                            'Tot_cursos':'Total cursos',
                                            'Tot_cursos_p':'Percentual de cursos'},
                                    hover_data={'NO_UF_M', 'Tot_cursos','Tot_cursos_p'},
                                    featureidkey="properties.NM_ESTADO")
        mapa.update_layout(coloraxis_colorbar=dict(len=1, x=0.5, y=-0.15, yanchor='bottom', xanchor='center', orientation='h',  
        title="Quantidade Cursos", titleside = "bottom"),
        margin=dict(t=0, b=0, l=0, r=0))
        mapa.update_layout(width=1000, height=700)
        st.plotly_chart(mapa, use_container_width=True)
        plt.close()
        
    with col2:
        titulo_secao01 =  '<p style="text-align: center; font-family:Courier; color:Blue; font-size: 16px;"><b>Distribuição Razão Habitantes por Total Cursos presenciais - Brasil</b></p>'
        st.markdown(titulo_secao01, unsafe_allow_html=True)
    
        mapa2 = px.choropleth_mapbox(qtd_cursos_uf_pop,         
                                    geojson=geojson_data,      
                                    locations='NO_UF_M',        
                                    color='Hab_Cursos',
                                    color_continuous_scale="viridis_r",
                                    range_color=(0, max(qtd_cursos_uf_pop['Hab_Cursos'])),
                                    mapbox_style="open-street-map",
                                    zoom=3, 
                                    center={"lat": -15, "lon": -57.33},
                                    opacity=1,
                                    labels={'NO_UF_M': 'Estado', 
                                    'Hab_Cursos':'Razão Pop/ Qtd Cursos',
                                    'Tot_cursos':'Total cursos',
                                    'Tot_cursos_p':'Percentual de cursos'},
                                     hover_data={'NO_UF_M', 'Tot_cursos','Tot_cursos_p', 'Hab_Cursos'},
                                     featureidkey="properties.NM_ESTADO")
        mapa2.update_layout(coloraxis_colorbar=dict(len=1, x=0.5, y=-0.15, yanchor='bottom', xanchor='center', orientation='h',  
                    title="Razão População/ Qtd Cursos", titleside = "bottom"),
                    margin=dict(t=0, b=0, l=0, r=0))
        mapa2.update_layout(width=1000, height=700)    
        st.plotly_chart(mapa2, use_container_width=True)
        plt.close()
    
    # Análise
    # ------------------------------------------------------------------------
    st.subheader("Análise:")
    st.write("O mapa à esquerda acima representa a distribuição dos cursos presenciais por UF. São Paulo é o estado que concentra a maior oferta de cursos superiores presenciais (quase 23% do total), seguido pelos estados de Minas Gerais (11%), Rio Grande do Sul (7,4%), Rio de Janeiro (7,2%) e Paraná (6,6%).")
    st.write("O mapa à direita acima representa a razão da quantidade ds cursos em relação à população do estado. Desta forma, pode-se perceber que, apesar da evidente maior concentração dos cursos nas regiões Sudeste e Sul, a demanda por cursos é maior nas regiões Norte e Nordeste.")
    st.markdown('---')
    

    titulo_secao01 =  '<p style="font-family:Courier; color:Blue; font-size: 20px;"><b>Top 10 cursos mais oferecidos no Brasil</b></p>'
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
        plt.close()
            
        
    # Análise
    # ------------------------------------------------------------------------
    st.subheader("Análise:")
    st.write("O total de cursos presenciais ofertados pelas IES no Brasil em 2022 foi de 31.309. Ao se analisar os 10 cursos mais frequentes, identificou-se um total de 11.717 cursos ofertados - com destaque para os cursos da Área Geral de Negócios, Administração e Direito (inclui cursos de Administração, Direito e Ciências Contábeis). Em seguida, estão em destaque também os cursos da área de saúde e bem-estar, como Educação Física, Enfermagem e Fisioterapia.")
    st.markdown('---')

# ------------------------------------------------------------------------
# Tab 05
# Plots por Regiao  
# ------------------------------------------------------------------------

with t_sit_reg:

    # ------------------------------------------------------------------------
    # Plot 06: Total de Cursos Presenciais por Regiao e Area Geral
    # ------------------------------------------------------------------------	
    titulo_plot06 =  '<p style="font-family:Courier; color:Blue; font-size: 20px;"><b>Distribuição da Qtd de Cursos Presenciais por Região e Area Geral </b></p>'
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
        plt.close()

    with col2: 
        titulo_plot06b =  '<p style="text-align: center; font-family:Courier; color:Blue; font-size: 20px;"><b>Regiao Norte</b></p>'
        st.markdown(titulo_plot06b, unsafe_allow_html=True)
        st.plotly_chart(fig_N, use_container_width=True)
        plt.close()

    col1, col2 = st.columns(2)
    with col1: 
        titulo_plot06c =  '<p style="text-align: center; font-family:Courier; color:Blue; font-size: 20px;"><b>Regiao Sul</b></p>'
        st.markdown(titulo_plot06c, unsafe_allow_html=True)
        st.plotly_chart(fig_S, use_container_width=True)
        plt.close()

    with col2: 
        titulo_plot06d =  '<p style="text-align: center; font-family:Courier; color:Blue; font-size: 20px;"><b>Regiao Centro-Oeste</b></p>'
        st.markdown(titulo_plot06d, unsafe_allow_html=True)
        st.plotly_chart(fig_CO, use_container_width=True)
        plt.close()

    titulo_plot06e =  '<p style="text-align: center; font-family:Courier; color:Blue; font-size: 20px;"><b>Regiao Sudeste</b></p>'
    st.markdown(titulo_plot06e, unsafe_allow_html=True)
    st.plotly_chart(fig_SE, use_container_width=True)
    plt.close()

    # ------------------------------------------------------------------------
    # Plot07: Análise
    # ------------------------------------------------------------------------
    st.subheader("Análise:")
    st.write("A distribuição da oferta de cursos por área em cada região evidenciou as áreas mais prevalentes: 'Negócios, Administração e Direito' e 'Saúde e bem-estar'. Em números absolutos, a região Sudeste destaca-se com uma grande concentração de cursos ofertados, principalmente nos estados de São Paulo, Minas Gerais e Rio de Janeiro (conforme aba 'Situação Atual - UF'.")

    st.write("Observa-se uma tendência consistente em quase todas as regiões: os cursos menos ofertados estão na área de 'Ciências Naturais, Matemática e Estatística' (exceto Região Norte).")
    
    st.markdown('---')

# ------------------------------------------------------------------------
# Tab 06
# Plots por UF  
# ------------------------------------------------------------------------
    
    
with t_sit_uf:    

    # ------------------------------------------------------------------------
    # Plot02: Top 5 cursos mais oferecidos em cada UF
    # ------------------------------------------------------------------------						
    titulo_plot02 =  '<p style="font-family:Courier; color:Blue; font-size: 20px;"><b>Top 5 cursos presenciais mais oferecidos em cada UF</b></p>'
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
    plt.close()

    # ------------------------------------------------------------------------
    # Plot02: Análise
    # ------------------------------------------------------------------------

    st.subheader("Análise:")
    st.write("A análise dos TOP 5 cursos mais ofertados em cada UF permitiu identificar os principais 10 diferentes cursos distribuídos entre os estados.") 
    st.write("Assim como na avaliação por estados, os cursos de Administração e Direito estão presentes nos TOP 5 de todas as regiões, associados agora também à presença do curso de Pedagogia.") 
    st.write("Os cursos de Educação Física só não estão presente no TOP 5 da região Norte e os de Ciências Contábeis no Nordeste. A Enfermagem, por sua vez, aparece no TOP 5 apenas nas regiões Norte e Nordeste, em substiuição aos outros dois cursos.")
    st.markdown('---')

    # ------------------------------------------------------------------------
    # Plot03: Total de Cursos Presenciais por UF/ Tipo Rede
    # ------------------------------------------------------------------------		
    titulo_plot03 =  '<p style="font-family:Courier; color:Blue; font-size: 25px;"><b>Distribuição da Qtd de Cursos Presenciais por UF e Rede</b></p>'
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
    plt.close()
    st.markdown("---")


    # ------------------------------------------------------------------------
    # Plot04: Total de Cursos Presenciais por UF/ Org Acadêmica 
    # ------------------------------------------------------------------------		

    titulo_plot04 =  '<p style="font-family:Courier; color:Blue; font-size: 25px;"><b>Distribuição da Qtd de Cursos Presenciais por UF e Org. Acadêmica</b></p>'
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
    plt.close()
    st.markdown("---")

    # ------------------------------------------------------------------------
    # Plot 05: Total de Cursos Presenciais por UF/Grau Academico
    # ------------------------------------------------------------------------		

    titulo_plot05 =  '<p style="font-family:Courier; color:Blue; font-size: 25px;"><b>Distribuição da Qtd de Cursos Presenciais por UF e Grau Academico</b></p>'
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
    plt.close()

    # ------------------------------------------------------------------------
    # Plot05: Análise
    # ------------------------------------------------------------------------
    st.subheader("Análise:")
    st.write("A distribuição da quantidade de cursos presenciais por estado e tipo de instituição revela alguns padrões. Como podemos observar, São Paulo se destaca como o estado com o maior número de instituições privadas de ensino em todo o Brasil. Enquanto isso, Minas Gerais lidera na quantidade de entidades públicas e de institutos federais.")

    st.write("Outro ponto notável é a preferência dos paulistas por cursos de bacharelado e tecnólogos, sugerindo uma inclinação específica nas escolhas educacionais dessa população.")
    st.markdown("---")

