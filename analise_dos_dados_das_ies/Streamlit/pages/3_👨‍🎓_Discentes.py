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


st.set_page_config(page_title='Analise Discentes', 
                    page_icon=':student:', 
				    layout='wide', 
                    initial_sidebar_state='expanded')

                    
st.title(':bar_chart: Análise dos Discentes das IES :male-student: :female-student: ')
st.subheader('Escopo: Matrículas, Ingressantes e Concluintes PRESENCIAIS')
st.subheader("Dados de 2012-2022")
st.markdown("---")  


# ------------------------------------------------------------------------
# Funcoes
# ------------------------------------------------------------------------

@st.cache_data
# carregar algumas colunas pois a carga do df é demorado
# dados_cursos_2012_2022.csv alterado para dados_cursos_2012_2022_reduzida01.csv
                                               
def carrega_cursos_2012_2022():
	df_all = pd.read_csv('./arquivos/dados_cursos_2012_2022_reduzida01.csv', sep='|', 
						low_memory=False, 
						usecols=['NU_ANO_CENSO','SG_UF','CO_IES',
                        'Tipo_Cat_Admn','Tipo_Org_Acad','Tipo_Org_Principal', 'Tipo_Grau_Acad','Tipo_Rede',
						'NO_CINE_AREA_GERAL', 'NO_CURSO','QT_CURSO','QT_MAT',
                        'QT_ING','QT_ING_FEM','QT_ING_MASC',
                        'QT_CONC','TIPO_INST',
                        'QT_VG_TOTAL', 'QT_VG_TOTAL_DIURNO', 'QT_VG_TOTAL_NOTURNO', 
                        'QT_INSCRITO_TOTAL', 
                        'QT_MAT_0_17', 'QT_MAT_18_24', 'QT_MAT_25_29', 'QT_MAT_30_34',
                        'QT_MAT_35_39', 'QT_MAT_40_49', 'QT_MAT_50_59', 'QT_MAT_60_MAIS',
                        'QT_ING_0_17', 'QT_ING_18_24', 'QT_ING_25_29', 'QT_ING_30_34','QT_ING_35_39', 'QT_ING_40_49', 'QT_ING_50_59', 'QT_ING_60_MAIS',
                        'QT_CONC_0_17', 'QT_CONC_18_24', 'QT_CONC_25_29', 'QT_CONC_30_34','QT_CONC_35_39', 'QT_CONC_40_49', 'QT_CONC_50_59', 'QT_CONC_60_MAIS'
                        ])
	return df_all

@st.cache_data	
def carrega_disc_ano_uf_area():
    disc_ano_uf_area = pd.read_csv('./arquivos/dados_disc_ano_uf_area.csv', sep='|',
    low_memory=False)
    return disc_ano_uf_area

    
# Vagas e Ingressantes por Area Geral/ Sexo por Ano    
# tab 05
@st.cache_data	
def carrega_distr_vag_ingr_sexo():
    distr_vag_ingr_sexo = pd.read_csv('./arquivos/distr_vag_ingr_sexo.csv', sep='|',
    low_memory=False)
    return distr_vag_ingr_sexo
    
# Vagas e Ingressantes por Area Geral/ Sexo por Ano    
# tab 05
@st.cache_data	
def carrega_distr_vag_ingr_sexo_uf():
    distr_vag_ingr_sexo_uf = pd.read_csv('./arquivos/distr_vag_ingr_sexo_uf.csv', sep='|',
    low_memory=False)
    return distr_vag_ingr_sexo_uf    

# matriculas, ingressantes e concluintes     
@st.cache_data	
def gerar_plot_evol_ano(df, col_ano, col_grupo, col_soma, legenda_outside):
    # exibe primeiros registros do df
    #print('Exibindo alguns registros do df consolidado...\n')
    df_plot = df.groupby([col_ano, col_grupo])[col_soma].sum().reset_index().rename(columns={col_soma:'Total'})
    #display(df_plot.head(5))
    ano_min = df_plot[col_ano].min()
    ano_max = df_plot[col_ano].max()
    print(f'Soma da coluna {col_soma} nos anos de {ano_min} a {ano_max}: {df[col_soma].sum()}')
    f, axes = plt.subplots(1, 1,  figsize=(20,8))
    # controle dos valores do eixo Y 
    data = df_plot.copy()
    y_max = df_plot['Total'].max()
    if y_max >= 10000: 
        data['Total'] = data['Total']/1000
        limite_sup = y_max/1000 * 1.10
        intervalo = round((limite_sup/10)/100)*100
        if intervalo==0: intervalo = limite_sup/10
        text_y_axis = 'Total (x 1000)'
    else:  
        limite_sup = y_max * 1.10
        intervalo = limite_sup / 10
        text_y_axis = 'Total'
    sns.pointplot(x=col_ano, y='Total', hue=col_grupo, 
                data=data.sort_values(by=([col_ano,'Total']), ascending=[False,False]), ax=axes,
                 markers='o')
    #axes.set_title(f'Evolução {col_soma} - PRESENCIAL por Ano', fontsize=20)
    axes.set_xticklabels(axes.get_xticklabels(), rotation=0, ha="right", fontsize=16)
    axes.set(xlabel=''); axes.set_ylabel(text_y_axis, fontsize=18)
    major_yticks = np.arange(0, limite_sup, intervalo); 
    axes.set_yticks(major_yticks)
    axes.tick_params(axis='y', labelsize=14)
    axes.grid(color='gray', linestyle='--', linewidth=1.2, axis='both', alpha=.2)
    axes.legend(loc='best', fontsize=18)
    if legenda_outside == 'S':
        axes.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, 
                    ncol=2, fontsize='large')
    return f
    
    
    
