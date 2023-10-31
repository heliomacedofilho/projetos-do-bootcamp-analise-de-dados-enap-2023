1) Estrutura da pasta:
main
    py_files
    venv

2) Se já tiver o venv: cd /caminho/para/venv >> source bin/activate 

3) Rodar o requirements: pip install -r requirements.txt (vai instalar no venv)

2) No terminal abrir o cron (digitar crontab -e) e copiar o código abaixo para rodar o código dia 14 e 28 às 12:00:

    0 12 14,28 * * cd ~/monitor/py_files/ && ~/monitor/venv/bin/python3 ~/monitor/py_files/download_extracao_zips.py >> ~/monitor/py_files/log.txt 2>&1

3) ATENÇÃO::::::: no mac há problema de autenticação, então é preciso colocar o seu token no .gitignore em um arquivo chamado token