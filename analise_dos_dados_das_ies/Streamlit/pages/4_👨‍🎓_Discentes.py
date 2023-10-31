import os
import pandas as pd 
import numpy as np 
import matplotlib
import matplotlib.pyplot as plt 
import seaborn as sns 
import plotly
import plotly.express as px
import streamlit as st


st.set_page_config(page_title='Analise Discentes', 
                    page_icon=':student:', 
				    layout='wide', 
                    initial_sidebar_state='expanded')

                    
st.title(':bar_chart: Análise dos Discentes das IES :male-student: :female-student: ')
st.subheader('Escopo: Matrículas, Ingressantes e Concluintes')
st.subheader("Dados de 2012-2022")
st.markdown("---")  

# ------------------------------------------------------------------------
# PARTE 01 - Evolução das Matriculas - Brasil
# ------------------------------------------------------------------------
st.title(':chart_with_upwards_trend: :adult: :books: Evolução das Matrículas :flag-br:')
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
df_all = carrega_df()	

# ------------------------------------------------------------------------				  
# Funcoes
# ------------------------------------------------------------------------
def gerar_plot_evol_ano(df, col_ano, col_grupo, col_soma, legenda_outside):

    # exibe primeiros registros do df
    print('Exibindo alguns registros do df consolidado...\n')
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
    #plt.show()


# ------------------------------------------------------------------------				  
# Prepara dataframes
# ------------------------------------------------------------------------
#plot01
serie_matr = df_all.groupby(['NU_ANO_CENSO', 'TIPO_INST'])['QT_MAT'].sum().reset_index().rename(columns={'QT_MAT':'Total_matriculas'})


# ------------------------------------------------------------------------				  
# Plot01:  Evolução da Qtd Matriculas Presenciais por Ano/ Tipo Rede (linha)
# ------------------------------------------------------------------------
titulo_plot01 =  '<p style="font-family:Courier; color:Black; font-size: 23px;"><b>Visualização da Evolução da Qtd de Matrículas PRESENCIAIS por Rede de Ensino</b></p>'
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
st.markdown("---")

# ------------------------------------------------------------------------				  
# Plot02:  Evolução da Qtd Matriculas Presenciais por Ano/ Grau Academico (linha)
# ------------------------------------------------------------------------
titulo_plot02 =  '<p style="font-family:Courier; color:Black; font-size: 23px;"><b>Visualização da Evolução da Qtd de Matrículas PRESENCIAIS por Grau Academico</b></p>'
st.markdown(titulo_plot02, unsafe_allow_html=True)

col_ano = 'NU_ANO_CENSO'
col_grupo = 'Tipo_Grau_Acad'
col_soma = 'QT_MAT'
legenda_outside = 'N'

f = gerar_plot_evol_ano(df_all, col_ano, col_grupo, col_soma, legenda_outside)                                            
st.pyplot(f)
st.markdown("---")


# ------------------------------------------------------------------------				  
# Plot03:  Evolução da Qtd Matriculas Presenciais por Ano/ Area Curso (linha)
# ------------------------------------------------------------------------
titulo_plot03 =  '<p style="font-family:Courier; color:Black; font-size: 23px;"><b>Visualização da Evolução da Qtd de Matrículas PRESENCIAIS por Area Geral do Curso</b></p>'
st.markdown(titulo_plot03, unsafe_allow_html=True)

col_ano = 'NU_ANO_CENSO'
col_grupo = 'NO_CINE_AREA_GERAL'
col_soma = 'QT_MAT'
legenda_outside = 'S'

df_areas = df_all[~df_all['NO_CINE_AREA_GERAL'].isin(['Programas básicos'])]
f = gerar_plot_evol_ano(df_areas, col_ano, col_grupo, col_soma, legenda_outside)                                            
st.pyplot(f)
st.markdown("---")

# ------------------------------------------------------------------------				  
# Plot04:  Evolução da Qtd Matriculas Presenciais por Ano/ Faixa Idade (linha)
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
titulo_plot04 =  '<p style="font-family:Courier; color:Black; font-size: 23px;"><b>Visualização da Evolução da Qtd de Matrículas PRESENCIAIS por Faixa de Idade</b></p>'
st.markdown(titulo_plot04, unsafe_allow_html=True)
                                            