# ------------------------------------------------------------------------
# Parametros plots seaborn
# ------------------------------------------------------------------------
sns.set(style="darkgrid")


# ------------------------------------------------------------------------
# Carrega dados 
# ------------------------------------------------------------------------
df_all = carrega_cursos_2012_2022()



url = "https://raw.githubusercontent.com/jonates/opendata/master/arquivos_geoespaciais/unidades_da_federacao.json"
response = requests.get(url).json()
geojson_data = response


# ------------------------------------------------------------------------				  
# Prepara dataframes
# ------------------------------------------------------------------------
serie_matr = df_all.groupby(['NU_ANO_CENSO', 'TIPO_INST'])['QT_MAT'].sum().reset_index().rename(columns={'QT_MAT':'Total_matriculas'})

# Evolução Discentes - Estados 
# Total e Perc Matr por Ano, UF, Rede de Ensino
tot_matr_uf = df_all.groupby(['NU_ANO_CENSO', 'SG_UF'])['QT_MAT'].sum()
tot_matr_uf_re = df_all.groupby(['NU_ANO_CENSO', 'SG_UF', 'TIPO_INST'])['QT_MAT'].sum()
perc_matr_uf_re = round((tot_matr_uf_re / tot_matr_uf*100),2)

distr_matr_uf_re = pd.DataFrame({'Total_Mat'  : tot_matr_uf_re,
                                 'Total_Mat_p': perc_matr_uf_re}).reset_index()

distr_matr_uf_re['Total_Mat_mil'] = distr_matr_uf_re['Total_Mat']/1000

# Total de ingressantes por Ano e por UF
tot_ing_uf = df_all.groupby(['NU_ANO_CENSO', 'SG_UF'])['QT_ING'].sum().reset_index().rename(columns={'QT_ING':'Total_Ingr'})
tot_ing_uf['Total_Ingr_mil'] = tot_ing_uf['Total_Ingr'] / 1000


