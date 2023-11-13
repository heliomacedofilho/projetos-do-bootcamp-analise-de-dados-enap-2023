from PIL import Image
import streamlit as st
import io

# Título
st.title("Projeto do Curso Análise de Dados (Turma Exclusiva para Mulheres) - ENAP/2023 ")
st.caption("Grupo: Análise dos dados das Instituições de Ensino Superior do Brasil")

st.markdown('---')

# Função para criar uma imagem redonda
#def imagem_redonda(path, width):
#    return f'<img src="{path}" width="{width}" style="border-radius:50%;" />'

# Função para carregar e redimensionar a imagem
def carregar_e_redimensionar_imagem(image_path, width):
    image = Image.open(image_path)
    image = image.resize((width, width))
    return image


col1, col2 = st.columns(2)

# Alana
with col1:
    image_path = "./Midia/perfil/alana.png"
    width = 180
    imagem = carregar_e_redimensionar_imagem(image_path, width)
    st.image(imagem, use_column_width=False, caption="Alana R. Ramos Vieira")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    
    #st.markdown('<hr style="border: 1px solid #ccc;">', unsafe_allow_html=True)
with col2:
    st.write("Nome: Alana R. Ramos Vieira")
    st.write("Aux. em administração - UNIFEI")
    st.write("Mestranda em Ciência e Tecnologia da Computação pela UNIFEI")
    st.write("Lattes: [http://lattes.cnpq.br/3478702303031054](http://lattes.cnpq.br/3478702303031054)")
    st.markdown('<hr style="border: 1px solid #ccc;">', unsafe_allow_html=True)


# Giana Lucca Kroth
with col1:
    #st.title("Perfil")
    image_path = "./Midia/perfil/giana.png"
    width = 180
    imagem = carregar_e_redimensionar_imagem(image_path, width)
    st.image(imagem, use_column_width=False, caption="Giana Lucca Kroth")
    #st.markdown('<hr style="border: 1px solid #ccc;">', unsafe_allow_html=True)
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
   
    

with col2:
    st.write("Nome: Giana Lucca Kroth")
    st.write("Analista de Tecnologia de Informação - UFSM - Divisão de Análise e Desenvolvimento de Sistemas")
    st.write("Mestre em Engenharia de Produção e Doutora em Administração pela UFSM")
    st.write("Lattes: [http://lattes.cnpq.br/3478702303031054](http://lattes.cnpq.br/3478702303031054)")
    st.markdown('<hr style="border: 1px solid #ccc;">', unsafe_allow_html=True)

# Gislaine Thompson dos Santos

with col1:
    image_path = "./Midia/perfil/gislaine.png"
    width = 180
    imagem = carregar_e_redimensionar_imagem(image_path, width)
    st.image(imagem, use_column_width=False, caption="Gislaine Thompson dos Santos")
    #st.markdown('<hr style="border: 1px solid #ccc;">', unsafe_allow_html=True)
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
   
with col2:
    #st.title("Perfil")
    st.write("Nome: Gislaine Thompson dos Santos")
    st.write("Enfermeira - Técnico-Administrativa em Educação na Universidade Federal do Rio Grande do Sul - UFRGS")
    st.write("Mestranda no Programa de Pós Graduação em Políticas Públicas na UFRGS")
    st.write("LinkedIn: [gislaine-thompson-0747a5277](https://www.linkedin.com/in/gislaine-thompson-0747a5277)")
    st.write("Lattes: [http://lattes.cnpq.br/4491885488972959](http://lattes.cnpq.br/4491885488972959)")

    st.markdown('<hr style="border: 1px solid #ccc;">', unsafe_allow_html=True)
#Lilian Cristine S. Menezes Dutra
with col1:
    image_path = "./Midia/perfil/lilian.png"
    width = 150
    imagem = carregar_e_redimensionar_imagem(image_path, width)
    st.image(imagem, use_column_width=False, caption="Lilian Cristine S. Menezes Dutra")
    #st.markdown('<hr style="border: 1px solid #ccc;">', unsafe_allow_html=True)
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
   
    
with col2:
    #st.title("Perfil")
    st.write("Nome: Lilian Cristine S. Menezes Dutra")
    st.write("Técnico em Tecnologia da Informação - UFRGS")
    st.write("Especialista em Gestão de TI - UFRGS")
    st.write("Email: lilian.menezes@ufrgs.br")
    st.write("LinkedIn: [lilian-menezesdutra](https://www.linkedin.com/in/lilian-menezesdutra)")
    st.write("Lattes: [http://lattes.cnpq.br/043433255803593](http://lattes.cnpq.br/043433255803593)")
    st.markdown('<hr style="border: 1px solid #ccc;">', unsafe_allow_html=True)

# Linha 5
with col1:
    image_path = "./Midia/perfil/renata.png"
    width = 180
    imagem = carregar_e_redimensionar_imagem(image_path, width)
    st.image(imagem, use_column_width=False, caption="Renata Guanaes Machado")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
   
    
with col2:
    st.write("Nome: Renata Guanaes Machado ")
    st.write("Auditora Federal de Finanças e Controle - CGU/DF")
    st.write("Mestre em Informática pela UFRJ e MBA em Ciência de Dados pela USP")
    st.write("Engenheira de Produção - UFRJ")
    st.write("LinkedIn: [rguanaes](https://www.linkedin.com/in//rguanaes/)")
    st.markdown('<hr style="border: 1px solid #ccc;">', unsafe_allow_html=True)

st.markdown('<hr style="border: 1px solid #ccc;">', unsafe_allow_html=True)