col_ano = 'NU_ANO_CENSO'
col_grupo = 'Faixa_etaria'
col_soma = 'Total_MAT'
legenda_outside = 'S'

f = gerar_plot_evol_ano(serie_matr_faixas, col_ano, col_grupo, col_soma, legenda_outside)                                            
st.pyplot(f)
st.markdown("---")
                      

# ------------------------------------------------------------------------
# PARTE 02 - Evolução das Matriculas - UFs
# ------------------------------------------------------------------------
st.title(':chart_with_upwards_trend: :adult: :books: Evolução das Matrículas nos Estados :classical_building:')

st.markdown("---")       


# ------------------------------------------------------------------------				  
# Prepara dataframes
# ------------------------------------------------------------------------
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


# ------------------------------------------------------------------------				  
# Plot01: Total Matriculas e Ingressantes por Rede Ensino 
# ------------------------------------------------------------------------
cores = sns.color_palette("terrain")
l_anos = range(2012,2023,1)

col1, col2, col3 = st.columns(3)
with col1:
    label01 = '<p style="font-family:Courier; color:#992600; font-size: 20px;"><b>Selecione um ano específico:</b></p>'
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
    
# para mostrar todos os anos
# for ano in range(2012, 2023, 1): # a = para cada ano 
    # data = distr_matr_uf_re[distr_matr_uf_re['NU_ANO_CENSO']==ano].sort_values(by='SG_UF', ascending=True)
    # f, axes = plt.subplots(1, 1,  figsize=(16, 8))
    # g = sns.barplot(x='SG_UF', y='Total_Mat_mil', hue='TIPO_INST', data=data, orient='v', ax=axes, palette = cores)
    
    # titulo = 'Total de Matrículas e Ingressantes - ' + str(ano)
    
    # axes.set_title(titulo, fontsize=18)
    # major_yticks = np.arange(0, 1600, 200)
    # axes.set_yticks(major_yticks)
    # axes.set(xlabel=''); axes.set(ylabel='')
    # axes.legend(loc='upper center', fontsize=18).set_visible(False)
    # axes.grid(visible=False)
    
    # ax2 = axes.twinx()
    # dados2 = tot_ing_uf[tot_ing_uf['NU_ANO_CENSO']==ano].sort_values(by='SG_UF', ascending=True)
    # ax2.plot(dados2['SG_UF'], dados2['Total_Ingr_mil'],color='#ff3333', label='Total_Ingr_mil')
    # ax2.set_ylabel("Total Ingressantes")
    # ax2.set_yticks(major_yticks)
    # ax2.grid(visible=True, linestyle = "dashed", color='white')
    
    # lines1, labels1 = axes.get_legend_handles_labels()
    # lines2, labels2 = ax2.get_legend_handles_labels()
    # ax2.legend(lines1 + lines2, labels1 + labels2, loc="upper center", fontsize=18)    
    # st.pyplot(f)
    
    
st.markdown("---")   
    
# ------------------------------------------------------------------------
# PARTE 03 - Evolução dos Ingressantes 
# ------------------------------------------------------------------------
st.title(':chart_with_upwards_trend: :adult: :sparkles: Evolução dos Ingressantes :flag-br:')
st.markdown("---")       

# ------------------------------------------------------------------------				  
# Plot01: Evolução da Qtd Ingressantes Presenciais por Ano/ Rede Ensino (linha)
# ------------------------------------------------------------------------
titulo_plot01 =  '<p style="font-family:Courier; color:Black; font-size: 23px;"><b>Visualização da Evolução da Qtd de Ingressantes PRESENCIAIS por Rede de Ensino</b></p>'
st.markdown(titulo_plot01, unsafe_allow_html=True)

col_ano = 'NU_ANO_CENSO'
col_grupo = 'TIPO_INST'
col_soma = 'QT_ING'
legenda_outside = 'N'

f = gerar_plot_evol_ano(df_all, col_ano, col_grupo, col_soma, legenda_outside)                                            
st.pyplot(f)
st.markdown("---")

# ------------------------------------------------------------------------				  
# Plot02:  Evolução da Qtd Ingressantes Presenciais por Ano/ Grau Academico (linha)
# ------------------------------------------------------------------------
titulo_plot02 =  '<p style="font-family:Courier; color:Black; font-size: 23px;"><b>Visualização da Evolução da Qtd de Ingressantes PRESENCIAIS por Grau Academico</b></p>'
st.markdown(titulo_plot02, unsafe_allow_html=True)

