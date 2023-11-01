# AUTOMATIZAÇÃO DE RELATÓRIO DE DADOS DE DOCUMENTOS DO SEI

`BOOTCAMP ANÁLISE DE DADOS - TURMA EXCLUSIVA PARA MULHERES`

`ENAP-2023`

O projeto consistiu da elaboração de um script que contém passos para a automatização de login e de pesquisa de formulário no ambiente SEI, salvando os dados encontrados em uma pasta, gerando um dataframe, plotando gráficos e salvando os dados finais em uma planilha.

Para isso, foram realizados os seguintes procedimentos:

1. Automatização, por meio do Selenium, de acesso ao SEI;
2. Automatização da pesquisa avançada por um tipo específico de documento SEI (no caso é um formulário, REMA) e pelo período descrito;
3. Criação de pasta com os arquivos html resultantes da busca;
4. Raspagem dos dados relevantes dos arquivos html, com auxílio do beautifulsoup;
5. Criação de dataframe, com os dados raspados de todos os arquivos resultantes da busca, para plotagem de gráficos e auxílio na análise dos dados;
6. Criação de planilha para compilar os dados.

Ferramentas utilizadas

Programa desenvolvido em linguagem Python e com o uso das bibliotecas selenium, streamlit, statsmodels, pandas, plotly express e beautifulsoup.

--------

# Custos de Internações Hospitalares e Emendas Parlamentares Destinadas à Saúde

`BOOTCAMP ANÁLISE DE DADOS - TURMA EXCLUSIVA PARA MULHERES`

`ENAP-2023`

Este projeto consiste de um painel desenvolvido com o objetivo de fazer uma análise dos dados das internações hospitalares, disponibilizados pelo Ministério da Saúde, e verificar a sua correlação com os valores repassados aos entes por meio emendas parlamentares, conforme dados do Portal da Transparência. O período selecionado para análise foi de 2014 (início dos dados das emendas) a 2022 (ano completo mais recente).

Fontes dos dados

1) Dados em Saúde
Os dados presentes nas análises foram extraídos do Tabnet. O Tabnet é uma ferramenta desenvolvida pelo Departamento de Informação e Informática do Sistema Único de Saúde (DataSUS) da Secretaria de Informação e Saúde Digital do Ministério da Saúde (MS). Os dados aqui utilizados são:
- Autorização de Internação Hospitalar (AIH) no formato reduzido (RD) com abrangência geográfica no nível municipal;
- Taxa de Mortalidade.
<a href='https://datasus.saude.gov.br/informacoes-de-saude-tabnet'>TabNet</a> 

2) Emendas Parlamentares
Os dados das emendas parlamentares para todos os estados do Brasil foram obtidos por meio de API fornecida pelo Portal da Transparência do Governo Federal (acessada por meio de prévio cadastro e recebimento de chave de acesso). Para este projeto, os dados foram coletados compreendo os anos de 2014 a 2022, com delimitação de parâmetros: função saúde, subgrupo assistência hospitalar e ambulatorial.
<a href='https://api.portaldatransparencia.gov.br/swagger-ui.html'>Portal da Transparência do Governo Federal</a>

3) Dados de População
Os dados de população dos municípios utilizados neste trabalho, foram obtidas a partir de duas fontes. 
Para os anos de 2014 a 2021, foram utilizadas as estimativas preliminares elaboradas pelo Ministério da Saúde, disponibilizadas pelo TabNet.
Enquanto o dado de população em 2022 foi obtido no site do Instituto Brasileiro de Geografia e Estatística - IBGE.
<a href='https://censo2022.ibge.gov.br/panorama/'>Panorama Censo 2022</a>

Ferramentas utilizadas

Programa desenvolvido em linguagem Python e com o uso das bibliotecas streamlit, statsmodels, pandas, plotly express e numpy.

## INTEGRANTES

* Daiana de Paula Sales
  <a href='https://www.https://github.com/dpsales'> Github</a>
  <a href='https://www.linkedin.com/in/daiana-sales-5908a621/'> Linkedin</a>
* Harlane Araújo de Magalhães
  <a href='https://www.linkedin.com/in/harlane-magalh%C3%A3es-39443a196/'> Linkedin</a>
* Michela Barreto Camboim Gonçalves Feitosa
  <a href='https://www.https://github.com/MichelaCamboim/'> Github</a>
  <a href='https://www.linkedin.com/in/michela-camboim/'> Linkedin</a>
* Paula Bittencourt Gomes
  <a href='https://github.com/pbitgomes'> Github</a>
* Priscilla Uchoa Martins
  <a href='https://github.com/PriscillaUchoa'> Github</a>
* Rosana Elisa Gonçalves Pinho
  <a href='https://github.com/rosanagg'> Github</a>
