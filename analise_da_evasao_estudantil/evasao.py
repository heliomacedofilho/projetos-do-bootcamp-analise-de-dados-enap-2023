import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency
import ssl
import numpy as np

ssl._create_default_https_context = ssl._create_unverified_context

#filepath = os.path.join(os.getcwd(), 'Dados', 'dataset_tratado_st.csv')

#url = 'https://github.com/heliomacedofilho/projetos-do-bootcamp-analise-de-dados-enap-2023/blob/main/analise_da_evasao_estudantil/Dados/dataset_tratado_st.csv'

#@st.cache_data

url = 'https://raw.githubusercontent.com/heliomacedofilho/projetos-do-bootcamp-analise-de-dados-enap-2023/e7236a97bb126ac8df02fbdee5227f21744af258/analise_da_evasao_estudantil/Dados/dataset_tratado_st.csv'

df_completo = pd.read_csv(url, engine='python', 
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
#st.markdown("---")

tab1, tab2, tab3 = st.tabs(["Análise Por Curso", "Análise Geral", 'Regressão Logística'])

chaves = ['ANO DE INGRESSO', 'SEMESTRE DE INGRESSO', 'TIPO DE INGRESSO', 'COTA',
       'NOME DO CURSO', 'AREA', 'SITUAÇÃO', 'MOTIVO DA SAÍDA', 'CAMPUS', 'TURNO',
       'ETNIA', 'SEXO', 'TIPO DE CURSO', 'LNG', 'LAT', 'LOCAL', 'LNG_ORGM',
       'LAT_ORGM', 'LOCAL DE ORIGEM', 'BAIXA RENDA', 'ESCOLA PÚBLICA', 'ETNIA PPI',
       'PCD', 'ESTADO']

valores = df_completo.columns

ch = {chave: valor for chave, valor in zip(chaves, valores)}

tipo_tab1 = ['ANO DE INGRESSO', 'SEMESTRE DE INGRESSO', 'TIPO DE INGRESSO', 'COTA',
                                    'CAMPUS', 'TURNO', 'ETNIA', 'SEXO', 'BAIXA RENDA', 'ESCOLA PÚBLICA', 
                                    'ETNIA PPI', 'PCD', 'ESTADO']

tipo_tab2 = ['ANO DE INGRESSO', 'TIPO DE INGRESSO', 'COTA', 'CAMPUS', 'TURNO']


numero_cursos = len(df_ingressantes_apos_2012['CURSO_NOME'].unique())

with tab1:
    st.header("Análise Por Curso")

    st.write(f'Bem-vindas e Bem-vindos ao painel de dados de evasão estudantil da UFJF. Aqui você vai encontrar informações sobre {str(numero_cursos)} cursos da UFJF, em uma série histórica de 2013 a 2023. Com os campos seletivos abaixo você pode selecionar o curso desejado e as informações que você deseja explorar como, forma de ingresso, tipos de cota de ingresso, questões sociais como sexo, etnia, renda e se o estudante é ou não oriundo de escola pública em sua educação básica. Uma vez selecionados os parâmetros, você visualizará dois gráficos: (i) um gráfico de barras com as informações de porcentagem de alunos evadidos, concluídos e ativos no curso escolhido, com informações da estatística de qui-quadrado dessas proporções; (ii) um gráfico de linhas com as informações de proporção de evadidos separados por sexo feminino e masculino.')

    info = st.selectbox('Selecione o tipo de informação:',
                                   (np.sort(tipo_tab1)))

    curso = st.selectbox('Selecione o curso:',
                                   (np.sort(df_ingressantes_apos_2012['CURSO_NOME'].unique())))
    
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
    
        fig.add_trace(go.Bar(x=df.index, y=df['evadidos'], name='Evadidos (%)', text=df['pct_evasao'], textposition='inside'))
        fig.add_trace(go.Bar(x=df.index, y=df['concluidos'], name='Concluídos (%)', text=df['pct_concluido'], textposition='inside'))
        fig.add_trace(go.Bar(x=df.index, y=df['ativos'], name='Ativos (%)', text=df['pct_ativo'], textposition='inside'))
        fig.update_layout(barmode='stack', xaxis_title=f'{info}', yaxis_title= 'NÚMERO DE ALUNOS', title=f'SITUAÇÃO X {info} - {curso}')
        
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

    valorp = table.loc[1, 'Valores']

    if valorp <= 0.05:
        st.write(f'A estatística de Qui-quadrado indica, com nível de confiança de 95%, que o fator {info} influencia na taxa de evasão do curso {curso}.')
    else:
        st.write(f'A estatística de Qui-quadrado indica que o fator {info} não influencia na taxa de evasão do curso {curso}.')
    
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
    
        fig.add_trace(go.Scatter(x=df.index, y=df['pct_evasao_feminino'], mode='lines+markers', line=dict(color='MediumSeaGreen'), marker=dict(size=8), name = 'Feminino (%)'))
        fig.add_trace(go.Scatter(x=df.index, y=df['pct_evasao_masculino'], mode='lines+markers', line=dict(color='SteelBlue'), marker=dict(size=8), name='Masculino (%)'))
    
        fig.update_layout(title=f'TAXA DE EVASÃO X {info} - {curso}', xaxis_title=f'{info}', yaxis_title='TAXA DE EVASÃO')
        
        # Exiba o gráfico no Streamlit
        st.plotly_chart(fig)
    
    evadido_vs_sexo_por_filtro(df_ingressantes_apos_2012, ch[info], curso)
    
    # ----------------- FIM SEGUNDO GRÁFICO -------------------------------


with tab2:
    st.header("Análise Geral")

    st.write('No gráfico abaixo, trazemos informações de cunho mais geral sobre as proporções de alunos evadidos da UFJF. Na caixa de seleção abaixo, você pode filtrar as informações que deseja visualizar, como o gráfico geral de evadidos por curso, e os gráficos com os demais parâmetros de análise: ingresso, renda, etnia, cota, sexo e outras. As informações trazidas aqui são o somatório de todos os cursos da UFJF que foram selecionados para a análise e respeitando a série temporal dos últimos 10 anos.')

    info = st.selectbox('Selecione o tipo de informação:',
                                   (np.sort(tipo_tab2)))

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
        arr = df_ingressantes_apos_2012['COTA'].dropna().unique()
        subinfo = st.selectbox('Selecione um grupo: ', np.sort(arr))
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

with tab3:
    st.header("Regressão Logística")


    # ----------------- INÍCIO REGRESSÃO LOGÍSTICA ------------------------

    curso_rl = st.selectbox('Selecione o curso desejado:',
                                   (np.sort(df_ingressantes_apos_2012['CURSO_NOME'].unique())))

    st.write(f'**REGRESSÃO LOGÍSTICA - {curso_rl}**')
    st.write('A regressão logística é um método de análise estatística usado para prever uma variável de resultado binária com base em uma ou mais variáveis independentes.')
    st.write('Matriz de Confusão:')
    st.write('Uma matriz de confusão é uma tabela usada para avaliar o desempenho do modelo de classificação. Ela resume o número de observações classificadas corretamente e incorretamente pelo modelo.')

    from sklearn.preprocessing import LabelEncoder
    encoder = LabelEncoder()

    df = df_ingressantes_apos_2012.loc[(df_ingressantes_apos_2012['ANO_INGRESSO'] < 2019)]
    df = df.loc[(df['SITUACAO'] != 'Ativo')]
    df['BAIXA_RENDA_Encoded'] = encoder.fit_transform(df['BAIXA_RENDA'])
    df['ESCOLA_PUBLICA_Encoded'] = encoder.fit_transform(df['ESCOLA_PUBLICA'])
    df['ETNIA_PPI_Encoded'] = encoder.fit_transform(df['ETNIA_PPI'])
    df['PCD_Encoded'] = encoder.fit_transform(df['PCD'])
    df['SEXO_Encoded'] = encoder.fit_transform(df['SEXO'])
    df['ANO_INGRESSO_Encoded'] = encoder.fit_transform(df['ANO_INGRESSO'])
    df['TIPO_INGRESSO_Encoded'] = encoder.fit_transform(df['TIPO_INGRESSO'])
    df['CAMPUS_Encoded'] = encoder.fit_transform(df['CAMPUS'])
    df['TURNO_Encoded'] = encoder.fit_transform(df['TURNO'])
    df['SITUACAO_Encoded'] = encoder.fit_transform(df['SITUACAO'])

    df_filtro = df.loc[df['CURSO_NOME'] == curso_rl]

    X = df_filtro[['BAIXA_RENDA_Encoded', 'ESCOLA_PUBLICA_Encoded', 'ETNIA_PPI_Encoded', 'PCD_Encoded', 'SEXO_Encoded',
                  'ANO_INGRESSO_Encoded', 'TIPO_INGRESSO_Encoded', 'CAMPUS_Encoded', 'TURNO_Encoded']]
    y = df_filtro['SITUACAO_Encoded']

    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, ConfusionMatrixDisplay 
    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Inicializando o modelo de regressão logística
    model = LogisticRegression()
    
    # Treinando o modelo com os dados de treinamento
    model.fit(X_train, y_train)
    
    # Fazendo previsões com o conjunto de teste
    y_pred = model.predict(X_test)
    
    # Avaliando a precisão do modelo
    accuracy = accuracy_score(y_test, y_pred)

    # Calcule a matriz de confusão
    conf_matrix = confusion_matrix(y_test, y_pred)
    #st.write('Matriz de Confusão:')
    #st.text(conf_matrix)
    
    # Exiba um relatório de classificação
    #report = classification_report(y_test, y_pred)
    #st.write('Relatório de Classificação:')
    #st.text(report)

    # Criar a representação gráfica da matriz de confusão
    #fig, ax = plt.subplots(figsize=(0.8, 0.6), dpi=150)
    #disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix)
    #disp.plot(cmap="Blues", ax=ax)

    from mlxtend.plotting import plot_confusion_matrix
    
    
    # Classes
    classes = ['Concluído', 'Evadido']
    
    fig, ax = plot_confusion_matrix(conf_mat = conf_matrix,
                                       class_names = classes,
                                       show_absolute = True,
                                       show_normed = False,
                                       colorbar = True)


    # Exibir a matriz de confusão no Streamlit
#    st.pyplot(fig)

    col1, col2 = st.columns(2)

    with col1:
        
        st.pyplot(fig)
        st.write("Acurácia do modelo: {:.2f}".format(accuracy))

    with col2:
        st.header("")


#    with col3:
#        st.header("")


    # ----------------- FIM REGRESSÃO LOGÍSTICA ---------------------------
