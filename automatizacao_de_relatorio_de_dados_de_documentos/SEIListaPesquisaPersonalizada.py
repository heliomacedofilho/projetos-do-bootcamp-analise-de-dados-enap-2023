# https://www.youtube.com/watch?v=f7Goh4LpHdM
# tasklist /fi "imagename eq chrome.exe" /v

# from urllib.error import HTTPError, URLError
# import urllib.request

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import (frame_to_be_available_and_switch_to_it)
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
# import pyperclip pode ajudar
from datetime import datetime, timedelta, date

import time, getpass, winsound

global Driver_do_Chrome
global LoginUsuario, Senha, ArqSaida, Encontrados
global TempoEsperaLogin, TempoEsperaPesquisa
global ListaRegistros

TempoEsperaLogin     = 10
TempoEsperaPesquisa  = 1

Driver_do_Chrome = 'c:/Angelica/Extracao/chromedriver.exe'
ArqSaida         = 'c:/RobosDados/Saida.csv'
LoginUsuario     = 'mdias'


def SomAvisaQueAcabou():
  for i in range(0,8):
    winsound.Beep(800, 500)
    winsound.Beep(440, 500)

def ContagemRegressiva(TempoEspera):
  frequencia = 440
  for i in range(1,TempoEspera):
    winsound.Beep(int(frequencia), 200)
    time.sleep(0.8)
    frequencia = frequencia * 1.03
# Fim ContagemRegressiva

def RemoveCaracteresNaoImprimiveis(Texto):
   newstring = ''
   for a in Texto: 
    if (a.isprintable()) == False: 
      newstring+=' '
    else: 
      newstring+= a 
   return newstring

def TiraAcentos(Texto):
   T = Texto
   CAcento = "àáâãäèéêëìíîïòóôõöùúûüÀÁÂÃÄÈÉÊËÌÍÎÒÓÔÕÖÙÚÛÜçÇñÑ"
   SAcento = "aaaaaeeeeiiiiooooouuuuAAAAAEEEEIIIOOOOOUUUUcCnN"
   Count = 0
   for a in CAcento:
      if Texto.find(a) > -1:
         T = T.replace(a,SAcento[Count])
      Count+=1
   return T

def LimpaTexto(T):
    S = RemoveCaracteresNaoImprimiveis(T)
    S = TiraAcentos(S)
    S = S.strip()
    S = S.upper()
    return S

def DigitaNaCaixaId(idCaixa, Texto):
  global browser
  Caixa = browser.find_element_by_id(idCaixa)
  Caixa.clear()
  Caixa.send_keys(Texto)
# Fim DigitaNaCaixaId

def UsuarioDigitaLoginEsenha():
  global LoginUsuario, Senha
  print('Login do SEI:')
  LoginUsuario = input()
  Senha = getpass.getpass("Digite sua senha (não vai aparecer na tela): ")

def FazLogin():
  global browser, Driver_do_Chrome, WebEspera
  global LoginUsuario, Senha
  chrome_options = webdriver.ChromeOptions()
  prefs = {"profile.default_content_setting_values.notifications" : 2}
  chrome_options.add_experimental_option("prefs",prefs)
  url = 'https://sip-pr.presidencia.gov.br/sip/login.php?sigla_orgao_sistema=PR&sigla_sistema=SEI'
  # browser = webdriver.Chrome(executable_path='c:\py\drivers\chromedriver.exe',chrome_options=chrome_options)
  browser = webdriver.Chrome(executable_path=Driver_do_Chrome,chrome_options=chrome_options)
  browser.implicitly_wait(10)
  browser.get(url)
  browser.maximize_window()
  WebEspera = WebDriverWait(browser, 20)
  
  DigitaNaCaixaId('txtUsuario', LoginUsuario)
  time.sleep(1)
  DigitaNaCaixaId('pwdSenha', Senha)
  time.sleep(1)

  # ContagemRegressiva(TempoEsperaLogin)

  LoginEnter = browser.find_element_by_id('sbmLogin')
  LoginEnter.click()
  time.sleep(2)
# Fom FazLogin()

def AvancaPagina():
  try:
    BannerPaginas = browser.find_element_by_class_name('paginas')
  except:
    return False
  ProcurarProxima = BannerPaginas.text
  if ProcurarProxima.find('xima') < 0:
    return False
  try:
    ClickProxima = browser.find_element_by_xpath('//*[@id="conteudo"]/div[2]/span[2]/a')
    ClickProxima.click()
    return True
  except:
    pass
  try:
    ClickProxima = browser.find_element_by_xpath('//*[@id="conteudo"]/div[2]/span/a')
    ClickProxima.click()
    return True
  except:
    return False
# Fim AvancaPagina

