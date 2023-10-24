import pandas as pd
import requests
import math as m
import os

#função para ler a API e jogar em um json
def read_api(url, params=None):
    response = requests.get(url, params=params) #fazendo a solicitação à API

    if response.status_code == 200: #verificando se a solicitação foi bem-sucedida
        content = response.json() #recebendo a resposta JSON
        return content
        
#fução para ler a api e jogar em um dataframe, conforme período de datas pesquisado
def leitura_api(data_inicio_pesquisa, data_fim_pesquisa):
    #definindo as variáveis iniciais necessáriaa para a url da api, além do que recebemos via parâmetro da função:
    pagina_pesquisada = "1"   #qual página eu quero ver os dados. Manter fixo, pois tenho que começar sempre da primeira página, para passar como parâmetro para a url (obrigatório)
    qtd_itens_por_pagina = "500"  #quantos dados haverá por página (500 é o máximo)
    url_inicio = f"https://pncp.gov.br/api/consulta/v1/contratos?dataInicial={data_inicio_pesquisa}&dataFinal={data_fim_pesquisa}&pagina={pagina_pesquisada}&tamanhoPagina={qtd_itens_por_pagina}" 
    
    #LENDO O JSON DA API E JOGANDO EM UM DATAFRAME 
    dic_dados_json_pagina = {}
    lista_dados_json = [] #inicializando uma lista para armazenar os dicionários de cada página
    
    #verificando quantos registros tem a consulta (da data de início a data fim) para ler todas as páginas necessárias
    #(na página 1 descobre o total de registros que haverá):
    dic_dados_json_inicio = read_api(url_inicio) #dicionario com dados só da 1ª página
    total_registros = dic_dados_json_inicio['totalRegistros']
    total_paginas = m.ceil((int(dic_dados_json_inicio['totalRegistros'])/int(qtd_itens_por_pagina))) # m.ceil: arredonda um número float sempre para cima, independente das casas decimais. Por exemplo se tiver menos registros na página que o limite de tamanho de itens da página. ie: tem 182 linhas, e pediu pra retornar 500
    print(f'total_registros: {total_registros} - qtd registros pagina: {qtd_itens_por_pagina} - total páginas: {total_paginas}')        
    
    #lendo todas as páginas e jogando em uma lista:
    if total_paginas == 1:
        lista_dados_json.append(dic_dados_json_inicio)
    else:
        for i in range(1, total_paginas+1):  
            url = f"https://pncp.gov.br/api/consulta/v1/contratos?dataInicial={data_inicio_pesquisa}&dataFinal={data_fim_pesquisa}&pagina={i}&tamanhoPagina={qtd_itens_por_pagina}"
            print(url)
            dic_dados_json_pagina = read_api(url) 
            lista_dados_json.append(dic_dados_json_pagina)
            
    # Jogando a lista em um dataframe
    df = pd.DataFrame(lista_dados_json)
    #df.iloc[0]
    #df.iloc[0]['data']
    
    #pegando apenas os cmapos de interesse no df, que é o conteúdo que está na chave 'data':
    #criando novo DataFrame a partir apenas da chave "data" de cada linha, do dataframe anterior
    df_final = pd.DataFrame([item for sublist in df['data'] for item in sublist])
    #df_final.head()
    #df_final.info()

    print("fim do processamento")
    return df_final
        
#função para gerar arquivo csv para o dataframe conforme as datas de início e fim informadas
def gera_csv(data_inicio_pesquisa, data_fim_pesquisa, df):
    #gerando o csv a partir da API
    #obs: estamos gerando o csv só para facilitar a nossa visualização, para podermos analisar os dados disponíveis no json. Mas, entendo que, para desenvolvermos o código, usaremos o dicionário acima.
    df.to_csv(f"dadosPNCP_{data_inicio_pesquisa}_{data_fim_pesquisa}.csv", index=False)  # salvando o DataFrame como um arquivo CSV O argumento 'index=False' evita que o índice seja salvo no arquivo CSV


#função para pegar os arquivos csv gerados dentro da pasta e unificá-los em um só
def une_csv():
    folderpath = os.path.join(os.getcwd(), 'dados')  #busca a pasta do projeto onde estão os arquivos
    dfs = []
    for file in os.listdir(folderpath):
         if file.endswith('.csv'):
             filepath = os.path.join(folderpath, file) #junta o nome da pasta com o nome do arquivo
             df = pd.read_csv(filepath) #header = None é apra não copiar o cabeçalho de cada csv no dataframe
             dfs.append(df)
    df_final = pd.concat(dfs) #df_final = pd.concat(dfs, ignore_index=True)  # Opcional: redefinir o índice do DataFrame final
    df_final.to_csv(f"dadosPNCP_completo.csv", index=False)  # salvando o DataFrame como um arquivo CSV O argumento 'index=False' evita que o índice seja salvo no arquivo CSV
    #return folderpath