#--------------------------------------------------------------------------------------------
# Prepara tabs
#------------------------------------------------------------------------------------------          
t_evol_mat, t_evol_ingr, t_evol_conc, t_faixas, t_vag_ing_sexo, t_mapas   = st.tabs([
                'Evolução Matriculas',
                'Evolução Ingressantes',      
                'Evolução Concluintes',      
                'Faixas Idade',
                'Vagas e Ingressantes',
                'Mapas de evolução', 
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
# Tab 01
# Brasil
# Plot01: Evolução da Qtd Matriculas por Ano/ Tipo Rede (linha)
# Plot02: Evolução da Qtd Matriculas por Ano/ Grau Academico (linha)
# Plot03: Evolução da Qtd Matriculas por Ano/ Area Curso (linha)
# Plot04:  Evolução da Qtd Matriculas por Ano/ Faixa Idade (linha)

# Estados
# Plot01: Total Matriculas e Ingressantes por Rede Ensino 
# ------------------------------------------------------------------------    
with t_evol_mat:

    # ------------------------------------------------------------------------				  
    # Brasil 
    # ------------------------------------------------------------------------
    st.subheader(':chart_with_upwards_trend: :adult: :books: Evolução Matrículas - Brasil :flag-br:')

    # ------------------------------------------------------------------------				  
    # Plot01: Evolução da Qtd Matriculas por Ano/ Tipo Rede (linha)
    # ------------------------------------------------------------------------
    titulo_plot01 =  '<p style="font-family:Courier; color:Blue; font-size: 20px;"><b>Evolução da Qtd de Matrículas por Rede de Ensino</b></p>'
    st.markdown(titulo_plot01, unsafe_allow_html=True)

    ano_min = serie_matr['NU_ANO_CENSO'].min()
    ano_max = serie_matr['NU_ANO_CENSO'].max()

    f, axes = plt.subplots(1, 1,  figsize=(20,8))

    data = serie_matr.copy()
    data['Total_matriculas'] = data['Total_matriculas']/1000

    axes = sns.pointplot(x='NU_ANO_CENSO', y='Total_matriculas', hue='TIPO_INST', 
                data=data.sort_values(by=(['NU_ANO_CENSO','Total_matriculas']), ascending=[False,False]), 
                 markers='o')

    axes.set_xticklabels(axes.get_xticklabels(), rotation=0, ha="right", fontsize=16)
    axes.set(xlabel=''); axes.set_ylabel('Total Matriculas (x 1000)', fontsize=18)

    limite_sup = serie_matr['Total_matriculas'].max()/1000 * 1.10
    intervalo = round((limite_sup/10)/100)*100
    major_yticks = np.arange(0, limite_sup, intervalo); 
    axes.set_yticks(major_yticks)
    axes.tick_params(axis='y', labelsize=14)

    axes.grid(color='gray', linestyle='--', linewidth=1.2, axis='both', alpha=.2)

    #axes.legend(loc='best', fontsize=18)
    axes.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=3,
               fontsize='x-large')

    st.pyplot(f)
    plt.close()
    st.markdown("---")

    # ------------------------------------------------------------------------				  
    # Plot02:  Evolução da Qtd Matriculas por Ano/ Grau Academico (linha)
    # ------------------------------------------------------------------------
    titulo_plot02 =  '<p style="font-family:Courier; color:Blue; font-size: 20px;"><b>Evolução da Qtd de Matrículas por Grau Academico</b></p>'
    st.markdown(titulo_plot02, unsafe_allow_html=True)

    col_ano = 'NU_ANO_CENSO'
    col_grupo = 'Tipo_Grau_Acad'
    col_soma = 'QT_MAT'
    legenda_outside = 'N'

    f = gerar_plot_evol_ano(df_all, col_ano, col_grupo, col_soma, legenda_outside)                                            
    st.pyplot(f)
    plt.close()
    st.markdown("---")

    # ------------------------------------------------------------------------				  
    # Plot03:  Evolução da Qtd Matriculas por Ano/ Area Curso (linha)
    # ------------------------------------------------------------------------
    titulo_plot03 =  '<p style="font-family:Courier; color:Blue; font-size: 20px;"><b>Evolução da Qtd de Matrículas por Area Geral do Curso</b></p>'
    st.markdown(titulo_plot03, unsafe_allow_html=True)

    col_ano = 'NU_ANO_CENSO'
    col_grupo = 'NO_CINE_AREA_GERAL'
    col_soma = 'QT_MAT'
    legenda_outside = 'S'

    df_areas = df_all[~df_all['NO_CINE_AREA_GERAL'].isin(['Programas básicos'])]
    f = gerar_plot_evol_ano(df_areas, col_ano, col_grupo, col_soma, legenda_outside)                                            
    st.pyplot(f)
    plt.close()
    st.markdown("---")

    # ------------------------------------------------------------------------				  
    # Plot04:  Evolução da Qtd Matriculas por Ano/ Faixa Idade (linha)
    # ------------------------------------------------------------------------
    # Preparar dados
    serie_matr_faixas_t1 = df_all.melt(id_vars=['NU_ANO_CENSO','CO_IES','NO_CURSO','QT_MAT'], var_name='Faixa_etaria', 
                                       value_name = 'Total_MAT',
                                       value_vars=['QT_MAT_0_17', 'QT_MAT_18_24', 'QT_MAT_25_29', 'QT_MAT_30_34',
                                                   'QT_MAT_35_39', 'QT_MAT_40_49', 'QT_MAT_50_59', 'QT_MAT_60_MAIS'])
    serie_matr_faixas_t2 = serie_matr_faixas_t1.groupby(['NU_ANO_CENSO', 'CO_IES','NO_CURSO','QT_MAT','Faixa_etaria'])['Total_MAT']\
                                                .sum().reset_index()
                                                
    serie_matr_faixas = serie_matr_faixas_t2.groupby(['NU_ANO_CENSO','Faixa_etaria'])['Total_MAT'].sum().reset_index()

    # Exibir plot
    titulo_plot04 =  '<p style="font-family:Courier; color:Blue; font-size: 20px;"><b>Evolução da Qtd de Matrículas por Faixa de Idade</b></p>'
    st.markdown(titulo_plot04, unsafe_allow_html=True)
                                                
    col_ano = 'NU_ANO_CENSO'
    col_grupo = 'Faixa_etaria'
    col_soma = 'Total_MAT'
    legenda_outside = 'S'

    f = gerar_plot_evol_ano(serie_matr_faixas, col_ano, col_grupo, col_soma, legenda_outside)                                            
    st.pyplot(f)
    plt.close()
    st.markdown("---")
    
    
    # ------------------------------------------------------------------------				  
    # Estados
    # ------------------------------------------------------------------------    
    st.subheader(':chart_with_upwards_trend: :adult: :books: Evolução Matrículas - Estados :classical_building:')

    # ------------------------------------------------------------------------				  
    # Plot01: Total Matriculas e Ingressantes por Rede Ensino 
    # ------------------------------------------------------------------------
    cores = sns.color_palette("terrain")
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
        titulo_plot01 =  f'<p style="font-family:Courier; color:Black; font-size: 23px;"><b>Total de Matrículas e Ingressantes - {ano_selecionado}</b></p>'
        st.markdown(titulo_plot01, unsafe_allow_html=True)   
        data = distr_matr_uf_re[distr_matr_uf_re['NU_ANO_CENSO']==ano_selecionado].sort_values(by='SG_UF', ascending=True)    
        f, axes = plt.subplots(1, 1,  figsize=(16, 8))
        g = sns.barplot(x='SG_UF', y='Total_Mat_mil', hue='TIPO_INST', data=data, orient='v', ax=axes, palette = cores)
        #axes.set_title(titulo, fontsize=18)
        major_yticks = np.arange(0, 1600, 200)
        axes.set_yticks(major_yticks)
        axes.set(xlabel=''); axes.set(ylabel='')
        axes.legend(loc='upper center', fontsize=18).set_visible(False)
        axes.grid(visible=False)
        
        ax2 = axes.twinx()
        dados2 = tot_ing_uf[tot_ing_uf['NU_ANO_CENSO']==ano_selecionado].sort_values(by='SG_UF', ascending=True)
        ax2.plot(dados2['SG_UF'], dados2['Total_Ingr_mil'],color='#ff3333', label='Total_Ingr_mil')
        ax2.set_ylabel("Total Ingressantes")
        ax2.set_yticks(major_yticks)
        ax2.grid(visible=True, linestyle = "dashed", color='white')
        
        lines1, labels1 = axes.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines1 + lines2, labels1 + labels2, loc="upper center", fontsize=18)    
        st.pyplot(f)
        plt.close()
      
    st.markdown("---")       
    
    
    
# ------------------------------------------------------------------------				  
# Tab 02
# Plot01: Evolução da Qtd Ingressantes por Ano/ Rede Ensino (linha)
# Plot02:  Evolução da Qtd Ingressantes por Ano/ Grau Academico (linha)
# Plot03:  Evolução da Qtd Ingressantes por Ano/ Area Curso (linha)
# Plot04:  Evolução da Qtd Ingressantes por Ano/ Faixa Idade (linha)
# ------------------------------------------------------------------------   

