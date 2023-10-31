import numpy as np
import os, pandas as pd, re
from datetime import date
import requests
import streamlit as st
import warnings
warnings.filterwarnings('ignore')
import seaborn as sns
import plotly.express as px
import plotly.express as px
import plotly.io as pio
from sklearn import preprocessing

st.set_page_config(page_title="Balanço Patrimonial do Estado do Espírito Santo 🏢", page_icon= '🏢', layout="wide")

def build_path(subfolder = 'data'):
    folderpath = os.path.join(os.getcwd(), 
                              'projeto', subfolder)
    folderpath = os.path.abspath(folderpath)
    if not os.path.exists(folderpath): 
        os.makedirs(folderpath)
    return folderpath


def get_dados_pcasp(
        filename='CPU_PCASP_2022.xlsx'):
    filepath = os.path.join(build_path(), filename)
    return pd.read_excel(filepath, sheet_name= 'Federação 2022')


pcasp = get_dados_pcasp()

pcasp = pcasp.drop(columns=['FUNÇÃO','STATUS','NATUREZA DO SALDO','CONTROLE','ÍTEM','SUBÍTEM'])

pcasp = pcasp.loc[pcasp['CLASSE'].isin([1, 2])]

pcasp['NÍVEL3'] = pcasp['CLASSE'].astype(str) + pcasp['GRUPO'].astype(str) + pcasp['SUBGRUPO'].astype(str)

pcasp['NÍVEL2'] = pcasp['CLASSE'].astype(str) + pcasp['GRUPO'].astype(str)

pcasp['NÍVEL1'] = pcasp['CLASSE'].astype(str)

pcasp_nivel_3 = pcasp.loc[(pcasp['SUBGRUPO']!= 0) & (pcasp['TÍTULO']== 0)]

pcasp_nivel_2 = pcasp.loc[(pcasp['GRUPO']!= 0) & (pcasp['SUBGRUPO']== 0)]

pcasp_nivel_1 = pcasp.loc[(pcasp['GRUPO']== 0)]

pcasp_nivel_1_2_3 = pd.concat([pcasp_nivel_1,pcasp_nivel_2,pcasp_nivel_3],axis=0)

build_path()

def get_dados_instancia(filename='instancia_MSC_API.csv'):
    filepath = os.path.join(build_path(), filename)
    return pd.read_csv(filepath, sep=';')

instancia = get_dados_instancia()

instancia = instancia.drop(columns=['tipo_matriz','cod_ibge','poder_orgao','financeiro_permanente','ano_fonte_recursos','fonte_recursos','mes_referencia','divida_consolidada','data_referencia','entrada_msc','tipo_valor','complemento_fonte'])

instancia = instancia.rename(columns={'classe_conta':'NÍVEL1', 'conta_contabil':'CONTA', 'exercicio': 'EXERCÍCIO', 'valor':'VALOR', 'natureza_conta':'NATUREZA_VALOR'})

instancia['CONTA'] = instancia['CONTA'].astype(str)

#  Multiplica por 1 - Desnecessária
instancia.loc[instancia['NÍVEL1'].isin([1]) & 
              (instancia['NATUREZA_VALOR']=='D'), 'VALOR'] = instancia['VALOR']*1

#  Multiplica por -1
instancia.loc[instancia['NÍVEL1'].isin([1]) & 
              (instancia['NATUREZA_VALOR']=='C'), 'VALOR'] = instancia['VALOR']*(-1)

#  Multiplica por 1 - Desnecessária
instancia.loc[instancia['NÍVEL1'].isin([2]) & 
              (instancia['NATUREZA_VALOR']=='C'), 'VALOR'] = instancia['VALOR']*1

#  Multiplica por -1
instancia.loc[instancia['NÍVEL1'].isin([2]) & 
              (instancia['NATUREZA_VALOR']=='D'), 'VALOR'] = instancia['VALOR']*(-1)

instancia['NÍVEL3'] = instancia['CONTA'].str.slice(0, 3)
instancia['NÍVEL2'] = instancia['CONTA'].str.slice(0,2)

coluna = [col for col in instancia if col != 'NÍVEL1'] + ['NÍVEL1']