#organiza os dados do csv compelto, pois nele havia algumas colunas com informações aninhadas (e foram separadas para melhor análise)
def trata_csv_completo():
    #lendo o arquivo CSV e carregando em um DataFrame
    df = pd.read_csv('dados/dadosPNCP_completo.csv', low_memory=False) #lowmemory = false = para corrigir o warning de tipo de dados que estava dando nas colunas abaixo
    
    #colunas com warning de tipo de dados: 8, 21, 22, 25 e 34: niFornecedorSubContratado, processo, unidadeSubRogada, receita, urlCipi
    #df.columns[17]  # coluna 18 = df.columns[17] porque o índice começa do 0
    #type(df.columns[24])
    #tentei corrigir mudando o dtype delas para string, mas ainda continou com warning em algumas.
    # por isso, usei a opção low_memory (é pior qporque consome mais memória, mas foi o jeito...:(
    
    #valores_distintos = df['categoriaProcesso'].unique()
    #valores_distintos
    
    #tratando os valores na coluna "tipoContrato" que estão no formato "{'id': 7, 'nome': 'Empenho'}", os separando em 2 novas colunas id e nome:
    #tratando os valores na coluna "categoriaProcesso" que estão no formato "{'id': 2, 'nome': 'Compras'}", os separando em 2 novas colunas id e nome:
    #tratando os valores na coluna "orgaoentidade" que estão no formato "{'cnpj': 000, 'razaoSocial': 'xxxx',...}", os separando em novas colunas correspondentes:
    #tratando os valores na coluna "unidadeOrgao" que estão no formato "{'ufNome': 'RS', 'codigoUnidade': 0000,...}", os separando em novas colunas correspondentes:
    #valores_distintos = df['categoriaProcesso'].unique()
    #print(valores_distintos)
    
    extrair_id = lambda valor: eval(valor)['id'] if valor else None # Função para extrair 'id'
    extrair_nome = lambda valor: eval(valor)['nome'] if valor else None # Função para extrair 'nome'
    extrair_cnpj = lambda valor: eval(valor)['cnpj'] if valor else None # Função para extrair 'cnpj'
    extrair_razaoSocial = lambda valor: eval(valor)['razaoSocial'] if valor else None # Função para extrair 'razaoSocial'
    extrair_poderId = lambda valor: eval(valor)['poderId'] if valor else None # Função para extrair 'poderId'
    extrair_esferaId = lambda valor: eval(valor)['esferaId'] if valor else None # Função para extrair 'esferaId'
    extrair_ufSigla = lambda valor: eval(valor)['ufSigla'] if valor else None # Função para extrair 'ufSigla'
    extrair_codigoUnidade = lambda valor: eval(valor)['codigoUnidade'] if valor else None # Função para extrair 'codigoUnidade'
    extrair_nomeUnidade = lambda valor: eval(valor)['nomeUnidade'] if valor else None # Função para extrair 'nomeUnidade'
    extrair_codigoIbge = lambda valor: eval(valor)['codigoIbge'] if valor else None # Função para extrair 'codigoIBGE'
    extrair_municipioNome = lambda valor: eval(valor)['municipioNome'] if valor else None # Função para extrair 'municipioNome'
    
    #criando as novas colunas no DataFrame
    df['tipoContrato_id'] = df['tipoContrato'].apply(extrair_id)
    df['tipoContrato_nome'] = df['tipoContrato'].apply(extrair_nome)
    df['categoriaProcesso_id'] = df['categoriaProcesso'].apply(extrair_id)
    df['categoriaProcesso_nome'] = df['categoriaProcesso'].apply(extrair_nome)
    df['orgaoEntidade_cnpj'] = df['orgaoEntidade'].apply(extrair_cnpj)
    df['orgaoEntidade_razaoSocial'] = df['orgaoEntidade'].apply(extrair_razaoSocial)
    df['orgaoEntidade_poderId'] = df['orgaoEntidade'].apply(extrair_poderId)
    df['orgaoEntidade_esferaId'] = df['orgaoEntidade'].apply(extrair_esferaId)
    df['unidadeOrgao_ufSigla'] = df['unidadeOrgao'].apply(extrair_ufSigla)
    df['unidadeOrgao_codigoUnidade'] = df['unidadeOrgao'].apply(extrair_codigoUnidade)
    df['unidadeOrgao_nomeUnidade'] = df['unidadeOrgao'].apply(extrair_nomeUnidade)
    df['unidadeOrgao_codigoIbge'] = df['unidadeOrgao'].apply(extrair_codigoIbge)
    df['unidadeOrgao_municipioNome'] = df['unidadeOrgao'].apply(extrair_municipioNome)
    
    # apagando as colunas antigas
    df.drop('tipoContrato', axis=1, inplace=True)
    df.drop('categoriaProcesso', axis=1, inplace=True)
    df.drop('orgaoEntidade', axis=1, inplace=True)
    df.drop('unidadeOrgao', axis=1, inplace=True)
    
    #df['tipoContrato_nome'][0:100]
    #df['categoriaProcesso_nome'][0:100]
    #df['orgaoEntidade_cnpj'][0:100]
    #df['unidadeOrgao_ufSigla'][0:100]
    
    df.to_csv(f"dadosPNCP_completo_tratado.csv", index=False)  # salvando o DataFrame como um arquivo CSV O argumento 'index=False' evita que o índice seja salvo no arquivo CSV
    
