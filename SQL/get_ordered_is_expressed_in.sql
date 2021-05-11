SELECT gene_id, uberon_id FROM (
SELECT g.geneId as gene_id, SUBSTRING_INDEX(cond.anatEntityId,'UBERON:',-1) as uberon_id, max(ge.score) as score FROM globalExpression as ge 
JOIN gene as g ON g.bgeeGeneId = ge.bgeeGeneId 
JOIN globalCond as cond on cond.globalConditionId = ge.globalConditionId  
JOIN temp_wikidata_uberon_ids as wd on wd.uberon_anatomical_id = cond.anatEntityId
where ge.callType='EXPRESSED'   and cond.speciesId=9606  group by gene_id, uberon_id ) as c
group by gene_id, uberon_id order by gene_id, max(score) desc