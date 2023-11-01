def load_data():
    figures = {'Gastos': {'UF': None, 'Município': None},
               'Gastos per capita': {'UF': None, 'Município': None}}
    de_para = {'gastos': 'Gastos', 'gastos_percapita': 'Gastos per capita',
               'UF': 'Estado', 'municipio': 'Município'}
    pickle_filenames = ['gastos-uf.pkl', 'gastos_pc-uf.pkl']
    url = 'https://github.com/heliomacedofilho/projetos-do-bootcamp-analise-de-dados-enap-2023/tree/main/automatizacao_de_relatorio_de_dados_de_documentos/analise_gastos_saude/figuras'
    for filename in pickle_filenames:
        variavel, local = filename.rstrip('.pkl').split('-')
        response = requests.get(f'{url}{filename}', stream='True')
        figures[de_para[variavel]][de_para[local]] = pickle.load(response.raw)
    return figures


load_data()

#############################

with open('../../figuras/gastos-uf.pkl', 'rb') as arquivo_pkl:
    figura = pickle.load(arquivo_pkl)

# Exiba a figura
st.pyplot(figura)


######
url = 'https://github.com/heliomacedofilho/projetos-do-bootcamp-analise-de-dados-enap-2023/tree/main/automatizacao_de_relatorio_de_dados_de_documentos/analise_gastos_saude/figuras'
response = requests.get(f'{url}{filename}', stream='True')
pickle.load(response.raw)