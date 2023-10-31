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
st.markdown("<h3 style='text-align: left; color: green;'>** BEATRIZ **</h3>", unsafe_allow_html=True)
st.write("Aluna Bootcamp ...")

st.markdown("<h3 style='text-align: left; color: green;'>** FERNANDA **</h3>", unsafe_allow_html=True)
st.write("Aluna Bootcamp ...")

st.markdown("<h3 style='text-align: left; color: green;'>** GRACIELE **</h3>", unsafe_allow_html=True)
st.write("Aluna Bootcamp ...")

st.markdown("<h3 style='text-align: left; color: green;'>** RISLA **</h3>", unsafe_allow_html=True)
st.write("Aluna Bootcamp ...")

st.markdown("<h3 style='text-align: left; color: green;'>** LILIAN **</h3>", unsafe_allow_html=True)
st.write("Aluna Bootcamp ...")

# escrevendo um subtítulo na página formato h2
st.markdown("<h3 style='text-align: left; color: green;'>** JANE ADRIANA **</h3>", unsafe_allow_html=True)

st.write("Mestre em Banco de Dados pela UnB e Graduada em Ciência da Computação pela UFMG. Especializações em Administração de Rede de computadores e Gestão Estratégica da Informação. Servidora Pública Federal. Pesquisadora com ênfase em arquitetura, inteligência, análise e banco de dados. Participação em projetos de governança, arquitetura, análise e inteligência de dados. Atualmente, ocupante do cargo de Coordenadora de Arquitetura de Dados e Colaboradora ativa das atividades desenvolvidas pelo Subcomitê Técnico subordinado ao Comitê de Governança de Dados- Decreto nº 10046. No setor privado, ocupante de cargos de Administração e Gestão de dados em empresas como BrasilTelecom/Oi e Construtel. Currículo lattes http://lattes.cnpq.br/5685310058221150 e LinkedIn: http://www.linkedin.com/in/jane-adriana0808")

