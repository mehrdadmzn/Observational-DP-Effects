"""Functions to extract phenoypte and eventdates from self reported mecical conditions, field 20002"""
import pandas as pd
from pandas import DataFrame
from typing import Tuple, List


def _step_1_self_reported_code_hit(code: str,
                                   df_reported: DataFrame,
                                   id_col: str = "eid",
                                   return_full_df: bool = False) -> DataFrame:
    """Find the rows in field 20002 that had the specified code in the data coding 6.

    Args:
        code: The code for the medical condition as used in Field 20002 (date coding 6)
        df_reported: The Pandas dataframe with eid and all the instances of the field 20002
        id_col: The name of the id col (default= eid)
        return_full_df: For debug purposes. If True, the output dataframe will contain all columns.

    Return:
        df_hit: A Pandas dataframe showing the eids that had the specified code in any of the instances of the field 20002
    """
    df = df_reported.copy()
    # Indicates a code hit
    df['code_hit'] = 0
    # The column that had the code
    df['col_hit'] = ""
    # The index of the column that had the code. This will be used to find the associated date in field 20008
    df['index_hit'] = -1
    for index, item in enumerate(df.columns):
        df.loc[df[item] == code, 'code_hit'] = 1
        df.loc[df[item] == code, 'col_hit'] = df.columns[index]
        df.loc[df[item] == code, 'index_hit'] = index - 1
    # Keep only code hits
    df_hit = df[df["code_hit"] == 1]
    # For debug purposes
    if not return_full_df:
        df_hit = df_hit[[id_col, 'col_hit', 'index_hit']]
    return df_hit


def _step_2_self_reported_code_hit_date(df_hit: DataFrame,
                                        df_reported_date: DataFrame,
                                        id_col: str = "eid",
                                        return_full_df: bool = False) -> DataFrame:
    """Finds the associated interpolated year in field 20008.

    Args:
        df_hit: The output of the step_1_self_reported_code_hit function
        df_reported_date: The Pandas dataframe with eid and all the instances of the field 20008
        id_col: The name of the id col (default= eid)
        return_full_df: For debug purposes. If True, the output dataframe will contain all columns.

    Return:
        df_hit_join: The dataframe with the inerpolated year associated with the code in field 20002
    """
    df = df_hit.copy()
    df['year_hit'] = 0
    index_offset = len(df.columns)
    out_col_list = df.columns
    df_hit_join = pd.merge(df, df_reported_date, on=id_col, how="left")
    df_hit_join['year_hit'] = df_hit_join.apply(lambda row: row.iloc[row['index_hit'] + index_offset], axis=1)
    if not return_full_df:
        df_hit_join = df_hit_join[out_col_list]
    return df_hit_join


def _step_3_self_reported_evdt_extractor(df_hit_date: DataFrame,
                                         code: str) -> DataFrame:
    """Trnasforms the interpolated date in field 20008 to yyyy-MM-dd format.
    Note that the interpolated field is in the yyyy.0 to yyyy.9 format.
    This function uses the number after the decimal point + 1 as the month, and 1 as the day.

    For example, the 2007.0 will be transformed to 2007-01-01 and 2007.9 will be transformed ot 2009-10-01

    Args:
        df_hit_date: The output of the  step_2_self_reported_code_hit_date function
        code: The code for the medical condition as used in Field 20002 (date coding 6)
    Return:
        The input datafrmae + the evdt_{code} as the event date.
    """
    df = df_hit_date.copy()
    cols_out = list(df.columns)
    df = df[df["year_hit"].notnull()]
    df['year_only'] = df['year_hit'].astype(int)
    # filter
    df = df[(df["year_only"] != -1) & (df["year_only"] != -3)]
    df['month_only'] = ((df['year_hit'] - df['year_only']) * 10 + 1).astype(int)
    col_evdt = f'''evdt_{code}'''
    df[col_evdt] = pd.to_datetime(df['year_only'].astype(str) +
                                  '-' +
                                  df['month_only'].astype(str) +
                                  '-' +
                                  "01")
    return df[cols_out + [col_evdt]]


def self_reported_pheno_extractor(df_reported: DataFrame,
                                  df_reported_date: DataFrame,
                                  code: str,
                                  id_col: str = "eid") -> DataFrame:
    """Extracts the self reported phenotype. Quality controls are not applied.

    Args:
        df_reported: The Pandas dataframe with eid and all the instances of the field 20002.
        df_reported_date: The Pandas dataframe with eid and all the instances of the field 20008.
        code: The code for the medical condition as used in Field 20002 (date coding 6).
        id_col: The name of the id col (default= eid).

    Return:
        df_hit_evdt: The dataframe with eid, col_hit (the column in 20002 that had the code),
            index_hit (the index of the column in 20002 that had the code),
            year_hit (the interpolated year),
            evdt_{code} (the event date of the "code" event in yyyy-MM-dd format
    """
    df_hit_in = _step_1_self_reported_code_hit(code, df_reported, id_col=id_col, return_full_df=False)
    df_hit_date_in = _step_2_self_reported_code_hit_date(df_hit_in, df_reported_date, id_col=id_col,
                                                         return_full_df=False)
    df_hit_evdt = _step_3_self_reported_evdt_extractor(df_hit_date_in, code=code)
    return df_hit_evdt