col_ano = 'NU_ANO_CENSO'
col_grupo = 'Tipo_Grau_Acad' 
col_soma = 'QT_ING'
legenda_outside='N'

f = gerar_plot_evol_ano(df_all, col_ano, col_grupo, col_soma, legenda_outside)
st.pyplot(f)
st.markdown("---")

# ------------------------------------------------------------------------				  
# Plot03:  Evolução da Qtd Ingressantes Presenciais por Ano/ Area Curso (linha)
# ------------------------------------------------------------------------
titulo_plot03 =  '<p style="font-family:Courier; color:Black; font-size: 23px;"><b>Visualização da Evolução da Qtd de Ingressantes PRESENCIAIS por Area Geral do Curso</b></p>'
st.markdown(titulo_plot03, unsafe_allow_html=True)

col_ano = 'NU_ANO_CENSO'
col_grupo = 'NO_CINE_AREA_GERAL'
col_soma = 'QT_ING'
legenda_outside = 'S'

# retirar area especifica: Programas básicos
df_areas = df_all[~df_all['NO_CINE_AREA_GERAL'].isin(['Programas básicos'])]

f = gerar_plot_evol_ano(df_areas, col_ano, col_grupo, col_soma, legenda_outside)
st.pyplot(f)
st.markdown("---")                                         
                               
# ------------------------------------------------------------------------				  
# Plot04:  Evolução da Qtd Ingressantes Presenciais por Ano/ Faixa Idade (linha)
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
titulo_plot04 =  '<p style="font-family:Courier; color:Black; font-size: 23px;"><b>Visualização da Evolução da Qtd de Ingressantes PRESENCIAIS por Faixa de Idade</b></p>'
st.markdown(titulo_plot04, unsafe_allow_html=True)

col_ano = 'NU_ANO_CENSO'
col_grupo = 'Faixa_etaria'
col_soma = 'Total_Ingress'
legenda_outside = 'S'

f = gerar_plot_evol_ano(serie_ingr_faixas, col_ano, col_grupo, col_soma, legenda_outside)
st.pyplot(f)
st.markdown("---")
                      
                      
# ------------------------------------------------------------------------
# PARTE 04 - Evolução dos Concluintes 
# ------------------------------------------------------------------------
st.title(':chart_with_upwards_trend: :student: Evolução dos Concluintes :flag-br:')
st.markdown("---")     

# ------------------------------------------------------------------------				  
# Plot01: Evolução da Qtd Concluintes Presenciais por Ano/ Rede Ensino (linha)
# ------------------------------------------------------------------------

titulo_plot01 =  '<p style="font-family:Courier; color:Black; font-size: 23px;"><b>Visualização da Evolução da Qtd de Concluintes PRESENCIAIS por Rede de Ensino</b></p>'
st.markdown(titulo_plot01, unsafe_allow_html=True)

col_ano = 'NU_ANO_CENSO'
col_grupo = 'TIPO_INST' 
col_soma = 'QT_CONC'
legenda_outside = 'N'

f = gerar_plot_evol_ano(df_all, col_ano, col_grupo, col_soma, legenda_outside)
st.pyplot(f)
st.markdown("---")

# ------------------------------------------------------------------------				  
# Plot02:  Evolução da Qtd Concluintes Presenciais por Ano/ Grau Academico (linha)
# ------------------------------------------------------------------------
titulo_plot02 =  '<p style="font-family:Courier; color:Black; font-size: 23px;"><b>Visualização da Evolução da Qtd de Concluintes PRESENCIAIS por Grau Academico</b></p>'
st.markdown(titulo_plot02, unsafe_allow_html=True)

col_ano = 'NU_ANO_CENSO'
col_grupo = 'Tipo_Grau_Acad' 
col_soma = 'QT_CONC'
legenda_outside='N'

f = gerar_plot_evol_ano(df_all, col_ano, col_grupo, col_soma, legenda_outside)
st.pyplot(f)
st.markdown("---")

# ------------------------------------------------------------------------				  
# Plot03:  Evolução da Qtd Concluintes Presenciais por Ano/ Area Curso (linha)
# ------------------------------------------------------------------------
titulo_plot03 =  '<p style="font-family:Courier; color:Black; font-size: 23px;"><b>Visualização da Evolução da Qtd de Concluintes PRESENCIAIS por Area Geral do Curso</b></p>'
st.markdown(titulo_plot03, unsafe_allow_html=True)