instancia=instancia[coluna]

instancia_grouped = instancia[['VALOR']].groupby([instancia['EXERCÍCIO'], instancia['NÍVEL3'], instancia['NATUREZA_VALOR']])

instancia_soma_nivel_3 = instancia[['VALOR']].groupby([instancia['EXERCÍCIO'], instancia['NÍVEL3']]).sum()

instancia_soma_nivel_2 = instancia[['VALOR']].groupby([instancia['EXERCÍCIO'], instancia['NÍVEL2']]).sum()

instancia_soma_nivel_1 = instancia[['VALOR']].groupby([instancia['EXERCÍCIO'], instancia['NÍVEL1']]).sum()

instancia_soma_nivel_3=instancia_soma_nivel_3.reset_index(level=['NÍVEL3','EXERCÍCIO'])

instancia_soma_nivel_2 = instancia_soma_nivel_2.reset_index(level=['NÍVEL2','EXERCÍCIO'])

instancia_soma_nivel_1 = instancia_soma_nivel_1.reset_index(level=['NÍVEL1','EXERCÍCIO'])

balanco_nivel_3 = pd.merge(pcasp_nivel_3, instancia_soma_nivel_3, how='inner')

balanco_nivel_3 = balanco_nivel_3.sort_values(by=['EXERCÍCIO','CONTA'])

balanco_nivel_3 = balanco_nivel_3.drop(columns=['CLASSE','GRUPO','SUBGRUPO','TÍTULO','SUBTÍTULO'])

balanco_nivel_2 = pd.merge(pcasp_nivel_2, instancia_soma_nivel_2, how='inner')

balanco_nivel_2 = balanco_nivel_2.sort_values(by=['EXERCÍCIO','CONTA'])

balanco_nivel_2 = balanco_nivel_2.drop(columns=['CLASSE','GRUPO','SUBGRUPO','TÍTULO','SUBTÍTULO'])

instancia_soma_nivel_1['NÍVEL1'] = instancia_soma_nivel_1['NÍVEL1'].astype(str)

balanco_nivel_1 = pd.merge(pcasp_nivel_1, instancia_soma_nivel_1, how='inner')

balanco_nivel_1 = balanco_nivel_1.sort_values(by=['EXERCÍCIO','CONTA'])

balanco_nivel_1 = balanco_nivel_1.drop(columns=['CLASSE','GRUPO','SUBGRUPO','TÍTULO','SUBTÍTULO'])

balanco_123 = pd.concat([balanco_nivel_1,balanco_nivel_2,balanco_nivel_3],axis=0)

balanco_123 = balanco_123.sort_values(by=['EXERCÍCIO','CONTA'])

lista_exercicios = list(set(balanco_123['EXERCÍCIO']))

balanco_123 = balanco_123.drop(columns=['NÍVEL3','NÍVEL2','NÍVEL1'])

balanco = []
for ano in lista_exercicios:
    balanco_ano = balanco_123.loc[balanco_123['EXERCÍCIO'] == ano]
    balanco_ano = balanco_ano.rename(columns={'VALOR': f'{ano}'})
    balanco_ano = balanco_ano.drop(columns=['EXERCÍCIO'])
    balanco.append(balanco_ano)

# balanco_final = pd.merge(balanco[0], balanco[1], how='left', on=['CONTA','TÍTULO.1'])
# balanco_final = pd.merge(balanco_final, balanco[2], how='left', on=['CONTA','TÍTULO.1'])
# balanco_final = pd.merge(balanco_final, balanco[3], how='left', on=['CONTA','TÍTULO.1'])

#balanco_final = pd.merge(balanco[0], balanco[1], how='left', on=['CONTA','TÍTULO.1'])
balanco_final = pd.merge(balanco[3], balanco[2], how='left', on=['CONTA','TÍTULO.1'])

#balanco_final = pd.merge(balanco_final, balanco[2], how='left', on=['CONTA','TÍTULO.1'])
balanco_final = pd.merge(balanco_final, balanco[1], how='left', on=['CONTA','TÍTULO.1'])

