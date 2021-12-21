Expression call download file documentation
===========================================

Bgee provides calls of baseline presence/absence of expression, and of differential over-/under-expression, either for single species, or compared between species (orthologous genes in homologous organs). This documentation describes the format of these [download files](https://bgee.org/?page=download&action=expr_calls "Bgee expression data page").

*   [Single-species download files](#single "Quick jump to this section")
    *   [Presence/absence of expression](#single_expr "Quick jump to this section")
    *   [Over-/under-expression across anatomy or life stages](#single_diff "Quick jump to this section")
*   [Multi-species download files](#multi "Quick jump to this section")
    *   [OMA Hierarchical orthologous groups](#oma_hog "Quick jump to OMA HOG file")
    *   [Over-/under-expression across anatomy or life stages](#multi_diff "Quick jump to this section")

<a name="single"></a>Single-species download files
--------------------------------------------------

Jump to:

*   [Presence/absence of expression](#single_expr "Quick jump to presence/absence of expression")
*   [Over-/under-expression across anatomy or life stages](#single_diff "Quick jump to differential expression")

### <a name="single_expr"></a>Presence/absence of expression

Bgee provides calls of presence/absence of expression. Each call corresponds to a unique combination of a gene, an anatomical entity, and a life stage, with reported presence or absence of expression. Life stages describe development and aging. Only "normal" expression is considered in Bgee (i.e., no treatment, no disease, no gene knock-out, etc.). Bgee collects data from different types, from different studies, in different organisms, and provides a summary from all these data as unique calls `gene - anatomical entity - developmental stage`, with confidence information, notably taking into account potential conflicts.

Calls of presence/absence of expression are very similar to the data that can be reported using _in situ_ hybridization methods; Bgee applies dedicated statistical analyses to generate such calls from EST, Affymetrix, and RNA-Seq data, with confidence information, and also collects _in situ_ hybridization calls from model organism databases. This offers the possibility to aggregate and compare these calls of presence/absence of expression between different experiments, different data types, and different species, and to benefit from both the high anatomy coverage provided by low-throughput methods, and the high genomic coverage provided by high-throughput methods.

After presence/absence calls are generated from the raw data, they are propagated using anatomical and life stage ontologies:

*   calls of expression are propagated to parent anatomical entities and parent developmental stages. For instance, if gene A is expressed in midbrain at young adult stage, it will also be considered as expressed in brain at adult stage.
*   calls of absence of expression are propagated to child anatomical entities (and not to child developmental stages). For instance, if gene A is reported as not expressed in the brain at young adult stage, it will also be considered as not expressed in the midbrain at young adult stage. This is only permitted when it does not generate any contradiction with expression calls from the same data type (for instance, no contradiction permitted of reported absence of expression by RNA-Seq, with report of expression by RNA-Seq for the same gene, in the same anatomical entity and developmental stage, or any child anatomical entity or child developmental stage).

Call propagation allows a complete integration of the data, even if provided at different anatomical or developmental levels. For instance: if gene A is reported to be expressed in the midbrain dura mater at young adult stage; gene B is reported to be expressed in the midbrain pia mater at late adult stage; and gene C has an absence of expression reported in the brain at adult stage; it is then possible to retrieve that, in the midbrain at adult stage, gene A and B are both expressed, while gene C is not, thanks to call propagation.

It is possible to select two different combinations of `condition parameters`:

*   anatomical entities only (by default) files contain one expression call for each unique pair of gene and anatomical entity.If more than one developmental stage map this unique pair, the resulting expression call correspond to summarized information coming from all developmental stages.
*   anatomical entities and developmental stages files contain one expression call for each unique gene, anatomical entity and developmental stage.

Presence/absence calls are then filtered and presented differently depending on whether a `simple file`, or an `advanced file` is used. Notably: `simple files` aim at providing summarized information over all data types, and only in anatomical entities and developmental stages actually used in experimental data; `advanced files` aim at reporting all information, allowing for instance to retrieve the contribution of each data type to a call, in all possible anatomical entities and developmental stages.

Jump to format description for:

*   [simple file](#single_expr_simple "Quick jump to simple file description")
*   [advanced file](#single_expr_advanced "Quick jump to advanced file description")

#### <a name="single_expr_simple"></a>Simple file

In simple files, propagated presence/absence expression calls are provided, but only calls in conditions of anatomical entity/developmental stage actually used in experimental data are displayed (no calls generated from propagation only).

Format description for single species simple expression file

|Column|Content|Example|
|--- |--- |--- |
|1|[Gene ID](#single_expr_simple_col1 "See Gene ID column description")|FBgn0005427|
|2|[Gene name](#single_expr_simple_col2 "See Gene name column description")|ewg|
|3|[Anatomical entity ID](#single_expr_simple_col3 "See Anatomical entity ID column description")|FBbt:00003404|
|4|[Anatomical entity name](#single_expr_simple_col4 "See Anatomical entity name column description")|mesothoracic extracoxal depressor muscle 66 (Drosophila)|
|5|[Developmental stage ID](#single_expr_simple_col5 "See Developmental stage ID column description") *|FBdv:00005348|
|6|[Developmental stage name](#single_expr_simple_col6 "See Developmental stage name column description") *|prepupal stage P4(ii) (Drosophila)|
|7|[Expression](#single_expr_simple_col7 "See Expression column description")|present|
|8|[Call quality](#single_expr_simple_col8 "See Call quality column description")|silver quality|
|9|[Expression rank](#single_expr_simple_col9 "See Expression rank column description")|1.24e4|

**\*** only present if 'developmental stage' is selected as a condition parameter.

Example lines for single species simple expression file

|Gene ID|Gene name|Anatomical entity ID|Anatomical entity name|Developmental stage ID|Developmental stage name|Expression|Call quality|Expression rank|
|--- |--- |--- |--- |--- |--- |--- |--- |--- |
|FBgn0005533|RpS17|UBERON:0000473|testis|UBERON:0000066|fully formed stage|present|silver quality|539|
|FBgn0005536|Mbs|UBERON:0000033|head|FBdv:00007085|day 10 of adulthood (Drosophila)|present|gold quality|1.57e3|
|FBgn0005558|ey|FBbt:00001684|embryonic/larval hemocyte (Drosophila)|FBdv:00005339|third instar larval stage (Drosophila)|absent|silver quality|2.35e4|

##### <a name="single_expr_simple_col1"></a>Gene ID (column 1)

Unique identifier of gene from Ensembl.

Please note that for _P. paniscus_ (bonobo) we use _P. troglodytes_ genome (chimpanzee), and that for _P. pygmaeus_ (Bornean orangutan) we use _P. abelii_ genome (Sumatran orangutan). Only for those species (bonobo and Bornean orangutan), we modify the Ensembl gene IDs, to ensure that we provide unique gene identifiers over all species. It is therefore necessary, to obtain correct Ensembl gene IDs for those species, to replace gene ID prefix 'PPAG' with 'ENSPTRG', and 'PPYG' prefix with 'ENSPPYG'.

##### <a name="single_expr_simple_col2"></a>Gene name (column 2)

Name of the gene defined by `Gene ID` (column 1)

##### <a name="single_expr_simple_col3"></a>Anatomical entity ID (column 3)

Unique identifier of the anatomical entity, from the Uberon ontology.

##### <a name="single_expr_simple_col4"></a>Anatomical entity name (column 4)

Name of the anatomical entity defined by `Anatomical entity ID` (column 3)

##### <a name="single_expr_simple_col5"></a>Developmental stage ID (column 5)

Unique identifier of the developmental stage, from the Uberon ontology.

##### <a name="single_expr_simple_col6"></a>Developmental stage name (column 6)

Name of the developmental stage defined by `Developmental stage ID` (column 5)

##### <a name="single_expr_simple_col7"></a>Expression (column 7)

Call generated from all data types for `Gene ID` (column 1), in `Anatomical entity ID` (column 3), at `Developmental stage ID` (column 5). Permitted values:

*   present: report of presence of expression, from Bgee statistical tests and/or from _in situ_ data sources.
*   absent: report of absence of expression, from Bgee statistical tests and/or from _in situ_ data sources.

In Bgee, calls of absence of expression are always discarded if there exists a contradicting call of expression, for the same gene, in the same anatomical entity and developmental stage, or in a child entity or child developmental stage.

##### <a name="single_expr_simple_col8"></a>Call quality (column 8)

Quality associated to the call. Permitted values:

*   high quality: presence or absence of expression reported as high quality from Bgee statistical tests and/or from _in situ_ data sources.
*   low quality: presence or absence of expression reported as low quality from Bgee statistical tests and/or from _in situ_ data sources.

From this quality a `summary quality` is calculated using all calls corresponding to the same gene and condition parameters coming from different experiments and/or data types.

Quality associated to the call in column `Expression` (column 7) is this `summary quality` and is calculated using following rules:

*   gold quality: 2 or more high quality calls.
*   silver quality: 1 high quality call or 2 low quality calls
*   bronze quality: 1 low quality call (for internal use only. Not present in this file).

##### <a name="single_expr_simple_col9"></a>Expression rank (column 9)

Rank score associated to the call. Rank scores of expression calls are normalized across genes, conditions and species.

A low score means that the gene is highly expressed in the condition.

[Back to presence/absence of expression menu](#single_expr)

#### <a name="single_expr_advanced"></a>Advanced file

Simple and advanced files contain the same expression calls (same number of lines) but advanced files contain more information on each call (more columns).

Advanced file information:

*   details of expression status generated from each data type are provided (present, absent, no data).
*   details of number of present high quality and present low quality calls from each data type.
*   details of number of absent high quality and absent low quality calls from _in situ_, Affymetrix, and RNA-Seq.
*   details of data type for which calls are observed. Each call is observed in at least one data type

Format description for single species advanced expression file

|Column|Content|Example|
|--- |--- |--- |
|1|[Gene ID](#single_expr_advanced_col1 "See Gene ID column description")|ENSDARG00000070769|
|2|[Gene name](#single_expr_advanced_col2 "See Gene name column description")|foxg1a|
|3|[Anatomical entity ID](#single_expr_advanced_col3 "See Anatomical entity ID column description")|UBERON:0000955|
|4|[Anatomical entity name](#single_expr_advanced_col4 "See Anatomical entity name column description")|brain|
|5|[Developmental stage ID](#single_expr_advanced_col5 "See Developmental stage ID column description") *|UBERON:0000113|
|6|[Developmental stage name](#single_expr_advanced_col6 "See Developmental stage name column description") *|post-juvenile adult stage|
|7|[Expression](#single_expr_advanced_col7 "See Expression column description")|present|
|8|[Call quality](#single_expr_advanced_col8 "See Call quality column description")|silver quality|
|9|[Expression rank](#single_expr_advanced_col9 "See Expression rank column description")|1.23e4|
|10|[Including observed data](#single_expr_advanced_col10 "See Including observed data column description")|yes|
|11|[Affymetrix data](#single_expr_advanced_col11 "See Affymetrix data column description")|present|
|12|[Affymetrix experiment count showing expression of this gene in this condition or in sub-conditions with a high quality](#single_expr_advanced_col12 "See Affymetrix experiment count showing expression of this gene in this condition or in sub-conditions with a high quality column description")|1|
|13|[Affymetrix experiment count showing expression of this gene in this condition or in sub-conditions with a low quality](#single_expr_advanced_col13 "See Affymetrix experiment count showing expression of this gene in this condition or in sub-conditions with a low quality column description")|0|
|14|[Affymetrix experiment count showing absence of expression of this gene in this condition or valid parent conditions with a high quality](#single_expr_advanced_col14 "See Affymetrix experiment count showing absence of expression of this gene in this condition or valid parent conditions with a high quality column description")|0|
|15|[Affymetrix experiment count showing absence of expression of this gene in this condition or valid parent conditions with a low quality](#single_expr_advanced_col15 "See Affymetrix experiment count showing absence of expression of this gene in this condition or valid parent conditions with a low quality column description")|0|
|16|[Including Affymetrix observed data](#single_expr_advanced_col16 "See Including Affymetrix observed data column description")|yes|
|17|[EST data](#single_expr_advanced_col17 "See EST data column description")|present|
|18|[EST experiment count showing expression of this gene in this condition or in sub-conditions with a high quality](#single_expr_advanced_col18 "See EST experiment count showing expression of this gene in this condition or in sub-conditions with a high quality column description")|0|
|19|[EST experiment count showing expression of this gene in this condition or in sub-conditions with a low quality](#single_expr_advanced_col19 "See EST experiment count showing expression of this gene in this condition or in sub-conditions with a low quality column description")|0|
|20|[Including EST observed data](#single_expr_advanced_col20 "See Including EST observed data column description")|no|
|21|[In situ data](#single_expr_advanced_col21 "See In situ data column description")|present|
|22|[In situ hybridization experiment count showing expression of this gene in this condition or in sub-conditions with a high quality](#single_expr_advanced_col22 "See In situ hybridization experiment count showing expression of this gene in this condition or in sub-conditions with a high quality column description")|1|
|23|[In situ hybridization experiment count showing expression of this gene in this condition or in sub-conditions with a low quality](#single_expr_advanced_col23 "See In situ hybridization experiment count showing expression of this gene in this condition or in sub-conditions with a low quality column description")|0|
|24|[In situ hybridization experiment count showing absence of expression of this gene in this condition or valid parent conditions with a high quality](#single_expr_advanced_col24 "In situ hybridization experiment count showing absence of expression of this gene in this condition or valid parent conditions with a high quality")|0|
|25|[In situ hybridization experiment count showing absence of expression of this gene in this condition or valid parent conditions with a low quality](#single_expr_advanced_col25 "See In situ hybridization experiment count showing absence of expression of this gene in this condition or valid parent conditions with a low quality column description")|0|
|26|[Including in situ observed data](#single_expr_advanced_col26 "See Including in situ observed data column description")|yes|
|27|[RNA-Seq data](#single_expr_advanced_col27 "See RNA-Seq data column description")|present|
|28|[RNA-Seq experiment count showing expression of this gene in this condition or in sub-conditions with a high quality](#single_expr_advanced_col28 "See RNA-Seq experiment count showing expression of this gene in this condition or in sub-conditions with a high quality column description")|1|
|29|[RNA-Seq experiment count showing expression of this gene in this condition or in sub-conditions with a low quality](#single_expr_advanced_col29 "See RNA-Seq experiment count showing expression of this gene in this condition or in sub-conditions with a low quality column description")|0|
|30|[RNA-Seq experiment count showing absence of expression of this gene in this condition or valid parent conditions with a high quality](#single_expr_advanced_col30 "See RNA-Seq experiment count showing absence of expression of this gene in this condition or valid parent conditions with a high quality column description")|0|
|31|[RNA-Seq experiment count showing absence of expression of this gene in this condition or valid parent conditions with a low quality](#single_expr_advanced_col31 "See RNA-Seq experiment count showing absence of expression of this gene in this condition or valid parent conditions with a low quality column description")|0|
|32|[Including RNA-Seq observed data](#single_expr_advanced_col32 "See Including RNA-Seq observed data column description")|yes|


**\*** only present if 'developmental stage' is selected as a condition parameter.

Example lines for single species advanced expression file

|Gene ID|Gene name|Anatomical entity ID|Anatomical entity name|Developmental stage ID|Developmental stage name|Expression|Call quality|Expression rank|Including observed data|Affymetrix data|Affymetrix experiment count showing expression of this gene in this condition or in sub-conditions with a high quality|Affymetrix experiment count showing expression of this gene in this condition or in sub-conditions with a low quality|Affymetrix experiment count showing absence of expression of this gene in this condition or valid parent conditions with a high quality|Affymetrix experiment count showing absence of expression of this gene in this condition or valid parent conditions with a low quality|Including Affymetrix observed data|EST data|EST experiment count showing expression of this gene in this condition or in sub-conditions with a high quality|EST experiment count showing expression of this gene in this condition or in sub-conditions with a low quality|Including EST observed data|In situ data|In situ hybridization experiment count showing expression of this gene in this condition or in sub-conditions with a high quality|In situ hybridization experiment count showing expression of this gene in this condition or in sub-conditions with a low quality|In situ hybridization experiment count showing absence of expression of this gene in this condition or valid parent conditions with a high quality|In situ hybridization experiment count showing absence of expression of this gene in this condition or valid parent conditions with a low quality|Including in situ observed data|RNA-Seq data|RNA-Seq experiment count showing expression of this gene in this condition or in sub-conditions with a high quality|RNA-Seq experiment count showing expression of this gene in this condition or in sub-conditions with a low quality|RNA-Seq experiment count showing absence of expression of this gene in this condition or valid parent conditions with a high quality|RNA-Seq experiment count showing absence of expression of this gene in this condition or valid parent conditions with a low quality|Including RNA-Seq observed data|
|--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |
|ENSDARG00000000002|ccdc80|UBERON:0000965|lens of camera-type eye|ZFS:0000033|Hatching:Long-pec (Danio)|present|gold quality|385|yes|no data|0|0|0|0|no|no data|0|0|no|no data|0|0|0|0|no|present|2|1|0|0|yes|
|ENSDARG00000000175|hoxb2a|UBERON:0004734|gastrula|ZFS:0000017|Gastrula:50%-epiboly (Danio)|absent|silver quality|3.6e4|yes|no data|0|0|0|0|no|no data|0|0|no|absent|0|0|0|1|no|absent|0|0|1|0|yes|
|ENSDARG00000000241|slc40a1|UBERON:0000922|embryo|ZFS:0000019|Gastrula:Shield (Danio)|present|silver quality|8.2e3|yes|present|0|1|0|0|yes|no data|0|0|no|no data|0|0|0|0|no|present|0|1|0|0|yes|

##### <a name="single_expr_advanced_col1"></a>Gene ID (column 1)

Unique identifier of gene from Ensembl.

Please note that for _P. paniscus_ (bonobo) we use _P. troglodytes_ genome (chimpanzee), and that for _P. pygmaeus_ (Bornean orangutan) we use _P. abelii_ genome (Sumatran orangutan). Only for those species (bonobo and Bornean orangutan), we modify the Ensembl gene IDs, to ensure that we provide unique gene identifiers over all species. It is therefore necessary, to obtain correct Ensembl gene IDs for those species, to replace gene ID prefix 'PPAG' with 'ENSPTRG', and 'PPYG' prefix with 'ENSPPYG'.

##### <a name="single_expr_advanced_col2"></a>Gene name (column 2)

Name of the gene defined by `Gene ID` (column 1)

##### <a name="single_expr_advanced_col3"></a>Anatomical entity ID (column 3)

Unique identifier of the anatomical entity, from the Uberon ontology.

##### <a name="single_expr_advanced_col4"></a>Anatomical entity name (column 4)

Name of the anatomical entity defined by `Anatomical entity ID` (column 3)

##### <a name="single_expr_advanced_col5"></a>Developmental stage ID (column 5)

Unique identifier of the developmental stage, from the Uberon ontology.

##### <a name="single_expr_advanced_col6"></a>Developmental stage name (column 6)

Name of the developmental stage defined by `Developmental stage ID` (column 5)

##### <a name="single_expr_advanced_col7"></a>Expression (column 7)

Call generated from all data types for `Gene ID` (column 1), in `Anatomical entity ID` (column 3), at `Developmental stage ID` (column 5). Permitted values:

*   present: report of presence of expression, from Bgee statistical tests and/or from _in situ_ data sources.
*   absent: report of absence of expression, from Bgee statistical tests and/or from _in situ_ data sources.

In Bgee, calls of absence of expression are always discarded if there exists a contradicting call of expression, for the same gene, in the same anatomical entity and developmental stage, or in a child entity or child developmental stage.

##### <a name="single_expr_advanced_col8"></a>Call quality (column 8)

Quality associated to the call. Permitted values:

*   high quality: presence or absence of expression reported as high quality from Bgee statistical tests and/or from _in situ_ data sources.
*   low quality: presence or absence of expression reported as low quality from Bgee statistical tests and/or from _in situ_ data sources.

From this quality a `summary quality` is calculated using all calls corresponding to the same gene and condition parameters coming from different experiments and/or data types.

Quality associated to the call in column `Expression` (column 7) is this `summary quality` and is calculated using following rules:

*   gold quality: 2 or more high quality calls.
*   silver quality: 1 high quality call or 2 low quality calls
*   bronze quality: 1 low quality call (for internal use only. Not present in this file).

##### <a name="single_expr_advanced_col9"></a>Expression rank (column 9)

Rank score associated to the call. Rank scores of expression calls are normalized across genes, conditions and species.

A low score means that the gene is highly expressed in the condition.

##### <a name="single_expr_advanced_col10"></a>Including observed data (column 10)

Permitted value: `yes`

Only calls which were actually seen in experimental data, at least once, are in this file.

##### <a name="single_expr_advanced_col11"></a>Affymetrix data (column 11)

Call generated by Affymetrix data for `Gene ID` (column 1), in `Anatomical entity ID` (column 3), at `Developmental stage ID` (column 5). Permitted values:

*   present: report of presence of expression from Bgee statistical tests. See `Affymetrix call quality` (column 11) for associated quality level.
*   absent: report of absence of expression from Bgee statistical tests, with no contradicting call of presence of expression generated by other Affymetrix probesets or chips for the same gene, in the same anatomical entity and developmental stage, or in a child entity or child developmental stage.
*   no data: no Affymetrix data available for this gene/anatomical entity/developmental stage (data either not available, or discarded by Bgee quality controls).

##### <a name="single_expr_advanced_col12"></a>Affymetrix experiment count showing expression of this gene in this condition or in sub-conditions with a high quality (column 12)

##### <a name="single_expr_advanced_col13"></a>Affymetrix experiment count showing expression of this gene in this condition or in sub-conditions with a low quality (column 13)

##### <a name="single_expr_advanced_col14"></a>Affymetrix experiment count showing absence of expression of this gene in this condition or valid parent conditions with a high quality (column 14)

##### <a name="single_expr_advanced_col15"></a>Affymetrix experiment count showing absence of expression of this gene in this condition or valid parent conditions with a low quality (column 15)

##### <a name="single_expr_advanced_col16"></a>Including Affymetrix observed data (column 16)

Permitted values: `yes` and `no`.

Defines whether this call was generated from propagation only, or whether this call was actually seen in experimental data in this anatomical entity/developmental stage condition.

In this column, the information is provided by solely considering Affymetrix data.

##### <a name="single_expr_advanced_col17"></a>EST data (column 17)

Call generated by EST data for `Gene ID` (column 1), in `Anatomical entity ID` (column 3), at `Developmental stage ID` (column 5). Note that EST data are not used to produce calls of absence of expression. Permitted values:

*   present: expression reported from Bgee statistical tests.
*   no data: no EST data available for this gene/anatomical entity/developmental stage (data either not available, or discarded by Bgee quality controls).

##### <a name="single_expr_advanced_col18"></a>EST experiment count showing expression of this gene in this condition or in sub-conditions with a high quality (column 18)

##### <a name="single_expr_advanced_col19"></a>EST experiment count showing expression of this gene in this condition or in sub-conditions with a low quality (column 19)

##### <a name="single_expr_advanced_col20"></a>Including EST observed data (column 20)

Permitted values: `yes` and `no`.

Defines whether this call was generated from propagation only, or whether this call was actually seen in experimental data in this anatomical entity/developmental stage condition.

In this column, the information is provided by solely considering EST data.

##### <a name="single_expr_advanced_col21"></a>In situ data (column 21)

Call generated by _in situ_ data for `Gene ID` (column 1), in `Anatomical entity ID` (column 3), at `Developmental stage ID` (column 5). Permitted values:

*   present: report of presence of expression from _in situ_ data sources.
*   absent: report of absence of expression from _in situ_ data sources, with no contradicting call of presence of expression generated by other _in situ_ hybridization evidence lines for the same gene, in the same anatomical entity and developmental stage, or in a child entity or child developmental stage.
*   no data: no _in situ_ data available for this gene/anatomical entity/developmental stage (data either not available, or discarded by Bgee quality controls).

##### <a name="single_expr_advanced_col22"></a>In situ hybridization experiment count showing expression of this gene in this condition or in sub-conditions with a high quality (column 22)

##### <a name="single_expr_advanced_col23"></a>In situ hybridization experiment count showing expression of this gene in this condition or in sub-conditions with a low quality (column 23)

##### <a name="single_expr_advanced_col24"></a>In situ hybridization experiment count showing absence of expression of this gene in this condition or valid parent conditions with a high quality (column 24)

##### <a name="single_expr_advanced_col25"></a>In situ hybridization experiment count showing absence of expression of this gene in this condition or valid parent conditions with a low quality (column 25)

##### <a name="single_expr_advanced_col26"></a>Including in situ observed data (column 26)

Permitted values: `yes` and `no`.

Defines whether this call was generated from propagation only, or whether this call was actually seen in experimental data in this anatomical entity/developmental stage condition.

In this column, the information is provided by solely considering _in situ_ data.

##### <a name="single_expr_advanced_col27"></a>RNA-Seq data (column 27)

Call generated by RNA-Seq data for `Gene ID` (column 1), in `Anatomical entity ID` (column 3), at `Developmental stage ID` (column 5). Permitted values:

*   present: report of presence of expression from Bgee statistical tests. See `RNA-Seq call quality` (column 20) for associated quality level.
*   absent: report of absence of expression from Bgee statistical tests, with no contradicting call of presence of expression generated by other RNA-Seq libraries for the same gene, in the same anatomical entity and developmental stage, or in a child entity or child developmental stage.
*   no data: no RNA-Seq data available for this gene/anatomical entity/developmental stage (data either not available, or discarded by Bgee quality controls).

##### <a name="single_expr_advanced_col28"></a>RNA-Seq experiment count showing expression of this gene in this condition or in sub-conditions with a high quality (column 28)

##### <a name="single_expr_advanced_col29"></a>RNA-Seq experiment count showing expression of this gene in this condition or in sub-conditions with a low quality (column 29)

##### <a name="single_expr_advanced_col30"></a>RNA-Seq experiment count showing absence of expression of this gene in this condition or valid parent conditions with a high quality (column 30)

##### <a name="single_expr_advanced_col31"></a>RNA-Seq experiment count showing absence of expression of this gene in this condition or valid parent conditions with a low quality (column 31)

##### <a name="single_expr_advanced_col32"></a>Including RNA-Seq observed data (column 32)

Permitted values: `yes` and `no`.

Defines whether this call was generated from propagation only, or whether this call was actually seen in experimental data in this anatomical entity/developmental stage condition.

In this column, the information is provided by solely considering RNA-Seq data.

[Back to presence/absence of expression menu](#single_expr)

This corresponds to the same expression state summary column as in simple files (column 7 of presence/absence simple file)

### <a name="single_diff"></a>Over-/under-expression across anatomy or life stages

**Please note, these data will be available in a future release.**

Bgee provides calls of over-/under-expression. A call corresponds to a gene, with significant variation of its level of expression, in an anatomical entity during a developmental stage, as compared to, either: i) other anatomical entities at the same (broadly defined) developmental stage (over-/under-expression across anatomy); ii) the same anatomical entity at different (precise) developmental stages (over-/under-expression across life stages). These analyses of differential expression are performed using Affymetrix and RNA-Seq experiments with at least 3 suitable conditions (anatomical entity/developmental stage), and at least 2 replicates for each; as for all data in Bgee, only "normal" expression is considered (i.e., no treatment, no disease, no gene knock-out, etc.).

Bgee runs all possible differential expression analyses for each experiment independently, then collects all results and provides a summary as unique calls `gene - anatomical entity - developmental stage`, with confidence information, and conflicts within each data type resolved using a voting system weighted by p-values (conflicts between different data types are treated differently). This offers the possibility to aggregate and compare these calls between different experiments, different data types, and different species.

Note that, as opposed to calls of presence/absence of expression, no propagation of differential expression calls is performed using anatomical and life stage ontologies.

Over-/under-expression calls are then filtered and presented differently depending on whether a `simple file`, or a `complete file` is used. Notably: `simple files` aim at providing summarized information over all data types; `complete files` aim at reporting all information, allowing for instance to retrieve the contribution of each data type to a call, or to retrieve all genes and conditions tested, including genes having no differential expression in these conditions.

Jump to format description for:

*   [simple file](#single_diff_simple "Quick jump to simple file description")
*   [complete file](#single_diff_complete "Quick jump to complete file description")

#### <a name="single_diff_simple"></a>Simple file

In simple files, only calls of over-expression and under-expression are provided, summarizing the contribution of each data type to the call.

Format description for single species simple differential expression file

|Column|Content|Example|
|--- |--- |--- |
|1|[Gene ID](#single_diff_simple_col1 "See Gene ID column description")|ENSG00000000419|
|2|[Gene name](#single_diff_simple_col2 "See Gene name column description")|DPM1|
|3|[Anatomical entity ID](#single_diff_simple_col3 "See Anatomical entity ID column description")|UBERON:0009834|
|4|[Anatomical entity name](#single_diff_simple_col4 "See Anatomical entity name column description")|dorsolateral prefrontal cortex|
|5|[Developmental stage ID](#single_diff_simple_col5 "See Developmental stage ID column description")|HsapDv:0000083|
|6|[Developmental stage name](#single_diff_simple_col6 "See Developmental stage name column description")|infant stage (human)|
|7|[Differential expression](#single_diff_simple_col7 "See Differential expression column description")|under-expression|
|8|[Call quality](#single_diff_simple_col8 "See Call quality column description")|high quality|

Example lines for single species simple differential expression file

|Gene ID|Gene name|Anatomical entity ID|Anatomical entity name|Developmental stage ID|Developmental stage name|Differential expression|Call quality|
|--- |--- |--- |--- |--- |--- |--- |--- |
|ENSG00000000003|TSPAN6|UBERON:0000922|embryo|HsapDv:0000017|Carnegie stage 10 (human)|over-expression|low quality|
|ENSG00000000419|DPM1|UBERON:0000922|embryo|HsapDv:0000020|Carnegie stage 13 (human)|under-expression|low quality|
|ENSG00000000457|SCYL3|UBERON:0000178|blood|HsapDv:0000094|65-79 year-old human stage (human)|over-expression|low quality|


##### <a name="single_diff_simple_col1"></a>Gene ID (column 1)

Unique identifier of gene from Ensembl.

Please note that for _P. paniscus_ (bonobo) we use _P. troglodytes_ genome (chimpanzee), and that for _P. pygmaeus_ (Bornean orangutan) we use _P. abelii_ genome (Sumatran orangutan). Only for those species (bonobo and Bornean orangutan), we modify the Ensembl gene IDs, to ensure that we provide unique gene identifiers over all species. It is therefore necessary, to obtain correct Ensembl gene IDs for those species, to replace gene ID prefix 'PPAG' with 'ENSPTRG', and 'PPYG' prefix with 'ENSPPYG'.

##### <a name="single_diff_simple_col2"></a>Gene name (column 2)

Name of the gene defined by `Gene ID` (column 1)

##### <a name="single_diff_simple_col3"></a>Anatomical entity ID (column 3)

Unique identifier of the anatomical entity, from the Uberon ontology.

##### <a name="single_diff_simple_col4"></a>Anatomical entity name (column 4)

Name of the anatomical entity defined by `Anatomical entity ID` (column 3)

##### <a name="single_diff_simple_col5"></a>Developmental stage ID (column 5)

Unique identifier of the developmental stage, from the Uberon ontology.

##### <a name="single_diff_simple_col6"></a>Developmental stage name (column 6)

Name of the developmental stage defined by `Developmental stage ID` (column 5)

##### <a name="single_diff_simple_col7"></a>Differential expression (column 7)

Call generated from all data types for `Gene ID` (column 1), in `Anatomical entity ID` (column 3), at `Developmental stage ID` (column 5). Permitted values:

*   over-expression: the gene was shown in one or more analyses to have a significant over-expression in this condition, as compared to the expression levels in other conditions of the analyses.
*   under-expression: the gene was shown in one or more analyses to have a significant under-expression in this condition, as compared to the expression levels in other conditions of the analyses.
*   weak ambiguity: there exists a call of over-expression or under-expression generated from a data type, but another data type showed no significant variation of the level of expression of this gene in the same condition; or, a gene was shown to be never expressed in a condition by some analyses of a given data type, but other analyses of different data types produced a call of over-expression or of absence of differential expression for the same gene, in the same condition (note that conflicts where a data type produced an under-expression call in a condition, while another data type showed the same gene to be never expressed in that condition, do not produce a `weak ambiguity` call, but a call of `under-expression low quality`).
*   strong ambiguity: there exists a call of over-expression or under-expression generated from a data type, but there exists a call in the opposite direction generated from another data type for the same gene, anatomical entity and developmental stage. For instance, gene A is reported to be over-expressed in the midbrain at young adult stage from Affymetrix data, but is reported to be under-expressed in the midbrain at young adult stage from RNA-Seq data.

##### <a name="single_diff_simple_col8"></a>Call quality (column 8)

Confidence in the differential expression call provided in `Differential expression` (column 7). Permitted values:

*   high quality: differential expression reported as high quality, with no contradicting call from same type of analysis (across anatomy/across life stages), for same gene, in same anatomical entity and developmental stage, (call generated either from multiple congruent analyses, or from a single analysis).
*   poor quality: differential expression reported as low quality, or there exists a conflict for the same gene, anatomical entity and developmental stage, from different analyses of a same data type (conflicts between different data types are treated differently). For instance, an analysis showed a gene to be over-expressed in a condition, while another analysis showed the same gene to be under-expressed or not differentially expressed in the same condition. Such conflicts are resolved by a voting system based on the number of conditions compared, weighted by p-value. Note that in one case, this quality level is used to reconcile conflicting calls from different data types: when a data type produced an under-expression call, while a different data type has shown that the same gene was never seen as expressed in the same condition. In that case, the overall summary is `under-expression low quality`.
*   NA: no quality applicable when ambiguity state in `Differential expression` (column 7).

[Back to over-/under-expression menu](#single_diff)

#### <a name="single_diff_complete"></a>Complete file

The differences between simple and complete files are that, in complete files:

*   details of the contribution of each data type to the final calls are provided, notably with information about best p-values, or number of supporting/conflicting analyses.
*   calls representing absence of differential expression are provided, allowing to determine all genes and conditions tested for differential expression.

Format description for single species complete differential expression file

|Column|Content|Example|
|--- |--- |--- |
|1|Gene ID|ENSMUSG00000093930|
|2|Gene name|Hmgcs1|
|3|Anatomical entity ID|UBERON:0002107|
|4|Anatomical entity name|liver|
|5|Developmental stage ID|UBERON:0000113|
|6|Developmental stage name|post-juvenile adult stage|
|7|Differential expression|over-expression|
|8|Call quality|high quality|
|9|Affymetrix data|over-expression|
|10|Affymetrix call quality|poor quality|
|11|Affymetrix best supporting p-value|0.0035659347|
|12|Affymetrix analysis count supporting Affymetrix call|1|
|13|Affymetrix analysis count in conflict with Affymetrix call|1|
|14|RNA-Seq data|over-expression|
|15|RNA-Seq call quality|high quality|
|16|RNA-Seq best supporting p-value|2.96E-8|
|17|RNA-Seq analysis count supporting RNA-Seq call|2|
|18|RNA-Seq analysis count in conflict with RNA-Seq call|0|


Example lines for single species complete differential expression file

|Gene ID|Gene name|Anatomical entity ID|Anatomical entity name|Developmental stage ID|Developmental stage name|Differential expression|Call quality|Affymetrix data|Affymetrix call quality|Affymetrix best supporting p-value|Affymetrix analysis count supporting Affymetrix call|Affymetrix analysis count in conflict with Affymetrix call|RNA-Seq data|RNA-Seq call quality|RNA-Seq best supporting p-value|RNA-Seq analysis count supporting RNA-Seq call|RNA-Seq analysis count in conflict with RNA-Seq call|
|--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |
|ENSMUSG00000000001|Gnai3|UBERON:0000081|metanephros|MmusDv:0000027|Theiler stage 20 (mouse)|no diff expression|high quality|no diff expression|high quality|0.22166589|1|0|no data|no data|1.0|0|0|
|ENSMUSG00000000028|Cdc45|UBERON:0000992|female gonad|MmusDv:0000035|Theiler stage 26 (mouse)|under-expression|poor quality|under-expression|poor quality|6.386149E-4|1|1|no data|no data|1.0|0|0|
|ENSMUSG00000000031|H19|UBERON:0002037|cerebellum|MmusDv:0000036|Theiler stage 27 (mouse)|over-expression|high quality|over-expression|high quality|1.2336E-6|2|0|no data|no data|1.0|0|0|

##### Gene ID (column 1)

Unique identifier of gene from Ensembl.

Please note that for _P. paniscus_ (bonobo) we use _P. troglodytes_ genome (chimpanzee), and that for _P. pygmaeus_ (Bornean orangutan) we use _P. abelii_ genome (Sumatran orangutan). Only for those species (bonobo and Bornean orangutan), we modify the Ensembl gene IDs, to ensure that we provide unique gene identifiers over all species. It is therefore necessary, to obtain correct Ensembl gene IDs for those species, to replace gene ID prefix 'PPAG' with 'ENSPTRG', and 'PPYG' prefix with 'ENSPPYG'.

##### Gene name (column 2)

Name of the gene defined by `Gene ID` (column 1)

##### Anatomical entity ID (column 3)

Unique identifier of the anatomical entity, from the Uberon ontology.

##### Anatomical entity name (column 4)

Name of the anatomical entity defined by `Anatomical entity ID` (column 3)

##### Developmental stage ID (column 5)

Unique identifier of the developmental stage, from the Uberon ontology.

##### Developmental stage name (column 6)

Name of the developmental stage defined by `Developmental stage ID` (column 5)

##### Differential expression (column 7)

Call generated from all data types for `Gene ID` (column 1), in `Anatomical entity ID` (column 5), at `Developmental stage ID` (column 3). Permitted values:

*   over-expression: the gene was shown in one or more analyses to have a significant over-expression in this condition, as compared to the expression levels in other conditions of the analyses.
*   under-expression: the gene was shown in one or more analyses to have a significant under-expression in this condition, as compared to the expression levels in other conditions of the analyses.
*   no diff expression: the gene was tested for differential expression in this condition, but was never shown to have a significant variation of expression as compared to the other conditions of the analyses.
*   weak ambiguity: there exists a call of over-expression or under-expression generated from a data type, but another data type showed no significant variation of the level of expression of this gene in the same condition; or, a gene was shown to be never expressed in a condition by some analyses of a given data type, but other analyses of different data types produced a call of over-expression or of absence of differential expression for the same gene, in the same condition (note that conflicts where a data type produced an under-expression call in a condition, while another data type showed the same gene to be never expressed in that condition, do not produce a `weak ambiguity` call, but a call of `under-expression low quality`).
*   strong ambiguity: there exists a call of over-expression or under-expression generated from a data type, but there exists a call in the opposite direction generated from another data type for the same gene, anatomical entity and developmental stage. For instance, gene A is reported to be over-expressed in the midbrain at young adult stage from Affymetrix data, but is reported to be under-expressed in the midbrain at young adult stage from RNA-Seq data.

This corresponds to the same differential expression state summary column as in simple files (column 7 of over-/under-expression simple file)

##### Call quality (column 8)

Confidence in the differential expression call provided in `Differential expression` (column 7). Permitted values:

*   high quality: differential expression reported as high quality, with no contradicting call from same type of analysis (across anatomy/across life stages), for same gene, in same anatomical entity and developmental stage, (call generated either from multiple congruent analyses, or from a single analysis).
*   poor quality: differential expression reported as low quality, or there exists a conflict for the same gene, anatomical entity and developmental stage, from different analyses of a same data type (conflicts between different data types are treated differently). For instance, an analysis showed a gene to be over-expressed in a condition, while another analysis showed the same gene to be under-expressed or not differentially expressed in the same condition. Such conflicts are resolved by a voting system based on the number of conditions compared, weighted by p-value. Note that in one case, this quality level is used to reconcile conflicting calls from different data types: when a data type produced an under-expression call, while a different data type has shown that the same gene was never seen as expressed in the same condition. In that case, the overall summary is `under-expression low quality`.
*   NA: no quality applicable when ambiguity state in `Differential expression` (column 7).

This corresponds to the same differential expression quality column as in simple files (column 8 of over-/under-expression simple file)

##### Affymetrix data (column 9)

Call generated from Affymetrix data for `Gene ID` (column 1), in `Anatomical entity ID` (column 5), at `Developmental stage ID` (column 3). Permitted values:

*   over-expression: the gene was shown in one or more analyses to have a significant over-expression in this condition, as compared to the expression levels in other conditions of the analyses.
*   under-expression: the gene was shown in one or more analyses to have a significant under-expression in this condition, as compared to the expression levels in other conditions of the analyses.
*   no diff expression: the gene was tested for differential expression in this condition, but was never shown to have a significant variation of expression as compared to the other conditions of the analyses.
*   no data: no analyses of this data type compared expression level of this gene in this condition.

##### Affymetrix call quality (column 10)

Confidence in the differential expression call provided in `Affymetrix data` (column 9). Permitted values:

*   high quality: differential expression reported as high quality, with no contradicting call from same type of analysis (across anatomy/across life stages), for same gene, in same anatomical entity and developmental stage, (call generated either from multiple congruent analyses, or from a single analysis).
*   poor quality: differential expression reported as low quality, or there exists a conflict for the same gene, anatomical entity and developmental stage, from different analyses of a same data type (conflicts between different data types are treated differently). For instance, an analysis showed a gene to be over-expressed in a condition, while another analysis showed the same gene to be under-expressed or not differentially expressed in the same condition. Such conflicts are resolved by a voting system based on the number of conditions compared, weighted by p-value. Note that in one case, this quality level is used to reconcile conflicting calls from different data types: when a data type produced an under-expression call, while a different data type has shown that the same gene was never seen as expressed in the same condition. In that case, the overall summary is `under-expression low quality`.
*   no data: no data associated to `Affymetrix data` (column 9).

##### Affymetrix best supporting p-value (column 11)

Best p-value from the Affymetrix analyses supporting the Affymetrix call provided in `Affymetrix data` (column 9). Set to 1.0 if no data available by Affymetrix.

##### Affymetrix analysis count supporting Affymetrix call (column 12)

Number of Affymetrix analyses supporting the Affymetrix call provided in `Affymetrix data` (column 9). Set to 0 if no data available by Affymetrix.

##### Affymetrix analysis count in conflict with Affymetrix call (column 13)

Number of Affymetrix analyses in conflict, generating a call different from the call provided in `Affymetrix data` (column 9). Set to 0 if no data available by Affymetrix.

##### RNA-Seq data (column 14)

Call generated from RNA-Seq data for `Gene ID` (column 1), in `Anatomical entity ID` (column 5), at `Developmental stage ID` (column 3). Permitted values:

*   over-expression: the gene was shown in one or more analyses to have a significant over-expression in this condition, as compared to the expression levels in other conditions of the analyses.
*   under-expression: the gene was shown in one or more analyses to have a significant under-expression in this condition, as compared to the expression levels in other conditions of the analyses.
*   no diff expression: the gene was tested for differential expression in this condition, but was never shown to have a significant variation of expression as compared to the other conditions of the analyses.
*   no data: no analyses of this data type compared expression level of this gene in this condition.

##### RNA-Seq call quality (column 15)

Confidence in the differential expression call provided in `RNA-Seq data` (column 14). Permitted values:

*   high quality: differential expression reported as high quality, with no contradicting call from same type of analysis (across anatomy/across life stages), for same gene, in same anatomical entity and developmental stage, (call generated either from multiple congruent analyses, or from a single analysis).
*   poor quality: differential expression reported as low quality, or there exists a conflict for the same gene, anatomical entity and developmental stage, from different analyses of a same data type (conflicts between different data types are treated differently). For instance, an analysis showed a gene to be over-expressed in a condition, while another analysis showed the same gene to be under-expressed or not differentially expressed in the same condition. Such conflicts are resolved by a voting system based on the number of conditions compared, weighted by p-value. Note that in one case, this quality level is used to reconcile conflicting calls from different data types: when a data type produced an under-expression call, while a different data type has shown that the same gene was never seen as expressed in the same condition. In that case, the overall summary is `under-expression low quality`.
*   no data: no data associated to `RNA-Seq data` (column 14).

##### RNA-Seq best supporting p-value (column 16)

Best p-value from the RNA-Seq analyses supporting the RNA-Seq call provided in `RNA-Seq data` (column 14). Set to 1.0 if no data available by RNA-Seq.

##### RNA-Seq analysis count supporting RNA-Seq call (column 17)

Number of RNA-Seq analyses supporting the RNA-Seq call provided in `RNA-Seq data` (column 14). Set to 0 if no data available by RNA-Seq.

##### RNA-Seq analysis count in conflict with RNA-Seq call (column 18)

Number of RNA-Seq analyses in conflict, generating a call different from the call provided in `RNA-Seq data` (column 14). Set to 0 if no data available by RNA-Seq.

[Back to over-/under-expression menu](#single_diff)

<a name="multi"></a>Multi-species download files
------------------------------------------------

Bgee provides the ability to compare expression data between species, with great anatomical detail, using formal concepts of homology: orthology of genes, homology of anatomical entities. This allows to perform accurate comparisons between species, even for distant species for which the anatomy mapping might not be obvious.

*   homology of anatomical entities: When comparing multiple species, only anatomical entities homologous between all species compared are considered, meaning, only anatomical entities derived from an organ existing before the divergence of the species compared. This requires careful annotations of the homology history of animal anatomy. These annotations are described in a separate project maintained by the Bgee team, see [homology annotation project on GitHub](https://github.com/BgeeDB/anatomical-similarity-annotations/ "See anatomical-similarity-annotations project on GitHub").  
    In practice, when comparing expression data between several species, the anatomical entities used are those with a homology relation valid for their Least Common Ancestor (LCA), or any of its ancestral taxa. For instance, if comparing data between human and zebrafish, the LCA would be the taxon _Euteleostomi_; as a result, annotations to this taxon would be used, such as the relation of homology between "tetrapod parietal bone" (UBERON:0000210) and "actinopterygian frontal bone" (UBERON:0004866); but also, annotations to ancestral taxa, such as the annotation stating that "ophthalmic nerve" appeared in the _Vertebrata_ common ancestor; annotations to more recent taxa than the LCA would be discarded, such as the annotation to the "forelimb" structure (UBERON:0002102), homologous in the _Tetrapoda_ lineage.
*   orthology of genes: relations of orthology between genes are retrieved using [OMA](https://omabrowser.org/oma/hogs/ "External link to OMA browser"); when comparing several species, Bgee identifies their Least Common Ancestor (LCA), and retrieve genes that have descended from a single common ancestral gene in that LCA. Relations of orthology between genes are provided in Bgee through [hierarchical orthologous groups files](#oma_hog "Jump to hierarchical orthologous groups file documentation").

Jump to:

*   [OMA Hierarchical orthologous groups](#oma_hog "Quick jump to OMA HOG file")
*   [Over-/under-expression across anatomy or life stages](#multi_diff "Quick jump to differential expression")

### <a name="oma_hog"></a>OMA Hierarchical orthologous groups file

**Please note, these data will be available in a future release.**

OMA Hierarchical orthologous groups files provide gene orthology relations, by grouping genes that have descended from a single common ancestral gene in the taxon of interest. The targeted taxon is provided in the file name. Orthologous genes are grouped by common OMA IDs, provided in the column OMA ID (column 1, see below).

Format description for OMA Hierarchical orthologous groups file
|Column|Content|Example|
|--- |--- |--- |
|1|OMA ID|10|
|2|Gene ID|ENSG00000105298|
|3|Gene name|CACTIN|

Example lines for a OMA Hierarchical orthologous groups file
|OMA ID|Gene ID|Gene name|
|--- |--- |--- |
|98828|ENSG00000158473|CD1D|
|98828|ENSMUSG00000028076|Cd1d1|
|98828|ENSMUSG00000041750|Cd1d2|

##### OMA ID (column 1)

Unique identifier of the OMA gene orthology group. Note that these identifiers are not stable between releases, and cannot be used to retrieve data from [the OMA browser](https://omabrowser.org/oma/hogs/ "External link to OMA browser"). They are provided solely to group data from orthologous genes belonging to a same orthology group. Genes member of a OMA gene orthology group can be retrieved through the associated [hierarchical orthologous groups file](#oma_hog "Jump to hierarchical orthologous groups file documentation").

##### Gene ID (column 2)

Unique identifier of gene from Ensembl.

Please note that for _P. paniscus_ (bonobo) we use _P. troglodytes_ genome (chimpanzee), and that for _P. pygmaeus_ (Bornean orangutan) we use _P. abelii_ genome (Sumatran orangutan). Only for those species (bonobo and Bornean orangutan), we modify the Ensembl gene IDs, to ensure that we provide unique gene identifiers over all species. It is therefore necessary, to obtain correct Ensembl gene IDs for those species, to replace gene ID prefix 'PPAG' with 'ENSPTRG', and 'PPYG' prefix with 'ENSPPYG'.

##### Gene name (column 3)

Name of the gene defined by `Gene ID` (column 2)

[Back to multi-species download files menu](#multi)

### <a name="multi_diff"></a>Over-/under-expression across anatomy or life stages in multiple species

**Please note, these data will be available in a future release.**

Bgee provides calls of over-/under-expression. A call corresponds to a gene, with significant variation of its level of expression, in an anatomical entity during a developmental stage, as compared to, either: i) other anatomical entities at the same (broadly defined) developmental stage (over-/under-expression across anatomy); ii) the same anatomical entity at different (precise) developmental stages (over-/under-expression across life stages). These analyses of differential expression are performed using Affymetrix and RNA-Seq experiments with at least 3 suitable conditions (anatomical entity/developmental stage), and at least 2 replicates for each; as for all data in Bgee, only "normal" expression is considered (i.e., no treatment, no disease, no gene knock-out, etc.).

Bgee runs all possible differential expression analyses for each experiment independently, then collects all results and provides a summary as unique calls `gene - anatomical entity - developmental stage`, with confidence information, and conflicts within each data type resolved using a voting system weighted by p-values (conflicts between different data types are treated differently). This offers the possibility to aggregate and compare these calls between different experiments, different data types, and different species.

In multi-species files, results are made comparable between orthologous genes, in homologous anatomical entities and comparable developmental stages: only genes sharing a common ancestral gene in the least common ancestor of the species compared are studied, and only in anatomical entities sharing a homology relation between all species compared, with data mapped to broad developmental stages shared across animal kingdom (see [use of homology in multi-species files](#multi "Quick jump to multi-species file description")).

Note that, as opposed to calls of presence/absence of expression, no propagation of differential expression calls is performed using anatomical and life stage ontologies.

Over-/under-expression calls are then filtered and presented differently depending on whether a `simple file`, or a `complete file` is used. Notably: `simple files` aim at providing one line per gene orthology group and homologous anatomical entities/developmental stage, and only for anatomical entities with a homology relation defined with good level of confidence. `complete files` aim at reporting all information, for each gene of the orthology groups, using all available homology relations between anatomical entities, and allowing for instance to retrieve the contribution of each data type to a call, or to retrieve all genes and conditions tested, including genes having no differential expression in these conditions.

Jump to format description for:

*   [simple file](#multi_diff_simple "Quick jump to simple file description")
*   [complete file](#multi_diff_complete "Quick jump to complete file description")

#### <a name="multi_diff_simple"></a>Simple file

In simple files, each line provides information for a gene orthology group, in a condition (homologous anatomical entity/comparable developmental stage); columns then provide, for each species, the number of genes over-expressed, under-expressed, not differentially expressed or with inconclusive results, and with no data. This means that the number of columns is variable depending on the number of species compared.

In simple files, only lines with data in at least two species, and at least one over-expression or under-expression call in a species, are provided, and only for anatomical entities with a homology relation defined with a good level of confidence.

Relations of orthology between genes member of a same orthology gene group are provided through the associated [hierarchical orthologous groups file](#oma_hog "Jump to hierarchical orthologous groups file documentation").

Format description for multi-species simple differential expression file

|Column|Content|Cardinality|Example|
|--- |--- |--- |--- |
|1|OMA ID|1|80|
|2|Anatomical entity IDs|1 or greater|UBERON:0001898|
|3|Anatomical entity names|1 or greater|hypothalamus|
|4|Developmental stage ID|1|UBERON:0000113|
|5|Developmental stage name|1|post-juvenile adult stage|
|6|Over-expressed gene count for species1 (e.g., Over-expressed gene count for Homo sapiens)|1|1|
|7|Under-expressed gene count for species1 (e.g., Under-expressed gene count for Homo sapiens)|1|0|
|8|Not diff. expressed gene count for species1 (e.g., Not diff. expressed gene count for Homo sapiens)|1|0|
|9|NA gene count for species1 (e.g., NA gene count for Homo sapiens)|1|0|
|10|Over-expressed gene count for species2 (e.g., Over-expressed gene count for Mus musculus)|1|1|
|11|Under-expressed gene count for species2 (e.g., Under-expressed gene count for Mus musculus)|1|0|
|12|Not diff. expressed gene count for species2 (e.g., Not diff. expressed gene count for Mus musculus)|1|0|
|13|NA gene count for species2 (e.g., NA gene count for Mus musculus)|1|0|
|...|Over-expressed gene count for speciesXX|1|...|
|...|...|||
|(species*4 + 6)|Gene IDs|2 or greater|ENSG00000169057|ENSMUSG00000031393|
|(species*4 + 7)|Gene names|2 or greater|MECP2|Mecp2|

Example lines for multi-species simple differential expression file

|OMA ID|Anatomical entity IDs|Anatomical entity names|Developmental stage ID|Developmental stage name|Over-expressed gene count for Homo sapiens|Under-expressed gene count for Homo sapiens|Not diff. expressed gene count for Homo sapiens|NA gene count for Homo sapiens|Over-expressed gene count for Mus musculus|Under-expressed gene count for Mus musculus|Not diff. expressed gene count for Mus musculus|NA gene count for Mus musculus|Gene IDs|Gene names|
|--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |
|93|UBERON:0000473|testis|UBERON:0000113|post-juvenile adult stage|0|1|0|0|0|1|0|0|ENSG00000162512|ENSMUSG00000025743|SDC3|Sdc3|
|93|UBERON:0000955|brain|UBERON:0000113|post-juvenile adult stage|1|0|0|0|1|0|0|0|ENSG00000162512|ENSMUSG00000025743|SDC3|Sdc3|
|93|UBERON:0001134|skeletal muscle tissue|UBERON:0000113|post-juvenile adult stage|0|1|0|0|0|1|0|0|ENSG00000162512|ENSMUSG00000025743|SDC3|Sdc3|

##### OMA ID (column 1)

Unique identifier of the OMA gene orthology group. Note that these identifiers are not stable between releases, and cannot be used to retrieve data from [the OMA browser](https://omabrowser.org/oma/hogs/ "External link to OMA browser"). They are provided solely to group data from orthologous genes belonging to a same orthology group. Genes member of a OMA gene orthology group can be retrieved through the associated [hierarchical orthologous groups file](#oma_hog "Jump to hierarchical orthologous groups file documentation").

##### Anatomical entity IDs (column 2)

Unique identifiers of the homologous anatomical entities, from the Uberon ontology. Cardinality 1 or greater. When more than one anatomical entity is used, they are separated with the character `|`.

In most cases, the cardinality is 1, as most of the homologous anatomical entities compared in different species are not derived enough so that they are described by different anatomical concepts. But the cardinality can sometimes be greater, when homologous anatomical entities are highly derived in the species compared, and represented by distinct anatomical concepts.

For instance, if comparing expression data in human and zebrafish, the anatomical entity "bulbus arteriosus" (UBERON:0004152) would be considered, as it is believed to be homologous in the _Euteleostomi_ lineage; as it is represented by the same anatomical term in both species, the cardinality of the value for this column would be 1. But homology relations between distinct anatomical concepts would also be considered, such as the homology between lung (UBERON:0002048) and swim bladder (UBERON:0006860): these organs are believed to descend from a same common ancestral organ, existing in the ancestor of _Gnathostomata_, but are now sufficiently derived that they are represented by different anatomical concepts in these species; the cardinality of the value of this column would be 2, and the IDs of these anatomical entities would be separated by the character `|`, e.g., `UBERON:0002048|UBERON:0006860`.

##### Anatomical entity names (column 3)

Names of the anatomical entities defined by `Anatomical entity IDs` (column 2). Cardinality 1 or greater. When more than one anatomical entity is used, they are separated with the character `|`. See `Anatomical entity IDs` column description for more details.

##### Developmental stage ID (column 4)

Unique identifier of the developmental stage, from the Uberon ontology. For multi-species analyses, only broad developmental stages are used, common to the species being compared.

##### Developmental stage name (column 5)

Name of the developmental stage defined by `Developmental stage ID` (column 4)

##### Over-expressed gene count for speciesXX

Number of genes, members of the OMA orthologous gene group with ID provided in `OMA ID` (column 1), shown in one or more analyses to have a significant over-expression in this condition (`Anatomical entity IDs` (column 2), at `Developmental stage ID` (column 4)), as compared to the expression levels in other conditions of the analyses. This means that there were no conflicts found between results generated from different data types (result generated either from a single data type, or from congruent analyses of different data types). Note that there can still be conflicts between different analyses within a same data type, but such conflicts are resolved by a voting system based on the number of conditions compared, weighted by p-value, in order to produce a single differential expression call, taking into account all analyses from a given data type.

Please note that the list of all genes member of the OMA orthologous gene group with ID provided in `OMA ID` (column 1) is provided through the [hierarchical orthologous groups file](#oma_hog "Jump to hierarchical orthologous groups file documentation").

##### Under-expressed gene count for speciesXX

Number of genes, members of the OMA orthologous gene group with ID provided in `OMA ID` (column 1), shown in one or more analyses to have a significant under-expression in this condition (`Anatomical entity IDs` (column 2), at `Developmental stage ID` (column 4)), as compared to the expression levels in other conditions of the analyses. This means that there were no conflicts found between results generated from different data types (result generated either from a single data type, or from congruent analyses of different data types). Note that there can still be conflicts between different analyses within a same data type, but such conflicts are resolved by a voting system based on the number of conditions compared, weighted by p-value, in order to produce a single differential expression call, taking into account all analyses from a given data type.

Please note that the list of all genes member of the OMA orthologous gene group with ID provided in `OMA ID` (column 1) is provided through the [hierarchical orthologous groups file](#oma_hog "Jump to hierarchical orthologous groups file documentation").

##### Not diff. expressed gene count for speciesXX

Number of genes, members of the OMA orthologous gene group with ID provided in `OMA ID` (column 1), that were tested for differential expression in this condition (`Anatomical entity IDs` (column 2), at `Developmental stage ID` (column 4)), but that were never shown to have a significant variation of their level of expression as compared to the other conditions of the analyses, or for which conflicting results were generated from different data types.

Please note that the list of all genes member of the OMA orthologous gene group with ID provided in `OMA ID` (column 1) is provided through the [hierarchical orthologous groups file](#oma_hog "Jump to hierarchical orthologous groups file documentation").

##### NA gene count for speciesXX

Number of genes, members of the OMA orthologous gene group with ID provided in `OMA ID` (column 1), that were not tested for differential expression in this condition (`Anatomical entity IDs` (column 2), at `Developmental stage ID` (column 4)).

Please note that the list of all genes member of the OMA orthologous gene group with ID provided in `OMA ID` (column 1) is provided through the [hierarchical orthologous groups file](#oma_hog "Jump to hierarchical orthologous groups file documentation").

##### Gene IDs

IDs of the genes member of the OMA orthologous gene group with ID provided in `OMA ID` (column 1). Cardinality 2 or greater. IDs are separated with the character |.

This column is provided as additional information, members of OMA orthologous gene groups can be retrieved through the use of the [hierarchical orthologous groups file](#oma_hog "Jump to hierarchical orthologous groups file documentation").

##### Gene names

Name of the genes member of the OMA orthologous gene group with ID provided in `OMA ID` (column 1). Cardinality 2 or greater. Names are separated with the character |.

This column is provided as additional information, members of OMA orthologous gene groups can be retrieved through the use of the [hierarchical orthologous groups file](#oma_hog "Jump to hierarchical orthologous groups file documentation").

[Back to over-/under-expression menu](#multi_diff)

#### <a name="multi_diff_complete"></a>Complete file

In complete files, information for all genes are provided, in all conditions tested, for anatomical entities homologous between all species compared, and comparable broad developmental stages. As opposed to simple multi-species files, all homology relations available for the anatomical entities are considered, even from homology hypotheses with low support; a column allows to retrieve the level of confidence in the homology hypothesis used. Also, the number of columns in complete files is not variable, whatever the number of species compared is.

Relations of orthology between genes can be retrieved through the use of the [hierarchical orthologous groups file](#oma_hog "Jump to hierarchical orthologous groups file documentation"). This allows notably to detect genes with no data for a condition: if a gene is listed as a member of an orthology group, but there is no call for this gene in a given condition, it means that there is no data available for this gene in this condition.

Format description for multi-species complete differential expression file

|Column|Content|Cardinality|Example|
|--- |--- |--- |--- |
|1|OMA ID|1|42865|
|2|Gene ID|1|ENSMMUG00000012094|
|3|Gene name|1|RAB17|
|4|Anatomical entity IDs|1 or greater|UBERON:0002037|
|5|Anatomical entity names|1 or greater|cerebellum|
|6|Developmental stage ID|1|UBERON:0018241|
|7|Developmental stage name|1|prime adult stage|
|8|Latin species name|1|Macaca_mulatta|
|9|Differential expression|1|under-expression|
|10|Call quality|1|high quality|
|11|Affymetrix data|1|no data|
|12|Affymetrix call quality|1|no data|
|13|Affymetrix best supporting p-value|1|1.0|
|14|Affymetrix analysis count supporting Affymetrix call|1|0|
|15|Affymetrix analysis count in conflict with Affymetrix call|1|0|
|16|RNA-Seq data|1|under-expression|
|17|RNA-Seq call quality|1|high quality|
|18|RNA-Seq best supporting p-value|1|8.82E-7|
|19|RNA-Seq analysis count supporting RNA-Seq call|1|1|
|20|RNA-Seq analysis count in conflict with RNA-Seq call|1|0|
|21|Anatomy homology CIO ID|1|CIO:0000003|
|22|Anatomy homology CIO name|1|high confidence from single evidence|


Example lines for multi-species complete differential expression file

|OMA ID|Gene ID|Gene name|Anatomical entity IDs|Anatomical entity names|Developmental stage ID|Developmental stage name|Latin species name|Differential expression|Call quality|Affymetrix data|Affymetrix call quality|Affymetrix best supporting p-value|Affymetrix analysis count supporting Affymetrix call|Affymetrix analysis count in conflict with Affymetrix call|RNA-Seq data|RNA-Seq call quality|RNA-Seq best supporting p-value|RNA-Seq analysis count supporting RNA-Seq call|RNA-Seq analysis count in conflict with RNA-Seq call|Anatomy homology CIO ID|Anatomy homology CIO name|
|--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |
|59|ENSMUSG00000030516|Tjp1|UBERON:0000948|heart|UBERON:0018241|prime adult stage|Mus_musculus|over-expression|high quality|over-expression|high quality|0.0|5|0|no data|no data|1.0|0|0|CIO:0000004|medium confidence from single evidence|
|59|ENSMMUG00000017878|Tjp1|UBERON:0000948|heart|UBERON:0018241|prime adult stage|Macaca_mulatta|no diff expression|high quality|no data|no data|1.0|0|0|no diff expression|high quality|0.6239275|2|0|CIO:0000004|medium confidence from single evidence|
|59|ENSBTAG00000015398|ZO1|UBERON:0000948|heart|UBERON:0018241|prime adult stage|Bos_taurus|over-expression|high quality|no data|no data|1.0|0|0|over-expression|high quality|8.741838E-4|1|0|CIO:0000004|medium confidence from single evidence|


##### OMA ID (column 1)

Unique identifier of the OMA gene orthology group. Note that these identifiers are not stable between releases, and cannot be used to retrieve data from [the OMA browser](https://omabrowser.org/oma/hogs/ "External link to OMA browser"). They are provided solely to group data from orthologous genes belonging to a same orthology group. Genes member of a OMA gene orthology group can be retrieved through the associated [hierarchical orthologous groups file](#oma_hog "Jump to hierarchical orthologous groups file documentation").

##### Gene ID (column 2)

Unique identifier of gene from Ensembl.

Please note that for _P. paniscus_ (bonobo) we use _P. troglodytes_ genome (chimpanzee), and that for _P. pygmaeus_ (Bornean orangutan) we use _P. abelii_ genome (Sumatran orangutan). Only for those species (bonobo and Bornean orangutan), we modify the Ensembl gene IDs, to ensure that we provide unique gene identifiers over all species. It is therefore necessary, to obtain correct Ensembl gene IDs for those species, to replace gene ID prefix 'PPAG' with 'ENSPTRG', and 'PPYG' prefix with 'ENSPPYG'.

Please note that the list of all genes member of the OMA ortholoogous gene group with ID provided in `OMA ID` (column 1) is provided through the [hierarchical orthologous groups file](#oma_hog "Jump to hierarchical orthologous groups file documentation"). If a gene listed in this file has no call for the condition `Anatomical entity IDs` (column 4), at `Developmental stage ID` (column 6), it means that there is no data available for this gene in this condition.

##### Gene name (column 3)

Name of the gene defined by `Gene ID` (column 2)

##### Anatomical entity IDs (column 4)

Unique identifiers of the homologous anatomical entities, from the Uberon ontology. Cardinality 1 or greater. When more than one anatomical entity is used, they are separated with the character `|`.

In most cases, the cardinality is 1, as most of the homologous anatomical entities compared in different species are not derived enough so that they are described by different anatomical concepts. But the cardinality can sometimes be greater, when homologous anatomical entities are highly derived in the species compared, and represented by distinct anatomical concepts.

For instance, if comparing expression data in human and zebrafish, the anatomical entity "bulbus arteriosus" (UBERON:0004152) would be considered, as it is believed to be homologous in the _Euteleostomi_ lineage; as it is represented by the same anatomical term in both species, the cardinality of the value for this column would be 1. But homology relations between distinct anatomical concepts would also be considered, such as the homology between lung (UBERON:0002048) and swim bladder (UBERON:0006860): these organs are believed to descend from a same common ancestral organ, existing in the ancestor of _Gnathostomata_, but are now sufficiently derived that they are represented by different anatomical concepts in these species; the cardinality of the value of this column would be 2, and the IDs of these anatomical entities would be separated by the character `|`, e.g., `UBERON:0002048|UBERON:0006860`.

##### Anatomical entity names (column 5)

Names of the anatomical entities defined by `Anatomical entity IDs` (column 4). Cardinality 1 or greater. When more than one anatomical entity is used, they are separated with the character `|`. See `Anatomical entity IDs` column description for more details.

##### Developmental stage ID (column 6)

Unique identifier of the developmental stage, from the Uberon ontology. For multi-species analyses, only broad developmental stages are used, common to the species being compared.

##### Developmental stage name (column 7)

Name of the developmental stage defined by `Developmental stage ID` (column 6)

##### Latin species name (column 8)

The latin name of the species which the gene in Gene ID (column 2) belongs to.

##### Differential expression (column 9)

Call generated from all data types for `Gene ID` (column 2), in `Anatomical entity IDs` (column 4), at `Developmental stage ID` (column 6). Permitted values:

*   over-expression: the gene was shown in one or more analyses to have a significant over-expression in this condition, as compared to the expression levels in other conditions of the analyses.
*   under-expression: the gene was shown in one or more analyses to have a significant under-expression in this condition, as compared to the expression levels in other conditions of the analyses.
*   no diff expression: the gene was tested for differential expression in this condition, but was never shown to have a significant variation of expression as compared to the other conditions of the analyses.
*   weak ambiguity: there exists a call of over-expression or under-expression generated from a data type, but another data type showed no significant variation of the level of expression of this gene in the same condition; or, a gene was shown to be never expressed in a condition by some analyses of a given data type, but other analyses of different data types produced a call of over-expression or of absence of differential expression for the same gene, in the same condition (note that conflicts where a data type produced an under-expression call in a condition, while another data type showed the same gene to be never expressed in that condition, do not produce a `weak ambiguity` call, but a call of `under-expression low quality`).
*   strong ambiguity: there exists a call of over-expression or under-expression generated from a data type, but there exists a call in the opposite direction generated from another data type for the same gene, anatomical entity and developmental stage. For instance, gene A is reported to be over-expressed in the midbrain at young adult stage from Affymetrix data, but is reported to be under-expressed in the midbrain at young adult stage from RNA-Seq data.

##### Call quality (column 10)

Confidence in the differential expression call provided in `Differential expression` (column 2). Permitted values:

*   high quality: differential expression reported as high quality, with no contradicting call from same type of analysis (across anatomy/across life stages), for same gene, in same anatomical entity and developmental stage, (call generated either from multiple congruent analyses, or from a single analysis).
*   poor quality: differential expression reported as low quality, or there exists a conflict for the same gene, anatomical entity and developmental stage, from different analyses of a same data type (conflicts between different data types are treated differently). For instance, an analysis showed a gene to be over-expressed in a condition, while another analysis showed the same gene to be under-expressed or not differentially expressed in the same condition. Such conflicts are resolved by a voting system based on the number of conditions compared, weighted by p-value. Note that in one case, this quality level is used to reconcile conflicting calls from different data types: when a data type produced an under-expression call, while a different data type has shown that the same gene was never seen as expressed in the same condition. In that case, the overall summary is `under-expression low quality`.
*   NA: no quality applicable when ambiguity state in `Differential expression` (column 2).

##### Affymetrix data (column 11)

Call generated from Affymetrix data for `Gene ID` (column 2), in `Anatomical entity IDs` (column 4), at `Developmental stage ID` (column 6). Permitted values:

*   over-expression: the gene was shown in one or more analyses to have a significant over-expression in this condition, as compared to the expression levels in other conditions of the analyses.
*   under-expression: the gene was shown in one or more analyses to have a significant under-expression in this condition, as compared to the expression levels in other conditions of the analyses.
*   no diff expression: the gene was tested for differential expression in this condition, but was never shown to have a significant variation of expression as compared to the other conditions of the analyses.
*   no data: no analyses of this data type compared expression level of this gene in this condition.

##### Affymetrix call quality (column 12)

Confidence in the differential expression call provided in `Affymetrix data` (column 9). Permitted values:

*   high quality: differential expression reported as high quality, with no contradicting call from same type of analysis (across anatomy/across life stages), for same gene, in same anatomical entity and developmental stage, (call generated either from multiple congruent analyses, or from a single analysis).
*   poor quality: differential expression reported as low quality, or there exists a conflict for the same gene, anatomical entity and developmental stage, from different analyses of a same data type (conflicts between different data types are treated differently). For instance, an analysis showed a gene to be over-expressed in a condition, while another analysis showed the same gene to be under-expressed or not differentially expressed in the same condition. Such conflicts are resolved by a voting system based on the number of conditions compared, weighted by p-value. Note that in one case, this quality level is used to reconcile conflicting calls from different data types: when a data type produced an under-expression call, while a different data type has shown that the same gene was never seen as expressed in the same condition. In that case, the overall summary is `under-expression low quality`.
*   no data: no data associated to `Affymetrix data` (column 9).

##### Affymetrix best supporting p-value (column 13)

Best p-value from the Affymetrix analyses supporting the Affymetrix call provided in `Affymetrix data` (column 11). Set to 1.0 if no data available by Affymetrix.

##### Affymetrix analysis count supporting Affymetrix call (column 14)

Number of Affymetrix analyses supporting the Affymetrix call provided in `Affymetrix data` (column 11). Set to 0 if no data available by Affymetrix.

##### Affymetrix analysis count in conflict with Affymetrix call (column 15)

Number of Affymetrix analyses in conflict, generating a call different from the call provided in `Affymetrix data` (column 11). Set to 0 if no data available by Affymetrix.

##### RNA-Seq data (column 16)

Call generated from RNA-Seq data for `Gene ID` (column 2), in `Anatomical entity IDs` (column 4), at `Developmental stage ID` (column 6). Permitted values:

*   over-expression: the gene was shown in one or more analyses to have a significant over-expression in this condition, as compared to the expression levels in other conditions of the analyses.
*   under-expression: the gene was shown in one or more analyses to have a significant under-expression in this condition, as compared to the expression levels in other conditions of the analyses.
*   no diff expression: the gene was tested for differential expression in this condition, but was never shown to have a significant variation of expression as compared to the other conditions of the analyses.
*   no data: no analyses of this data type compared expression level of this gene in this condition.

##### RNA-Seq call quality (column 17)

Confidence in the differential expression call provided in `RNA-Seq data` (column 16). Permitted values:

*   high quality: differential expression reported as high quality, with no contradicting call from same type of analysis (across anatomy/across life stages), for same gene, in same anatomical entity and developmental stage, (call generated either from multiple congruent analyses, or from a single analysis).
*   poor quality: differential expression reported as low quality, or there exists a conflict for the same gene, anatomical entity and developmental stage, from different analyses of a same data type (conflicts between different data types are treated differently). For instance, an analysis showed a gene to be over-expressed in a condition, while another analysis showed the same gene to be under-expressed or not differentially expressed in the same condition. Such conflicts are resolved by a voting system based on the number of conditions compared, weighted by p-value. Note that in one case, this quality level is used to reconcile conflicting calls from different data types: when a data type produced an under-expression call, while a different data type has shown that the same gene was never seen as expressed in the same condition. In that case, the overall summary is `under-expression low quality`.
*   no data: no data associated to `RNA-Seq data` (column 16).

##### RNA-Seq best supporting p-value (column 18)

Best p-value from the RNA-Seq analyses supporting the RNA-Seq call provided in `RNA-Seq data` (column 16). Set to 1.0 if no data available by RNA-Seq.

##### RNA-Seq analysis count supporting RNA-Seq call (column 19)

Number of RNA-Seq analyses supporting the RNA-Seq call provided in `RNA-Seq data` (column 16). Set to 0 if no data available by RNA-Seq.

##### RNA-Seq analysis count in conflict with RNA-Seq call (column 20)

Number of RNA-Seq analyses in conflict, generating a call different from the call provided in `RNA-Seq data` (column 16). Set to 0 if no data available by RNA-Seq.

##### Anatomy homology CIO ID (column 21)

Unique identifier from the [Confidence Information Ontology](https://github.com/BgeeDB/confidence-information-ontology/blob/master/src/ontology/cio-simple.obo "External link to CIO in OBO"), providing the confidence in the annotation of homology of anatomical entities defined in `Anatomical entity IDs` (column 4). This ontology is an attempt to provide a mean to capture the confidence in annotations. See [project home](https://github.com/BgeeDB/confidence-information-ontology "External link to CIO project") for more details.

##### Anatomy homology CIO name (column 22)

Name of the CIO term defined by `Anatomy homology CIO ID` (column 21)

[Back to over-/under-expression menu](#multi_diff)