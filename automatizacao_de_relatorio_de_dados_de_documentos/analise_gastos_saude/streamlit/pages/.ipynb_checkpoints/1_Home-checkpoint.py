# pages/page1.py
import streamlit as st


st.set_page_config(
page_title="Home",
page_icon="🏥",
layout='wide',
initial_sidebar_state='expanded')

st.markdown('# Gastos Hospitalares no Brasil')
st.markdown("---")
st.write("## Projeto Final do Bootcamp de Análise de Dados - ENAP")
st.write("### Turma Exclusiva para Mulheres - Outubro/2023")
st.sidebar.success("Select a page")


st.markdown(
    """
    Escrever em resumo o objetivo do trabalho
    ### Fontes dos Dados
    - Os dados presentes nas análises foram extraídos do Tabnet, ferramenta desenvolvida pelo Departamento de Informação e Informática do Sistema Único de Saúde (DataSUS) da Secretaria de Informação e Saúde Digital do Ministério da Saúde (MS). Esta ferramenta abrange dados epidemiológicos, de mortalidade, da rede assistencial, de internações hospitalares, de procedimentos realizados na atenção primária, entre outras. Para este trabalho, foram usadas as informações do Sistema de Informações Hospitalares (SIH), referentes às internações hospitalares aprovadas no período de 2013 a 2022. Foram usados os dados de Autorização de Internação Hospitalar (AIH) no formato reduzido (RD) com abrangência geográfica no nível municipal. Foi selecionado para o campo linha os municípios brasileiros. Para as colunas, foi selecionado o ano/mês de processamento. O conteúdo utilizado foi o valor total dos procedimentos presentes na AIH realizados naquela internação. Esse valores são regulamentados pela Tabela Unificada de Procedimentos, Medicamentos e Órteses, Próteses e Materiais Especiais do SUS (SIGTAP).
    Fonte: https://datasus.saude.gov.br/informacoes-de-saude-tabnet/
    - API Portal da Transparência
    - IBGE - População
    ### Ferramentas Utilizadas
    Programa desenvolvido em linguagem Python e com o uso das bibliotecas streamlit, pandas, plotly express
    
"""
    )
