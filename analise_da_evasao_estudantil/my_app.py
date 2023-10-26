import streamlit as st
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

    ax = evadido_vs_ingressante[['evadidos', 'concluidos', 'ativos']].loc[curso].plot(kind='bar', stacked=True, figsize=[10,6])
    
    df = evadido_vs_ingressante.loc[curso]
    
    for i, eixo_x in enumerate(ax.get_xticklabels()):
        
        linha = int(eixo_x.get_text()) if eixo_x.get_text().isdigit() else eixo_x.get_text()
        
        pct_evasao_float = df['pct_evasao'].loc[linha]
        pct_evasao_str = f"{pct_evasao_float:.2%}"
        altura_y_evadidos = df['evadidos'].loc[linha]
        
        pct_concluintes_float = df['pct_concluido'].loc[linha]
        pct_concluintes_str = f"{pct_concluintes_float:.2%}"
        altura_y_concluintes = df['concluidos'].loc[linha]
        
        pct_ativos_float = df['pct_ativo'].loc[linha]
        pct_ativos_str = f"{pct_ativos_float:.2%}"
        altura_y_ativos = df['ativos'].loc[linha]
        
        if pct_evasao_float >= 0.05:
            ax.annotate(pct_evasao_str, xy=(i, altura_y_evadidos), rotation=45)
        
        if pct_concluintes_float >= 0.05:
            ax.annotate(pct_concluintes_str, xy=(i, altura_y_evadidos + altura_y_concluintes), rotation=45)
            
        if pct_ativos_float >= 0.05:
            ax.annotate(pct_ativos_str, xy=(i, altura_y_evadidos + altura_y_concluintes + altura_y_ativos), rotation=45)
    
    st.pyplot()

st.write("Gráfico de Barras:")

cota_por_curso(evadido_vs_ingressante_por_filtro(df_ingressantes_apos_2012, info), curso)

