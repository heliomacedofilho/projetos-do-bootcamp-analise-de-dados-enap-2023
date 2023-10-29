import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency
import ssl

#ssl._create_default_https_context = ssl._create_unverified_context

filepath = os.path.join(os.getcwd(), 'Dados', 'dataset_tratado.csv')

#filepath = 'https://github.com/heliomacedofilho/projetos-do-bootcamp-analise-de-dados-enap-2023/blob/main/analise_da_evasao_estudantil/Dados/dataset_tratado.csv'

df_completo = pd.read_csv(filepath, engine='python', 
                     on_bad_lines='warn', header=0, sep = ",")


# ----------------- INÍCIO FILTROS DATAFRAME-------------------------------

df_ingressantes_apos_2012 = df_completo.loc[(df_completo['ANO_INGRESSO'] > 2012)]

df_ingressantes_apos_2012 = df_ingressantes_apos_2012.loc[(df_ingressantes_apos_2012['TIPO_INGRESSO'] == 'SiSU') 
            | (df_ingressantes_apos_2012['TIPO_INGRESSO'] == 'PISM')] 
#            | (df_ingressantes_apos_2012['TIPO_INGRESSO'] == 'SiSU VAGA OCIOSA')
#            | (df_ingressantes_apos_2012['TIPO_INGRESSO'] == 'PISM VAGA OCIOSA')]

df_ingressantes_apos_2012 = df_ingressantes_apos_2012[~df_ingressantes_apos_2012['CURSO_NOME'].str.contains("ABI -", regex=False)]

df_ingressantes_apos_2012 = df_ingressantes_apos_2012[~df_ingressantes_apos_2012['CURSO_NOME'].str.contains("CIÊNCIAS EXATAS", regex=False)]

df_ingressantes_apos_2012 = df_ingressantes_apos_2012[~df_ingressantes_apos_2012['CURSO_NOME'].str.contains("BACHARELADO INTERDISCIPLINAR", regex=False)]

# ----------------- FIM FILTROS DATAFRAME-------------------------------


# ----------------- INÍCIO CONFIG PAG WEB ------------------------------
# Título do aplicativo
st.set_page_config(page_title="Evasão de alunos na UFJF", page_icon= '📚', layout="wide")
st.markdown('# Evasão de alunos na UFJF 📚')
st.markdown("---")

chaves = ['ANO DE INGRESSO', 'SEMESTRE DE INGRESSO', 'TIPO DE INGRESSO', 'COTA',
       'NOME DO CURSO', 'AREA', 'SITUAÇÃO', 'MOTIVO DA SAÍDA', 'CAMPUS', 'TURNO',
       'ETNIA', 'SEXO', 'TIPO DE CURSO', 'LNG', 'LAT', 'LOCAL', 'LNG_ORGM',
       'LAT_ORGM', 'LOCAL DE ORIGEM', 'BAIXA RENDA', 'ESCOLA PÚBLICA', 'ETNIA PPI',
       'PCD', 'ESTADO']

valores = df_completo.columns

ch = {chave: valor for chave, valor in zip(chaves, valores)}

info = st.sidebar.selectbox('Selecione o tipo de informação:',
                                   ('ANO DE INGRESSO', 'SEMESTRE DE INGRESSO', 'TIPO DE INGRESSO', 'COTA',
                                    'CAMPUS', 'TURNO', 'ETNIA', 'SEXO', 'BAIXA RENDA', 'ESCOLA PÚBLICA', 
                                    'ETNIA PPI', 'PCD', 'ESTADO'))

curso = st.sidebar.selectbox('Selecione o curso:',
                                   (df_ingressantes_apos_2012['CURSO_NOME'].unique()))

st.write("Escreva o texto aqui!")

# ----------------- FIM CONFIG PAG WEB ---------------------------------


# ----------------- INÍCIO PRIMEIRO GRÁFICO ----------------------------

def calcular_qtt_situacao(df_ingressantes_apos_2012, filtro, situacao):
    df = df_ingressantes_apos_2012.loc[df_ingressantes_apos_2012['SITUACAO'] == situacao]
    return df.groupby('CURSO_NOME')[filtro].value_counts()


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
    df.columns = ['total', 'evadidos', 'concluidos', 'ativos']

    #calculando os percentuais
    df['pct_evasao'] = df['evadidos']/df['total']
    df['pct_concluido'] = df['concluidos']/df['total']
    df['pct_ativo'] = df['ativos']/df['total']
   
    return df

