# pages/page1.py
import streamlit as st

# st.set_page_config(
#     page_title="Automatização de criação de Relatório oriundos de documentos SEI",
#     page_icon= ':large_blue_square:',
#     layout='wide',
#     initial_sidebar_state='expanded')
st.title(':blue[Automatização de Relatório de dados de Documentos] :large_blue_square:')
st.header(':blue[Automação de Relatório de dados de Documentos]', divider='rainbow')
st.caption("Projeto Final do Bootcamp de Análise de Dados - ENAP :game_die: :game_die: :game_die:")
st.caption("Turma Exclusiva para Mulheres - Outubro/2023 :cherry_blossom:")
#st.sidebar.success("Select a page")
#st.write('Resumo das atividades')
st.subheader('Introdução', divider='rainbow')


st.markdown(
    """
    Em meados de 2017, o Governo federal, no intuito de aperfeiçoar a gestão de processos e documentos físicos, promoveu a implementação do Sistema Eletrônico de Informações, então conhecido como (SEI).
    Originalmente desenvolvido pelo Tribunal Regional Federal da 4ª Região (TRF4) como ferramenta de gestão interna que engloba conjunto de módulos e funcionalidades que promovem a eficiência administrativa, o SEI foi ganhando espaço e reconhecimento devido às suas características inovadoras e do sucesso em sua cessão sem ônus para outras instituições, passando de um sistema eletrônico da Justiça Federal da 4ª região para ferramenta que compunha o projeto estratégico de implementação em toda a Administração Pública Federal.
    Para mais informações, acesse: https://www.gov.br/economia/pt-br/assuntos/processo-eletronico-nacional
    """
    )
st.subheader('Finalidade / Problema', divider='rainbow')   
st.markdown(
    """
    Assim, com o uso do sistema, a redução do quantitativo de servidores públicos, a ampliação de atividades/tarefas executadas pelos servidores e a necessidade de adaptação a nova realidade por meio do aperfeiçoamento dos processos de trabalho, identificamos a necessidade de automação de geração de dados por meio de buscas no sistema SEI.
    Atualmente essa busca de forma manualizada que demanda vários ‘cliques’ para acessos aos dados, devido a limitações do sistema e de suas ferramentas de busca, estabelecemos como objetivo precípuo a “Automatização da Pesquisa, Coleta de Dados em Documentos Estruturados(Formulários) com Geração de Planilhas/DataFrames/Dashboards/Streamlit”. 
    """
    )
st.subheader('Fontes dos Dados', divider='rainbow')  
st.markdown(
        """
        - Documentos SEI em html 
        - Manual da Rede de Litoteca
        """
        )
st.subheader('Método e Metodologia', divider= 'rainbow')        
st.markdown(        
        """
        O Projeto tem como premissas: a inovação por meio da automação de tarefas, economia do dinheiro público devido a otimização da utilização das ferramentas com foco em resultados, a transparência administrativa eo compartilhamento do conhecimento produzido por meio da geração de uma “Documentação específica no GITHUB”.
        Para o projeto foram utilizadas as seguintes bibliotecas:
        - Request
        - Selenium
        - BeautifulSoup
        - Streamlit
        - Pandas
        - Plotly express
        - Folium
        """
    )
st.subheader('Críticas dos dados', divider= 'rainbow')
st.markdown(        
        """
        Os dados são gerados em HTML, para isso foi necessário delimitar onde a informação está na página HTML, por meio do http://xpather.com/.
        Os dados retornados demandaram:
        -	a transformação do valor de resposta da TAG de Sim para valores Booleanos;
        -	a vinculação das Unidades Executoras às Litotecas responsáveis pelas amostras; e
        -	concatenar o custo internacional de empréstimo  por material requisitado.
        
        Foram identificadas falhas no preenchimento do formulário o que inviabilizou análises inicialmente planejadas, o retorno de resultados, permitindo detectar a necessidade de aperfeiçoamento do fluxo do processo.
        """
    )