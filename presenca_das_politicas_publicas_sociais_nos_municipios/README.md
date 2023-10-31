
<p align="center">
  <img src="https://github.com/heliomacedofilho/projetos-do-bootcamp-analise-de-dados-enap-2023/assets/148554023/bfd78954-f0aa-4f39-9c16-ef0bc86dca47)](https://github.com/heliomacedofilho/projetos-do-bootcamp-analise-de-dados-enap-2023/assets/148554023/bfd78954-f0aa-4f39-9c16-ef0bc86dca47">
 
  <img src="https://github.com/heliomacedofilho/projetos-do-bootcamp-analise-de-dados-enap-2023/assets/148554023/c3f02ab7-9bf4-41cc-94b2-4a295972cc45">
</p>

  

# <h1 align="center"> Presença das políticas públicas sociais nos municípios brasileiros
</h1>

# ![Badge em Desenvolvimento](http://img.shields.io/static/v1?label=STATUS&message=CONCLUÍDO&color=GREEN&style=for-the-badge) ![Badge Outubro/2023](http://img.shields.io/static/v1?label=DATA&message=Outubro/2023&color=blue&style=for-the-badge)

# :scroll: Descrição do Projeto
O projeto **Presença das Políticas Públicas Sociais (PPS) nos municípios brasileiros** é a etapa final para conclusão do curso Bootcamp em Análise de Dados (turma exclusiva para mulheres) – 2023, ofertado pela Escola Nacional de Administração Pública - Enap.
Os detalhes do projeto serão apresentados a seguir.

## :arrow_right_hook: Justificativa

* A Política de Dados Abertos do Poder Executivo Federal, instituída pelo Decreto nº 8.777/2016, define regras para promover a abertura de dados governamentais no âmbito dos órgãos e entidades federais, como ministérios, autarquias, agências reguladoras e fundações públicas (Lei de Acesso à Informação (LAI) - Lei nº 12.527/2012).  

* O Ministério do Desenvolvimento e Assistência Social, Família e Combate à Fome (MDS) publica no <a href="https://dados.gov.br/home">Portal de Dados Abertos</a> 44 conjuntos de dados relacionados a diferentes Políticas Públicas Sociais (PPS) de sua responsabilidade, tais como Cadastro Único, Programa Bolsa Família, Benefício de Prestação Continuada, Registro Mensal de Atendimentos, Programa de Aquisição de Alimentos, Programa Cisternas, dentre outros.

* Os conjuntos de dados publicados em ambiente aberto podem ser utilizados para a realização de diversas análises do campo do desenvolvimento e assistência social e, se utilizados em conjunto, podem apresentar um retrato da participação dessas PPS nos municípios brasileiros.

* É importante avaliar a qualidade dos dados disponibilizados em ambiente aberto de modo a identificar a necessidade de promover melhorias nos conjuntos de dados e fortalecer a transparência ativa e a Política de Dados Abertos.

## :checkered_flag: Objetivos do projeto
  
  - :heavy_check_mark: Avaliar a qualidade dos dados abertos disponibilizados pelo MDS.
  
  - :bar_chart: Promover análise dos dados disponibilizados selecionados.
  
  - :thumbsup: Identificar a presença das Política Públicas Sociais (PPS) nos municípios.

## :diamond_shape_with_a_dot_inside: Metodologia

* `Acesso aos dados`:  Para o desenvolvimento do projeto foram utilizados os dados disponibilizados pelo MDS no Portal de Dados Abertos. Caso o dado disponibilizado no portal estivesse defasado em relação a outra fonte de acesso aberto, foi utilizado o dado mais atual possível e reportada no projeto a necessidade de promover o ajuste no portal.

* `Cálculo do Índice`: Para a avaliação da presença das Políticas Públicas Sociais (PPS) nos municípios brasileiros, foi calculado um índice composto, a partir da avaliação de programas selecionados, considerando as seguintes premissas:
  
  * Possuir os dados disponibilizados no Portal de Dados Abertos.
  
  * Ser universal.

