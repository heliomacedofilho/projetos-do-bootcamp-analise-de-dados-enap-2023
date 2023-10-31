import streamlit as st
from PIL import Image



# Título e Logo
st.title("Análise de Instituições de Ensino Superior no Brasil")
col1, col2, col3 = st.columns(3)

with col1:
   st.header(" ")
with col2:
   st.header(" ")
with col3:
   image = Image.open("./Midia/enap.png")
   st.image(image)


# Introdução ao Projeto
st.header("Introdução ao Projeto")
# Breve descrição do propósito e objetivo do projeto.
st.write(" O Projeto visa analisar às Instituições de Ensino Superior (IES) no Brasil utilizando Dados Abertos disponibilizados por estruturas do Governo Federal. ")
st.write("A educação é considerada como uma estrutura social determinante para o desenvolvimento do país, da sociedade e dos indivíduos. O ensino superior, para além da formação de profissionais qualificados, proporciona o desenvolvimento de avanços científicos oriundos da pesquisa e a disseminação de conhecimentos para a sociedade, mediante ações de extensão, com grande impacto social. Portanto, a análise das Instituições de Ensino Superior no Brasil pode fornecer subsídios para fundamentação de políticas públicas e insights para problemas, bem como para divulgação de dados visando transparência na ação estatal")

# Metodologia
st.header("Metodologia")
st.write("Foi realizada uma análise descritiva de dados relacionados à distribuição geográfica das iES no Brasil, por tipo de organização e categoria administrativa. Também foram analisados os dados e distribuição geográfica dos cursos ofertados por estas instituições, oferta de matrículas e características do corpo docente e discente")
st.write("Para a realização do projeto, foram obtidos dados do Censo da Educação Superior, Indicadores Sociais do Brasil, UF e municípios e dados do Atlas do Desenvolvimento Humano. Os dados foram carregados em formato .csv e, posteriormente, passaram por um processo de limpeza e preparação, com transformação de dados, manipulação de dados ausentes e renomeação de variáveis. Após esta etapa, realizou-se a combinação e mesclagem de conjunto de dados, conforme as necessidades identificadas na etapa anterior e os objetivos do projeto.")
st.write("Os dataframes criados passaram a ser analisados de modo exploratório e plotagens, por eixos temáticos: IES, cursos, matrículas, discentes, docentes e técnicos-administrativos. Para alguns dados, foram criadas séries temporais e plotagens com dados agregados.")

# Fonte de Dados
st.header("Fonte de Dados")
st.write("**Censo da Educação Superior** - Inep, 2023 - microdados 2012 a 2022. Link: https://download.inep.gov.br/microdados/microdados_censo_da_educacao_superior_2022.zip ")
st.write("**Indicadores sociais - IBGE**. Link: https://www.ibge.gov.br/estatisticas/downloads-estatisticas.html")
st.write("**Atlas do Desenvolvimento Humano** - AtlasBR - 2010. Link: http://www.atlasbrasil.org.br/acervo/biblioteca") 
#st.write("Descrição das variáveis e o que elas representam.")

