[![DOI](https://zenodo.org/badge/DOI/10.1093/nar/gkae1118.svg)](https://doi.org/10.1093/nar/gkae1118)
[![DOI](https://zenodo.org/badge/DOI/10.1093/nar/gkaa793.svg)](https://doi.org/10.1093/nar/gkaa793)
[![Bluesky](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fpublic.api.bsky.app%2Fxrpc%2Fapp.bsky.actor.getProfile%2F%3Factor%3Dbgee.org&query=%24.followersCount&style=social&logo=bluesky&label=Follow%20%40bgee.org)](https://bsky.app/profile/bgee.org)
[![Mastodon](https://img.shields.io/mastodon/follow/109308703977124988?style=social&label=Follow%20%40bgeedb&domain=https%3A%2F%2Fgenomic.social)](https://genomic.social/%40bgeedb)

## Wikidata BgeeDB-bot

This software tool is a bot to insert gene expression data from the Bgee database into Wikidata.
Currently, only existing wikidata gene entries from Ensembl and wikidata anatomic entities (e.g.
[stomach](https://www.wikidata.org/wiki/Q1029907)) with a cross-reference to
UBERON ontology are considered (including Cell ontology). This bot inserts to wikidata gene pages 
["expressed in"](https://www.wikidata.org/wiki/Property:P5572) statements. 
For example, see the statement "expressed in" at BRAF gene wikidata page: https://www.wikidata.org/wiki/Q17853226.

Note that at most 10 "expression in" statements are included per gene page. The 10 exclusive UBERON anatomic entities 
(terms prefixed with UBERON and CL) where the gene is expressed. 

### Editing and generating configuration file
The [properties.template](properties.template) contains all variables needed to be set up for running this bot. 
Variables:
* **WDUSER**: the wikidata username.
* **WDPASS**: the wikidata password.
  
* **EXPRESSION_CALLS_FILE**: the TSV file path containing the "is expressed in" relations to insert in Wikidata ordered 
  by descending gene expression score. When considering the EasyBgee v14.2, we can execute the SQL query 
  [get_ordered_is_expressed_in](get_ordered_is_expressed_in.sql) over the 
[EasyBgee](https://bgee.org/?page=download&action=dumps) MySQL database to generate the "is expressed in" relations as
a TSV file with the following heading:
```
gene_id	uberon_id
```
where UBERON ids are defined by removing their prefix `UBERON:` when it exists (e.g. UBERON:0002369 => 0002369) and for
the other ids that are not prefixed with `UBERON:`, the `:` is replaced with `_` such as the following example:
modified from `CL:0000711` to `CL_0000711`. 
For example, an `INPUT_BGEE_DATA_TSV` file with two entries is show below.
```
gene_id                 uberon_id
ENSMUSG00000000001	0002369
ENSMUSG00000000001	CL_0000711
```

For further information about the variables to set, refer to the [properties.template](properties.template). 
Before executing any make command this file must be renamed from `properties.template` to `properties`.

After editing the `properties` file, if you do not have pipenv installed in your python3.7 (or superior) interpreter, 
run first the make command below in the current project directory.

```
make install_pipenv 
```
If pipenv is already installed, run the make command below in the current project directory:

```
make 
```
**REMARK** A temporary file called `count.tmp` is generated to be able to restart the execution from the last successful
Wikidata insertion. To rerun the bot from the beginning, this file must be removed.

**DEPRECATED** Execute the make command line below to generate the relations  "is expressed in" for human and mouse genes
from EasyBgee v14.2
```
make get_input_expression_data 
```
The output file is placed at the file path defined in the `EXPRESSION_CALLS_FILE` variable.