* `Análise da renda`: Para os cálculos da renda das pessoas e famílias foram utilizados os dados do Cadastro Único, instrumento que identifica e caracteriza as famílias de baixa renda, e os dados dos Censos de 2010 e de 2022. O CadÚnico é a porta de entrada para várias políticas sociais e os dados de renda estão atualizados e permitem fazer o recorte da população alvo das PPS para as análises.
  
  A análise de renda englobou o cálculo da variação das taxas de pobreza, a partir dos dados do CadÚnico e do Censo populacional, e a variação do número das famílias em situação de pobreza e     extrema-pobreza ao longo do tempo. Importante registrar que essa análise foi apenas um exercício para a prática das ferramentas aprendidas no curso. Análises futuras poderão englobar a avaliação do comportamento da presença das PPS por meio do índice ao longo do tempo e a sua comparação com as variações da renda poderá ser feita com propriedade.

## :memo: Políticas Públicas Sociais selecionadas

### :dollar::family_man_woman_boy: Programa Bolsa Família (PBF)
O Programa Bolsa Família[^1] contribui no combate à pobreza, garantindo renda básica ao público alvo do programa e buscando integrar políticas públicas, de modo a estimular a emancipação das famílias, para que alcancem autonomia e superem situações de vulnerabilidade social.

O público-alvo do PBF são as famílias com renda mensal por pessoa de até R$ 218 (duzentos e dezoito reais). Isso significa que toda a renda gerada pelas pessoas da família, por mês, dividida pelo número de pessoas da família deve ser, no máximo, R$ 218. 

Para acessar o programa, a família deverá estar inscrita no Cadastro Único para Programas Sociais.

### :dollar::older_woman::wheelchair: Benefício de Prestação Continuada (BPC)
O Benefício de Prestação Continuada da Assistência Social[^2] é o pagamento de um salário mínimo mensal ao idoso acima de 65 anos ou à pessoa com deficiência de qualquer idade com impedimentos de natureza física, mental, intelectual ou sensorial de longo prazo, que comprovem não possuir meios de prover à própria manutenção ou tê-la provida por sua família, e cuja renda por pessoa do grupo familiar seja menor que 1/4 do salário-mínimo vigente.

### :writing_hand: Registro Mensal de Atendimentos (RMA)
O Registro Mensal de Atendimentos][^3] é um sistema onde são registradas mensalmente as informações relativas aos serviços ofertados e o volume de atendimentos nos Centros de Referência da Assistência Social (CRAS), Centros de Referência Especializados de Assistência Social (CREAS) e Centro de Referência Especializado para População em Situação de Rua (Centros POP). Seu principal objetivo é uniformizar essas informações e, dessa forma, proporcionar dados qualificados que contribuam para o desenvolvimento do Sistema Único de Assistência Social (SUAS). 

Considerando a premissa de seleção de políticas universais para comporem o índice, foram utilizados os registros apenas do CRAS, pois os demais serviços estão presentes apenas em municípios que preencham critérios específicos.

### :card_index: Índice de Gestão Descentralizada (IGD)
O Índice de Gestão Descentralizada[^4] é um indicador que mede os resultados da gestão do Programa Bolsa Família e do Cadastro Único obtidos em um mês. Representa uma estratégia para medir o desempenho de cada município, estimular resultados cada vez mais qualitativos e também compor a base de cálculo de recursos a serem transferidos aos municípios. 

O cálculo do IGD é composto por 4 fatores: 1) taxa de atualização cadastral e taxas de acompanhamento das condicionalidades de saúde e educação; 2) adesão ao Sistema Único de Assistência Social (Suas); 3) prestação de contas; e 4) parecer das contas do uso dos recursos.

Para o cálculo do Índice da presença das PPS nos municípios brasileiros foram utilizados os dados do Fator 1 do IGD, por estarem disponibilizados no Portal de Dados Abertos e por ser o fator mais diretamente relacionado a entregas à sociedade. 


## :memo: Demais Políticias Públicas utilizadas

### :computer: Cadastro Único para Programas Sociais (CadÚnico)
O Cadastro Único para Programas Sociais[^5] é um instrumento que identifica e caracteriza as famílias de baixa renda, permitindo que o governo conheça melhor a realidade socioeconômica dessa população que reside em todo território nacional. Nele são registradas informações como: características da residência, identificação de cada pessoa da família, escolaridade, situação de trabalho e renda, entre outras.

Deste modo, o Cadastro Único proporciona um mapa da parcela mais pobre e vulnerável da população brasileira, permitindo aos governos federal, estadual, municipal e distrital saber quem são, onde moram, como vivem e do que necessitam essas famílias. Isso facilita o diagnóstico para a criação de novos programas e a organização da oferta de serviços para essa população, além da seleção de público para esses programas e serviços.