col_ano = 'NU_ANO_CENSO'
col_grupo = 'NO_CINE_AREA_GERAL'
col_soma = 'QT_CONC'
legenda_outside = 'S'

# retirar area especifica: Programas básicos
df_areas = df_all[~df_all['NO_CINE_AREA_GERAL'].isin(['Programas básicos'])]

f = gerar_plot_evol_ano(df_areas, col_ano, col_grupo, col_soma, legenda_outside)
st.pyplot(f)
st.markdown("---")   

# ------------------------------------------------------------------------				  
# Plot04:  Evolução da Qtd Concluintes Presenciais por Ano/ Faixa Idade (linha)
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
titulo_plot04 =  '<p style="font-family:Courier; color:Black; font-size: 23px;"><b>Visualização da Evolução da Qtd de Concluintes PRESENCIAIS por Faixa de Idade</b></p>'
st.markdown(titulo_plot04, unsafe_allow_html=True)

col_ano = 'NU_ANO_CENSO'
col_grupo = 'Faixa_etaria'
col_soma = 'Total_Concl'
legenda_outside = 'S'

f = gerar_plot_evol_ano(serie_concl_faixas, col_ano, col_grupo, col_soma, legenda_outside)
st.pyplot(f)
st.markdown("---")

# ------------------------------------------------------------------------
# PARTE 05 - Todos Matriculas, Ingressos e Concluintes
# ------------------------------------------------------------------------
st.title(':books: :adult: :sparkles: Matriculas, Ingressantes e Concluintes por Idade :male-student: :female-student:')
st.markdown("---")     


# ------------------------------------------------------------------------				  
# Plot01: 0 a 17
# ------------------------------------------------------------------------
titulo_plot01 =  '<p style="font-family:Courier; color:Black; font-size: 23px;"><b>Visualização da Evolução das Matrículas, Ingressantes e Concluintes PRESENCIAIS - Faixa: 0 a 17 anos</b></p>'
st.markdown(titulo_plot01, unsafe_allow_html=True)

df1 = serie_matr_faixas[serie_matr_faixas['Faixa_etaria']=='QT_MAT_0_17'].rename(columns={'Total_MAT':'Total'})
df2 = serie_ingr_faixas[serie_ingr_faixas['Faixa_etaria']=='QT_ING_0_17'].rename(columns={'Total_Ingress':'Total'})
df3 = serie_concl_faixas[serie_concl_faixas['Faixa_etaria']=='QT_CONC_0_17'].rename(columns={'Total_Concl':'Total'})
serie_0_17 = pd.concat([df1, df2, df3])

col_ano = 'NU_ANO_CENSO'
col_grupo = 'Faixa_etaria'
col_soma = 'Total'
legenda_outside = 'N'

f = gerar_plot_evol_ano(serie_0_17, col_ano, col_grupo, col_soma, legenda_outside)
st.pyplot(f)
st.markdown("---")

# ------------------------------------------------------------------------				  
# Plot02: 18 a 24
# ------------------------------------------------------------------------
titulo_plot02 =  '<p style="font-family:Courier; color:Black; font-size: 23px;"><b>Visualização da Evolução das Matrículas, Ingressantes e Concluintes PRESENCIAIS - Faixa: 18 a 24 anos</b></p>'
st.markdown(titulo_plot01, unsafe_allow_html=True)

df1 = serie_matr_faixas[serie_matr_faixas['Faixa_etaria']=='QT_MAT_18_24'].rename(columns={'Total_MAT':'Total'})
df2 = serie_ingr_faixas[serie_ingr_faixas['Faixa_etaria']=='QT_ING_18_24'].rename(columns={'Total_Ingress':'Total'})
df3 = serie_concl_faixas[serie_concl_faixas['Faixa_etaria']=='QT_CONC_18_24'].rename(columns={'Total_Concl':'Total'})
serie_18_24 = pd.concat([df1, df2, df3])

col_ano = 'NU_ANO_CENSO'
col_grupo = 'Faixa_etaria'
col_soma = 'Total'
legenda_outside = 'N'

f = gerar_plot_evol_ano(serie_18_24, col_ano, col_grupo, col_soma, legenda_outside)
st.pyplot(f)
st.markdown("---")

