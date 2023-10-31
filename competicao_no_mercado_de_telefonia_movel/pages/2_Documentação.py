### ************************************************************************************###
### Bibliotecas necessárias ###
### ************************************************************************************###
import streamlit as st
from PIL import Image

### ************************************************************************************###
### Adicionando o título da página ###
### ************************************************************************************###

st.markdown("-------------------")
st.markdown("<h3 style='text-align: justify; color: black;'> SOBRE A DOCUMENTAÇÃO</h3>", unsafe_allow_html=True)
st.markdown("-------------------")
###************************************************************************************###

### ************************************************************************************###
### Adicionando texto no corpo da página ###
### ************************************************************************************###
st.markdown("<h4 style='text-align: justify; color: green;'> OBJETIVOS DO PROJETO</h4>", unsafe_allow_html=True)
st.markdown("- Construir uma série temporal de acessos no mercado de telefonia móvel")
st.markdown("- Identificar padrões e tendências nesse mercado")
st.markdown("- Analisar a qualidade do serviço a partir da tecnologia (4G, 3G e 2G))")
st.markdown("- Criar um relatório final com as análises realizadas e publicação dos scripts de análise")


st.markdown("<h5 style='text-align: justify; color: black;'>A documentação complementar desse projeto pode ser acessada pelos links abaixo especificados:</h5>", unsafe_allow_html=True)
st.markdown("-------------------")

# Localize o arquivo .pdf
arquivo_pdf = "./documentacao/monitoramentoFrequenciaEvasaoPresenca.pdf"


# Instruções para o usuário
st.write("Clique no botão abaixo para fazer o download do relatório do projeto no formato PDF.")

with open(arquivo_pdf, "rb") as pdf_file:
    PDFbyte = pdf_file.read()

st.download_button(label="Relatório do Projeto",
                    data=PDFbyte,
                    file_name="RelatorioProjeto.pdf",
                    mime='application/octet-stream')