with t_evol_ingr:
    # ------------------------------------------------------------------------				  
    # Brasil 
    # ------------------------------------------------------------------------
    st.subheader(':chart_with_upwards_trend: :adult: :sparkles: Evolução Ingressantes - Brasil :flag-br:')
    
    
    # ------------------------------------------------------------------------				  
    # Plot01: Evolução da Qtd Ingressantes por Ano/ Rede Ensino (linha)
    # ------------------------------------------------------------------------
    titulo_plot01 =  '<p style="font-family:Courier; color:Blue; font-size: 20px;"><b>Evolução da Qtd de Ingressantes por Rede de Ensino</b></p>'
    st.markdown(titulo_plot01, unsafe_allow_html=True)

    col_ano = 'NU_ANO_CENSO'
    col_grupo = 'TIPO_INST'
    col_soma = 'QT_ING'
    legenda_outside = 'N'

    f = gerar_plot_evol_ano(df_all, col_ano, col_grupo, col_soma, legenda_outside)                                            
    st.pyplot(f)
    plt.close()
    st.markdown("---")
    
    # Plot01: Análise
    # ------------------------------------------------------------------------
    st.subheader("Análise:")    
    st.write('Uma constatação interessante é com relação ao total de ingressantes em cursos presenciais: este total vem apresentando queda desde 2014 e registrou o menor valor nos últimos dez anos em 2021. No último ano, em 2022, este número voltou a subir.')

    # ------------------------------------------------------------------------				  
    # Plot02:  Evolução da Qtd Ingressantes por Ano/ Grau Academico (linha)
    # ------------------------------------------------------------------------
    titulo_plot02 =  '<p style="font-family:Courier; color:Blue; font-size: 20px;"><b>Evolução da Qtd de Ingressantes por Grau Academico</b></p>'
    st.markdown(titulo_plot02, unsafe_allow_html=True)

    col_ano = 'NU_ANO_CENSO'
    col_grupo = 'Tipo_Grau_Acad' 
    col_soma = 'QT_ING'
    legenda_outside='N'

    f = gerar_plot_evol_ano(df_all, col_ano, col_grupo, col_soma, legenda_outside)
    st.pyplot(f)
    plt.close()
    st.markdown("---")

    # ------------------------------------------------------------------------				  
    # Plot03:  Evolução da Qtd Ingressantes por Ano/ Area Curso (linha)
    # ------------------------------------------------------------------------
    titulo_plot03 =  '<p style="font-family:Courier; color:Blue; font-size: 20px;"><b>Evolução da Qtd de Ingressantes por Area Geral do Curso</b></p>'
    st.markdown(titulo_plot03, unsafe_allow_html=True)

    col_ano = 'NU_ANO_CENSO'
    col_grupo = 'NO_CINE_AREA_GERAL'
    col_soma = 'QT_ING'
    legenda_outside = 'S'

    # retirar area especifica: Programas básicos
    df_areas = df_all[~df_all['NO_CINE_AREA_GERAL'].isin(['Programas básicos'])]

    f = gerar_plot_evol_ano(df_areas, col_ano, col_grupo, col_soma, legenda_outside)
    st.pyplot(f)
    plt.close()
    st.markdown("---")                                         
                                   
    # ------------------------------------------------------------------------				  
    # Plot04:  Evolução da Qtd Ingressantes por Ano/ Faixa Idade (linha)
    # ------------------------------------------------------------------------    
    # Preparar dados     
    serie_ingr_faixas_t1 = df_all.melt(id_vars=['NU_ANO_CENSO','CO_IES','NO_CURSO','QT_ING'], var_name='Faixa_etaria', 
                                       value_name = 'Total_Ingress',
                                       value_vars=['QT_ING_0_17', 'QT_ING_18_24', 'QT_ING_25_29', 'QT_ING_30_34',
                                                   'QT_ING_35_39', 'QT_ING_40_49', 'QT_ING_50_59', 'QT_ING_60_MAIS'])

    serie_ingr_faixas_t2 = serie_ingr_faixas_t1.groupby(['NU_ANO_CENSO', 'CO_IES','NO_CURSO','QT_ING','Faixa_etaria'])['Total_Ingress']\
    .sum().reset_index()

    serie_ingr_faixas = serie_ingr_faixas_t2.groupby(['NU_ANO_CENSO','Faixa_etaria'])['Total_Ingress'].sum().reset_index()

    # Exibir plot
    titulo_plot04 =  '<p style="font-family:Courier; color:Blue; font-size: 20px;"><b>Evolução da Qtd de Ingressantes por Faixa de Idade</b></p>'
    st.markdown(titulo_plot04, unsafe_allow_html=True)

    col_ano = 'NU_ANO_CENSO'
    col_grupo = 'Faixa_etaria'
    col_soma = 'Total_Ingress'
    legenda_outside = 'S'

    f = gerar_plot_evol_ano(serie_ingr_faixas, col_ano, col_grupo, col_soma, legenda_outside)
    st.pyplot(f)
    plt.close()
    st.markdown("---")


    
