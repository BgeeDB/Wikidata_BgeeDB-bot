from os import PathLike
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
from pandas.io.parsers import *
from typing import Union
from pandas import Series, DataFrame
from io import StringIO
import numpy as np

class InputCSVDataDAO:

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def get_results_as_pandas_parser(sparql_endpoint: str = None, sparql_query: str = None,
                                     csv_file_path: PathLike = None, column_datatype: dict = None, separator : str = ','
                                     ) -> Union[TextFileReader, Series, DataFrame, None]:
        """This method convert either a SPARQL query response or a CSV file into a pandas object.

        :param sparql_endpoint: the SPARQL endpoint URL. It should support CSV response.
        :param sparql_query: the SPARQL query to be addressed to the SPARQL endpoint
        :param csv_file_path: the file path to load a CSV file
        :param column_datatype: (optional) explicitly define the CSV column types, e.g. {'uberon_id':np.str}
        :return: a panda object
        """
        if sparql_query is not None and sparql_endpoint is not None:
            sparql = SPARQLWrapper(sparql_endpoint)
            sparql.setQuery(sparql_query)
            #JSON format is preferable, because not all SPARQL endpoints support well other formats
            sparql.setReturnFormat(JSON)
            result_dic = sparql.query().convert()
            results = StringIO("")
            header = ""
            header_list = result_dic['head']['vars']
            for var in header_list:
                header = header + "," + var
            results.write(header[1:] + "\n")
            for binding in result_dic['results']['bindings']:
                row = ""
                for var in header_list:
                    row = row + "," + str(binding[var]['value'])
                results.write(row[1:] + "\n")
            results.seek(0)
        else:
            if csv_file_path is not None:
                results = csv_file_path
            else:
                raise ValueError("Values must be set for either sparql-related or file path parameters.")
        csv_result_panda = pd.read_csv(results, sep=separator, low_memory=False, dtype=column_datatype)
        if isinstance(results, StringIO):
            results.close()
        return csv_result_panda

    @staticmethod
    def get_limited_results_grouped_by_column_pd(pandas_parsed_data: Union[TextFileReader, Series, DataFrame],
                                           column: str, limit: int = 10) -> DataFrame:
        """Limit the number of table rows per group. Resulted rows are grouped by a common value of a given column in
         a pandas DataFrame object.

        :param pandas_parsed_data: a pandas object.
        :param column: the column to apply the group by operation.
        :param limit: the maximum number of values per group.
        :return: a pandas DataFrame.
        """
        data_frame_to_dict = pandas_parsed_data.to_dict()
        index_to_cell_value_dict = data_frame_to_dict.get(column)
        indexes = []
        count = 0
        keys = index_to_cell_value_dict.keys()
        for index in keys:
            current_cell = index_to_cell_value_dict.get(index)
            if index+1 < keys.__len__():
                next_cell = index_to_cell_value_dict.get(index+1)
                if current_cell == next_cell:
                    if count < limit:
                        indexes.append(index)
                        count = count + 1
                else:
                    if count < limit:
                        indexes.append(index)
                    count = 0
            else:
                if count < limit:
                    indexes.append(index)
        original_columns = data_frame_to_dict.keys()
        data_subset = []
        for (index, series) in pandas_parsed_data.iterrows():
            if index in indexes:
                data_subset.append(series.to_numpy())
        df = pd.DataFrame(data=data_subset, columns=original_columns)
        return df

    @staticmethod
    def get_limited_results_grouped_by_column_dict(pandas_parsed_data: Union[TextFileReader, Series, DataFrame],
                                           column: str, column2: str, limit: int = 10) -> dict:
        """Limit the number of table rows per group. Resulted rows are grouped by a common value of a given column in
         a pandas DataFrame object. The result is a dictionary composed of column and column2.

        :param pandas_parsed_data: a pandas object.
        :param column: the column to apply the group by operation.
        :param column2: the second column to be considered in the output.
        :param limit: the maximum number of values per group.
        :return:
        """
        dict_aux = pandas_parsed_data.groupby(column).agg({column2: lambda x: list(x)}).to_dict()[column2]
        dict_response = {}
        for key, value in dict_aux.items():
            if len(value) >= 10:
                dict_response[key] = value[0:10]
            else:
                dict_response[key] = value[0:len(value)]
        return dict_response

def ask_query(sparql_endpoint: str = None, sparql_query: str = None) -> bool:
    sparql = SPARQLWrapper(sparql_endpoint)
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)
    if sparql.queryType != "ASK":
        raise ValueError("It is not a ASK query type.", sparql_query)
    else:
        results = sparql.query().convert()
        return results['boolean']