# ------------------------------------------------------------------------				  
# Plot03: 25 a 29
# ------------------------------------------------------------------------
titulo_plot03 =  '<p style="font-family:Courier; color:Black; font-size: 23px;"><b>Visualização da Evolução das Matrículas, Ingressantes e Concluintes PRESENCIAIS - Faixa: 25 a 29 anos</b></p>'
st.markdown(titulo_plot01, unsafe_allow_html=True)

df1 = serie_matr_faixas[serie_matr_faixas['Faixa_etaria']=='QT_MAT_25_29'].rename(columns={'Total_MAT':'Total'})
df2 = serie_ingr_faixas[serie_ingr_faixas['Faixa_etaria']=='QT_ING_25_29'].rename(columns={'Total_Ingress':'Total'})
df3 = serie_concl_faixas[serie_concl_faixas['Faixa_etaria']=='QT_CONC_25_29'].rename(columns={'Total_Concl':'Total'})
serie_25_29 = pd.concat([df1, df2, df3])

col_ano = 'NU_ANO_CENSO'
col_grupo = 'Faixa_etaria'
col_soma = 'Total'
legenda_outside = 'N'

f = gerar_plot_evol_ano(serie_25_29, col_ano, col_grupo, col_soma, legenda_outside)
st.pyplot(f)
st.markdown("---")

# ------------------------------------------------------------------------				  
# Plot04: 30 a 34
# ------------------------------------------------------------------------
titulo_plot04 =  '<p style="font-family:Courier; color:Black; font-size: 23px;"><b>Visualização da Evolução das Matrículas, Ingressantes e Concluintes PRESENCIAIS - Faixa: 30 a 34 anos</b></p>'
st.markdown(titulo_plot01, unsafe_allow_html=True)

df1 = serie_matr_faixas[serie_matr_faixas['Faixa_etaria']=='QT_MAT_30_34'].rename(columns={'Total_MAT':'Total'})
df2 = serie_ingr_faixas[serie_ingr_faixas['Faixa_etaria']=='QT_ING_30_34'].rename(columns={'Total_Ingress':'Total'})
df3 = serie_concl_faixas[serie_concl_faixas['Faixa_etaria']=='QT_CONC_30_34'].rename(columns={'Total_Concl':'Total'})
serie_30_34 = pd.concat([df1, df2, df3])

col_ano = 'NU_ANO_CENSO'
col_grupo = 'Faixa_etaria'
col_soma = 'Total'
legenda_outside = 'N'

f = gerar_plot_evol_ano(serie_30_34, col_ano, col_grupo, col_soma, legenda_outside)
st.pyplot(f)
st.markdown("---")

# ------------------------------------------------------------------------				  
# Plot05: 35 a 39
# ------------------------------------------------------------------------
titulo_plot05 =  '<p style="font-family:Courier; color:Black; font-size: 23px;"><b>Visualização da Evolução das Matrículas, Ingressantes e Concluintes PRESENCIAIS - Faixa: 35 a 39 anos</b></p>'
st.markdown(titulo_plot01, unsafe_allow_html=True)

df1 = serie_matr_faixas[serie_matr_faixas['Faixa_etaria']=='QT_MAT_35_39'].rename(columns={'Total_MAT':'Total'})
df2 = serie_ingr_faixas[serie_ingr_faixas['Faixa_etaria']=='QT_ING_35_39'].rename(columns={'Total_Ingress':'Total'})
df3 = serie_concl_faixas[serie_concl_faixas['Faixa_etaria']=='QT_CONC_35_39'].rename(columns={'Total_Concl':'Total'})
serie_35_39 = pd.concat([df1, df2, df3])

col_ano = 'NU_ANO_CENSO'
col_grupo = 'Faixa_etaria'
col_soma = 'Total'
legenda_outside = 'N'

f = gerar_plot_evol_ano(serie_35_39, col_ano, col_grupo, col_soma, legenda_outside)
st.pyplot(f)
st.markdown("---")

# ------------------------------------------------------------------------				  
# Plot06: Acima 40
# ------------------------------------------------------------------------
titulo_plot06 =  '<p style="font-family:Courier; color:Black; font-size: 23px;"><b>Visualização da Evolução das Matrículas, Ingressantes e Concluintes PRESENCIAIS - Faixa: Acima de 40 anos</b></p>'
st.markdown(titulo_plot01, unsafe_allow_html=True)

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

