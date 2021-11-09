import io
from time import strftime, gmtime
import json
from datetime import datetime
from wikidataintegrator import wdi_core, wdi_login, wdi_helpers
from config import *
from query_catalog import *
from input_data_preprocessing import InputCSVDataDAO, np, ask_query
import time
from os import path

#Wikidata RDF properties considered
PROPS = {
    'expressed in': 'P5572',
    'stated in': 'P248',
    'retrieved': 'P813',
    'reference URL': 'P854',
    'UBERON ID': 'P1554',
    'Ensembl gene ID': 'P594',
    'found in taxon': 'P703',
    'instance of': 'P31',
    'Cell Ontology ID': 'P7963',
    'series ordinal': 'P1545'
}

#Existing wikidata individuals considered
ITEMS = {
    'Bgee': 'Q54985720',
    'Homo sapiens': 'Q15978631',
    'gene': 'Q7187'
}


def create_reference(item_id: str, database_target: str = ITEMS['Bgee'], url_prefix: str = GENE_PAGE_PREFIX) -> list:
    """Create wikidata reference subgraph to the Bgee database.

    :param item_id: the id considered in URL (i.e. url_prefix) query parameter. For example,
     Bgee database gene pages uses Ensembl ids in their URL such as https://bgee.org/?page=gene&gene_id=ENSG00000216588.
    :param database_target: the wikidata individual representing the database to be referenced.
    :param url_prefix: a URL prefix where url_prefix + itemid produces a valid URL to be referenced valid.
    :return: a list with wikidata statements
    """
    stated_in = wdi_core.WDItemID(database_target, PROPS['stated in'], is_reference=True)
    retrieved = wdi_core.WDTime(strftime("+%Y-%m-%dT00:00:00Z", gmtime()), PROPS['retrieved'], is_reference=True)
    url = url_prefix + item_id
    ref_url = wdi_core.WDUrl(url, PROPS['reference URL'], is_reference=True)
    return [stated_in, retrieved, ref_url]


def shortest_string_in_list(string_list: list) -> str:
    """
    Get the shortest string in terms of length from a list of string values.

    :param string_list: a list of string values.
    :return: the shortest string
    """
    next_index = 1
    size_list = len(string_list)
    if string_list is None or size_list == 0:
        raise
    else:
        shortest = string_list[0]
        while next_index < size_list and size_list > 1:
            if len(shortest) > len(string_list[next_index]):
                shortest = string_list[next_index]
            next_index = next_index + 1
    return shortest


def get_1to1_uberon_to_wikidata_id_mappings(uberon_wiki_id_map: dict = None) -> dict:
    """
    A mapper from an UBERON ontology term id to its corresponding wikidata individual id. If there is more than one
     wikidata entry per UBERON term, the entry with the shortest label is chosen. Therefore, the mappings are always
      1 UBERON id to 1 wikidata entry id.
    :param uberon_wiki_id_map: A dictionary where keys are UBERON ids that maps to a list of wikidata entry ids.
    :return: 1-to-1 mappings between UBERON ids and wikidata entry ids
    """
    response = {}
    if uberon_wiki_id_map is None:
        uberon_wiki_id_mapper = wdi_helpers.id_mapper(PROPS['UBERON ID'], return_as_set=True)
        uberon_wiki_id_mapper.update(wdi_helpers.id_mapper(PROPS['Cell Ontology ID'], return_as_set=True))
        #choose the Wikidata entry with the shortest label when there is a uberon id mapping to several wikidata entries
        uberon_wiki_id_map = {k: list(v) for k, v in uberon_wiki_id_mapper.items() if len(v) > 1}
        uberon_wiki_id_map = get_1to1_uberon_to_wikidata_id_mappings(uberon_wiki_id_map)
        uberon_wiki_id_map.update({k: v.pop() for k, v in uberon_wiki_id_mapper.items() if len(v) == 1})
        response = uberon_wiki_id_map
    else:
        for uberon_id, wikidata_ids in uberon_wiki_id_map.items():
            labels = []
            label_to_wiki_item = {}
            for wiki_id in wikidata_ids:
                item = wdi_core.WDItemEngine(wd_item_id=wiki_id, search_only=True)
                labels.append(item.get_label())
                label_to_wiki_item[item.get_label()] = wiki_id
            response[uberon_id] = label_to_wiki_item[shortest_string_in_list(labels)]
    return response


