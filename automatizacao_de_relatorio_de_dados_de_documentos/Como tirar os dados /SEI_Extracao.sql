-- A query abaixo tem como finalidade a extração de textos Públicos para envio para treinamento de modelos linguísticos de inteligência artificial (LLMs).
-- Esta query em específico realiza a extração de textos publicados oficialmente no Boletim de Serviço Eletrônico do SEI da entidade (página "Publicações Eletrônicas" do SEI).
	-- Evidentemente, somente terá textos publicados na página "Publicações Eletrônicas" do SEI se a entidade utilizar tal ferramenta como seu Boletim de Serviço Eletrônico.
-- Esses textos de documentso publicados ficam por natureza na Internet e não tem como retornar o que é publicado, se equivalendo ao Diário Oficial da Unidão (DOU), sendo que do próprio órgão.
-- A query de extração abaixo funciona em base do SEI MySQL. Depois faremos query igual que funcione em SQL Server e em Oracle.
-- A query abaixo segue o Leiaute de envio de textos para treinamento de modelos linguísticos a seguir: https://docs.google.com/spreadsheets/d/15YzO8OjZl5fYj2yUITwoFy6k7i24uLrU0eJ5EMIy7aw/edit?usp=sharing
SELECT
     LPAD(c.cnpj, 14, '0') AS NU_CNPJ_ENTIDADE -- CNPJ da entidade de origem do dataset de texto enviado, com exatamente 14 dígitos, incluindo zeros à esquerda.
    ,uf.sigla AS UF_SEDE_ENTIDADE -- UF da sede da entidade de origem do texto enviado.
    ,'E' AS TP_PODER_ENTIDADE -- DEVE alterar manualmente para representar o valor correto. Indica o tipo de Poder ao qual a entidade está vinculada.
    ,'F' AS TP_ESFERA_ENTIDADE -- DEVE alterar manualmente para representar o valor correto. Indica o tipo de Esfera a qual a entidade está vinculada.
    ,'I' AS TP_PERSONALIDADE_JURID_ENTIDADE -- DEVE alterar manualmente para representar o valor correto. Indica o tipo da Personalidade jurídica da entidade.
    ,DATE(NOW()) AS DT_REFERENCIA_EXTRACAO
    ,DATE(pb.dta_publicacao) AS DT_REFERENCIA_TEXTO
    ,'B' AS TP_ARMAZENAMENTO_ORIGEM -- DEVE alterar manualmente para representar o valor correto.
    ,CASE
        WHEN e.nome REGEXP 'Decisório|Acórdão' THEN 'F'
        ELSE 'D' END AS TP_TEXTO -- DEVE alterar manualmente para representar o valor correto.
	,'C' AS TP_FINALIDADE_TREINAMENTO -- DEVE alterar manualmente para representar o valor correto.
	,'P' AS TP_NIVEL_ACESSO -- ATENÇÃO: Inicialmente somente recebemos datasets de textos Públicos.
	,e.nome AS NO_TIPO_DOCUMENTO
    ,tp.nome AS NO_TEMATICA_TEXTO
    ,dc.conteudo AS TEXTO_PARA_TREINAMENTO
FROM documento d
INNER JOIN serie e
    ON e.id_serie = d.id_serie
INNER JOIN documento_conteudo dc    
    ON dc.id_documento = d.id_documento
INNER JOIN publicacao pb
    ON pb.id_documento = d.id_documento
INNER JOIN procedimento pr
    ON pr.id_procedimento = d.id_procedimento
INNER JOIN tipo_procedimento tp
    ON tp.id_tipo_procedimento = pr.id_tipo_procedimento    
INNER JOIN unidade u
    ON u.id_unidade = d.id_unidade_responsavel
INNER JOIN orgao o
    ON o.id_orgao = u.id_orgao
INNER JOIN contato c
    ON c.id_contato = o.id_contato
INNER JOIN uf
    ON uf.id_uf = c.id_uf
;