## Wikidata BgeeDB-bot

This software tool is a bot to insert human gene expression data from the Bgee database into Wikidata.
Currently, only existing wikidata gene entries from Ensembl and wikidata anatomic entities (e.g.
[stomach](https://www.wikidata.org/wiki/Q1029907)) with a cross-reference to
UBERON ontology are considered. This bot inserts to wikidata human gene pages 
["expressed in"](https://www.wikidata.org/wiki/Property:P5572) statements. 
For example, see the statement "expressed in" at BRAF gene wikidata page: https://www.wikidata.org/wiki/Q17853226.

Note that at most 10 "expression in" statements are included per gene page. The 10 exclusive UBERON anatomic entities 
(terms prefixed with UBERON: ) where the gene is expressed. UBERON terms that are not prefixed with UBERON: such as CL:
are not taken into account because there is no cross-reference to them in the Wikidata anatomic entity entries.

### Editing configuration file 
* **INPUT_BGEE_DATA_TSV**: the TSV file path containing the "is expressed in" relations.
  The SQL query [get_ordered_is_expressed_in](get_ordered_is_expressed_in.sql) may be executed over the 
[EasyBgee](https://bgee.org/?page=download&action=dumps) MySQL database to generate the "is expressed in" relations as
a TSV file with the following heading:
```
gene_id	uberon_id
```

Execute the MySQL command line below to generate the relations  "is expressed in" for human genes from EasyBgee v14.2
```
mysql -u USER -p easybgee_v14_2 < get_ordered_is_expressed_in.sql > wikidata_bgeev14_2.tsv
```
* **WDUSER**: the wikidata username.
* **WDPASS**: the wikidata password.
