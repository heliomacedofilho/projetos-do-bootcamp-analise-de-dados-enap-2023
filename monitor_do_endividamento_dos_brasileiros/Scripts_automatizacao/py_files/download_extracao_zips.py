#!/usr/bin/env python
# coding: utf-8
import zipfile
import os
import requests
import datetime
import subprocess
import shutil
import pandas

            
#cron
#*/1 * * * * cd ~/Projects/monitor/py_files/ && ~/Projects/monitor/venv/bin/python3 ~/Projects/monitor/py_files/download_extracao_zips.py >> ~/Projects/monitor/py_files/log.txt 2>&1

#*/1 * * * * cd ~/monitor/py_files/ && ~/monitor/venv/bin/python3 ~/monitor/py_files/download_extracao_zips.py >> ~/monitor/py_files/log.txt 2>&1

diretorio_gerador_csv = "~/Projects/monitor/py_files/"
diretorio_streamlit = "~/Projects/cron_test/"
diretorio_pyhon = '~/Projects/monitor/venv/bin/python3'

diretorio_gerador_csv = "~/monitor/py_files/"
diretorio_streamlit = "~/monitor/"
diretorio_pyhon = '~/monitor/venv/bin/python3'

#monitor/py_files

diretorio_gerador_csv = os.path.expanduser(diretorio_gerador_csv)
diretorio_streamlit = os.path.expanduser(diretorio_streamlit)
diretorio_pyhon = os.path.expanduser(diretorio_pyhon)


def buscar_arquivos_csv():

    # Lista para armazenar os nomes dos arquivos .csv
    arquivos_csv = []

    # Percorre todos os arquivos e pastas no diretório
    for arquivo in os.listdir(diretorio_gerador_csv):
        # Verifica se o arquivo termina com .csv
        if arquivo.endswith(".csv"):
            arquivos_csv.append(arquivo)

    # Imprime a lista dos arquivos .csv
    for arquivo_csv in arquivos_csv:
        copiar_csv(arquivo_csv)


def copiar_csv(arquivo):
    # Copiando o arquivo
    shutil.copy(diretorio_gerador_csv + arquivo, diretorio_streamlit + arquivo)


def git_add_commit_push(message):
    token = ''
    if os.path.exists(diretorio_gerador_csv + 'token'):
        with open(os.path.join(diretorio_gerador_csv, 'token'), 'r') as arquivo:
            token = arquivo.readline().strip()
    url_repositorio_original = "https://github.com/monitordoendividamento/monitor.git"
    url_com_token = url_repositorio_original.replace('https://', f'https://{token}@')
    try:
         # Configura a URL do repositório remoto com o token
        subprocess.run(["git", "-C", diretorio_streamlit, "remote", "set-url", "origin", url_com_token], check=True)

        # Navega até o diretório do repositório
        subprocess.run(["git", "-C", diretorio_streamlit, "add", "."], check=True)

        # Commit com a mensagem fornecida
        subprocess.run(["git", "-C", diretorio_streamlit, "commit", "-am", message], check=True)

        # Push para o repositório remoto
        subprocess.run(["git", "-C", diretorio_streamlit, "push", "origin" , "main"], check=True)
        print("Git add, commit e push realizados com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar comandos do Git: {e}")


def rodar_geradores_csv():
    #scripts = ['teste1.py', 'teste2.py', 'teste3.py']
    scripts = ["df_corr_ibge_scr_pj.py", "df_corr_porte_pf.py", "pf_juros_inflacao_modalidade_endividamentolp.py",
               "pf_ocupacao_modalidade_endividamento.py", "pf_porte_endividamentolp_desemprego.py",
               "pf_rendimento_modalidade_noperacoes_endividamento.py", "PJ_agro.py", "PJ_micro_peq_problematico.py",
               "pj_porte_modalidade_endividamentocp.py", "pf_modalidade_endividamentolp_inflacao.py",
               "pf_modalidade_endividamentolp_juros.py", "pf_porte_endividamentolp_inflacao.py",
               "pf_pj_uf_ocupacao_ativoproblematico-mapas.py"]
    # scripts = [scripts[0]]
    for script in scripts:
        script = diretorio_gerador_csv + script
        print(script)
        result = subprocess.run([diretorio_pyhon, script], stdout=subprocess.PIPE)
        print(result.stdout.decode())