O público-alvo são as famílias que vivem com renda mensal de até meio salário-mínimo por pessoa. As famílias com renda acima desse valor podem ser cadastradas para participarem de programas ou serviços específicos. Destaca-se que o cadastramento leva em conta se as famílias fazem parte de povos e comunidades tradicionais ou de grupos específicos, entre eles, indígenas, quilombolas, ribeirinhos e população em situação de rua. 

[^1]: Medida Provisória nº 1.164, de 2 de março de 2023; Lei nº 14.601, de 19 de junho de 2023.
[^2]: Constituição Federal de 1988 (art. 203, inciso V); Lei nº 8.742, de 7 de dezembro de 1993 (arts. 20, 20-B, 21 e 21-A); Decreto nº 6.214, de 26 de setembro de 2007; Decreto nº 8.805, de 07 de julho de 2016.
[^3]: Lei nº 8.742, de 7 de dezembro de 1993; Resoluções da Comissão Intergestores Tripartite (CIT) n° 4/2011 e n° 20/2013.
[^4]: Portaria MC nº 769, de 29 de abril de 2022.
[^5]: Lei nº 8.742, de 7 de dezembro de 1993; Decreto nº 11.016, de 29 de março de 2022.

# :date: Conjuntos de dados utilizados
- `Cadastro Único`: [Cadastro Único - Famílias/Pessoas por faixas de renda per capita - MI Social](https://dados.gov.br/dados/conjuntos-dados/cadastro-unico---familiaspessoas-por-faixas-de-renda-per-capita---mi-social)) - Os dados do CadÚnico utilizados foram os disponibilizados no Portal de Dados Abertos, sendo a última referência vigente a de setembro/2023. Para os cálculos de cada programa, foram usadas as seguintes referências:

  * **Programa Bolsa Família**: para o cálculo da presença do PBF nos municípios brasileiros foram comparados os dados das famílias beneficiárias do programa de setembro/2023, com os dados de famílias das faixas de pobreza e extrema-pobreza do CadÚnico de agosto/2023, pois para o pagamento do PBF de um determinado mês, são utilizados os dados do CadÚnico do mês anterior para preparação da folha de pagamento. 

  * **Registro Mensal de Atendimento**: para o cálculo da presença dos atendimentos dos CRAS nos municípios foram utilizados os dados do RMA do ano de 2022, dividido por doze, de modo a comparar o número médio de atendimentos de 2022 com o número de pessoas em situação de pobreza e extrema-pobreza cadastradas no CadÚnico em dez/2022.

   * **Análise de renda**: a partir dos dados do CadÚnico de 2012 a 2023, foram feitas análises do número de famílias que estavam na faixa da pobreza, ou seja, em situação de pobreza e extrema-pobreza, em agosto de cada ano, permitindo analisar a variação do número de famílias nesta faixa ao longo do tempo. 
     
   * **Taxa pobreza CadÚnico**:  a partir dos dados do CadÚnico, de abril/2012 e agosto/2023, foram feitas análises das taxas de pobreza do Cadastro Único, utilizando para tanto o número de pessoas em situação de pobreza e extrema-pobreza, pela população do Censo de 2010 e do Censo de 2023, respectivamente. O recorte de 2012 se deveu por apenas a partir de abril constarem dados por faixa de renda.

- `Programa Bolsa Família`: [Bolsa Família – MI Social](https://dados.gov.br/dados/conjuntos-dados/bolsa-familia---mi-social) - Os dados do PBF utilizados foram os disponibilizados no Portal de Dados Abertos. Destaca-se que ao acessar os dados do PBF estavam disponíveis tanto os dados do mês de setembro quanto os de outubro de 2023. Entretanto, considerando que para a preparação da folha de pagamento do programa são utilizados os dados do CadÚnico do mês anterior, optou-se por utilizar os dados do PBF de setembro de 2023.

- `Benefício de Prestação Continuada`: [BPC por município pagador](https://dados.gov.br/dados/conjuntos-dados/bpc-por-municipio-pagador)) - Para o cálculo da presença do BPC nos municípios brasileiros foram comparados os dados de pagamento do BPC do ano de 2022 com os dados do Fundo de Participação Municipal do mesmo ano. Destaca-se que os dados de 2023 também estão disponibilizados em dados abertos, até a referência de maio/2023. Entretanto, a metodologia utilizada comparou o valor total do ano para os dois conjuntos de dados, de modo a  minimizar o efeito das variações mensais de pagamento. 

- `Registro Mensal Atendimento do CRAS`: [RMA 2022 CRAS](https://aplicacoes.mds.gov.br/snas/vigilancia/index2.php) - Para o cálculo da presença do atendimento dos CRAS nos municípios brasileiros foram utilizados os dados do ano de 2022, de modo a  minimizar o efeito das variações mensais, tanto do atendimento quanto do seu registro, o qual não é realizado necessariamente no mesmo mês do atendimento. No Portal de Dados Abertos estão disponibilizados apenas os dados do RMA até 2021, mas a própria página direciona para o Portal da Vigilância Socioassistencial da Secretaria Nacional de Assistência Social, de onde foram acessados os dados mais recentes. 
  
- `Índice de Gestão Descentralizada`:  [IGD-M PBF - Taxas](https://aplicacoes.cidadania.gov.br/vis/data3/data-explorer.php) - Para o cálculo da classificação dos municípios a partir do resultado do IGD foram utilizados os dados de julho/2023, última referência disponibilizada pelo MDS na ferramenta Vis Data, no momento da coleta. Embora os dados do IGD-M estejam disponibilizados no Portal Dados Abertos para a mesma referência, ao analisar a base foram identificadas inconsistências. 
  
- `Fundo de Participação do Município (FPM)`:  [FPM por Município](https://www.tesourotransparente.gov.br/ckan/dataset/transferencias-obrigatorias-da-uniao-por-municipio/resource/d69ff32a-6681-4114-81f0-233bb6b17f58) - Como o público alvo do BPC é um recorte da população brasileira (Pessoas com deficiência e Idosos a partir de 65 anos que preencham as regras do programa) e não há a obrigatoriedade de estar cadastrada no CadÚnico para acesso ao programa, para avaliar a sua presença nos municípios brasileiros, foram comparados os dados de pagamento do BPC com os valores repassados por meio do FPM. Esta é uma comparação tradicional realizada para reforçar o papel da Previdência social, conforme explicado no informe [Previdência Social e Redistribuição de Renda Intermunicipal](http://sa.previdencia.gov.br/site/arquivos/office/3_090608-155706-828.pdf). Com o objetivo de comparar com o mesmo período do BPC, foi utilizado o valor total do FPM repassado aos municípios em 2022, disponível no Portal do Tesouro Nacional Transparente.

- `Taxa de pobreza`: Para promover a análise da variação da taxa da pobreza, foram utilizados os dados do CadÚnico da referência próxima aos dos dados de população dos dois últimos Censos disponíveis, conforme segue abaixo:
  - `População dos municípios Censo 2010`: [Tabela 1378 - População residente, por situação do domicílio, sexo e idade, segundo a condição no domicílio e compartilhamento da responsabilidade pelo domicílio](https://sidra.ibge.gov.br/tabela/1378)
  - `População dos municípios Censo 2022`: [Prévia da População dos Municípios com base nos dados do Censo Demográfico 2022 coletados até 25/12/2022](https://www.ibge.gov.br/estatisticas/sociais/populacao/22827-censo-demografico-2022.html?edicao=35938&t=resultados)

- `Produto Interno Bruto Municipal`: [PIB por Unidade da Federação 2020](https://www.ibge.gov.br/estatisticas/economicas/contas-nacionais/9088-produto-interno-bruto-dos-municipios.html) - De modo a comparar o resultado do Índice da presença das PPS nos municípios com outros dados econômicos foram utilizados os dados do PIB municipal per capita. Entretanto, ao fazer uma análise preliminar entre as duas variáveis, identificou-se uma correlação linear desprezível. Desta forma, o resultado não foi apresentado no presente projeto.
 
# :mag_right: Metodologia para cálculo do Índice das PPS nos municípios brasileiros
A partir do resultado da análise da presença de cada um dos programas selecionados, foram definidos os intervalos com uma melhor distribuição dos municípios a partir dos casos concretos e, para cada faixa definida, foi atribuída uma nota de 0, no caso de resultado igual a zero, a no máximo 11, conforme imagem abaixo.

![Metodologia](https://github.com/heliomacedofilho/projetos-do-bootcamp-analise-de-dados-enap-2023/assets/148554023/3cce4ea6-073a-4a82-8559-fe09c22ad4a8)

Como, a depender do caso concreto foi identificada a necessidade de distribuir os resultados em um número maior ou menor de faixas para atribuição da nota, posteriormente foi feita a padronização das notas atribuídas, de modo que cada programa recebesse a nota de presença nos municípios de 0 a 2.5, conforme imagem abaixo.

![Padronizacao_nota](https://github.com/heliomacedofilho/projetos-do-bootcamp-analise-de-dados-enap-2023/assets/148554023/c65c5daf-e618-4929-bc84-663a7b400cd1)

Por fim, foram somadas as notas padronizadas atribuídas aos quatro programas para cada um dos municípios brasileiros, podendo pontuar no total de 0 a 10 em relação à presença das PPS.

# :mag_right: Metodologia para as análises de renda
* `Taxa da pobreza`: A partir dos dados do CadÚnico foram feitas análises das taxas de pobreza do Cadastro Único considerando os dados de população do Censo. Para tanto, o total do número de pessoas em situação de pobreza e extrema-pobreza do Cadastro Único, de abril/2012 e de agosto/2023, foi dividido pela população do Censo de 2010 e do Censo de 2022, respectivamente.
  
  Após o cálculo da taxa de pobreza para cada um dos dois períodos analisados, foi feito o cálculo da diferença das taxas da pobreza de 2012 e de 2023 e os municípios classificados de acordo com as variações de aumento ou redução da taxa da pobreza, conforme imagem abaixo.
  
   ![metodologia_dif_tx_pob](https://github.com/heliomacedofilho/projetos-do-bootcamp-analise-de-dados-enap-2023/assets/148554023/6b2f20db-0050-4acc-a6ee-db44498757fa)

* `Variação do número de famílias na faixa da pobreza`: A partir dos dados do CadÚnico foi realizada a análise da variação do número total de famílias na faixa da pobreza, ou seja, em situação de pobreza e extrema-pobreza ao longo do tempo. Para tanto, foi utilizado o número total de famílias do CadÚnico dos meses de agosto de cada ano, incluídas nesta faixa.  

# :hammer: Scripts desenvolvidos

  - [Script da análise do Cadastro Único](https://github.com/heliomacedofilho/projetos-do-bootcamp-analise-de-dados-enap-2023/blob/main/presenca_das_politicas_publicas_sociais_nos_municipios/CadastroUnico.ipynb)
  
  - [Script da análise do Programa Bolsa Família](https://github.com/heliomacedofilho/projetos-do-bootcamp-analise-de-dados-enap-2023/blob/main/presenca_das_politicas_publicas_sociais_nos_municipios/PBF.ipynb)
  
  - [cript da análise do Benefício de Prestação Continuada](https://github.com/heliomacedofilho/projetos-do-bootcamp-analise-de-dados-enap-2023/blob/main/presenca_das_politicas_publicas_sociais_nos_municipios/BPC-2022.ipynb)
  
  - [Script da análise do Índice de Gestão Descentralizada](https://github.com/heliomacedofilho/projetos-do-bootcamp-analise-de-dados-enap-2023/blob/main/presenca_das_politicas_publicas_sociais_nos_municipios/igd_m.ipynb)
  
  - [Script da análise do Registro Mensal Atendimento (RMA) do CRAS](https://github.com/heliomacedofilho/projetos-do-bootcamp-analise-de-dados-enap-2023/blob/main/presenca_das_politicas_publicas_sociais_nos_municipios/RMA.ipynb)
  
  - [Script da análise do Pib Municipal](https://github.com/heliomacedofilho/projetos-do-bootcamp-analise-de-dados-enap-2023/blob/main/presenca_das_politicas_publicas_sociais_nos_municipios/pib_pc.ipynb)
  
  - [Script do Índice de avaliação da presença das PPS nos municípios brasileiros](https://github.com/heliomacedofilho/projetos-do-bootcamp-analise-de-dados-enap-2023/blob/main/presenca_das_politicas_publicas_sociais_nos_municipios/Indice%20Geral%20PPS.ipynb)

# :wrench: Conjuntos de dados com indicação de ajuste no Portal de Dados Abertos
De uma maneira geral, os dados disponibilizados nos Portal de dados abertos pelo MDS acessados para o desenvolvimento do presente projeto estavam organizados de maneira adequada, atualizados e sem inconsistências, com exceção dos conjuntos abaixo destacados: 

- `Registro Mensal Atendimento do CRAS`: [Registro Mensal de Atendimentos - RMA](https://dados.gov.br/dados/conjuntos-dados/registro-mensal-de-atendimentos-rma) - A última atualização dos dados do RMA no Portal de Dados Abertos foi em 26/08/2021. Embora no Portal de Dados Abertos tenha o caminho para o Portal da Vigilância Sociassistencial, da Secretaria Nacional de Assistência Saocial, onde estão disponibilizados os dados atualizados, de modo a qualificar o Portal de Dados Abertos, sugere-se a sua atualização, nem que sejam apenas referente aos dados dos anos fechados, 2021 e 2022, direcionando o cidadão para o outro portal apenas para obter os dados do ano corrente.
  
- `Índice de Gestão Descentralizada`:  [IGD-M PBF - Taxas 2023](https://dados.gov.br/dados/conjuntos-dados/indice-de-gestao-descentralizada---igd---mi-social) - O arquivo csv com os dados do IGD no Portal de Dados Abertos está apresentando inconsistências, com alguns municípios apresentando resultados em casas decimais e outros na casa das centenas. Seugere-se que os arquivos sejam analisados e substituídos de modo a corrigir as inconsistências.

Registra-se que a disponibilização dos dados em outros portais abertos permitiu que as dificuldades encontradas fossem superadas e as análises dos programas previamente selecionados executadas sem dificuldade.

# :woman_student: Aprendizados para a vida
O processo do desenvolvimento do Projeto permitiu construirmos aprendizados que poderão ser usados ao longo do percurso da jornada de analistas de dados. 

Para além de treinar as ferramentas aprendidas durante o BootCamp, enfrentamos dificuldades que nos trouxeram grandes oportunidades de crescimento, que gostaríamos de dividir com todas:

* Abra o arquivo a ser utilizado antes de carregá-lo na interface onde serão desenvolvidas as análises. Muitas vezes uma simples leitura do arquivo permite a identificação imediata de algum padrão de inconsistência que pode indicar a necessidade de substituição do arquivo e que, ao analisar na interface de desenvolvimento, pode ser observado apenas após um longo tempo de escrita de códigos
  
* Ao partir de uma premissa para analisar os dados selecionados, que envolvam um conjunto de dados muito extenso, faça um exercício com uma amostra inicial. Até mesmo pensando em dados hipotéticos, teste a sua ideia antes de dar início à analise de todo o conjunto de dados. Isso poderá poupar muitas horas de escrita de códigos que no final não serão usados

* Ao trabalhar em um projeto no GitHub, com mais de uma pessoa trabalhando no mesmo arquivo, lembre-se sempre de ao terminar de escrever o código no jupyter lab, salvar o arquivo, fazer o commit (para pegar as alterações da pasta local e preparar o arquivo para ir para o GitHub) e depois clicar no push para o seu repositório do projeto do GitHub ser atualizado. Apenas salvar o arquivo no jupyter lab poderá fazer com que a atualização do GitHub por outra pessoa gere arquivos com conflitos que demandrão muitas horas de trabalho para você recuperar a sua versão.
  
# :angel: Pessoas Contribuidoras

  Bruno Garcia
  
  Fabio Paim
  
  Hélio Bomfim de Macêdo Filho
  
  Kalina Rabbani
  
  Ricardo de Lima
  
  Thais Salzer  
  
# :two_women_holding_hands:Pessoas Desenvolvedoras do Projeto

![Equipe_zoom](https://github.com/heliomacedofilho/projetos-do-bootcamp-analise-de-dados-enap-2023/assets/148554023/f46dd7fe-3c44-4183-b7e0-c7c9c81ab82e)

# 😌 Perdendo o arquivo pela milésima vez

![Mariana_zoom](https://github.com/heliomacedofilho/projetos-do-bootcamp-analise-de-dados-enap-2023/assets/148554023/180e9397-6b4e-4483-8e5a-daa715ba22d9)

# :star2:Recrutador de talentos

![Gif_gatos_botas](https://github.com/heliomacedofilho/projetos-do-bootcamp-analise-de-dados-enap-2023/assets/148554023/85784c8c-09d0-45ba-bdc6-c02881919e30)

