"""Imports all columsn associated with one field from the parquet file"""
import pandas as pd
from pandas import DataFrame
from typing import Tuple, List
from pandas.io.parsers import TextFileReader
import dask.dataframe as dd

def import_eid_from_parquet(parquet_path: str, eid_col: str = "eid") -> DataFrame:
    """Imports the index column (eid) from the parquet files.

    Args:
        parquet_path: The path of the csv files converted from the enc_ukb file
        id_col: The name of the index column, default is "eid"

    Returns:
        df_out: A Dask datafarme with one column (eid)

    """
    try:
        df_out = dd.read_parquet(parquet_path, columns=[eid_col])
        return df_out
    # Todo better exception handling
    except Exception as e:
        print(e)
    return None

def eid_union(eid_dd_list: List) -> DataFrame:
    """Makes a union of eids from each individual dask just in case

    Args:
        eid_dd_list: List of dast dataframes with one column only (eid).
        These dataframes are the outputs of import_eid_from parquet.
    Returns:
        A dask dataframe with one column (eid) of all eids from Dask dataframes
    """


def parquet_field_list(parquet_path: str) -> List[str]:
    """Returns the list of all fields in a parquet file

    Args:
        parquet_path: The path of the parquet files converted from the enc_ukb file

    Returns:
        A list of column names, wit the eid as the first columns (index = 0)
    """

    list_out, _ = __parquet_field_list_and_df(parquet_path)
    return list_out

