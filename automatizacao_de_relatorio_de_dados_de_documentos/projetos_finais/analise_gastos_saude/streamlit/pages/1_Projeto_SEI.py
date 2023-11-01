# pages/page1.py
import streamlit as st

st.set_page_config(page_icon=":large_blue_square:",
                   layout="wide")
st.title(':blue[Automatização de Relatório de dados de Documentos SEI] :large_blue_square:')
st.header(':blue[Automação de Relatório de dados de Documentos]', divider='rainbow')
st.caption("Projeto Final do Bootcamp de Análise de Dados - ENAP :game_die: :game_die: :game_die:")
st.caption("Turma Exclusiva para Mulheres - Outubro/2023 :cherry_blossom:")

st.subheader('Introdução', divider='rainbow')

st.markdown(
    """
    Em meados de 2017, o Governo Federal, no intuito de aperfeiçoar a gestão de processos e documentos físicos, promoveu a implementação do Sistema Eletrônico de Informações, então conhecido como SEI.
    Originalmente desenvolvido pelo Tribunal Regional Federal da 4ª Região (TRF4) como ferramenta de gestão interna que engloba conjunto de módulos e funcionalidades que promovem a eficiência administrativa, o SEI foi ganhando espaço e reconhecimento devido às suas características inovadoras e ao sucesso em sua cessão sem ônus para outras instituições, passando de um sistema eletrônico da Justiça Federal da 4ª região para ferramenta que compunha o projeto estratégico de implementação em toda a Administração Pública Federal.
    Para mais informações, acesse: [Processo Eletrônico Nacional]('https://www.gov.br/economia/pt-br/assuntos/processo-eletronico-nacional')
    """
    )
st.subheader('Finalidade / Problema', divider='rainbow')   
st.markdown(
    """
    Assim, com o uso do sistema, a redução do quantitativo de servidores públicos, a ampliação de atividades/tarefas executadas pelos servidores e a necessidade de aperfeiçoamento dos processos de trabalho, identificamos a necessidade de automação da geração de dados por meio de pesquisa de documentos no sistema SEI.
    Atualmente essa busca é realizada de forma manual e demanda vários ‘cliques’ para acessos aos dados, devido às limitações do sistema e de suas ferramentas de pesquisa, motivo pelo qual estabelecemos como objetivo precípuo a “Automatização da Pesquisa e Coleta de Dados em Documentos Estruturados(Formulários), com Geração de Planilhas/DataFrames/Dashboards/Streamlit”, de forma a auxiliar a geração de relatórios descritivos, assim como a tomada de decisões no âmbito administrativo. 
    """
    )
st.subheader('Fontes dos Dados', divider='rainbow')  
st.markdown(
        """
        - Documentos SEI em HTML; 
        - Manual da Rede de Litotecas.
        """
        )
st.subheader('Método e Metodologia', divider= 'rainbow')        
st.markdown(        
        """
        O Projeto tem como premissas a inovação por meio da automação de tarefas, economia do dinheiro público devido à otimização da utilização das ferramentas com foco em resultados, a transparência administrativa e o compartilhamento do conhecimento produzido por meio da criação de uma “Documentação específica no GITHUB”, onde o código aplicado neste projeto estará disponível para que outros servidores possam realizar adaptações.
        Programa desenvolvido em linguagem Python e com o uso das bibliotecas streamlit, selenium, requests, pandas, plotly express, folium e beautifulsoup.
        """
    )
st.subheader('Críticas aos dados', divider= 'rainbow')
st.markdown(        
        """
        Os dados são gerados em HTML, para isso foi necessário delimitar onde a informação está na página HTML, por meio do http://xpather.com/.
        Os dados retornados demandaram:
        -	a transformação do valor de resposta da TAG de Sim para valores Booleanos;
        -	a vinculação das Unidades Executoras às Litotecas responsáveis pelas amostras; e
        -	concatenar o custo internacional de empréstimo  por material requisitado.
        
Foram identificadas falhas no preenchimento do formulário por parte dos usuários, o que inviabilizou as análises inicialmente planejadas e o retorno de resultados, permitindo detectar a necessidade de aperfeiçoamento do fluxo do processo no órgão utilizado como lócus.
        """
    )