# Resultados Principais
st.header("Resultados Principais")
st.write("**Instituições** - As IES estão presentes em todos os estados do território nacional, em maior número nos estados da região sudeste do país (1.098 IES, 42,31%), condizente com a proporção populacional da região que é de aproximadamente 40 % da população total do país.")
st.write("Observa-se que das 2.595 Instituições de Ensino Superior (IES) do Brasil, há uma predominância de Faculdades (75,84%) e Centros Universitários (14,68%), totalizando 2.349 IES, ou seja, 90,52% do total de instituições no país. Ainda que dentre essas organizações estejam algumas públicas, o resultado é condizente com o encontrado na distribuição das IES por categoria administrativa, em que as instituições privadas (com e sem fim lucrativo) ocupam a proporção de 87,98% do total de IES no Brasil.")
st.write("**Cursos** - Durante a análise da série temporal de 2012 a 2022, observou-se distintos comportamentos entre Instituições públicas e privadas, revelando padrões de crescimento distintos. Enquanto as entidades públicas mantiveram um aumento constante e linear ao longo dos anos, as instituições privadas demonstraram uma dinâmica mais variada. Notavelmente, entre 2017 e 2018, houve uma inversão nesse padrão, marcando um ponto de inflexão significativo, onde as instituições privadas iniciaram um notável avanço, sinalizando uma mudança substancial na dinâmica educacional. A análise da oferta de cursos mostrou uma tendência de crescimento contínuo, com um impulso notável em torno de 2017, seguindo uma estabilização em uma escala ligeiramente menor. A predominância da oferta de cursos por entidades privadas, em especial por Faculdades e Universidades, ressaltou o papel significativo dessas instituições.")
st.write("Ao explorar as preferências acadêmicas através de um mapa de calor, observou-se uma mudança significativa nos cursos mais procurados ao longo dos anos. Em 2012, a área predominante era 'Negócios, Administração e Direito', mas em 2022, 'Saúde e Bem-Estar' emergiu como a área de maior destaque, podendo ainda ser um reflexo da massiva demanda causada durante a pandemia em 2020/2021. Essa análise destacou a capacidade adaptativa das instituições de ensino em resposta às tendências do mercado de trabalho e às preferências dos estudantes.")
st.write("**Matrículas e discentes** - Ao analisar a evolução da quantidade de ingressantes ao longo do tempo, em cursos presenciais, é possível identificar que a queda no número de matrículas é puxada pelas instituições privadas, em uma tendencia descendente desde  o ano de 2014. A análise do número de matrículas no geral, aponta uma queda de matrículas na faixa etária entre 18 e 34 anos ao longo da última década, principalmente nos últimos 5 anos. ")
st.write("**Servidores Docentes e Técnico-administrativos** - Os docentes das IES particulares são, no geral, mais novos e com escolaridade abaixo dos docentes das IES públicas. A maioria também possui jornada de trabalho menor - horista ou com jornada parcial de trabalho. Nas IES públicas, a maioria dos docentes tem doutorado e possuem jornada de trabalho integral. Em todos os casos observa-se uma predominancia de docentes brancos e do sexo masculino. Os docentes com deficiência representam apenas 0,4% do total. Concluímos que, embora se tenha políticas de inclusão, a representatividade dos docentes ainda é baixa")
st.write("Ao analisar a série temporal que abrange o período de 2012 a 2022, percebe-se que a região Sul é a que apresenta maior número de técnico-administrativos (TAEs) por alunos matriculados, impulsionado pelas instituições privadas. Entre as públicas, a região Sudeste é a que apresenta maior número de TAEs/Aluno, porém em grande queda de 2016 a 2020. Dentre as privadas, as com fins lucrativos são as que apresentam o menor numero de TAES. A relação entre homens e mulheres TAEs é bastante proporcional nas instituições públicas, e nas privadas o número de homens é um pouco maior. Quanto a escolaridade, nas privadas o maior numero de TAEs são com superior incompleto, e dos que possuem formação superior as mulheres são maioria. Nas públicas as mulheres se destacam pela maior escolaridade.")
#st.write("Breve explicação dos resultados.")

# Conclusões e Recomendações
st.header("Conclusões e Recomendações")
st.write("Nesta primeira etapa foram analisados os dados sobre as IES de forma a proporcionar um painel visual descritivo sobre as informações disponíveis em relação às instituições, cursos, matrículas e servidores.")
st.write("Recomenda-se estudos futuros que possibilitem um estudo mais complexo, como correlações e outras análises estatíticas que possam ser realizadas com os dados disponíveis.")

# Agradecimentos
st.header("Agradecimentos")
st.write("Agradecimentos especiais ao Hélio Bomfim de Macêdo Filho, Kalina Rabbani, Thais Salzer, Bruno Garcia, Fabio Paim, Ricardo de Lima, Ricardo Ferreira da Silva Cunha, Josilene Aires Moreira, Ana Lúcia Ferraz Amstalden e demais integrantes da ENAP.")


