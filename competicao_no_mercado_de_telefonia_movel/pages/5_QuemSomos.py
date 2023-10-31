### ************************************************************************************###
### Bibliotecas necessárias ###
### ************************************************************************************###
import streamlit as st
from PIL import Image

### ************************************************************************************###
### Adicionando o título da página ###
### ************************************************************************************###
st.markdown("-------------------")
st.title("Sobre as Estrelas do Projeto")
st.markdown("<h3 style='text-align: left; color: green;'>Projeto liderado pelas seguintes mulheres maravilha:</h3>", unsafe_allow_html=True)
st.markdown("-------------------")

### ************************************************************************************###
### Adicionando IMAGEM página ###
### ************************************************************************************###

# Importar a imagem
image = Image.open("fig/mulhermaravilha.png")
left_co, cent_co,last_co = st.columns(3)
with cent_co:
    st.image(image, width=50)


### ************************************************************************************###
### Adicionando  texto no corpo da página ###
### ************************************************************************************###
# escrevendo um subtítulo na página formato h2
st.markdown("<h3 style='text-align: left; color: green;'>** BEATRIZ PIERRI**</h3>", unsafe_allow_html=True)
st.write("Formada em Direito pela Universidade Federal de Santa Catarina e especialista em Finanças, Investimentos e Riscos pela FGV. Servidora pública federal da carreira de Especialista em Políticas Públicas e Gestão Governamental, vem exercendo suas atribuições em áreas relacionadas à prestação de apoio jurídico consultivo tanto na Administração Pública Federal quanto em passagem por sociedade de economia mista no Estado de Minas Gerais (Cemig). Há 4 anos atua com análise da defesa da concorrência no Conselho Administrativo de Defesa Econômica (Cade), notadamente em análise de atos de concentração ordinários (indústria, navegação marítima, portos etc.). Aficionada por finanças e investimentos, vem se aprofundando em programação com linguagem Python e Análise de Dados, com especial interesse para a ciência de dados voltada para as área de Economia, Defesa da Concorrência e Finanças. Linkedin: https://www.linkedin.com/in/beatrizpierri ")

st.markdown("<h3 style='text-align: left; color: green;'>** FERNANDA DE CASTRO SOUZA **</h3>", unsafe_allow_html=True)
st.write("Graduada em Ciências Atuariais pela UFMG com MBA Executivo em Finanças pelo IBMEC e Mestre em Métodos Quantitativos para Decisão Econômica e Empresarial pela Universidade de Lisboa. Servidora pública federal da Agência Nacional de Saúde Suplementar – ANS desde 2007. Atualmente, ocupante do cargo de Coordenadora de Informações da Diretoria de Fiscalização, área responsável extração e análise de dados sobre reclamações de beneficiários e produção de informações estratégicas para tomadas de decisões. Tem interesse pela área de tecnologia, análise e ciências de dados.")

st.markdown("<h3 style='text-align: left; color: green;'>** GRACIELE RODRIGUES **</h3>", unsafe_allow_html=True)
st.write("Mestranda em Administração Pública. Graduada em Biblioteconomia pela Universidade de Brasília. Especialização em Auditoria Governamental. Servidora Pública Federal na Agência Nacional de Energia Elétrica – ANEEL, desde 2006. Atualmente, ocupante do cargo de Assessora Adjunta de Gestão Estratégica na STR/ANEEL. Atuante também na Coordenação de Regulação Tarifária, coordenação responsável pela regulação e definição da estrutura tarifária da distribuição e gestão de informações de mercado das distribuidoras de energia elétrica.")

st.markdown("<h3 style='text-align: left; color: green;'>** JANE ADRIANA **</h3>", unsafe_allow_html=True)
st.write("Mestre em Banco de Dados pela UnB e Graduada em Ciência da Computação pela UFMG. Especializações em Administração de Rede de computadores e Gestão Estratégica da Informação. Servidora Pública Federal. Pesquisadora com ênfase em arquitetura, inteligência, análise e banco de dados. Participação em projetos de governança, arquitetura, análise e inteligência de dados. Atualmente, ocupante do cargo de Coordenadora de Arquitetura de Dados e Colaboradora ativa das atividades desenvolvidas pelo Subcomitê Técnico subordinado ao Comitê de Governança de Dados- Decreto nº 10046. No setor privado, ocupante de cargos de Administração e Gestão de dados em empresas como BrasilTelecom/Oi e Construtel. Currículo lattes http://lattes.cnpq.br/5685310058221150 e LinkedIn: http://www.linkedin.com/in/jane-adriana0808")

st.markdown("<h3 style='text-align: left; color: green;'>** LILIAN FERNADA DANTAS NAKAYAMA**</h3>", unsafe_allow_html=True)
st.write("Graduada em Engenharia Química pela Universidade Federal de Uberlândia (UFU). Servidora Pública Federal desde 2017. Desde o início da carreira no serviço público atua em área de gestão, tendo trabalhado com gerenciamento e melhoria de processos por quatro anos, além de ter ministrado alguns cursos ligados à área. Atualmente, é ocupante do cargo de Coordenadora de inteligência de dados e otimização de processos no Gabinete da Diretoria da ANAC. No setor privado, já atuou como engenheira de processamento na empresa Cargill S/A, onde coordenava a refinaria de óleo de soja para produção de Biodiesel no Mato Grosso do Sul (MS).")


st.markdown("<h3 style='text-align: left; color: green;'>** RISLA MIRANDA **</h3>", unsafe_allow_html=True)
st.write("Servidora pública federal desde 2013. Mestra em Direitos Humanos pela UnB. Atuou em políticas públicas de audiovisual e de cultura e educação. Esteve à frente da criação, monitoramento, pesquisa e avaliação de ações do governo federal em gênero e formação. Hoje atua no Conselho Administrativo de Defesa Econômica (CADE) com política pública de concorrência. Pythonista e cientista de dados em construção, tem interesse em ciência de dados aplicada à política pública. Pesquisa audiovisual e gênero no Coletivo Arte Aberta. Tem interesse em políticas públicas de economia e gênero.")