def get_ensembl2wikidata_gene_ids(species_item: str = ITEMS['Homo sapiens']) -> dict:
    """Get a mapper from Ensembl ids to Wikidata gene ids.

    :param species_item: specifies the wikidata species entry
    :return: a dictionary where the keys are Ensembl ids and the values are Wikidata gene ids.
    """
    uberon_wiki_id_mapper = wdi_helpers.id_mapper(PROPS['Ensembl gene ID'],
                                                  filters=[(PROPS['found in taxon'], species_item),
                                                           (PROPS['instance of'], ITEMS['gene'])],
                                                  return_as_set=True, raise_on_duplicate=True)
    return uberon_wiki_id_mapper



def run_one(wd_expressed_in_statements: dict, login, append_data:boolean = APPEND_DATA):
    """Insert statements of wikidata_gene_id expressed in wikidata_organ_id along with its reference.

    :param wd_expressed_in_statements: the Wikidata expressed in statements dictionary where the key is a wikidata gene
     id and the value is a list of Wikidata anatomic entity items.
    :param login: the Wikidata login object.
    """
    # create the item object, specifying the qid
    count = 0
    for wikidata_gene_id, organ_statements in wd_expressed_in_statements.items():
        if append_data:
            item = wdi_core.WDItemEngine(wd_item_id=wikidata_gene_id, search_only=True,
                                         global_ref_mode='STRICT_KEEP_APPEND')
            item.update(organ_statements, [PROPS['expressed in']])
        else:
            item = wdi_core.WDItemEngine(data=organ_statements, wd_item_id=wikidata_gene_id, fast_run=True,
                                 fast_run_base_filter={PROPS['expressed in']: ''})
        wdi_helpers.try_write(item, record_id=wikidata_gene_id+"-"+str(count),
                              record_prop=PROPS['expressed in'],
                          login=login, edit_summary="Update gene expression based on the Bgee database")
        count = count + 1


def gene_expressed_in_organ_statements(bgee_gene_id: object, wikidata_gene_ids: list, wikidata_organ_ids: list) -> dict:
    """Get Wikidata gene id to Wikidata anatomic entity items dictionary.

    :param bgee_gene_id: the gene id used in Bgee such as an Ensembl identifier
    :param wikidata_gene_ids: the Wikidata gene identifiers that corresponds to bgee_gene_id
    :param wikidata_organ_ids: the ordered Wikidata anatomic entity items that bgee_gene_id is expressed
    :return: a dictionary where key = Wikidata gene id, value = Wikidata anatomic entity items, otherwise an empty dictionary
    """
    reference = create_reference(bgee_gene_id)
    count_order = 1
    result_dict = {}
    statements = []
    for wikidata_organ_id in wikidata_organ_ids:
        #we consider that the organs ids are already ordered
        order = wdi_core.WDString(str(count_order), PROPS['series ordinal'], is_qualifier=True)
        count_order = count_order + 1
        expressed_in_statement = wdi_core.WDItemID(wikidata_organ_id, PROPS['expressed in'], references=[reference],
                                                   qualifiers=[order])
        statements.append(expressed_in_statement)
    for wikidata_gene_id in wikidata_gene_ids:
        result_dict.update({wikidata_gene_id: statements})
    return result_dict


def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
        # Print New Line on Complete
        if iteration == total:
            print()