# ------------------------------------------------------------------------				  
# Tab 03
# Plot01: Evolução da Qtd Concluintes por Ano/ Rede Ensino (linha)
# Plot02: Evolução da Qtd Concluintes por Ano/ Grau Academico (linha)
# Plot03: Evolução da Qtd Concluintes por Ano/ Area Curso (linha)
# Plot04: Evolução da Qtd Concluintes por Ano/ Faixa Idade (linha)
# ------------------------------------------------------------------------   
with t_evol_conc:

    # ------------------------------------------------------------------------				  
    # Brasil 
    # ------------------------------------------------------------------------
    st.subheader(':chart_with_upwards_trend: :student: Evolução Concluintes - Brasil :flag-br:')
    
    
    # ------------------------------------------------------------------------				  
    # Plot01: Evolução da Qtd Concluintes por Ano/ Rede Ensino (linha)
    # ------------------------------------------------------------------------

    titulo_plot01 =  '<p style="font-family:Courier; color:Blue; font-size: 20px;"><b>Evolução da Qtd de Concluintes por Rede de Ensino</b></p>'
    st.markdown(titulo_plot01, unsafe_allow_html=True)

    col_ano = 'NU_ANO_CENSO'
    col_grupo = 'TIPO_INST' 
    col_soma = 'QT_CONC'
    legenda_outside = 'N'

    f = gerar_plot_evol_ano(df_all, col_ano, col_grupo, col_soma, legenda_outside)
    st.pyplot(f)
    plt.close()
    st.markdown("---")

    # ------------------------------------------------------------------------				  
    # Plot02:  Evolução da Qtd Concluintes por Ano/ Grau Academico (linha)
    # ------------------------------------------------------------------------
    titulo_plot02 =  '<p style="font-family:Courier; color:Blue; font-size: 20px;"><b>Evolução da Qtd de Concluintes por Grau Academico</b></p>'
    st.markdown(titulo_plot02, unsafe_allow_html=True)

    col_ano = 'NU_ANO_CENSO'
    col_grupo = 'Tipo_Grau_Acad' 
    col_soma = 'QT_CONC'
    legenda_outside='N'

    f = gerar_plot_evol_ano(df_all, col_ano, col_grupo, col_soma, legenda_outside)
    st.pyplot(f)
    plt.close()
    st.markdown("---")

    # ------------------------------------------------------------------------				  
    # Plot03:  Evolução da Qtd Concluintes por Ano/ Area Curso (linha)
    # ------------------------------------------------------------------------
    titulo_plot03 =  '<p style="font-family:Courier; color:Blue; font-size: 20px;"><b>Evolução da Qtd de Concluintes por Area Geral do Curso</b></p>'
    st.markdown(titulo_plot03, unsafe_allow_html=True)

    col_ano = 'NU_ANO_CENSO'
    col_grupo = 'NO_CINE_AREA_GERAL'
    col_soma = 'QT_CONC'
    legenda_outside = 'S'

    # retirar area especifica: Programas básicos
    df_areas = df_all[~df_all['NO_CINE_AREA_GERAL'].isin(['Programas básicos'])]

    f = gerar_plot_evol_ano(df_areas, col_ano, col_grupo, col_soma, legenda_outside)
    st.pyplot(f)
    plt.close()
    st.markdown("---")   

    # ------------------------------------------------------------------------				  
    # Plot04:  Evolução da Qtd Concluintes por Ano/ Faixa Idade (linha)
    # ------------------------------------------------------------------------    
    # Preparar dados  
    serie_concl_faixas_t1 = df_all.melt(id_vars=['NU_ANO_CENSO','CO_IES','NO_CURSO','QT_CONC'], 
                                       var_name='Faixa_etaria', 
                                       value_name = 'Total_Concl',
                                       value_vars=['QT_CONC_0_17', 'QT_CONC_18_24', 'QT_CONC_25_29', 'QT_CONC_30_34','QT_CONC_35_39', 'QT_CONC_40_49', 'QT_CONC_50_59', 'QT_CONC_60_MAIS'])
    serie_concl_faixas_t2 = serie_concl_faixas_t1.groupby(['NU_ANO_CENSO', 'CO_IES','NO_CURSO','QT_CONC','Faixa_etaria'])['Total_Concl']\
    .sum().reset_index()

    serie_concl_faixas = serie_concl_faixas_t2.groupby(['NU_ANO_CENSO','Faixa_etaria'])['Total_Concl'].sum().reset_index()

    # Exibir plot
    titulo_plot04 =  '<p style="font-family:Courier; color:Blue; font-size: 20px;"><b>Evolução da Qtd de Concluintes por Faixa de Idade</b></p>'
    st.markdown(titulo_plot04, unsafe_allow_html=True)

    col_ano = 'NU_ANO_CENSO'
    col_grupo = 'Faixa_etaria'
    col_soma = 'Total_Concl'
    legenda_outside = 'S'

    f = gerar_plot_evol_ano(serie_concl_faixas, col_ano, col_grupo, col_soma, legenda_outside)
    st.pyplot(f)
    plt.close()
    st.markdown("---")


