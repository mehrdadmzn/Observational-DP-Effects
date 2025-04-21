import os
import sys

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_path, '..'))

import env.parameters as P
from util.parquet_maker import dask_to_parquet
import pandas as pd
import dask.dataframe as dd

pd.set_option('display.max_rows', 500)

dd_1 = dd.read_parquet(f'''{P.output_parquet_path}/{P.core_1_name}''')
dd_2 = dd.read_parquet(f'''{P.output_parquet_path}/{P.core_2_name}''')
dd_3 = dd.read_parquet(f'''{P.output_parquet_path}/{P.core_3_name}''')

# Any common columns?
cols_1 = dd_1.columns
cols_2 = dd_2.columns
cols_3 = dd_3.columns

cols_1_no_eid = [item for item in cols_1 if item != "eid"]
cols_2_no_eid = [item for item in cols_2 if item != "eid"]
cols_3_no_eid = [item for item in cols_2 if item != "eid"]

# intersection does not work
# There are shared columns between core_1 and core_2 but the number of eids are the same
# they are the same columns, so here we keep only one
# cols_intersect = cols_1.intersection(cols_2).intersection(cols_3)

intersect_1_2 = [item for item in cols_2_no_eid if item in cols_1_no_eid]
intersect_1_3 = [item for item in cols_3_no_eid if item in cols_1_no_eid]
intersect_2_3 = [item for item in cols_3_no_eid if item in cols_2_no_eid]

if (len(intersect_1_2) > 0) | (len(intersect_1_3) > 0) | (len(intersect_2_3) > 0):
    print("There are column overlaps. The columns will be unique selected from core_1, core_2, then core_3. ")
else:
    print("No column overlap.")
# Make unique columns
# cols_1_unique = [item for item in cols_1 if item not in cols_1_no_eid]
print(f'''Number of columns in core_1 = {len(cols_1)}''')
cols_2_unique = [item for item in cols_2 if item not in cols_1_no_eid]
print(f'''Number of columns in core_2 = {len(cols_2)}''')
print(f'''Number of overlapping cols dropped form core_2 = {len(cols_2)-len(cols_2_unique)}''')
print(f'''Number of unique cols in core_2 (+eid) = {len(cols_2_unique)}''')
dd_2 = dd_2[cols_2_unique]
cols_3_unique = [item for item in cols_3 if item not in cols_1_no_eid + cols_2_no_eid]
print(f'''Number of columns in core_3 = {len(cols_3)}''')
print(f'''Number of overlapping cols dropped form core_3 = {len(cols_3)-len(cols_3_unique)}''')
print(f'''Number of unique cols in core_3 (+eid) = {len(cols_3_unique)}''')
dd_3 = dd_3[cols_3_unique]

print("Set index")
dd_1 = dd_1.set_index("eid")
dd_2 = dd_2.set_index("eid")
dd_3 = dd_3.set_index("eid")

print("Repartition")
dd_1 = dd_1.repartition(partition_size="100MB")
dd_2 = dd_2.repartition(partition_size="100MB")
dd_3 = dd_3.repartition(partition_size="100MB")

# Joining
print("Joining")
dd_join_1 = dd.merge(dd_1, dd_3, on="eid", how="outer")
dd_join_out = dd.merge(dd_join_1, dd_2, on="eid", how="outer")
dd_join_out = dd_join_out.reset_index()

print(f'''Saving as {P.core_all_name}...''')
dask_to_parquet(dd_join_out,
                output_path=P.output_parquet_path,
                output_parquet_name=P.core_all_name,
                write_index=False)
print("Done")