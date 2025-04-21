import os
import sys

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_path, '..'))

from util.parquet_maker import txt_to_dask
from env.parameters import P

for item in ["gp_clinical",
             "gp_scripts",
             "hesin",
             "hesin_diag",
             "hesin_critical",
             "hesin_oper"]:

    try:
        print(f'''Writing {item} ...''')
        txt_to_dask(f'''{P.data_portal_path}/{item}.txt''',
                    output_path=P.output_parquet_path,
                    output_name=item, delimiter="\t")
        print(f'''{item}: Done /n''')
    except Exception as e:
        print(e)