#balanco_final = pd.merge(balanco_final, balanco[3], how='left', on=['CONTA','TÍTULO.1'])
balanco_final = pd.merge(balanco_final, balanco[0], how='left', on=['CONTA','TÍTULO.1'])


pd.options.display.float_format = 'R${:,.2f}'.format

balanco_final_exercicio = balanco_final.T
lista = []
for i in range(32):
    lista.append((i,list(balanco_final_exercicio.loc['TÍTULO.1'])[i]))

d = dict(lista)

balanco_final_exercicio.rename(columns = d, inplace=True)
balanco_final_exercicio = balanco_final_exercicio[2:]
balanco_final_exercicio.index.names = ['EXERCÍCIO']
balanco_final_exercicio = balanco_final_exercicio.reset_index(level=['EXERCÍCIO'])


balanco_final['CONTA'] = balanco_final['CONTA'].astype(str)
balanco_final['CLASSE'] = balanco_final['CONTA'].str.slice(0,1)

balanco_normalizado = balanco_final.copy()

st.markdown('# Balanço Patrimonial do Estado do Espírito Santo 🏢')
st.markdown("#### Série Histórica 2019-2022 a partir da MSC ")
st.markdown("---")

escolha_ente = st.sidebar.selectbox('Escolha o Ente', ('ES', ''))

st.sidebar.write("Escolha um ou mais anos")
ano2019=st.sidebar.checkbox("2019")
ano2020=st.sidebar.checkbox("2020")
ano2021=st.sidebar.checkbox("2021")
ano2022=st.sidebar.checkbox("2022")
listaAnos=[]
if ano2019:
    listaAnos.append("2019")
if ano2020:
    listaAnos.append("2020")
if ano2021:
    listaAnos.append("2021")
if ano2022:
    listaAnos.append("2022")
    

escolha_descr = st.sidebar.selectbox('Escolha os dados', balanco_123['TÍTULO.1'].unique())


# Gráfico Geral com Série histórica por contas
chart_data = pd.DataFrame(balanco_final, columns=listaAnos)
st.bar_chart(chart_data)
st.markdown("---")

#st.write(f'Ente escolhido: {escolha_ente}')    
#st.write(f'Check box marcados: {listaAnos}')
#st.write(f'Conta escolhida: {escolha_descr}')

# Gráfico Geral com Série histórica de todas as contas
st.bar_chart(balanco_final_exercicio, y=escolha_descr,x='EXERCÍCIO',color=escolha_descr)
st.markdown("---")

for ano in listaAnos:
    # Gráfico Treemap ATIVO                             
    st.header('Mapa do Ativo de ' + listaAnos[listaAnos.index(ano)])
    ativo = px.treemap(balanco_final.loc[balanco_final['CLASSE'] == '1'], 
                     path = [px.Constant("Ativo"), 'TÍTULO.1'], 
                     values = listaAnos[listaAnos.index(ano)], 
                     color_continuous_scale='RdBu',
                     color = listaAnos[listaAnos.index(ano)],             
                     color_continuous_midpoint=0)

    ativo.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    st.plotly_chart(ativo)
    
    coluna_ano = listaAnos[listaAnos.index(ano)]
    
    if balanco_final[coluna_ano].min() < 0 :
        
        listanorm = preprocessing.normalize([balanco_normalizado[coluna_ano].values.tolist()]) 
        coluna_ano = coluna_ano+'ABS'
        listanormal = listanorm-(listanorm.min()*2)
        balanco_normalizado[coluna_ano] = pd.DataFrame(listanormal).T
    
    # Gráfico Treemap PASSIVO
    st.header('Mapa do Passivo e Patrimônio Líquido de ' + listaAnos[listaAnos.index(ano)])
    passivo = px.treemap(balanco_normalizado.loc[balanco_normalizado['CLASSE'] == '2'], 
                     path = [px.Constant("Passivo"), 'TÍTULO.1'], 
                     values = coluna_ano, 
                     color_continuous_scale='RdBu',
                     color = listaAnos[listaAnos.index(ano)],             
                     color_continuous_midpoint=np.average(balanco_normalizado[coluna_ano]))

    passivo.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    st.plotly_chart(passivo)
    st.markdown("---")
    