# ------------------------------------------------------------------------				  
# Tab 04:  Todos Matriculas, Ingressos e Concluintes
# ------------------------------------------------------------------------     
with t_faixas: 
    st.subheader(':books: :adult: :sparkles: Matriculas, Ingressantes e Concluintes por Idade :male-student: :female-student:')

    # ------------------------------------------------------------------------				  
    # Plot01: 0 a 17
    # ------------------------------------------------------------------------

    # prepara dados
    df1 = serie_matr_faixas[serie_matr_faixas['Faixa_etaria']=='QT_MAT_0_17'].rename(columns={'Total_MAT':'Total'})
    df2 = serie_ingr_faixas[serie_ingr_faixas['Faixa_etaria']=='QT_ING_0_17'].rename(columns={'Total_Ingress':'Total'})
    df3 = serie_concl_faixas[serie_concl_faixas['Faixa_etaria']=='QT_CONC_0_17'].rename(columns={'Total_Concl':'Total'})
    serie_0_17 = pd.concat([df1, df2, df3])
    
    df1 = serie_matr_faixas[serie_matr_faixas['Faixa_etaria']=='QT_MAT_18_24'].rename(columns={'Total_MAT':'Total'})
    df2 = serie_ingr_faixas[serie_ingr_faixas['Faixa_etaria']=='QT_ING_18_24'].rename(columns={'Total_Ingress':'Total'})
    df3 = serie_concl_faixas[serie_concl_faixas['Faixa_etaria']=='QT_CONC_18_24'].rename(columns={'Total_Concl':'Total'})
    serie_18_24 = pd.concat([df1, df2, df3])
    
    df1 = serie_matr_faixas[serie_matr_faixas['Faixa_etaria']=='QT_MAT_25_29'].rename(columns={'Total_MAT':'Total'})
    df2 = serie_ingr_faixas[serie_ingr_faixas['Faixa_etaria']=='QT_ING_25_29'].rename(columns={'Total_Ingress':'Total'})
    df3 = serie_concl_faixas[serie_concl_faixas['Faixa_etaria']=='QT_CONC_25_29'].rename(columns={'Total_Concl':'Total'})
    serie_25_29 = pd.concat([df1, df2, df3])
    
    df1 = serie_matr_faixas[serie_matr_faixas['Faixa_etaria']=='QT_MAT_30_34'].rename(columns={'Total_MAT':'Total'})
    df2 = serie_ingr_faixas[serie_ingr_faixas['Faixa_etaria']=='QT_ING_30_34'].rename(columns={'Total_Ingress':'Total'})
    df3 = serie_concl_faixas[serie_concl_faixas['Faixa_etaria']=='QT_CONC_30_34'].rename(columns={'Total_Concl':'Total'})
    serie_30_34 = pd.concat([df1, df2, df3])

    df1 = serie_matr_faixas[serie_matr_faixas['Faixa_etaria']=='QT_MAT_35_39'].rename(columns={'Total_MAT':'Total'})
    df2 = serie_ingr_faixas[serie_ingr_faixas['Faixa_etaria']=='QT_ING_35_39'].rename(columns={'Total_Ingress':'Total'})
    df3 = serie_concl_faixas[serie_concl_faixas['Faixa_etaria']=='QT_CONC_35_39'].rename(columns={'Total_Concl':'Total'})
    serie_35_39 = pd.concat([df1, df2, df3])
    
    df1 = serie_matr_faixas[serie_matr_faixas['Faixa_etaria']=='QT_MAT_40_49'].rename(columns={'Total_MAT':'Total'})
    df2 = serie_ingr_faixas[serie_ingr_faixas['Faixa_etaria']=='QT_ING_40_49'].rename(columns={'Total_Ingress':'Total'})
    df3 = serie_concl_faixas[serie_concl_faixas['Faixa_etaria']=='QT_CONC_40_49'].rename(columns={'Total_Concl':'Total'})
    df4 = serie_matr_faixas[serie_matr_faixas['Faixa_etaria']=='QT_MAT_50_59'].rename(columns={'Total_MAT':'Total'})
    df5 = serie_ingr_faixas[serie_ingr_faixas['Faixa_etaria']=='QT_ING_50_59'].rename(columns={'Total_Ingress':'Total'})
    df6 = serie_concl_faixas[serie_concl_faixas['Faixa_etaria']=='QT_CONC_50_59'].rename(columns={'Total_Concl':'Total'})
    df7 = serie_matr_faixas[serie_matr_faixas['Faixa_etaria']=='QT_MAT_60_MAIS'].rename(columns={'Total_MAT':'Total'})
    df8 = serie_ingr_faixas[serie_ingr_faixas['Faixa_etaria']=='QT_ING_60_MAIS'].rename(columns={'Total_Ingress':'Total'})
    df9 = serie_concl_faixas[serie_concl_faixas['Faixa_etaria']=='QT_CONC_60_MAIS'].rename(columns={'Total_Concl':'Total'})
    serie_acima40 = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9])
    serie_acima40['Faixa_etaria'] = np.where(serie_acima40['Faixa_etaria'].str.contains('QT_CONC'),'QT_CONC_acima_40',serie_acima40['Faixa_etaria'])
    serie_acima40['Faixa_etaria'] = np.where(serie_acima40['Faixa_etaria'].str.contains('QT_ING'),'QT_ING_acima_40',serie_acima40['Faixa_etaria'])
    serie_acima40['Faixa_etaria'] = np.where(serie_acima40['Faixa_etaria'].str.contains('QT_MAT'),'QT_MAT_acima_40',serie_acima40['Faixa_etaria'])
    serie_acima40 = serie_acima40.groupby(['NU_ANO_CENSO','Faixa_etaria'])['Total'].sum().reset_index()    
    
    #titulo_plot01 =  '<p style="font-family:Courier; color:Blue; font-size: 20px;"><b>Evolução dos Discentes - Faixa: 0 a 17 anos</b></p>'
    #st.markdown(titulo_plot01, unsafe_allow_html=True)
    #titulo_plot02 =  '<p style="font-family:Courier; color:Blue; font-size: 20px;"><b>Evolução dos Discentes - Faixa: 18 a 24 anos</b></p>'
    #st.markdown(titulo_plot02, unsafe_allow_html=True)
    #titulo_plot03 =  '<p style="font-family:Courier; color:Blue; font-size: 20px;"><b>Evolução dos Discentes - Faixa: 25 a 29 anos</b></p>'
    #st.markdown(titulo_plot03, unsafe_allow_html=True)
    #titulo_plot05 =  '<p style="font-family:Courier; color:Blue; font-size: 20px;"><b>Evolução dos Discentes - Faixa: 35 a 39 anos</b></p>'
    #st.markdown(titulo_plot05, unsafe_allow_html=True)
    #titulo_plot04 =  '<p style="font-family:Courier; color:Blue; font-size: 20px;"><b>Evolução dos Discentes - Faixa: 30 a 34 anos</b></p>'
    #st.markdown(titulo_plot04, unsafe_allow_html=True)
    #titulo_plot06 =  '<p style="font-family:Courier; color:Blue; font-size: 20px;"><b>Evolução dos Discentes - Faixa: Acima de 40 anos</b></p>'
    #st.markdown(titulo_plot06, unsafe_allow_html=True)
    
    
    # prepara lista de opções de faixas 
    l_faixas = ['0 a 17 anos', '18 a 24 anos', '25 a 29 anos', '30 a 34 anos', '35 a 39 anos','Acima de 40 anos']
    col1, col2, col3 = st.columns(3)
    with col1:
        label01 = '<p style="font-family:Courier; color:#992600; font-size: 16px;"><b>Selecione uma Faixa Etária:</b></p>'
        st.markdown(label01, unsafe_allow_html=True) 
    with col2:
        faixa_selected = st.selectbox(label="Selecione uma Faixa Etária:", options=l_faixas, label_visibility="collapsed")
    with col3:    
        st.subheader(':classical_building:')
    
    col_ano = 'NU_ANO_CENSO'
    col_grupo = 'Faixa_etaria'
    col_soma = 'Total'
    legenda_outside = 'N'

    if faixa_selected == '0 a 17 anos': f = gerar_plot_evol_ano(serie_0_17, col_ano, col_grupo, col_soma, legenda_outside)
    if faixa_selected == '18 a 24 anos': f = gerar_plot_evol_ano(serie_18_24, col_ano, col_grupo, col_soma, legenda_outside)
    if faixa_selected == '25 a 29 anos': f = gerar_plot_evol_ano(serie_25_29, col_ano, col_grupo, col_soma, legenda_outside)
    if faixa_selected == '30 a 34 anos': f = gerar_plot_evol_ano(serie_30_34, col_ano, col_grupo, col_soma, legenda_outside)
    if faixa_selected == '35 a 39 anos': f = gerar_plot_evol_ano(serie_35_39, col_ano, col_grupo, col_soma, legenda_outside)
    if faixa_selected == 'Acima de 40 anos': f = gerar_plot_evol_ano(serie_acima40, col_ano, col_grupo, col_soma, legenda_outside)
    
    st.pyplot(f)


