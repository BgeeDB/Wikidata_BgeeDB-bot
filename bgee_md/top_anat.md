TopAnat documentation
=====================

TopAnat is a tool to identify and visualize enriched anatomical terms, from the expression patterns of a list of genes.

It allows to discover where genes from a set are preferentially expressed, as compared to a background, represented by default by all expression data in Bgee for the requested species. It is is similar to a Gene Ontology enrichment test, except that it analyzes the anatomical structures where genes are expressed, rather than their GO functional annotations.

See also our [blog post](https://bgeedb.wordpress.com/category/topanat/ "Link to the Bgee Wordpress blog") about TopAnat for more information.

**Please note that the results can be slow to compute**, typically from 5 to 30 minutes, depending on the amount of data to process.

Quick start
-----------

### How to use

*   Enter a list of Ensembl identifiers into the first form field,
*   Optionally, enter a list of background genes,
*   Optionally, change the program parameters with the dropdown menu.
*   Click the 'Submit your job' button.

### Examples

*   [Mouse genes mapped to the GO term "spermatogenesis"](?page=top_anat#/result/00fecfca04bf1b2cf88ced9b0a937d68f0eea6cb "TopAnat example").
*   [Human genes involved in autism and epilepsy, with decorrelation](?page=top_anat#/result/8fce889da7b4519c5792573ed3933032c8122819 "TopAnat example").
*   [Mouse genes mapped to the GO term "neurological system process", with decorrelation and high quality data only](?page=top_anat#/result/e37009ba698919c75d06e81b3eca5d48f78210a0 "TopAnat example").
*   [Cow genes with the keyword 'muscle' in their UniProtKB/Swiss-Prot description](?page=top_anat#/result/7e8c74c073be03be4c40810c16c6be06c0bef1be "TopAnat example").
*   [Platypus genes located on X chromosome](?page=top_anat#/result/5fc8ff1fcfed7cfba0f82f82a67b418ce8a709b6 "TopAnat example").

Note of caution
---------------

In your analyses, you should be extremely careful about the definition of your universe (i.e., your background genes). The cases where it is correct to use the default background (i.e., all genes with data in Bgee for the selected species) should be actually rare. For instance, if you are studying a list of genes assigned to a specific GO category, then your universe should be 'all genes with a GO annotation', and not 'all genes with data in Bgee'. Of course, it is still useful to use the default background, for preliminary analyses, or when the biological signal extracted from your gene list is very strong. But it should often be more rigorously defined for data used in publications.

More information
----------------

TopAnat is based on [topGO](https://bioconductor.org/packages/topGO/ "topGO package in Bioconductor"). Adaptation of topGO courtesy of Adrian Alexa.