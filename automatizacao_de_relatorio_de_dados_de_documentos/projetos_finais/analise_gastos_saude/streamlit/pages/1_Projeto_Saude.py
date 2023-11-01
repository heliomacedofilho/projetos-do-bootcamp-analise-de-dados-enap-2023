# pages/page1.py
import streamlit as st

st.set_page_config(
    page_title="Projeto Saúde",
    page_icon="🏥",
    layout='wide')

st.markdown('# Custos de Internações Hospitalares e Emendas Parlamentares Destinadas à Saúde')
st.markdown("---")
st.write("## Projeto Final do Bootcamp de Análise de Dados - ENAP")
st.write("### Turma Exclusiva para Mulheres - Outubro/2023")

st.markdown(
    """
    <p style='text-align: justify;'>
    Este painel foi desenvolvido como projeto final do curso de análise de dados, turma exclusiva para mulheres. 
    Seu objetivo foi fazer uma análise dos dados das internações hospitalares e verificar a sua correlação com os valores repassados aos entes por emendas parlamentares. O período selecionado foi de 2014 (início dos dados das emendas) a 2022 (ano mais recente).
    </p>

    <h3 style='text-align: justify;'>
    Fontes dos Dados
    </h3>

    <h4 style='text-align: justify;'>
    1) Dados em Saúde
    </h4>
    <p style='text-align: justify;'>
    Os dados presentes nas análises foram extraídos do Tabnet. O Tabnet é uma 
    ferramenta desenvolvida pelo Departamento de Informação e Informática do Sistema 
    Único de Saúde (DataSUS) da Secretaria de Informação e Saúde Digital do Ministério
    da Saúde (MS). Esta ferramenta abrange dados epidemiológicos, de mortalidade, 
    da rede assistencial, de internações hospitalares, de procedimentos realizados 
    na atenção primária, entre outras.
    Para este trabalho, foram usadas as informações do Sistema de Informações 
    Hospitalares (SIH), referentes às internações hospitalares aprovadas no período 
    de 2014 a 2022. Foram usados os dados de Autorização de Internação Hospitalar 
    (AIH) no formato reduzido (RD) com abrangência geográfica no nível municipal. 
    Foi selecionado para o campo linha os municípios brasileiros. Para as colunas, 
    foi selecionado o ano/mês de processamento. O conteúdo utilizado foi o valor total dos 
    procedimentos presentes na AIH realizados naquela internação. Esse valores são regulamentados pela 
    Tabela Unificada de Procedimentos, Medicamentos e Órteses, Próteses e Materiais Especiais do SUS (SIGTAP).
    Foram utilizadas ainda informações sobre taxa de mortalidade, calculada pela razão entre o número de óbitos e número de internações, dada também pelo TabNet.
    </p>
    <p style='text-align: justify;'>
    Datasus Saúde Governo Federal: <a href='https://datasus.saude.gov.br/informacoes-de-saude-tabnet'>TabNet</a>
    </p>
    
    <h4 style='text-align: justify;'>
    2) Emendas Parlamentares
    </h4>
    <p style='text-align: justify;'>
    As emendas parlamentares são propostas realizadas pelos deputados para financiar 
    políticas públicas. São realizadas por meio de emendas ao projeto de Lei 
    Orçamentária Anual (LOA), que é votado anualmente pelos parlamentares e passam a 
    fazer parte do orçamento público estadual para o ano seguinte. 
    A execução orçamentária e financeira das emendas é obrigatória.
    </p>
    <p style='text-align: justify;'>
    Os dados das emendas parlamentares para todos os estados do Brasil foram obtidos 
    por meio de API fornecida pelo Portal da Transparência do Governo Federal.
    Para acessar os dados disponibilizados pela API, é necessário fazer um cadastro 
    no portal e receber uma chave de acesso.
    </p>
    <p style="text-align: justify;">
    <a href='https://api.portaldatransparencia.gov.br/swagger-ui.html'>Portal da Transparência do Governo Federal</a>
    </p>
    <p style="text-align: justify;">
    Neste projeto, os dados foram coletados para os anos de 2014 e 2022, com 
    delimitação de parâmetros: função saúde, subgrupo assistência hospitalar e 
    ambulatorial. Assim, este relatório apresenta informações sobre os valores 
    das emendas parlamentares brasileiras para financiar projetos na área de saúde, 
    especificamente, Assistência Hospitalar e Ambulatorial, abrangendo período 
    anterior e posterior à pandemia do Covid-19.
    </p>
    <h4 style='text-align: justify;'>
    3) Dados de População
    </h4>
    <p style='text-align: justify;'>
    Os dados de população dos municípios utilizados neste trabalho, foram obtidas a partir de duas 
    fontes. Para os anos de 2014 a 2021, foram utilizadas as estimativas preliminares
    elaboradas pelo Ministério da Saúde, disponibilizados pelo TabNet.
    </p>
    <p style='text-align: justify;'>
    O dado de população em 2022 foi obtido no site do Instituto Brasileiro de Geografia e Estatística - IBGE.
    </p>
    <p style="text-align: justify;">
    <a href='https://censo2022.ibge.gov.br/panorama/'>Panorama Censo 2022</a>
    </p>
    <h3 style='text-align: justify;'>
    Ferramentas Utilizadas
    </h3>
    
    <p style='text-align: justify;'>
    Programa desenvolvido em linguagem Python e com o uso das bibliotecas streamlit, statsmodels, pandas, plotly express e numpy.
    </p>
    """,
    unsafe_allow_html=True
)