# ------------------------------------------------------------------------				  
# Tab 05: Visualização Vagas e Ingressantes por Area Geral/ Sexo por Ano
# ------------------------------------------------------------------------ 
# Carrega dataframes 
distr_vag_ingr_sexo = carrega_distr_vag_ingr_sexo()
distr_vag_ingr_sexo_uf = carrega_distr_vag_ingr_sexo_uf()
lista_areas = list(distr_vag_ingr_sexo['NO_CINE_AREA_GERAL'].unique())
lista_UF = list(distr_vag_ingr_sexo_uf['NO_UF'].unique())

with t_vag_ing_sexo:
    
    # ------------------------------------------------------------------------
    # Plot 01: Visualização Vagas e Ingressantes por Area Geral por Ano
    # ------------------------------------------------------------------------	
    st.subheader(':school: :adult: :books: Vagas e Ingressantes por Sexo :flag-br:')
    col1, col2, col3 = st.columns(3)
    with col1:
        label01 = '<p style="font-family:Courier; color:#992600; font-size: 16px;"><b>Selecione uma area de conhecimento:</b></p>'
        st.markdown(label01, unsafe_allow_html=True) 
    with col2:
        area_selecionada = st.selectbox(label="Selecione uma Area de conhecimento Geral específica:", options=lista_areas, label_visibility="collapsed")
    with col3:    
        st.subheader(':books:')

    if area_selecionada:
        titulo_plot01 =  f'<p style="font-family:Courier; color:Blue; font-size: 16px;"><b>Vagas e Ingressantes para a Area Geral: {area_selecionada}</b></p>'
        st.markdown(titulo_plot01, unsafe_allow_html=True)    
        dados1 = distr_vag_ingr_sexo[
        (distr_vag_ingr_sexo['NO_CINE_AREA_GERAL']==area_selecionada)]
        fig = px.bar(dados1,
                 y='Total', 
                 x='NU_ANO_CENSO', 
                 color='Variavel_total',
                 color_discrete_sequence=px.colors.qualitative.G10,
                 barmode = 'group', width=1200, height=500)
        fig.update_layout(yaxis=dict(title='Total', titlefont_size=18, tickfont_size=16),
        xaxis=dict(title='', tickfont_size=18),      
        legend=dict(x=0.03,y=0.96, font = dict(size = 18))) 
        fig.update_layout(plot_bgcolor='#dbe0f0') 
        st.plotly_chart(fig, use_container_width=True)
        plt.close()
        
    # ------------------------------------------------------------------------
    # Plot 02: Visualização Vagas e Ingressantes por Area Geral por Ano
    # Selecionar UF
    # ------------------------------------------------------------------------	
    st.markdown("---") 
    st.subheader(':school: :adult: :books: Vagas e Ingressantes por Sexo - UF :classical_building:')        
    
    col1, col2, col3 = st.columns(3)
    with col1:
        label02 = '<p style="font-family:Courier; color:#992600; font-size: 16px;"><b>Selecione uma UF:</b></p>'
        st.markdown(label02, unsafe_allow_html=True) 
    with col2:
        UF_selecionada = st.selectbox(label="Selecione uma UF:", options=lista_UF, label_visibility="collapsed")
    with col3:    
        st.subheader(':classical_building:')
        
    col4, col5, col6 = st.columns(3)
    with col4:
        label03 = '<p style="font-family:Courier; color:#992600; font-size: 16px;"><b>Selecione uma area de conhecimento:</b></p>'
        st.markdown(label03, unsafe_allow_html=True) 
    with col5:
        area_selecionada2 = st.selectbox(label="Selecione uma Area de conhecimento Geral específica2:", options=lista_areas, label_visibility="collapsed")
    with col6:    
        st.subheader(':books:')
    
    if area_selecionada2 and UF_selecionada: 
        titulo_plot02 =  f'<p style="font-family:Courier; color:Blue; font-size: 16px;"><b>Vagas e Ingressantes da UF {UF_selecionada} para a Area Geral: {area_selecionada2}</b></p>'
        st.markdown(titulo_plot02, unsafe_allow_html=True)    
        dados2 = distr_vag_ingr_sexo_uf[
        (distr_vag_ingr_sexo_uf['NO_CINE_AREA_GERAL']==area_selecionada2) & 
        (distr_vag_ingr_sexo_uf['NO_UF']==UF_selecionada)]        
        fig2 = px.bar(dados2,
                     y='Total', 
                     x='NU_ANO_CENSO', 
                     color='Variavel_total',
                     hover_data = {'NO_UF', 'Variavel_total', 'Total'},
                     color_discrete_sequence=px.colors.qualitative.G10,
                     barmode = 'group', width=1200, height=500)
        fig2.update_layout(yaxis=dict(title='Total', titlefont_size=18, tickfont_size=16),
                          xaxis=dict(title='', tickfont_size=18),      
                          legend=dict(x=0.03,y=0.96, font = dict(size = 18))) 
        fig2.update_layout(plot_bgcolor='#dbe0f0')
        st.plotly_chart(fig2, use_container_width=True)
        plt.close()
        