def qc_self_reported_against_cohort(df_self_reported_pheno: DataFrame,
                                    evdt_col: str,
                                    df_cohort: DataFrame,
                                    drop_wrong_dates: bool = True,
                                    id_col: str = "eid",
                                    dob_col: str = "dob",
                                    dod_col: str = "dod"):
    """Reports or cleans the self reported phenotype for wrong event dates.
    This funciton drops -1 and -3 categories and any event dates still before the date of birth or the date of death.

    Args:
        df_self_reported_pheno: The dataframe with the event dates for a specific code in the field 20002.
        evdt_col: The name of the event date column. It is in the evdt_{code} format.
        df_cohort: The Pandas dataframe of the cohort with at least eid, date of birth and date of death columns.
        drop_wrong_dates: If False, the function only reports discrepencies. If True, it will return the dataframe
            with discrepencies removed.
        id_col: The name of the id col (defaul= eid).
        dob_col: The name of the date of birth col (default = dob)
        dod_col: The name of the date of deat col (default  = dod)

    Return:
        The original or clean dataframe (depending on drop_wrong_dates)
    """
    cols_out = df_self_reported_pheno.columns
    df = pd.merge(df_self_reported_pheno, df_cohort[[id_col, dob_col, dod_col]], on=id_col, how="left")
    count_dob_before = df[df[evdt_col] < df['dob']].shape[0]
    qc_passed = True
    if count_dob_before > 0:
        print(f'''Records with event date before the date of birth = {count_dob_before}''')
        qc_passed = False
        if drop_wrong_dates:
            df = df[df[evdt_col] >= df['dob']]
            print(f'''Records with event date before the date of birth are dropped''')
            print(f'''Remaining records = {df.shape[0]}''')
    count_dob_equal = df[df[evdt_col] == df['dob']].shape[0]
    if count_dob_equal > 0:
        print(f'''Records with event date as the date of birth = {count_dob_equal}''')
        qc_passed = False
        if drop_wrong_dates:
            df = df[df[evdt_col] > df['dob']]
            print(f'''Records with event date as the date of birth are dropped''')
            print(f'''Remaining records = {df.shape[0]}''')
    count_dod_after = df[(df[dod_col].notnull()) & (df[evdt_col] > df[dod_col])].shape[0]
    if count_dod_after > 0:
        qc_passed = False
        print(f'''Records with event date after the date of death = {count_dod_after}''')
        if drop_wrong_dates:
            df = df[df[evdt_col] <= df['dod']]
            print(f'''Records with event date after the date of death are dropped''')
            print(f'''Remaining records = {df.shape[0]}''')
    count_dod_equal = df[(df[dod_col].notnull()) & (df[evdt_col] == df[dod_col])].shape[0]
    if count_dod_equal > 0:
        qc_passed = False
        print(f'''Records with event date as the date of death = {count_dod_equal}''')
        if drop_wrong_dates:
            df = df[df[evdt_col] < df['dod']]
            print(f'''Records with event date as the date of death are dropped''')
            print(f'''Remaining records = {df.shape[0]}''')
    if qc_passed:
        print("No issues found.")

    return df[cols_out]


def join_multiple_self_reported_phenos(dict_codes_self_reported: DataFrame,
                                       keep_minimum: bool = True):
    """Joins multiple self-reported phenotypes.

    Args:
        dict_codes_self_reported: A dictionary with keys as codes in the filed 20002 and
        the values the outputs of the self_reported_pheno_extractor function.
        keep_minimum: Whether to keep the minimum of event dates or the maximum.

    Return:
        A joined dataframe with the 'evdt_self_reported' column added.

    """
    # join
    dict_keys = list(dict_codes_self_reported.keys())
    df_all = dict_codes_self_reported.get(dict_keys[0])
    for key in dict_keys[1:]:
        df_all = pd.merge(df_all, dict_codes_self_reported.get(key), on="eid", how="outer")
    for item in dict_keys:
        df_all[f'''evdt_{item}'''] = pd.to_datetime(df_all[f'''evdt_{item}'''])
    if keep_minimum:
        df_all['evdt_self_reported'] = df_all[[f'''evdt_{item}''' for item in dict_keys]].min(axis=1)
    else:
        df_all['evdt_self_reported'] = df_all[[f'''evdt_{item}''' for item in dict_keys]].max(axis=1)
    return df_all