def format_value(value):
        return "{:.1f}".format(value)

def cota_por_curso(evadido_vs_ingressante, curso):
    
    df = evadido_vs_ingressante.loc[curso]
    
    fig = go.Figure()

    multiplicador = 100
    df['pct_evasao'] = (df['pct_evasao']*multiplicador).apply(format_value)
    df['pct_concluido'] = (df['pct_concluido']*multiplicador).apply(format_value)
    df['pct_ativo'] = (df['pct_ativo']*multiplicador).apply(format_value)

    fig.add_trace(go.Bar(x=df.index, y=df['evadidos'], name='Evadidos', text=df['pct_evasao'], textposition='inside'))
    fig.add_trace(go.Bar(x=df.index, y=df['concluidos'], name='Concluídos', text=df['pct_concluido'], textposition='inside'))
    fig.add_trace(go.Bar(x=df.index, y=df['ativos'], name='Ativos', text=df['pct_ativo'], textposition='inside'))
    fig.update_layout(barmode='stack', xaxis_title=f'{info}', title=f'SITUAÇÃO X {info}')
    
    st.plotly_chart(fig)

cota_por_curso(evadido_vs_ingressante_por_filtro(df_ingressantes_apos_2012, ch[info]), curso)

# ----------------- FIM PRIMEIRO GRÁFICO ------------------------------


# ----------------- INÍCIO TABELA QUI-QUADRADO ------------------------

df_chi2 = df_ingressantes_apos_2012.loc[df_ingressantes_apos_2012['CURSO_NOME'] == curso]

frequency_table = pd.crosstab(df_chi2[ch[info]], df_chi2['SITUACAO'], margins=False)

chi2, p, dof, expected = chi2_contingency(frequency_table)

data = {
    'Estatística': ['Qui-Quadrado', 'Valor-p', 'Graus de Liberdade'],
    'Valores': [chi2, p, int(dof)],    
}

table = pd.DataFrame(data)

st.markdown("""
<style>
div[data-testid="stTable"] table {
    width: 50%; /* Largura da tabela */
    height: 100px; /* Altura da tabela */
    overflow: auto; /* Adiciona barras de rolagem se necessário */
}
</style>
""", unsafe_allow_html=True)

st.write('Tabela Qui-Quadrado')

st.table(table)

# ----------------- FIM TABELA QUI-QUADRADO ---------------------------


# ----------------- INÍCIO SEGUNDO GRÁFICO ----------------------------

def qtt_evadidos_por_sexo(df_ingressantes_apos_2012, filtro, sexo):
    df = df_ingressantes_apos_2012.loc[df_ingressantes_apos_2012['SITUACAO'] == 'Evadido']
    df = df.loc[df_ingressantes_apos_2012['SEXO'] == sexo]
    return df.groupby('CURSO_NOME')[filtro].value_counts()

def qtt_ingressantes_por_sexo(df_ingressantes_apos_2012, filtro, sexo):
    df = df_ingressantes_apos_2012.loc[df_ingressantes_apos_2012['SEXO'] == sexo]
    return df.groupby('CURSO_NOME')[filtro].value_counts()

