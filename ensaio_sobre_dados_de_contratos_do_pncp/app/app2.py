#streamlit run app.py

import requests
import pickle
import streamlit as st

st.title("Ensaio sobre dados do Portal Nacional de Compras Públicas (PNCP) 🛒🛒🛒")

aba1, aba2, aba3, aba4 = st.tabs(['Adesão ao Portal', 'Publicadores de Contratos', 'Overview Fornecedores', 'Fornecedores com Sanções'])

#@st.cache(allow_output_mutation=True)  #para melhorar o desempenho da página   --deprecated!
@st.cache_data
def load_data(tipo): #carregar dados de mapas e gráficos, em formato pickle, de um repositório remoto e os organiza em uma estrutura de dicionário para posterior uso no aplicativo. 
    if tipo == 'sancoes': #Joyce
        pickle_filenames = ['sancao_barra_top10_fornecedores.pkl', 'sancao_barra_top10_orgaos.pkl', 'sancao_treemap_Uffornecedores.pkl', 'sancao_heatmap_municipiosFornecedores.pkl',
                            'sancao_lolipop_top10_fornecedores.pkl', 'sancao_treemap_fornecedoresUf.pkl', 
                            'sancao_boxplot_esferaOrgaos.pkl']
    elif tipo == 'publicadores':  #Gabi
        pickle_filenames = ['publicadores_treemap_qtde_publicador.pkl', 'publicadores_barra_publicador_ente_2.pkl',
                            'publicadores_treemap_top10_3.pkl', 'publicadores_barra_fed_outropub_4.pkl']
    elif tipo == 'adesao':  #Lia
        pickle_filenames = ['adesao_visao_geral1.pkl', 'adesao_visao_geral_por_ano_M2.pkl', 'adesao_esferas_por_mes_M3.pkl', 
                            'adesao_heatmap_muncomenv4.pkl']
                            #'adesao_heatmap_percetmunmap5.pkl', 'adesao_heatmap_estados_qtde_contratos.pkl', 'adesao_heatmap_estados_repres_percent.pkl']  #estão muito epsados e travando a página
    # elif tipo == 'fornecedores': #Monica
        #pickle_filenames = ['']
    
    url = 'https://raw.githubusercontent.com/JoyceBelga/bootcamp_PNCP/main/' 
    figures = {}
    for filename in pickle_filenames:
        response = requests.get(f'{url}{filename}', stream='True')        
        figures[filename] = pickle.load(response.raw) 
    return figures 

dic_adesao = load_data('adesao')
dic_sancoes = load_data('sancoes')
dic_publicadores = load_data('publicadores')
#dic_fornecedores = load_data('fornecedores')

with aba1: #Lia
    st.pyplot(pickle.load(open('adesao_visao_geral1.pkl','rb')))   #matplotlib!
    #st.pyplot(pickle.load(open('adesao_visao_geral_por_ano_M2.pkl','rb')))   #matplotlib!
    st.pyplot(pickle.load(open('adesao_esferas_por_mes_M3.pkl','rb')))   #matplotlib!
    st.plotly_chart(dic_adesao['adesao_heatmap_muncomenv4.pkl'])  #plotly
    # st.plotly_chart(dic_adesao['adesao_heatmap_percetmunmap5.pkl'])  #plotly
    # st.plotly_chart(dic_adesao['adesao_heatmap_estados_qtde_contratos.pkl'])  #plotly
    # st.plotly_chart(dic_adesao['adesao_heatmap_estados_repres_percent.pkl'])  #plotly
with aba2: #Gabi
    st.plotly_chart(dic_publicadores['publicadores_treemap_qtde_publicador.pkl']) #plotly
    st.plotly_chart(dic_publicadores['publicadores_barra_publicador_ente_2.pkl']) #plotly
    st.plotly_chart(dic_publicadores['publicadores_treemap_top10_3.pkl']) #plotly
    st.plotly_chart(dic_publicadores['publicadores_barra_fed_outropub_4.pkl']) #plotly
with aba3: #Monica
    st.write("[gráficos da Monica]")    
with aba4: #Joyce
    st.plotly_chart(dic_sancoes['sancao_barra_top10_fornecedores.pkl']) #plotly
    st.plotly_chart(dic_sancoes['sancao_barra_top10_orgaos.pkl']) #plotly
    st.plotly_chart(dic_sancoes['sancao_treemap_Uffornecedores.pkl']) #plotly
    st.plotly_chart(dic_sancoes['sancao_heatmap_municipiosFornecedores.pkl']) #plotly
    st.plotly_chart(dic_sancoes['sancao_lolipop_top10_fornecedores.pkl']) #plotly
    st.plotly_chart(dic_sancoes['sancao_treemap_fornecedoresUf.pkl']) #plotly
    st.plotly_chart(dic_sancoes['sancao_boxplot_esferaOrgaos.pkl'])

    