def main():
    login = wdi_login.WDLogin(WDUSER, WDPASS)
    count = 0
    total = 100
    printProgressBar(count, total, prefix='Progress:', suffix='Complete', length=50)
    # setup wikidata log
    wdi_core.WDItemEngine.setup_logging(header=json.dumps(
        {'name': 'Bgee gene expression', 'timestamp': str(datetime.now()), 'run_id': str(datetime.now())}))
    # query wikidata to get mapping from uberon ids to wikidata ids
    uberon2wikidata_id_map = get_1to1_uberon_to_wikidata_id_mappings()
    # Load uberon ids to wikidata ids dictionary from a constant variable.
    # uberon2wikidata_id_map = UBERON2WIKIDATA_ID
    # Query wikidata to get mappings from Ensembl ids to wikidata ids
    ensembl2wikidata_pandas = InputCSVDataDAO.get_results_as_pandas_parser(BGEE_SPARQL_ENDPOINT,
                                                                           WIKIDATA2ENSEMBL_GENE_ID_MAP_QUERY)
    # Load ensembl ids to wikidata ids dictionary from a CSV file.
    # ensembl2wikidata_pandas = InputCSVDataDAO.get_results_as_pandas_parser(csv_file_path='ens2wikidata_ids.csv')
    ensembl2wikidata_id_map = ensembl2wikidata_pandas.groupby('ens_gene_id').agg(
        {'wikidata_gene_id': lambda x: list(x)}).to_dict()['wikidata_gene_id']
    # Query Bgee to get gene expression calls
    # It is limited to ~1.000.000 entries
    # gene_expression_file = InputCSVDataDAO().get_results_as_pandas_parser(BGEE_SPARQL_ENDPOINT,
    #                                                                       BGEE_EXPRESSION_QUERY_HUMAN_UBERON_PREFIXED,
    #                                                                      column_datatype={'uberon_id': np.str})
    # Get gene expression cals from a CSV file.
    gene_expression_file = InputCSVDataDAO().get_results_as_pandas_parser(csv_file_path=INPUT_BGEE_DATA_TSV,
                                                                          column_datatype={'uberon_id': np.str},
                                                                          separator='\t')
    # limit by group of 10 the bgee expression calls for each gene
    expressed_in_dict = InputCSVDataDAO.get_limited_results_grouped_by_column_dict(
        gene_expression_file, "gene_id", "uberon_id")
    uberon_wiki_list = uberon2wikidata_id_map.keys()
    ens_wiki_list = ensembl2wikidata_id_map.keys()
    heading = "ensembl_id,uberon_id,wikidata_gene_ids,wikidata_organ_id\n"
    added_statements = io.StringIO()
    added_statements.write(heading)
    total = len(expressed_in_dict.items())
    printProgressBar(count, total, prefix='Progress:', suffix='Complete', length=50)
    if path.exists("count.tmp"):
        with open("count.tmp", "r") as count_file:
            START_INDEX = int(count_file.readline())
        if START_INDEX >= total:
            print("All entries were already processed. To redo it, delete the file count.tmp in the current directory.")
    # Add bgee expression call statements to wikidata
    for ens_id, uberon_ids in expressed_in_dict.items():
        if count >= START_INDEX and count < total:
            wikidata_organ_list = []
            wikidata_gene_list = []
            if ens_id in ens_wiki_list:
                wikidata_gene_list = ensembl2wikidata_id_map[ens_id]
                for uberon_id in uberon_ids:
                    if uberon_id in uberon_wiki_list:
                        wikidata_organ_id = uberon2wikidata_id_map[uberon_id]
                        wikidata_organ_list.append(wikidata_organ_id)
                        added_statements.write(ens_id + "," + uberon_id + "," + str(wikidata_gene_list) + \
                                               "," + wikidata_organ_id + "\n")
                    else:
                        if uberon_id not in uberon_wiki_list:
                            # if a corresponding uberon item doesn't exist in wikidata, log it and skip
                            msg = wdi_helpers.format_msg(uberon_id, PROPS['expressed in'], "",
                                                         "UBERON term {} was not found in wikidata".format(uberon_id))
                            wdi_core.WDItemEngine.log("WARNING", msg)
            else:
                # if the item doesn't exist, log it and skip
                msg = wdi_helpers.format_msg(ens_id, PROPS['expressed in'], "",
                                             "It does not exist a Wikidata gene (from source Ensembl)" +
                                             " corresponding to the Ensembl id {} in wikidata".format(ens_id))
                wdi_core.WDItemEngine.log("WARNING", msg)
            if len(wikidata_gene_list) and len(wikidata_organ_list):
                wd_expressed_in_dict = gene_expressed_in_organ_statements(ens_id, wikidata_gene_list,
                                                                          wikidata_organ_list)
                run_one(wd_expressed_in_dict, login)
            with open("inserted_statements.csv", "a") as processed_file:
                processed_file.write(added_statements.getvalue())
                added_statements.close()
                added_statements = io.StringIO()
            if count % 100 == 0 and count > 0:
                time.sleep(10)
        count = count + 1
        printProgressBar(count, total, prefix='Progress:', suffix='Complete', length=50)
        with open("count.tmp", "w") as count_file:
            count_file.write(str(count))

if __name__ == '__main__':
    #Currently the bot can only update the entries of expressed in statements, if only if,
    #there is not other data source assining 'expressed in' (P5572) assertions into gene wikidata pages.
    try:
        # it considers the case where 'expressed in' statements from other data sources are assigned to wikidata genes
        if ask_query(BGEE_SPARQL_ENDPOINT, WIKIDATA_ONLY_BGEE_DATA):
            print("The bot cannot be executed in the overwrite mode, because there are 'expressed in' gene entries "
                  "in Wikidata which are not stated by this bot.")
            print("If you want to execute the bot in an append data mode, please set APPEND_DATA = True"
                  " in the config.py file and re-run this bot.")
        else:
            main()
    except ValueError as ve:
        print(ve.args[0] + str(ve.args[1]))
    except Exception as e:
        print(e.args)



