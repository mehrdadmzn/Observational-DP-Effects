"""Functions to get information about fields"""
from typing import Dict, List


def field_source(csv_dict: Dict, search_for_field: str):
    """Finds the csv files (from a basket) that contains the field in search_for field

    Args:
        csv_dict: The main csv/field/path dicitonary
        search_for_field: The target field to be located

    Returns:
        key_out: the key to the csv_dictionary (poining to the path of the source of the field)
        field_out: Prints the first instance of the field

    """
    key_out = ""
    field_out = ""
    for key in csv_dict.keys():
        for item in csv_dict.get(key).get("fields"):
            if item.startswith(f'''{search_for_field}-'''):
                print(f'''Field {search_for_field} is in {key}''')
                # print(item)
                key_out = key
                field_out = item
                break
    return key_out, field_out

def list_field_instances(main_dict:Dict, source_name:str, search_for_field:str):
    list_temp = main_dict.get(source_name).get("fields")
    list_out = [item for item in list_temp if item.startswith(f'''{search_for_field}-''')]
    return list_out