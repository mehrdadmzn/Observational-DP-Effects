"""Imports all columsn associated with one field from the csv file"""
import pandas as pd
from pandas import DataFrame
from typing import Tuple, List
from pandas.io.parsers import TextFileReader
import dask.dataframe as dd


def import_eid_from_csv(csv_path: str, eid_col: str = "eid") -> DataFrame:
    """Imports the index column (eid) from the original csv data.

    Args:
        csv_path: The path of the csv files converted from the enc_ukb file
        eid_col: The name of the index column, default is "eid"

    Returns:
        df_out: A Pandas datafarme with one column (eid)

    """
    try:
        df_out = pd.read_csv(csv_path, usecols=[0])
        return df_out
    except FileNotFoundError:
        print(f'''File {csv_path} does not exist.''')
    except pd.errors.EmptyDataError:
        print("The file is empty")
    except pd.errors.ParserError as e:
        print(f'''Parsing error: {e}''')
    return None



def __csv_field_list_and_df(csv_path: str) -> Tuple[List[str], pd.DataFrame]:
    """Reads the name of the columns/fields in the original csv file in a list and the first row of the csv.
    This is recommented for internal use in the module only

    Args:
        csv_path: The path of the csv files converted from the enc_ukb file

    Returns:
        A list of column names, wit the eid as the first columns (index = 0)
        And a dataframe with the firs trow of the csv file

    """
    try:
        first_row = pd.read_csv(csv_path, nrows=1)
        col_indices = first_row.columns
        col_names = list(col_indices)
        return col_names, first_row
    except FileNotFoundError:
        print(f'''File {csv_path} does not exist.''')
    except pd.errors.EmptyDataError:
        print("The file is empty")
    except pd.errors.ParserError as e:
        print(f'''Parsing error: {e}''')
    return None


def csv_field_list(csv_path: str) -> List[str]:
    """Returns the list of all fields in a csv file

    Args:
        csv_path: The path of the csv files converted from the enc_ukb file

    Returns:
        A list of column names, wit the eid as the first columns (index = 0)
    """

    list_out, _ = __csv_field_list_and_df(csv_path)
    return list_out


def import_field_from_csv(csv_path: str, field_name: str, eid_col: str = "eid") -> pd.DataFrame:
    """Import the columns associated with a field from the original csv data.
    
    Args:
        csv_path: The path of the csv files converted from the enc_ukb file
        field_name: The field name/code in UK Biobank showcase
        eid_col: The name of the index column, default is "eid"

    Returns:
        df_out: A Pandas dataframe with patid as the index and all columns associated with the field_name.

    """
    first_row = None
    df_out = None
    col_names, first_row = __csv_field_list_and_df(csv_path)
    query_names = [col for col in col_names if col.startswith(f'''{field_name}-''')]
    if len(query_names) > 0:
        query_indices = [first_row.columns.get_loc(col) for col in query_names]
        df_out = pd.read_csv(csv_path, usecols=[0] + query_indices)
    else:
        raise Exception(f'''The field {field_name} does not exist in {csv_path}''')
    return df_out
