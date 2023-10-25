import streamlit as st

import pandas as pd
import os 


st.set_page_config(page_title="Evasão de alunos na UFJF", page_icon= '🏃‍♀️', layout="wide")
st.markdown('# Evasão de alunos na UFJF 🏃‍♀️📚')
st.markdown("---")

filepath = os.path.join(os.getcwd(), 'Dados', 'dataset_grad_pres.csv')

# Cria o DataFrame completo, com todos os dados do arquivo dataset_grad_pres.csv

df_completo = pd.read_csv(filepath, engine='python', 
                     on_bad_lines='warn', encoding='iso-8859-1', header=0, sep = ";")

########################### TABELA ##################
# Grupo / Baixa renda / Escola Pública /  Etnia-PPI / PCD
# Grupo A sim sim sim não
# Grupo A1 sim sim sim sim
# Grupo B sim sim não não
# Grupo B1 sim sim não sim
# Grupo C não não não não
# Grupo D não sim sim não
# Grupo D1 não sim  sim sim
# Grupo E não sim não não
# Grupo E1 não sim não sim

# Inclui no final do DataFrame df_completo as colunas:
# Baixa renda; Escola pública; Etnia; PPI; PCD
# e preenche seus valores com "Sim" ou "Não", de acordo com a tabela acima

def classificar_baixa_renda(cota):
    baixa_renda_categorias = ["Grupo A", "Grupo A1", "Grupo B", "Grupo B1"]

    if cota in baixa_renda_categorias:
        return "Sim"
    else:
        return "Não"

df_completo['Baixa renda'] = df_completo['COTA'].apply(classificar_baixa_renda)

def classificar_escola_publica(cota):
    escola_publica_categorias = ["Grupo A", "Grupo A1", "Grupo B", "Grupo B1", "Grupo D", "Grupo D1", "Grupo E", "Grupo E1"]

    if cota in escola_publica_categorias:
        return "Sim"
    else:
        return "Não"

df_completo['Escola pública'] = df_completo['COTA'].apply(classificar_escola_publica)

def classificar_etnia_PPI(cota):
    etnia_ppi_categorias = ["Grupo A", "Grupo A1", "Grupo D", "Grupo D1"]

    if cota in etnia_ppi_categorias:
        return "Sim"
    else:
        return "Não"

df_completo['Etnia PPI'] = df_completo['COTA'].apply(classificar_etnia_PPI)

def classificar_PCD(cota):
    pcd_categorias = ["Grupo A1", "Grupo B1", "Grupo D1", "Grupo E1"]

    if cota in pcd_categorias:
        return "Sim"
    else:
        return "Não"

df_completo['PCD'] = df_completo['COTA'].apply(classificar_PCD)

# Para visualizar os 5 primeiros registros do DataFrame completo, retire o # do início da linha abaixo

#df_completo.head()

# DataFrame somente com alunos que ingressaram de 2013 em diante

df_ingressantes_apos_2012 = df_completo.loc[(df_completo['ANO_INGRESSO'] > 2012)]

# Para visualizar os 5 primeiros registros do DataFrame somente com alunos que ingressaram de 2013 em diante, retire o # do início da linha abaixo

#df_ingressantes_apos_2012.head()

# Mantém no DataFrame df_ingressantes_apos_2012 apenas os alunos que ingressaram por SiSU ou PISM

df_ingressantes_apos_2012 = df_ingressantes_apos_2012.loc[(df_ingressantes_apos_2012['TIPO_INGRESSO'] == 'SiSU') 
            | (df_ingressantes_apos_2012['TIPO_INGRESSO'] == 'PISM') 
            | (df_ingressantes_apos_2012['TIPO_INGRESSO'] == 'SiSU VAGA OCIOSA')
            | (df_ingressantes_apos_2012['TIPO_INGRESSO'] == 'PISM VAGA OCIOSA')]

# Retira do DataFrame df_ingressantes_apos_2012 os cursos que contêm "ABI -" no nome
# REGISTRAR AQUI POR QUE RESOLVEMOS ELIMINAR ESSES REGISTROS

df_ingressantes_apos_2012 = df_ingressantes_apos_2012[~df_ingressantes_apos_2012['CURSO_NOME'].str.contains("ABI -", regex=False)]

# Retira do DataFrame df_ingressantes_apos_2012 os cursos que contêm "OPÇÃO 2º CICLO CIÊNCIAS EXATAS" no nome
# REGISTRAR AQUI POR QUE RESOLVEMOS ELIMINAR ESSES REGISTROS

df_ingressantes_apos_2012 = df_ingressantes_apos_2012[~df_ingressantes_apos_2012['CURSO_NOME'].str.contains("OPÇÃO 2º CICLO CIÊNCIAS EXATAS", regex=False)]

# Retira do DataFrame df_ingressantes_apos_2012 os cursos que contêm "BACHARELADO INTERDISCIPLINAR" no nome
# REGISTRAR AQUI POR QUE RESOLVEMOS ELIMINAR ESSES REGISTROS

df_ingressantes_apos_2012 = df_ingressantes_apos_2012[~df_ingressantes_apos_2012['CURSO_NOME'].str.contains("BACHARELADO INTERDISCIPLINAR", regex=False)]

