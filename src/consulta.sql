SET NOCOUNT ON
SELECT T.Id,
T.Nome,
T.Status,
S.Servico,
T.InicioReal,
T.TerminoReal,
T.AlertaPrazo,
T.Origem,
T.Numero,
T.Escalonado,
e.PerguntaDescricao as Pergunta,
E.Conteudo as Resposta,
es.Descricao as 'Local',
Nivel_03 as 'CR',
Cr.Gerente,
E.Recurso as Supervisor,
Longitude,
Latitude,
T.TarefaPai
FROM FT_TAREFA T WITH(NOLOCK)
JOIN FT_CHECKLIST_RESPOSTA_FULL E WITH(NOLOCK) ON E.TAREFAID = T.ID
INNER JOIN DM_ESTRUTURA ES WITH(NOLOCK) ON ES.ID_ESTRUTURA = T.ID_ESTRUTURA
INNER JOIN DM_CR CR WITH(NOLOCK) ON CR.ID_CR = ES.ID_CR
INNER JOIN DM_EXECUCAO Ex WITH(NOLOCK) on Ex.TarefaIs = T.Id 
INNER JOIN DM_SERVICO S WITH(NOLOCK) ON S.Id_Servico = T.Id_Servico 
WHERE ES.HierarquiaDescricao LIKE '%SICOOB %'
AND CR.GerenteRegional = 'CHARLES GELMINI ALMEIDA'


use DW_Vista
select top 1 * from DM_EXECUCAO