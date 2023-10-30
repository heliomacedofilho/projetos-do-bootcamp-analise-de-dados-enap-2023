=============================================
Bem-vindo ao monitor do endividamento dos brasileiros!
=============================================

O **monitor do endividamento dos brasileiros** surgiu como projeto final do *bootcamp* em análise de dados para mulheres da Escola Nacional de Administração Pública (ENAP).

Inicialmente, o objetivo era analisar os dados fornecidos pelo Banco Central do Brasil referentes ao endividamento de pessoas físicas e jurídicas. A intenção era explorar vários critérios e, com base nesses dados, fornecer insumos para estudos que revelassem os perfis de endividamento da população e das empresas brasileiras. 

Ao longo do processo de criação, foram adicionadas variáveis macroeconômicas obtidas por meio de bases públicas como do IBGE e da Câmara dos Deputados.

O Monitor foi construído utilizando a linguagem de programação Python 🐍.

Sobre os dados e atualização
--------

Os dados utilizados para a construção do painel visual (*dashboard*) do Monitor são obtidos a partir do Sistema de Informações de Crédito (SCR) do Banco Central do Brasil. Nessa base constam dados sobre:

- Parcelas de crédito por período de vencimento
- Quantidade de operações de crédito
- Modalidade das operações de crédito
- Porte dos clientes
- Estado da federação do contratante
- Setor de atuação das empresas contrantes

Para conferir mais detalhes sobre a metodologia utilizada pelo Banco Central do Brasil clique `aqui <https://www.bcb.gov.br/content/estabilidadefinanceira/scr/scr.data/scr_data_metodologia.pdf>`_.

Os dados do painel são atualizados conforme disponibilização dos dados pelo Banco Central do Brasil.

Fontes de dados
--------
    
- Sistema de Informações de Crédito (Banco Central do Brasil)
- Sistema Gerenciador de Séries Temporais (Banco Central do Brasil)
- Sistema IBGE de Recuperação Automática (IBGE)
- Dados Abertos da Câmara dos Deputados

Bibliotecas utilizadas para extração, análise e visualização dos dados
--------

- Zipfile
- Os
- Pandas
- Deflater
- Requests
- Plotly
- Seaborn
- Streamlit
- SidraPy

Nosso contato
--------

O Monitor é uma construção colaborativa. 

Tem dúvidas ou quer sugerir uma melhoria?

Entre em contato conosco! 💌

monitordoendividamento@gmail.com