def CapturaConteudoPagina():
  global Encontrados
  listaResultados = browser.find_elements_by_class_name('resultado')
  # Agora é bem chato, porque tem que pegar os pedacinhos que interessam
  # e fatiar
  RegistroSEI = []
  for Resultado in listaResultados:
    htmlResultado = Resultado.get_attribute('outerHTML')
    soup = BeautifulSoup(htmlResultado, 'html.parser')
    htmlTexto = soup.text
    linhasTexto = htmlTexto.split('\n')
    qtdLinhas = len(linhasTexto)

    i = 0
    while linhasTexto[i] == '':
      i = i + 1 
    Posicao = linhasTexto[i].find('Nº')
    Linha = linhasTexto[i]
    Assunto  = Linha[:Posicao - 1]
    Assunto  = LimpaTexto(Assunto)
    Processo = Linha[Posicao +  3 :Posicao + 23]
    TpDoc    = Linha[Posicao + 24 :]
    TpDoc    = LimpaTexto(TpDoc)
    
    i = i + 1
    NrSEI = linhasTexto[i]
    i = i + 1
    Linha = linhasTexto[i]
    PedacoTexto = ''
    while not Linha[0:17] == 'Unidade Geradora:':
      PedacoTexto = PedacoTexto + Linha
      Linha = linhasTexto[i]
      i = i + 1
    PedacoTexto = LimpaTexto(PedacoTexto)
    UnidadeGeradora = Linha[18:]
    Linha = linhasTexto[i]
    Usuario = Linha[9:]
    i = i + 1
    Linha = linhasTexto[i]
    Data =   Linha[6:]
    Data = Data[6:10] + '-' + Data [3:5] + '-' + Data[0:2]  
    ListaRegistros.append([Processo, Assunto, TpDoc, NrSEI, PedacoTexto, UnidadeGeradora, Usuario, Data])
  winsound.Beep(1000, 200)
# fim CapturaConteudoPagina()

def ComplementaComDadosDoProcesso():
  global WebEspera

  def PegaValorCaixa(Caixa):
    ValorCaixa   = browser.find_element_by_id(Caixa)
    ValorCaixa   = ValorCaixa.get_attribute('value')
    ValorCaixa   = str(ValorCaixa)
    ValorCaixa   = LimpaTexto(ValorCaixa)
    return ValorCaixa

  def MudaJanela():
   
    def Abre_e_Fecha():
      global browser, Driver_do_Chrome, WebEspera
      # Esquisitissimo, mas tem que abrir outra janela, mesmo que seja so para fechar
      chrome_options = webdriver.ChromeOptions()
      prefs = {"profile.default_content_setting_values.notifications" : 2}
      chrome_options.add_experimental_option("prefs",prefs)
      url = 'https://sei-pr.presidencia.gov.br/sei'
      # browser = webdriver.Chrome(executable_path='c:\py\drivers\chromedriver.exe',chrome_options=chrome_options)
      browser_2 = webdriver.Chrome(executable_path=Driver_do_Chrome,chrome_options=chrome_options)
      browser_2.implicitly_wait(10)
      browser_2.get(url)
      browser_2.maximize_window()
      WebEspera = WebDriverWait(browser, 20)
      time.sleep(5)
      browser_2.close()

    winsound.Beep(800, 3000)
    # Abre_e_Fecha()
    # Lembrar da janela atual, para poder depois fechar
    
    HandleAbaAtual = browser.current_window_handle
    # Abrir uma nova aba (que para o Selenium, e o mesmo que uma janela, tem um Handle)
    browser.execute_script("window.open('https://sei-pr.presidencia.gov.br/sei/', '_blank')")
    # Aí pegamos a lista de abas, que devem ser duas: a que a gente abriu e a outra
    ListaHandles = browser.window_handles
    # Olha Aba por Aba, que sao so duas
    for Aba in ListaHandles:
      if HandleAbaAtual != Aba:
        # Lembrar da aba nova, para poder pegar o controle da mesma
        NovoHandle = Aba
      else:
        # A aba antiga pode ser fechada
        browser.close() 
    Abre_e_Fecha()
    browser.switch_to.window(NovoHandle)
    browser.get('https://sei-pr.presidencia.gov.br/sei/')

  IndiceListaRegistros = 1
  for Registro in ListaRegistros[1:]:
    Processo = Registro[0]
    DigitaNaCaixaId('txtPesquisaRapida', Processo)
    Caixa = browser.find_element_by_id('txtPesquisaRapida')
    Caixa.send_keys(Keys.ENTER)
    try:
      # Tem vezes que o SEI diz que o pedido foi recusado e vai para uma janela
      # que nao sai de jeito nenhum. Entao vamos abrir uma aba nova e fechar essa
      # janela incomoda
      WebEspera.until(frame_to_be_available_and_switch_to_it(('name','ifrVisualizacao')))
      time.sleep(2)
    except:
      browser.close()
      FazLogin()
      DigitaNaCaixaId('txtPesquisaRapida', Processo)
      Caixa = browser.find_element_by_id('txtPesquisaRapida')
      Caixa.send_keys(Keys.ENTER)

    # Ha processos que sao sigilosos, entao simplesmente nao aparece a capa
    # Temos que prever isso, senao o programa da erro
    try:
      Botoes = browser.find_elements_by_class_name('botaoSEI')
      for umBotao in Botoes:
        htmlUmBotao = umBotao.get_attribute('outerHTML')
        # print(htmlUmBotao)
        htmlUmBotao = str(htmlUmBotao)
        if htmlUmBotao.find('sei_consultar_alterar_protocolo.gif') > -1:
          umBotao.click()
          break
      # Se a caixa "Autuacao" nao existir, da erro
      Autuacao      = browser.find_element_by_id('txtDtaGeracaoExibir')
    except:
      ListaRegistros[IndiceListaRegistros] = ListaRegistros[IndiceListaRegistros] + ['Falha', '', '', '', '', '']
      Saida = open(ArqSaida, 'a', encoding="utf-8")
      Linha = '\t'.join(ListaRegistros[IndiceListaRegistros])
      Saida.write(Linha + '\n')
      Saida.close()
      IndiceListaRegistros = IndiceListaRegistros + 1
      # print('Excecao',IndiceListaRegistros)
      browser.switch_to.default_content() # saindo do frame para poder digitar outro processo
      winsound.Beep(1000, 200)
      continue
    
    Processo      = PegaValorCaixa('txtProtocoloExibir')
    Autuacao      = PegaValorCaixa('txtDtaGeracaoExibir')
    TipoProcesso  = PegaValorCaixa('hdnNomeTipoProcedimento')
    Especificacao = PegaValorCaixa('txtDescricao')

    Assuntos      = browser.find_element_by_id('selAssuntos')
    Assuntos      = Assuntos.get_attribute('outerHTML')
    soup          = BeautifulSoup(Assuntos,'html.parser')
    Lista         = soup.find_all('option')
    Assuntos = ''
    for UmAssunto in Lista:
      UmAssunto = str(UmAssunto)
      Posicao = UmAssunto.find('>')
      UmAssunto = UmAssunto[Posicao + 1 :]
      UmAssunto = UmAssunto[:len(UmAssunto)-9]
      UmAssunto = LimpaTexto(UmAssunto)
      UmAssunto = UmAssunto.replace('|',' ')
      Assuntos = Assuntos + '|' + UmAssunto
    Assuntos = Assuntos[1:]

    Interessados  = browser.find_element_by_id('selInteressadosProcedimento')
    Interessados  = Interessados.get_attribute('outerHTML')
    soup          = BeautifulSoup(Interessados,'html.parser')
    Lista         = soup.find_all('option')
    Interessados = ''
    for UmInteressado in Lista:
      UmInteressado = str(UmInteressado)
      Posicao = UmInteressado.find('>')
      UmInteressado = UmInteressado[Posicao + 1 :]
      UmInteressado = UmInteressado[:len(UmInteressado)-9]
      UmInteressado = LimpaTexto(UmInteressado)
      UmInteressado = UmInteressado.replace('|',' ')
      Interessados = Interessados + '|' + UmInteressado
    Interessados = Interessados[1:]

    Observacoes   = PegaValorCaixa('txaObservacoes')
  
    ListaRegistros[IndiceListaRegistros] = ListaRegistros[IndiceListaRegistros] + [Processo, Autuacao, TipoProcesso, Especificacao, Assuntos, Interessados, Observacoes]
    # print(ListaRegistros)
    print(IndiceListaRegistros)
    Saida = open(ArqSaida, 'a', encoding="utf-8")
    Linha = '\t'.join(ListaRegistros[IndiceListaRegistros])
    Saida.write(Linha + '\n')
    Saida.close()
    IndiceListaRegistros = IndiceListaRegistros + 1
    browser.switch_to.default_content() # saindo do frame para poder digitar outro processo
    winsound.Beep(1000, 200)
    
