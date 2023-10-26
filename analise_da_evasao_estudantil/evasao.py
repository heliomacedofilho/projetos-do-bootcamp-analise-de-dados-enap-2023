import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import os
import pandas as pd
import matplotlib.pyplot as plt

st.set_option('deprecation.showPyplotGlobalUse', False)

# Título do aplicativo
st.set_page_config(page_title="Evasão de alunos na UFJF", page_icon= '📚', layout="wide")
st.markdown('# Evasão de alunos na UFJF 📚')
st.markdown("---")

info = st.sidebar.selectbox('Selecione o tipo de informação:',
                                   ('ANO_INGRESSO', 'SEMESTRE_INGRESSO', 'TIPO_INGRESSO', 'COTA',\
                                    'CAMPUS', 'TURNO', 'ETNIA', 'SEXO'))


curso = st.sidebar.selectbox('Selecione o curso:',
                                   ('CIÊNCIAS BIOLÓGICAS', 'ADMINISTRAÇÃO', 'CIÊNCIAS CONTÁBEIS',
       'CIÊNCIAS ECONÔMICAS', 'DIREITO', 'FARMÁCIA', 'FISIOTERAPIA',
       'MEDICINA', 'FILOSOFIA', 'NUTRIÇÃO', 'FÍSICA', 'ODONTOLOGIA',
       'GEOGRAFIA', 'EDUCAÇÃO FÍSICA', 'HISTÓRIA', 'LETRAS', 'PEDAGOGIA',
       'SERVIÇO SOCIAL', 'ENFERMAGEM', 'ENGENHARIA CIVIL', 'PSICOLOGIA',
       'ARQUITETURA E URBANISMO', 'CIÊNCIA DA COMPUTAÇÃO',
       'ENGENHARIA DE PRODUÇÃO', 'MÚSICA', 'CIÊNCIAS EXATAS',
       'ENGENHARIA COMPUTACIONAL', 'ESTATÍSTICA', 'MATEMÁTICA', 'QUÍMICA',
       'ENGENHARIA ELÉTRICA - ENERGIA',
       'ENGENHARIA ELÉTRICA - ROBÓTICA E AUTOMAÇÃO INDUSTRIAL',
       'ENGENHARIA ELÉTRICA - SISTEMAS DE POTÊNCIA',
       'ENGENHARIA ELÉTRICA - SISTEMAS ELETRÔNICOS',
       'ENGENHARIA ELÉTRICA -  TELECOMUNICAÇÕES', 'ENGENHARIA MECÂNICA',
       'BACHARELADO INTERDISCIPLINAR EM ARTES E DESIGN',
       'CINEMA E AUDIOVISUAL', 'BACHARELADO EM ARTES VISUAIS',
       'BACHARELADO EM DESIGN', 'BACHARELADO EM MODA',
       'LICENCIATURA EM ARTES VISUAIS',
       'ENGENHARIA AMBIENTAL E SANITÁRIA',
       'BACHARELADO INTERDISCIPLINAR EM CIÊNCIAS HUMANAS',
       'CIÊNCIA DA RELIGIÃO', 'CIÊNCIAS SOCIAIS', 'TURISMO',
       'SISTEMAS DE INFORMAÇÃO', 'JORNALISMO', 'MEDICINA VETERINÁRIA',
       'LETRAS - LIBRAS', 'LICENCIATURA EM MÚSICA',
       'RÁDIO  TV E INTERNET'))


 

filepath = os.path.join(os.getcwd(), 'Dados', 'dataset_grad_pres.csv')

# Cria o DataFrame completo, com todos os dados do arquivo dataset_grad_pres.csv

df_completo = pd.read_csv(filepath, engine='python', 
                     on_bad_lines='warn', encoding='iso-8859-1', header=0, sep = ";")

df_ingressantes_apos_2012 = df_completo.loc[(df_completo['ANO_INGRESSO'] > 2012)]

df_ingressantes_apos_2012 = df_ingressantes_apos_2012.loc[(df_ingressantes_apos_2012['TIPO_INGRESSO'] == 'SiSU') 
            | (df_ingressantes_apos_2012['TIPO_INGRESSO'] == 'PISM') 
            | (df_ingressantes_apos_2012['TIPO_INGRESSO'] == 'SiSU VAGA OCIOSA')
            | (df_ingressantes_apos_2012['TIPO_INGRESSO'] == 'PISM VAGA OCIOSA')]

df_ingressantes_apos_2012 = df_ingressantes_apos_2012[~df_ingressantes_apos_2012['CURSO_NOME'].str.contains("ABI -", regex=False)]

df_ingressantes_apos_2012 = df_ingressantes_apos_2012[~df_ingressantes_apos_2012['CURSO_NOME'].str.contains("CIÊNCIAS EXATAS", regex=False)]

df_ingressantes_apos_2012 = df_ingressantes_apos_2012[~df_ingressantes_apos_2012['CURSO_NOME'].str.contains("BACHARELADO INTERDISCIPLINAR", regex=False)]


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

def cota_por_curso(evadido_vs_ingressante, curso):
    
    df = evadido_vs_ingressante.loc[curso]
    
    fig = go.Figure()

    def format_value(value):
        return "{:.1f}".format(value)

    multiplicador = 100
    df['pct_evasao'] = (df['pct_evasao']*multiplicador).apply(format_value)
    df['pct_concluido'] = (df['pct_concluido']*multiplicador).apply(format_value)
    df['pct_ativo'] = (df['pct_ativo']*multiplicador).apply(format_value)

    fig.add_trace(go.Bar(x=df.index, y=df['evadidos'], name='evadidos', text=df['pct_evasao'], textposition='inside'))
    fig.add_trace(go.Bar(x=df.index, y=df['concluidos'], name='concluidos', text=df['pct_concluido'], textposition='inside'))
    fig.add_trace(go.Bar(x=df.index, y=df['ativos'], name='ativos', text=df['pct_ativo'], textposition='inside'))
    fig.update_layout(barmode='stack', title=f'Situação x {info}')
    
    st.plotly_chart(fig)

st.write("Gráfico de Barras:")

cota_por_curso(evadido_vs_ingressante_por_filtro(df_ingressantes_apos_2012, info), curso)