# Retira do DataFrame df_ingressantes_apos_2012 os cursos que contêm "CIÊNCIAS EXATAS" no nome
# REGISTRAR AQUI POR QUE RESOLVEMOS ELIMINAR ESSES REGISTROS

df_ingressantes_apos_2012 = df_ingressantes_apos_2012[~df_ingressantes_apos_2012['CURSO_NOME'].str.contains("CIÊNCIAS EXATAS", regex=False)]

# DataFrame de alunos evadidos de 2013 em diante
df_evadidos = df_ingressantes_apos_2012.loc[df_ingressantes_apos_2012['SITUACAO'] == 'Evadido']

# Quantidade de evadidos por curso
qtt_evadidos_por_curso = df_evadidos['CURSO_NOME'].value_counts()

import matplotlib.pyplot as plt
import seaborn as sns

# EXPLICAR O QUE A FUNÇÃO ABAIXO FAZ 

def calcular_qtt_situacao(df_ingressantes_apos_2012, filtro, situacao):
    df = df_ingressantes_apos_2012.loc[df_ingressantes_apos_2012['SITUACAO'] == situacao]
    return df.groupby('CURSO_NOME')[filtro].value_counts()

# EXPLICAR O QUE A FUNÇÃO ABAIXO FAZ 

def evadido_vs_ingressante_por_filtro(df_ingressantes, filtro):
    #calcular uma série com o número de alunos, evadidos, número de concluídos e número de ativos
    qtt_filtro_por_curso = df_ingressantes.groupby('CURSO_NOME')[filtro].value_counts()
    qtt_evadidos_por_filtro = calcular_qtt_situacao(df_ingressantes, filtro, 'Evadido')
    qtt_concluidos_por_filtro =  calcular_qtt_situacao(df_ingressantes, filtro, 'Concluido')
    qtt_ativos_por_filtro =  calcular_qtt_situacao(df_ingressantes, filtro, 'Ativo')
    
    #cruzamento das Series criadas anterioresmente    
    df = pd.merge(qtt_filtro_por_curso, qtt_evadidos_por_filtro, 
                                      how='left', on=['CURSO_NOME', filtro], suffixes=('_total', '_evadidos')).fillna(0)
    df = pd.merge(df, qtt_concluidos_por_filtro, 
                                      how='left', on=['CURSO_NOME', filtro], suffixes=('', '_concluintes')).fillna(0)
    df = pd.merge(df, qtt_ativos_por_filtro, 
                                      how='left', on=['CURSO_NOME', filtro], suffixes=('', '_ativos')).fillna(0)
    df = df.rename(columns={'count': 'count_concluintes'}).sort_values(filtro)

    #calculando os percentuais
    df['pct_evasao'] = df['count_evadidos']/df['count_total']
    df['pct_concluido'] = df['count_concluintes']/df['count_total']
    df['pct_ativo'] = df['count_ativos']/df['count_total']
   
    return df

# EXPLICAR O QUE A FUNÇÃO FAZ 

def cota_por_curso(evadido_vs_ingressante, curso):
    
    #ax = evadido_vs_ingressante[['count_evadidos', 'count_concluintes', 'count_ativos']].loc[curso].plot(kind='bar', stacked=True, figsize=[10,6])

    st.bar_chart(df_ingressantes_apos_2012, x="ANO_INGRESSO", y=['SITUACAO'])
    
    df = evadido_vs_ingressante.loc[curso]
    
    for i, eixo_x in enumerate(ax.get_xticklabels()):
        
        linha = int(eixo_x.get_text()) if eixo_x.get_text().isdigit() else eixo_x.get_text()
        
        pct_evasao_float = df['pct_evasao'].loc[linha]
        pct_evasao_str = f"{pct_evasao_float:.2%}"
        altura_y_evadidos = df['count_evadidos'].loc[linha]
        
        pct_concluintes_float = df['pct_concluido'].loc[linha]
        pct_concluintes_str = f"{pct_concluintes_float:.2%}"
        altura_y_concluintes = df['count_concluintes'].loc[linha]
        
        pct_ativos_float = df['pct_ativo'].loc[linha]
        pct_ativos_str = f"{pct_ativos_float:.2%}"
        altura_y_ativos = df['count_ativos'].loc[linha]
        
        if pct_evasao_float >= 0.05:
            ax.annotate(pct_evasao_str, xy=(i, altura_y_evadidos), rotation=45)
        
        if pct_concluintes_float >= 0.05:
            ax.annotate(pct_concluintes_str, xy=(i, altura_y_evadidos + altura_y_concluintes), rotation=45)
            
        if pct_ativos_float >= 0.05:
            ax.annotate(pct_ativos_str, xy=(i, altura_y_evadidos + altura_y_concluintes + altura_y_ativos), rotation=45)


# Para gerar um gráfico que mostra a relação entre ingressantes e evadidos por curso, 
# incluindo qualquer outra coluna do DataFrame df_ingressantes_apos_2012,
# substitua as variáveis abaixo (coluna e curso)

coluna = "COTA"
curso = "MEDICINA"

cota_por_curso(evadido_vs_ingressante_por_filtro(df_ingressantes_apos_2012, coluna), curso)
