import os
import sys

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_path, '..'))

from util.parquet_maker import csv_to_parquet
from env.parameters import P


csv_to_parquet(f'''{P.raw_data_path}/ukb675320.csv''',
               output_path=P.output_parquet_path,
               output_name = "core_1", delimiter=",")

csv_to_parquet(f'''{P.raw_data_path}/ukb675321.csv''',
               output_path=P.output_parquet_path,
               output_name = "core_2", delimiter=",")

csv_to_parquet(f'''{P.raw_data_path}/ukb676966.csv''',
               output_path=P.output_parquet_path,
               output_name = "core_3", delimiter=",")

csv_to_parquet(f'''{P.raw_data_path}/ukb677573.csv''',
               output_path=P.output_parquet_path,
               output_name = "core_4", delimiter=",")