def cria_arquivo_log(atualizou):
    # Obtém a data e hora atuais
    data_hora_atual = datetime.datetime.now()

    # Expande o diretório pessoal e específica o caminho completo para o diretório onde deseja criar o arquivo
    nome_arquivo = data_hora_atual.strftime('%Y-%m-%d_%H-%M-%S') + '.txt'

    # Abre o arquivo em modo de escrita e escreve a hora atual nele
    with open(os.path.join(diretorio_gerador_csv, nome_arquivo), 'w') as arquivo:
        arquivo.write(str(data_hora_atual) + "_" + atualizou)

    print(f'O arquivo {os.path.join(diretorio_gerador_csv, nome_arquivo)} foi criado com sucesso.')


def atualizar_arquivo_se_diferente(minha_string):
    nome_arquivo = 'ultimo_ano_mes.txt'
    linha_atual = ''

    # Verifique se o arquivo existe
    if os.path.exists(diretorio_gerador_csv + nome_arquivo):
        with open(os.path.join(diretorio_gerador_csv, nome_arquivo), 'r') as arquivo:
            linha_atual = arquivo.readline().strip()

    # Se a linha lida for diferente da sua string, atualize o arquivo
    print(linha_atual, minha_string)
    if linha_atual != minha_string:
        with open(os.path.join(diretorio_gerador_csv, nome_arquivo), 'w') as arquivo:
            arquivo.write(minha_string)
        cria_arquivo_log("SIM_DIFERENTE")
        rodar_geradores_csv()
        buscar_arquivos_csv()
        git_add_commit_push("teste")
    else:
        cria_arquivo_log("NAO_DIFERENTE")


def baixar_novo_arquivo():
    # Criar uma lista de anos para os quais você deseja baixar os arquivos
    ano_atual = datetime.datetime.now().year
    for ano in [ano_atual, ano_atual - 1]:
        # Construir o URL dinamicamente com base no ano
        url = f'https://www.bcb.gov.br/pda/desig/planilha_{ano}.zip'
        # Baixar o arquivo ZIP
        r = requests.get(url, allow_redirects=True)
        if r.status_code != 200:
            continue
        else:
            # Especificar o nome do arquivo ZIP para salvar
            arquivo_zip = f'planilha_{ano}.zip'
            # Salvar o arquivo ZIP
            with open(os.path.join(diretorio_gerador_csv, arquivo_zip), 'wb') as f:
                f.write(r.content)
            print(f"Arquivo {arquivo_zip} baixado com sucesso!")
            ultimo_arquivo = extrair_zip_por_ano(ano)
            atualizar_arquivo_se_diferente(ultimo_arquivo)
            break


def baixar_todos_arquivos():
    # Criar uma lista de anos para os quais você deseja baixar os arquivos
    anos = list(range(2012, 2024))
    for ano in anos:
        # Construir o URL dinamicamente com base no ano
        url = f'https://www.bcb.gov.br/pda/desig/planilha_{ano}.zip'
        # Baixar o arquivo ZIP
        r = requests.get(url, allow_redirects=True)
        # Especificar o nome do arquivo ZIP para salvar
        arquivo_zip = f'planilha_{ano}.zip'
        # Salvar o arquivo ZIP
        with open(arquivo_zip, 'wb') as f:
            f.write(r.content)
        print(f"Arquivo {arquivo_zip} baixado com sucesso!")


def extrair_zip_por_ano(ano):
    zip_file_name = f'planilha_{ano}.zip'
    extracao_dir = f'planilha_{ano}'
    lista_arquivos = []

    with zipfile.ZipFile(diretorio_gerador_csv + zip_file_name, 'r') as zip_ref:
        zip_ref.extractall(diretorio_gerador_csv + extracao_dir)

    extracted_files = os.listdir(diretorio_gerador_csv + extracao_dir)
    for file_name in extracted_files:
        print(f"Arquivo extraído: {file_name}")
        lista_arquivos.append(file_name)
    print(lista_arquivos)
    # Achar o arquivo com a data mais recente (maior valor)
    arquivo_mais_recente = "planilha_" + max([arquivo.split("_")[1].split(".")[0] for arquivo in lista_arquivos]) + ".csv"
    print(arquivo_mais_recente)

    return arquivo_mais_recente


if __name__ == '__main__':
    baixar_novo_arquivo()
    # baixar_arquivos()
    # for ano in range(2012, 2024):
    #     extrair_zip_por_ano(ano)
