import os
import sys

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_path, '..'))

from env.parameters import P
from util.parquet_maker import dask_to_parquet
import pandas as pd
import dask.dataframe as dd

pd.set_option('display.max_rows', 500)

dd_all_previous= dd.read_parquet(f'''{P.output_parquet_path}/{P.core_all_name}_previous''')
dd_new = dd.read_parquet(f'''{P.output_parquet_path}/{P.core_4_name}''')


# Any common columns?
cols_1 = dd_all_previous.columns
cols_2 = dd_new.columns


cols_1_no_eid = [item for item in cols_1 if item != "eid"]
cols_2_no_eid = [item for item in cols_2 if item != "eid"]

# intersection does not work
# There are shared columns between core_1 and core_2 but the number of eids are the same
# they are the same columns, so here we keep only one
# cols_intersect = cols_1.intersection(cols_2).intersection(cols_3)

intersect_1_2 = [item for item in cols_2_no_eid if item in cols_1_no_eid]


if (len(intersect_1_2) > 0):
    print("There are column overlaps. The columns will be unique selected from core_all and the new core file. ")
else:
    print("No column overlap.")
# Make unique columns
# cols_1_unique = [item for item in cols_1 if item not in cols_1_no_eid]
print(f'''Number of columns in core_all = {len(cols_1)}''')
cols_2_unique = [item for item in cols_2 if item not in cols_1_no_eid]
print(f'''Number of columns in the new core = {len(cols_2)}''')
print(f'''Number of overlapping cols dropped form the new core = {len(cols_2)-len(cols_2_unique)}''')
print(f'''Number of unique cols in the new core (+eid) = {len(cols_2_unique)}''')
dd_new = dd_new[cols_2_unique]


print("Set index")
dd_all_previous = dd_all_previous.set_index("eid")
dd_new = dd_new.set_index("eid")


print("Repartition")
dd_all_previous = dd_all_previous.repartition(partition_size="100MB")
dd_new = dd_new.repartition(partition_size="100MB")

# Joining
print("Joining")
dd_join = dd.merge(dd_all_previous, dd_new, on="eid", how="outer")
dd_join = dd_join.reset_index()

print(f'''Saving as {P.core_all_name}...''')
dask_to_parquet(dd_join,
                output_path=P.output_parquet_path,
                output_parquet_name=P.core_all_name,
                write_index=False)
print("Done")