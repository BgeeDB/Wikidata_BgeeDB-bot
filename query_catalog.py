from config import WD_TAXA_SPACE_SEP

BGEE_EXPRESSION_QUERY_HUMAN = '''
#Bgee SPARQL query to get expression data for human genes and their corresponding anatomical entities

PREFIX orth: <http://purl.org/net/orth#>
PREFIX up: <http://purl.uniprot.org/core/>
PREFIX genex: <http://purl.org/genex#>
PREFIX obo: <http://purl.obolibrary.org/obo/>
prefix dct: <http://purl.org/dc/terms/>

SELECT ?gene_id ?anatomical_entity ?max_score {
 ?seq a orth:Gene .
 ?seq orth:organism <http://bgee.org/#ORGANISM_9606>.
 ?seq dct:identifier ?gene_id.
{SELECT DISTINCT ?seq ?anatomical_entity (MAX(?score) as ?max_score) {
     ?exp    genex:hasSequenceUnit ?seq.
    ?exp genex:hasExpressionCondition ?cond .
    ?cond genex:hasAnatomicalEntity ?anatomical_entity .
    ?exp genex:hasExpressionLevel ?score.
    ?anatomical_entity rdfs:label ?anatName .
    ?cond obo:RO_0002162 <http://purl.uniprot.org/taxonomy/9606> . 
}group by ?seq ?anatomical_entity  }
}order by ?gene_id, desc(?max_score) 
'''
BGEE_EXPRESSION_QUERY_HUMAN_UBERON_PREFIXED = '''
######
##Bgee SPARQL query to get expression data for human genes and their corresponding anatomical entities
##This query solely consider anatomic entity terms prefixed with obo:UBERON_
######
PREFIX orth: <http://purl.org/net/orth#>
PREFIX up: <http://purl.uniprot.org/core/>
PREFIX genex: <http://purl.org/genex#>
PREFIX obo: <http://purl.obolibrary.org/obo/>
prefix dct: <http://purl.org/dc/terms/>
PREFIX lscr: <http://purl.org/lscr#>


SELECT ?gene_id ?uberon_id  {
#values ?seq {<http://omabrowser.org/ontology/oma#GENE_ENSG00000237468>
#<http://omabrowser.org/ontology/oma#GENE_ENSG00000237467>}
 ?seq a orth:Gene .
 ?seq orth:organism <http://bgee.org/#ORGANISM_9606>.
 ?seq dct:identifier ?gene_id.
 ?seq lscr:xrefEnsemblGene ?gene_ensembl_uri
{SELECT DISTINCT ?seq ?anatomical_entity STRAFTER(str(?anatomical_entity), "UBERON_" ) as ?uberon_id (MAX(?score) as ?max_score) {
    ?exp a genex:Expression.
    ?exp    genex:hasSequenceUnit ?seq.
    ?exp genex:hasExpressionCondition ?cond .
    ?cond genex:hasAnatomicalEntity ?anatomical_entity .
    ?exp genex:hasExpressionLevel ?score.
    ?anatomical_entity rdfs:label ?anatName .
    ?cond obo:RO_0002162 <http://purl.uniprot.org/taxonomy/9606> .

}group by ?seq ?anatomical_entity }
filter (?uberon_id !='')
} order by ?gene_id, desc(?max_score) '''

WIKIDATA2ENSEMBL_GENE_ID_MAP_QUERY = '''
######
## Wikidata SPARQL query to compose a mapping between wikidata ids and Ensembl gene ids.
######
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX pr: <http://www.wikidata.org/prop/reference/>
PREFIX prov: <http://www.w3.org/ns/prov#>

SELECT DISTINCT ?wikidata_gene_id ?ens_gene_id
WHERE 
{service<https://query.wikidata.org/sparql>{
  VALUES ?taxon {''' + WD_TAXA_SPACE_SEP + '''}
   ?item wdt:P703  ?taxon ;
         wdt:P31 wd:Q7187;
        p:P594/prov:wasDerivedFrom ?xref.
  ?xref pr:P248 ?stated_in_db;
        pr:P594 ?ens_gene_id}
  BIND(STRAFTER(STR(?item),STR(wd:)) as ?wikidata_gene_id) } ORDER BY ?ens_gene_id'''

WIKIDATA_GET_UBERON_IDS= '''
######
## Wikidata SPARQL query to get UBERON ids (including cell IDs).
######
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX pr: <http://www.wikidata.org/prop/reference/>
PREFIX prov: <http://www.w3.org/ns/prov#>

SELECT DISTINCT ?uberon_id_prefixed
WHERE 
{
  {?item wdt:P1554 ?uberon_id.
   BIND(CONCAT(STR("UBERON:"),STR(?uberon_id)) as ?uberon_id_prefixed) }
  UNION
   {
    ?item wdt:P7963 ?onto_cl_id
    BIND(REPLACE(STR(?onto_cl_id),"_",":") as ?uberon_id_prefixed) 
 }
}'''

WIKIDATA_ONLY_BGEE_DATA= '''
######
## Wikidata SPARQL query to verify if there is any expressed in statement in wikidata
## that is not from Bgee database.
######
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX p: <http://www.wikidata.org/prop/>
PREFIX pr: <http://www.wikidata.org/prop/reference/>
PREFIX ps: <http://www.wikidata.org/prop/statement/>
PREFIX prov: <http://www.w3.org/ns/prov#>
ASK WHERE  {
service<https://query.wikidata.org/sparql>{
?gene wdt:P31 wd:Q7187 ; #instance of Gene
    wdt:P5572 ?anat; #expressed in
    p:P5572 ?o. #expressed in
 ?o ps:P5572 ?anat ; #expressed in
    prov:wasDerivedFrom ?xref. 
 #?xref pr:P248 ?db. #stated in
 filter not exists { ?xref pr:P248 wd:Q54985720.} #stated by Bgee DB
}} '''