# ------------------------------------------------------------------------				  
# Tab 06: 
# ------------------------------------------------------------------------    
disc_ano_uf_area = carrega_disc_ano_uf_area()
l_var = ['Total vagas', 'Total inscritos', 'Total ingressantes', 'Total matrículas', 'Total concluintes']
l_cursos = sorted(list(disc_ano_uf_area['NO_CINE_AREA_GERAL'].unique()))

with t_mapas:
    titulo_plot01 =  '<p style="font-family:Courier; color:Black; font-size: 20px;"><b>Evolução da Quantidade de discentes</b></p>'
    st.markdown(titulo_plot01, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        label01 = '<p style="font-family:Courier; color:#992600; font-size: 16px;"><b>Selecione uma variável de interesse:</b></p>'
        st.markdown(label01, unsafe_allow_html=True) 
            
    with col2:
        var_selecionada = st.selectbox(label="Selecione uma variável de interesse:", options=l_var, label_visibility="collapsed")
            
    with col3:
        st.subheader(':mag:')
        
    col1, col2, col3 = st.columns(3)
    with col1:
        label02 = '<p style="font-family:Courier; color:#992600; font-size: 16px;"><b>Selecione uma área geral de curso:</b></p>'
        st.markdown(label02, unsafe_allow_html=True) 
            
    with col2:
        area_selecionada = st.selectbox(label="Selecione uma área geral de curso:", options=l_cursos, label_visibility="collapsed")
            
    with col3:
        st.subheader(':books:')        


    filtered_data = disc_ano_uf_area[
                    (disc_ano_uf_area['NO_CINE_AREA_GERAL']==area_selecionada)]
                    
    if var_selecionada=='Total vagas': var_selecionada_nome = 'Tot_vagas_pop' 
    elif var_selecionada=='Total inscritos': var_selecionada_nome = 'Tot_inscr_pop'
    elif var_selecionada=='Total ingressantes': var_selecionada_nome = 'Tot_ingr_pop'
    elif var_selecionada=='Total matrículas': var_selecionada_nome = 'Tot_matr_pop'
    elif var_selecionada=='Total concluintes': var_selecionada_nome = 'Tot_concl_pop'
    else: var_selecionada_nome = None
    
    mapa = px.choropleth_mapbox(filtered_data, 
                                   geojson=geojson_data,      
                                   locations='NO_UF_M',        
                                   color=var_selecionada_nome,
                                   color_continuous_scale="RdYlBu_r",
                                   range_color=(0, max(filtered_data[var_selecionada_nome])),
                                   animation_frame='NU_ANO_CENSO', 
                                   mapbox_style="open-street-map",
                                   zoom=2.2, 
                                   center={"lat": -15, "lon": -57.33},
                                   opacity=1,
                                   labels={'NU_ANO_CENSO':'Ano Censo',
                                           'NO_UF_M': 'Estado'},
                                   featureidkey="properties.NM_ESTADO")

    mapa.update_layout(
            coloraxis_colorbar=dict(
                len=1, x=0.5, y=-0.55, yanchor='bottom', xanchor='center', orientation='h',  
                title="Razão da Quantidade por População do Estado (x1000)", titleside = "bottom"),
                margin=dict(t=0, b=0, l=0, r=0))

    mapa.update_layout(width=1000, height=700)
    st.plotly_chart(mapa, use_container_width=True)
    plt.close()
                

                
