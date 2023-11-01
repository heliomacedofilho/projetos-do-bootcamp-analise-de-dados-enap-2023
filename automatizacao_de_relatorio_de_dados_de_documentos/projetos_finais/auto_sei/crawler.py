import os
from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import getpass
import warnings
from sqlalchemy import create_engine
from bs4 import BeautifulSoup
import re
from collections import OrderedDict
import pandas as pd

def custom_input(prompt, encrypted=False):
    pass 

def _main(_login, _password, _pasta, _nomes_arquivos, dir_saida="."):
    """
    #########################################################################
    # busca todos os arquivos período explícito sem especificar a data
    #########################################################################
    """

    def build_path(subfolder):
        current_folder = os.getcwd()
        folderpath = os.path.join(current_folder, subfolder)
        folderpath = os.path.abspath(folderpath)
        if not os.path.exists(folderpath): os.makedirs(folderpath)
        return folderpath

    # build_path('nomes_arquivos')
    # build_path('arquivos')

    driver = webdriver.Chrome()
    driver.implicitly_wait(0.5)
    url = 'https://sip.sgb.gov.br/sip/login.php?sigla_orgao_sistema=CPRM&sigla_sistema=SEI&infra_url=L3NlaS8='
    driver.get(url)

    login = driver.find_element("xpath", '//*[@id="txtUsuario"]')
    password = driver.find_element("xpath", '//*[@id="pwdSenha"]')
    submit_button = driver.find_element("xpath", '//*[@id="sbmLogin"]')

    login.send_keys(_login)
    password.send_keys(_password)
    submit_button.click()

    # home page

    searching = driver.find_element("xpath", '//*[@id="main-menu"]/li[5]/a')
    searching.click()

    # search page

    doc_type = driver.find_element("xpath", '//*[@id="selSeriePesquisa"]')
    doc_date_explicit = driver.find_element("xpath", '//*[@id="optPeriodoExplicito"]')
    sub_button = driver.find_element("xpath", '//*[@id="sbmPesquisar"]')

    doc_type.send_keys('REMA - Empréstimo de Materiais ou Ex. Geológicos')
    doc_date_explicit.click()
    sub_button.click()

    #################################################
    # 
    # getting files
        # creating folder
        
    #pasta = input('Entrar com o nome da pasta:')
    build_path(pasta)
    # 
    #nomes_arquivos = input('Entrar com o nome da pasta dos nomes')
    build_path(nomes_arquivos)

        # creating files

    today_date = datetime.now().strftime('%Y%m%d_%H%M%S')

    def get_files():

        original_window = driver.current_window_handle 
        page_docs_search = driver.find_element("xpath", '//*[@id="conteudo"]')
        page_docs = page_docs_search.text.split('Atividade Fim: ')[1:]
        
        file_name = []
        for i in range(len(page_docs)):
            a = page_docs[i].split('(REMA - Empréstimo de Materiais ou Ex. Geológicos) ')[1].split('\n1')[0]
            file_name.append(a)
        with open(os.path.join(".", nomes_arquivos, f'{today_date}.txt'), 'a') as file:
            file.write(a +'\n')
        # file.close()

        links = []
        for i in range(1, len(page_docs)+1):
            a = driver.find_element("xpath", '//*[@id="conteudo"]/table[%s]/tbody/tr[1]/td[1]/a[2]' %i)
            link = a.get_attribute('href')
            links.append(link)
        
        index = -1
        for i in links:
            index +=1
            name = file_name[index]
            driver.switch_to.new_window('tab')
            driver.get(i)
            with open(os.path.join(".", pasta, f"documento_{name}.html"), 'w', encoding='iso-8859-1') as file:
                file.write(driver.page_source)        
            driver.close()
            driver.switch_to.window(original_window)
    

    #################################################
    # pagination 

    pages = driver.find_element(by=By.CLASS_NAME, value="paginas")
    list_pages = pages.text.split(' ')[:-1]

    get_files()

    for i in range(1, len(list_pages)):
        
        try:
            next_page = driver.find_element("xpath", '//*[@id="conteudo"]/div[2]/a[%s]' %i)
            next_page.click()
            time.sleep(6)
            get_files()
        except (NameError, TypeError) as e:
            warnings.warn(f"{e.__class__.__name__}: {e}")
        time.sleep(6)          

    driver.close()
    driver.quit()    
    
    # Gravar os htmls em sqlite
    fname = [os.path.join(pasta, arq) for arq in os.listdir(pasta) if arq.endswith(".html")]

    lista_df=[]

    for i in fname:
        with open(i, "r", encoding="iso-8859-1") as f:
            soup = BeautifulSoup(f.read(), "html.parser")

        tags = [tag for tag in soup.find("div", id="conteudo").children if len(tag.text.strip()) > 0 and not re.match(r"^\d+\.", tag.text.strip())]
        # Cada HTML, um dicionário ordenado
        dict_series = OrderedDict()

        for index in range(len(tags)):
            tag = tags[index]
            
            if tag.name == "b":
                key = tag.text.strip().rstrip(":")
                value = tags[index + 1].text.strip()
                
                dict_series[key] = value


        # Empilhar todos os dicionários para criar o df e interpretar os dtypes
        df = (
            pd.DataFrame([dict_series])
                .apply(lambda x: pd.to_numeric(x.str.replace(",", "."), errors="ignore"))
                .apply(lambda x: x.replace("Sim", True).replace("Não", False))        
        )
        lista_df.append(df)
    
    out = os.path.join(dir_saida, "db.sqlite")
    db_url = out.replace("\\", "/")
    engine = create_engine(f"sqlite:///{db_url}")
    
    rema = pd.concat(lista_df, ignore_index=index)
    
    # Clean
    rema.iloc[:,37] = rema.iloc[:,37].astype('str').apply(lambda x: x.lower())

    rema.iloc[:,37] = (
        rema.iloc[:,37]
        # .replace(['geremi', '/', '-', 'sureg','/dimini/derem', 'residência de '], '')
        .replace(['lamin', 'sureg-sp', 'sp', 'sureg-sp/geremi'], 'sp')
        .replace(['geremi-be', 'sureg-be', 'sureg be','sureg_be','superintendência regional de belém','be'], 'pa')
        .replace(['geremi-bh', 'sureg-bh','belo horizonte','sureg bh', 'bh', 'digeco', 'diemge','digeom'], 'mg')
        .replace(['geremi-pa', 'sureg-pa','porto alegre',
                'superintendência regional de Porto Alegre',
                'universidade federal do rio grande do sul',
                'unisinos','ufrgs', 'rs', 'mining venture'], 'rs')
        .replace(['xxxxx','derem','nacional','0','divisão de geodinâmica - digeod'],'df')
        .replace(['sureg-ma', 'geremi-ma', 'manaus'], 'ma')
        .replace(['fortaleza','refo'], 'ce')
        .replace(['sureg-go'],'go')
        .replace(['residência de porto velho','porto velho', 'repo'], 'ro')
        .replace(['sureg-re/dimini/derem'], 'pe')
        .replace(['sureg-sa'], 'ba')
    )
    
    rema.to_sql("rema", engine, if_exists="replace")
    
    return out
    
    
if __name__ == '__main__':
    # login page
    login=input("Digite ID SEI: ")
    password=getpass.getpass("Digite sua senha: ")
    pasta=input('Entrar com o nome da pasta: ')
    nomes_arquivos = input('Entrar com o nome da pasta dos nomes: ')
    result = _main(login, password, pasta, nomes_arquivos)
    print(result)