col_ano = 'NU_ANO_CENSO'
col_grupo = 'Faixa_etaria'
col_soma = 'Total'
legenda_outside = 'N'


f = gerar_plot_evol_ano(serie_acima40, col_ano, col_grupo, col_soma, legenda_outside)
st.pyplot(f)
st.markdown("---")


# ------------------------------------------------------------------------
# PARTE 06 - Visualização Vagas e Ingressantes por Area Geral por Ano
# ------------------------------------------------------------------------                   
st.title(':school: :adult: :books: Vagas e Ingressantes por Sexo :flag-br:')
st.markdown("---")     


# PREPARA DADOS
distr_vag_ingr_sexo = df_all.groupby(['NU_ANO_CENSO', 'NO_CINE_AREA_GERAL']).agg ({
                                              'QT_VG_TOTAL':'sum',
                                              'QT_VG_TOTAL_DIURNO':'sum',
                                              'QT_VG_TOTAL_NOTURNO':'sum',
                                              'QT_INSCRITO_TOTAL':'sum',
                                              'QT_ING':'sum',
                                              'QT_ING_FEM':'sum',
                                              'QT_ING_MASC':'sum' })

distr_vag_ingr_sexo = distr_vag_ingr_sexo.reset_index().rename(columns={
                                                                'QT_VG_TOTAL':'Total_vagas',
                                                                'QT_VG_TOTAL_DIURNO':'Total_vag_d',
                                                                'QT_VG_TOTAL_NOTURNO':'Total_vagas_n',
                                                                'QT_INSCRITO_TOTAL':'Total_insc',
                                                                'QT_ING':'Total_ing',
                                                                'QT_ING_FEM':'Total_ing_f',
                                                                'QT_ING_MASC':'Total_ing_m'})

                                                                
distr_vag_ingr_sexo_melt = distr_vag_ingr_sexo.melt(
    id_vars=['NU_ANO_CENSO','NO_CINE_AREA_GERAL'], 
    value_vars=['Total_vagas','Total_vag_d','Total_vagas_n','Total_insc','Total_ing','Total_ing_f','Total_ing_m'],
    var_name='Variavel_total',
    value_name='Total')
                                                                
distr_vag_ingr_sexo_plot01 = distr_vag_ingr_sexo_melt[distr_vag_ingr_sexo_melt['Variavel_total'].\
                                        isin(['Total_vagas','Total_ing_f','Total_ing_m'])]                                                                
# ------------------------------------------------------------------------
# Plot 01: Visualização Vagas e Ingressantes por Area Geral por Ano
# ------------------------------------------------------------------------	
lista_areas = list(distr_vag_ingr_sexo_plot01['NO_CINE_AREA_GERAL'].unique())

col1, col2, col3 = st.columns(3)

with col1:
    label01 = '<p style="font-family:Courier; color:#992600; font-size: 20px;"><b>Selecione uma area de conhecimento específica:</b></p>'
    st.markdown(label01, unsafe_allow_html=True) 
    
with col2:
    area_selecionada = st.selectbox(label="Selecione uma Area de conhecimento Geral específica:", options=lista_areas, label_visibility="collapsed")
    
with col3:    
    st.subheader(':date:')

if area_selecionada:
    titulo_plot01 =  f'<p style="font-family:Courier; color:Black; font-size: 23px;"><b>Visualização Vagas e Ingressantes para a Area Geral: {area_selecionada}</b></p>'
    st.markdown(titulo_plot01, unsafe_allow_html=True)    
    
    
    dados1 = distr_vag_ingr_sexo_plot01[
    (distr_vag_ingr_sexo_plot01['NO_CINE_AREA_GERAL']==area_selecionada)]
    fig = px.bar(dados1,
             y='Total', 
             x='NU_ANO_CENSO', 
             color='Variavel_total',
             color_discrete_sequence=px.colors.qualitative.G10,
             barmode = 'group', width=1200, height=700)
    fig.update_layout(yaxis=dict(title='Total'),
    xaxis=dict(title='', tickfont_size=18),      
    legend=dict(x=0.03,y=0.96, font = dict(size = 18))) 
    
    fig.update_layout(plot_bgcolor='#dbe0f0') 
    
    st.plotly_chart(fig, use_container_width=True)


    
    


