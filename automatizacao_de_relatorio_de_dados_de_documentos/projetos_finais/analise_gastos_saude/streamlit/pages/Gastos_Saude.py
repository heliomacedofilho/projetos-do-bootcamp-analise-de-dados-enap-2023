# pages/page1.py
import streamlit as st


# st.set_page_config(
#     page_title="Home",
#     page_icon="🏥",
#     layout='wide',
#     initial_sidebar_state='expanded')

st.markdown('# Gastos Hospitalares no Brasil')
st.markdown("---")
st.caption("## Projeto Final do Bootcamp de Análise de Dados - ENAP")
st.subheader("### Turma Exclusiva para Mulheres - Outubro/2023", divider='rainbow')
#st.sidebar.success("Select a page")


st.markdown(
    """
    <p style='text-align: justify;'>
    Escrever em resumo o objetivo do trabalho
    </p>

    <h3 style='text-align: justify;'>
    Fontes dos Dados
    </h3>

    <h4 style='text-align: justify;'>
    1) Dados de Gastos em Saúde
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
    foi selecionado o ano/mês de processamento. O conteúdo utilizado foi o valor total.
    </p>
    <p style='text-align: justify;'>
    [Datasus Saúde Governo Federal](https://datasus.saude.gov.br/informacoes-de-saude-tabnet/)
    </p>
    <p style='text-align: justify;'>
    1) NÓS USAMOS A VARIÁVEL GASTO TOTAL. ELA É GASTO TOTAL COM QUE? É SOMA DE 
    VALORES MONETÁRIOS? DE TODOS OS GASTOS DE QUE?
    2) MORTALIDADE = PRECISAMOS DEFINIR É UM VALOR MÉDIO (OU SOMA) DE QUE?
    3) AIH-VALOR = É SOMA (OU MÉDIA) DE QUE? VALORES MONETÁRIOS OU DE AUTORIZAÇÕES 
    DE INTERNAÇÃO?
    4) DIAS = SOMA OU MÉDIA DE DIAS DE QUE?
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
    [Portal da Transparência Governo Federal](https://api.portaldatransparencia.gov.br/swagger-ui.html)
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
    elaboradas pelo ministério da Saúde. ONDE PEGA ESSE DADO? NO TABNET?
    FALTA COLOCAR ONDE.
    </p>
    <p style='text-align: justify;'>
    O dado de população em 2022 foi obtido no Instituto Brasileiro de Geografia e Estatística - IBGE.
    </p>
    <p style="text-align: justify;">
    [Portal do IBGE](https://censo2022.ibge.gov.br/panorama/)
    </p>
    <h3 style='text-align: justify;'>
    Ferramentas Utilizadas
    </h3>
    
    <p style='text-align: justify;'>
    Programa desenvolvido em linguagem Python e com o uso das bibliotecas streamlit, pandas, plotly express.
    </p>
    """,
    unsafe_allow_html=True
)
