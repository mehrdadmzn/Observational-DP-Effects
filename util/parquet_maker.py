import pandas as pd
import numpy as np
import dask.dataframe as dd
from pathlib import Path


def dask_to_parquet(dask_df, output_path, output_parquet_name, write_index=True):
    """Converts Dask to Parquet
    """
    folder_path_text = f'''{output_path}/{output_parquet_name}'''
    folder_path = Path(folder_path_text)
    try:
        if folder_path.exists():
            if any(folder_path.iterdir()):
                raise OSError("folder for parquet file is not empty")
            else:
                create_file = True
        else:
            print(f'''{folder_path_text} does not exist. Creating the folder''')
            create_file = True
        if create_file:
            print(f'''To parquet ...''')
            dask_df.to_parquet(folder_path_text, write_index=write_index)
            print(f'''parquet files saved in {folder_path_text}''')

    except OSError as oe:
        print(f"Cause OSError: {oe}")
    except Exception as e:
        print(f"Cause Exception: {e}")


def csv_to_parquet(csv_file: str, output_path: str, output_name: str, delimiter=",", write_index=False):
    """Converts CSV to Parquet
    """
    dd_in = dd.read_csv(csv_file, delimiter=delimiter, dtype=str)
    dask_to_parquet(dd_in, output_path=output_path, output_parquet_name=output_name, write_index=write_index)


def txt_to_dask(txt_file: str, output_path: str, output_name: str, delimiter="\t", write_index=False):
    dd_in = dd.read_csv(txt_file, delimiter=delimiter, dtype=str)
    dask_to_parquet(dd_in, output_path=output_path, output_parquet_name=output_name, write_index=write_index)
