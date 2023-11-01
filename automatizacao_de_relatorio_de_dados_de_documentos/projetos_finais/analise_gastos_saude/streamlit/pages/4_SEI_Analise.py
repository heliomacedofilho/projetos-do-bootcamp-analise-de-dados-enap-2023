import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Analise dos dados do SEI",
                   page_icon=":large_blue_square:",
                   layout="wide")

st.header(':blue[Automação de Relatório de dados de Documentos]', divider='rainbow')
st.title("Analise dos dados do SEI")
st.caption("Projeto Final do Bootcamp de Análise de Dados - ENAP :game_die::game_die::game_die:")
st.caption("Turma Exclusiva para Mulheres - Outubro/2023 :cherry_blossom:")

st.cache_data
def gerar_df():
    df = pd.read_excel('./data/rema.xlsx',
                       engine='openpyxl')
                       #usecols='I:W')
                       #nrows=244)
    return df

df_metodos = gerar_df()

st.header("Métodos Utilizados para os Empréstimos", divider='rainbow')
st.bar_chart(df_metodos
            .reset_index()
            .melt(id_vars=["index"], value_vars=df_metodos.columns[6:22],var_name = 'Métodos Analíticos')
            .query('value == True')
            .loc[:, 'Métodos Analíticos']
            .value_counts(ascending=True))
            #title='Métodos do Empréstimo')
st.header("Finalidade dos Empréstimos", divider='rainbow')
st.line_chart(df_metodos
            .reset_index()
            .melt(id_vars=["index"], value_vars=df_metodos.columns[22:32],var_name = 'Finalidade')
            .query('value == True')
            .loc[:, 'Finalidade']
            .value_counts(ascending=True)) 
            #title='Finalidade do Empréstimo')

#st.scatter_chart(df_metodos.iloc[:, 54])
custos = df_metodos.iloc[:,52]

#_custos = (custos.style.format({"custo": 'R$ {:0.2f}'}))
#st.line_chart
st.scatter_chart(custos)


st.header("Tipo de Solicitantes", divider='rainbow')
fig = px.pie(df_metodos.iloc[:, 2].value_counts().reset_index(), values= 'count', names='Tipo de Solicitante', title='Tipo de Usuário')
#     df  
#     )
st.plotly_chart(fig)

# plt.title("Tipo Usuário")
# ax.pie(sizes, labels=labels, autopct='%1.1f%%')

# st.pyplot()


# nomes_originais = ['Gastos Hospitalares', 'Gastos Hosp. per capita', 'Mortalidade', 'Emendas Parlamentares']

# anos = ['Escolha o ano', '2014', '2015', '2016',
#         '2017', '2018', '2019', '2020', '2021', '2022']

# estados = ['Escolha um estado', 'RO', 'AC', 'AM', 'RR', 'PA', 'AP', 'TO', 'MA', 'PI', 'CE', 'RN',
#            'PB', 'PE', 'AL', 'SE', 'BA', 'MG', 'ES', 'RJ', 'SP', 'PR', 'SC',
#            'RS', 'MS', 'MT', 'GO', 'DF']

# with st.sidebar:
#     st.sidebar.header("Nível de Agregação: UF")
#     st.subheader('Seleção de Filtros')
#     fvariavel = st.selectbox('Selecione a Variável:', options=nomes_originais)
#     fano = st.selectbox('Selecione o Ano:', options=anos)
#     fuf = st.selectbox('Selecione o Estado:', options=estados)

# # filtrando a variável desejada
# nomes_alvo = ['custos', 'gastos_percapita','mortalidade', 'valor_emendas']
# mapeamento = dict(zip(nomes_originais, nomes_alvo))
# nome_alvo = mapeamento.get(fvariavel, fvariavel)
# df_filtro = df[nome_alvo]

# # filtrando ano
# # filtrando ano
# if fano != anos[0] and fuf != estados[0]:
#     dados_usuario = df.loc[(df['ano'] == int(fano)) & (df['uf'] == fuf)]
# elif fano != anos[0] and fuf == estados[0]:
#     dados_usuario = df.loc[(df['ano'] == int(fano))]
# elif fano == anos[0] and fuf != estados[0]:
#     dados_usuario = df.loc[(df['uf'] == fuf)]
# else:
#     dados_usuario = df

# col1, col2 = st.columns(2)



# with col1:
#     fig_barr_ano_uf = px.bar(dados_usuario.sort_values(by=nome_alvo, ascending=True), x='ano', y=nome_alvo, color='uf', template='plotly_dark').update_layout(
#         barmode='relative', title=fvariavel, title_x=0.5).update_layout(
#             legend_title_text='UF').update_xaxes(
#                 title='Ano', showgrid=False).update_yaxes(title=nome_alvo, showgrid=False)
#     st.plotly_chart(fig_barr_ano_uf, use_container_width=True)

# with col2:
#     fig_scatter_total = px.scatter(dados_usuario, x='ano', y=nome_alvo, title=fvariavel, template='plotly_dark').update_layout(
#         title_x=0.5).update_xaxes(
#             title = 'Ano',showgrid=False).update_yaxes(
#                 title = fvariavel, showgrid=False)
#     st.plotly_chart(fig_scatter_total, use_container_width=True)


# col3, col4 = st.columns(2)

# with col3:
#     fig_barr_ano_uf_horizontal = px.bar(dados_usuario.sort_values(by=nome_alvo, ascending=True), x=nome_alvo, y='uf', color='ano', template='plotly_dark').update_layout(
#         barmode='relative', title=fvariavel, title_x=0.5).update_layout(
#             legend_title_text='Ano').update_xaxes(
#                 title=nome_alvo, showgrid=False).update_yaxes(
#                     title='Estados', showgrid=False)
#     st.plotly_chart(fig_barr_ano_uf_horizontal, use_container_width=True)

# with col4:
#     fig_barr_ano_uf = px.line(dados_usuario, x='ano', y=nome_alvo, color='uf', template='plotly_dark').update_layout(
#         barmode='relative', title=fvariavel, title_x=0.5).update_layout(
#             legend_title_text='UF').update_xaxes(
#                 title='Ano', showgrid=False).update_yaxes(title=nome_alvo, showgrid=False)
#     st.plotly_chart(fig_barr_ano_uf, use_container_width=True)
