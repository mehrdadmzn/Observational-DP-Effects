"Functions for basic field processing/extraction"
import pandas as pd
from pandas import DataFrame
import dask.dataframe as dd


def drop_null_filed_4_instance(df_field: DataFrame,
                               field: str) -> DataFrame:
    """Drops the null values in fields with standard four instances only

    Args:
        df_field: The Pandas dataframe with eid and the four instances of the field.
        field: The name/number of the field.

    Returns:
        df_out: The Pandas dataframe with rows with all null values across instances dropped.
    """

    df_out = df_field.copy()
    df_out = df_out[(df_out[f'''{field}-0.0'''].notnull()) |
                    (df_out[f'''{field}-1.0'''].notnull()) |
                    df_out[f'''{field}-2.0'''].notnull() |
                    df_out[f'''{field}-3.0'''].notnull()]
    drop_size = df_field.shape[0] - df_out.shape[0]
    if drop_size == 0:
        print("No null values found.")
    else:
        print(f'''{df_field.shape[0] - df_out.shape[0]} null rows will be dropped''')
    return df_out