# fim ComplementaComDadosDoProcesso

######    MAIN  ######
UsuarioDigitaLoginEsenha()
FazLogin()
# Aqui pára e dá um tempo para o usuario fazer a pesquisa
DigitaNaCaixaId('txtPesquisaRapida', '')
ContagemRegressiva(TempoEsperaPesquisa)
print('Faça a pesquisa e em seguida aperte enter.')
input()

ListaRegistros = [['Lis_Processo','Lis_Assunto', 'Lis_TpDoc', 'Lis_NrSEI', 'Lis_PedacoTexto', 'Lis_UnidadeGeradora', 'Lis_Usuario', 'Lis_Data', \
                   'Capa_Processo','Capa_Autuacao', 'Capa_TipoProcesso', 'Capa_Especificacao', 'Capa_Assuntos', 'Capa_Interessados', 'Capa_Observacoes']]
Saida = open(ArqSaida, 'w', encoding="utf-8")
Titulo  = 'Lis_Processo\tLis_Assunto\tLis_TpDoc\tLis_NrSEI\tLis_PedacoTexto\tLis_UnidadeGeradora\tLis_Usuario\tLis_Data\t \
           Capa_Processo\tCapa_Autuacao\tCapa_TipoProcesso\tCapa_Especificacao\tCapa_Assuntos\tCapa_Interessados\tCapa_Observacoes'  
Saida.write(Titulo + '\n')
Saida.close()

# A pesquisq pode ter varias paginas.
HaMaisPaginas = True
i = 0
while  HaMaisPaginas:
  CapturaConteudoPagina()
  HaMaisPaginas = AvancaPagina()
  i+=1
  print(i)

ComplementaComDadosDoProcesso()

SomAvisaQueAcabou()
  
