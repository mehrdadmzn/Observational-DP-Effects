from typing import Tuple, List

def list_field_instances(col_list: List, search_for_field: str):
    """Listing the instances of a field
    """
    list_out = [item for item in col_list if item.startswith(f'''{search_for_field}-''')]
    return list_out


def field_availability_check(col_list: List, search_for_field: str) -> bool:
    """Checks if a field is available in a downloaded basket
    """
    list_out = list_field_instances(col_list, search_for_field)
    if len(list_out) == 0:
        return False
    return True