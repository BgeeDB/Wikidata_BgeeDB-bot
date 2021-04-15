SELECT gene_id, uberon_id FROM (
SELECT g.geneId as gene_id, SUBSTRING_INDEX(cond.anatEntityId,'UBERON:',-1) as uberon_id, max(ge.score) as score FROM easybgee_v14_2.globalExpression as ge 
JOIN easybgee_v14_2.gene as g ON g.bgeeGeneId = ge.bgeeGeneId 
JOIN easybgee_v14_2.globalCond as cond on cond.globalConditionId = ge.globalConditionId 
where ge.callType='EXPRESSED' and cond.anatEntityId LIKE 'UBERON:%'  and cond.speciesId=9606  group by gene_id, uberon_id ) as c
group by gene_id, uberon_id order by gene_id, max(score) desc