def evadido_vs_sexo_por_filtro(df_ingressantes, filtro, curso):
    qtt_total_feminino_por_filtro = qtt_ingressantes_por_sexo(df_ingressantes, filtro, 'F')
    qtt_total_masculino_por_filtro = qtt_ingressantes_por_sexo(df_ingressantes, filtro, 'M')
    
    qtt_feminino_por_filtro = qtt_evadidos_por_sexo(df_ingressantes, filtro, 'F')
    qtt_masculino_por_filtro = qtt_evadidos_por_sexo(df_ingressantes, filtro, 'M')
    df = pd.merge(qtt_total_feminino_por_filtro, qtt_total_masculino_por_filtro, 
                                      how='left', on=['CURSO_NOME', filtro], suffixes=('_total_feminino', '_total_masculino')).fillna(0)
    df = pd.merge(df, qtt_feminino_por_filtro, 
                                      how='left', on=['CURSO_NOME', filtro], suffixes=('', '_feminino')).fillna(0)
    df = pd.merge(df, qtt_masculino_por_filtro, 
                                      how='left', on=['CURSO_NOME', filtro], suffixes=('', '_masculino')).fillna(0)

    df = df.loc[curso].sort_index()

    df.columns = ['total_feminino', 'total_masculino', 'evadido_feminino', 'evadido_masculino']


    #calculando os percentuais
    df['pct_evasao_feminino'] = df['evadido_feminino']/df['total_feminino']
    df['pct_evasao_masculino'] = df['evadido_masculino']/df['total_masculino']

    multiplicador = 100
    df['pct_evasao_feminino'] = df['pct_evasao_feminino']*multiplicador
    df['pct_evasao_masculino'] = df['pct_evasao_masculino']*multiplicador

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df.index, y=df['pct_evasao_feminino'], mode='lines+markers', name='feminino'))
    fig.add_trace(go.Scatter(x=df.index, y=df['pct_evasao_masculino'], mode='lines+markers', name='masculino'))

    fig.update_layout(title=f'TAXA DE EVASÃO X {info}', xaxis_title=f'{info}', yaxis_title='TAXA DE EVASÃO')
    
    # Exiba o gráfico no Streamlit
    st.plotly_chart(fig)

evadido_vs_sexo_por_filtro(df_ingressantes_apos_2012, ch[info], curso)

# ----------------- FIM SEGUNDO GRÁFICO -------------------------------


# ----------------- INÍCIO TERCEIRO GRÁFICO ---------------------------

def evasao_por_grupo(df, info, subinfo):
    df = evadido_vs_ingressante_por_filtro(df, info)
    filtro_por_subinfo = df.loc[df.index.get_level_values(info) == subinfo]
    ordena_por_evasao = filtro_por_subinfo.sort_values(by=['pct_evasao'], ascending=False)
    #plot_grafico(ordena_por_evasao.index.get_level_values('CURSO_NOME'),
    #            ordena_por_evasao['pct_evasao'], subinfo)

    ordena_por_evasao['pct_evasao'] = (ordena_por_evasao['pct_evasao']*100).apply(format_value)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(x=ordena_por_evasao.index.get_level_values('CURSO_NOME'), y=ordena_por_evasao['pct_evasao'], name='taxa', text=ordena_por_evasao['pct_evasao'], textposition='inside'))

    fig.update_layout(title=f'TAXA DE EVASÃO X {info} - {subinfo}', xaxis_title=f'{info} - {subinfo}', yaxis_title='TAXA DE EVASÃO', width=1000, height=800)
    
    # Exiba o gráfico no Streamlit
    st.plotly_chart(fig)

if info == 'ANO DE INGRESSO':
    subinfo = st.selectbox('Selecione o ano: ', df_ingressantes_apos_2012['ANO_INGRESSO'].unique())
    evasao_por_grupo(df_ingressantes_apos_2012, ch[info], int(subinfo))
elif info == 'COTA':
    subinfo = st.selectbox('Selecione um grupo: ', df_ingressantes_apos_2012['COTA'].unique())
    evasao_por_grupo(df_ingressantes_apos_2012, ch[info], subinfo)
elif info == 'TIPO DE INGRESSO':
    subinfo = st.selectbox('Selecione um tipo de ingresso: ', df_ingressantes_apos_2012['TIPO_INGRESSO'].unique())
    evasao_por_grupo(df_ingressantes_apos_2012, ch[info], subinfo)
elif info == 'CAMPUS':
    subinfo = st.selectbox('Selecione um campus: ', df_ingressantes_apos_2012['CAMPUS'].unique())
    evasao_por_grupo(df_ingressantes_apos_2012, ch[info], subinfo)
elif info == 'TURNO':
    subinfo = st.selectbox('Selecione um turno: ', df_ingressantes_apos_2012['TURNO'].unique())
    evasao_por_grupo(df_ingressantes_apos_2012, ch[info], subinfo)

# ----------------- FIM TERCEIRO GRÁFICO -------------------------------
