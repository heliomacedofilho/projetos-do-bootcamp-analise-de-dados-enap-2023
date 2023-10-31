### ************************************************************************************###
### Bibliotecas necessárias ###
### ************************************************************************************###
import streamlit as st
from PIL import Image

### ************************************************************************************###
### Adicionando o título da página ###
### ************************************************************************************###
st.markdown("-------------------")
st.markdown("<h3 style='text-align: center; color: black;'> PAINEL PERSONALIZADO</h3>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: black;'> PARA EXIBIÇÃO DE INFORMAÇÕES</h3>", unsafe_allow_html=True)
st.markdown("-------------------")

### ************************************************************************************###
### Adicionando texto no corpo da página ###
### ************************************************************************************###
st.markdown("<h6 style='text-align: justify; color: black;'>Para dar mais transparência e publicidade à população brasileira, esta página tem por diretriz divulgar o Painel de Inteligência de Negócio (BI) para o Mercado Regulado de Telefonia Móvel. A publicação desse painel em uma página pública e centralizada visa promover uma fiscalização ativa da sociedade.</h6>", unsafe_allow_html=True)

st.markdown("<h6 style='text-align: justify; color: black;'>Ao analisarem dados, situações e desempenhos históricos e atuais, os tomadores de decisão obtém vislumbres valiosos que permitem melhor embasamento e mais assertividade em suas decisões.  Os processos de BI baseiam-se na transformação de dados em informações reais, depois em conhecimento e, por fim, em decisões que permitirão ações para o aprimoramento da telefonia móvel no território brasileiro. </h6>", unsafe_allow_html=True)




# Link para o PBI
#src="https://app.powerbi.com/view?r=eyJrIjoiMGU2Njc3NWQtZDkzNC00YWZhLWFmYmMtNDcyOTlmN2RlNjZlIiwidCI6IjlkYmE0ODBjLTRmYTctNDJmNC1iYmEzLTBmYjEzNzVmYmU1ZiJ9" 

src="https://app.powerbi.com/view?r=eyJrIjoiMzUwY2MxMTctMWZiMy00ZDc2LThlNDktZWEyYjJjOGMxYzljIiwidCI6IjlkYmE0ODBjLTRmYTctNDJmNC1iYmEzLTBmYjEzNzVmYmU1ZiJ9"

# Exiba o link de página
st.markdown(f"[Link para o Painel Mercado Regulado de Telefonia Móvel ]({src})")




