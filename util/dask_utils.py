import pandas as pd
from pandas import DataFrame
from typing import Tuple, List
from pandas.io.parsers import TextFileReader
import dask.dataframe as dd
import dask


def __dask_field_list_and_df(dd_in: dask.dataframe.DataFrame) -> Tuple[List[str], dask.dataframe.DataFrame]:
    """Reads the name of the columns/fields in the dask files in a list, and the dask dataframe
    This is recommended for internal use in the module only

    Args:
        dd_in: The dask dataframe of the core dada

    Returns:
        A list of column names, wit the eid as the first column (index = 0)
        And a dask dataframe

    """
    try:
        col_indices = dd_in.columns
        col_names = list(col_indices)
        return col_names, dd_in
        # Todo better exception handling
    except Exception as e:
        print(e)
    return None


def import_field_from_dask(dd_in: dask.dataframe.DataFrame, field_name: str,
                           eid_col: str = "eid") -> dask.dataframe.DataFrame:
    """Import the columns associated with a field from a dask file

    Args:
        dd_in: The dask dataframe of the csv files converted from the enc_ukb file
        field_name: The field name/code in UK Biobank showcase
        eid_col: The name of the index column, default is "eid"

    Returns:
        df_out: A Dask dataframe with eid as the index and all columns associated with the field_name.

    """
    first_row = None
    df_out = None
    col_names = dd_in.columns
    field_name_list = [col for col in col_names if col.startswith(f'''{field_name}-''')]
    if len(field_name_list) > 0:
        query_names = [eid_col] + field_name_list
        df_out = dd_in[query_names]
    else:
        raise Exception(f'''The field {field_name} does not exist''')
    return df_out
