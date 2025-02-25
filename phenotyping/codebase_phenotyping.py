"""Functions for code-base phenotyping"""
import pandas as pd
from pandas import DataFrame
from typing import Tuple, List


def pheno_all_evdt_extractor(df_data_clean: DataFrame,
                             col_evdt_data: str,
                             col_code_data: str,
                             df_codelist: DataFrame,
                             col_code_codelist: str,
                             col_vocab_codelist: str,
                             use_vocab: str,
                             col_assign_pheno_name: str,
                             assign_pheno_name: str,
                             col_codelist_multicategory: str = None,
                             join_type: str = 'any'
                             ) -> DataFrame:
    """ Extracts all event dates where there is an exact code hit

    Args:
        df_data_clean: Clean input data (event dates are clean, between date of birth and death)
        col_evdt_data: The name of the column in the data holding the event dates (e.g. diagnosis date). For example
            epistart in HES
        col_code_data: The name of the column in data holding the code. For example, diag_icd10 in HES
        df_codelist: The codelist in Pandas dataframe
        col_code_codelist: The code column in the codelist
        col_vocab_codelist: The column specifying the vocabulary or coding system in the codelist
        use_vocab: The only vocabulary that is going to be used in the extraction.
            If multiple vocabularies are needed, consolidate them into a single vocabulary label before this function.
        col_assign_pheno_name: The new column specifying the phenotype name (e.g. pheno, or pheno_name)
        assign_pheno_name: The value to assing to the col_assign_pheno_name (e.g. asthma  or diabetes)
        col_codelist_multicategory: If the phenotype is multi-category (such as smoking),
            specify the name of the category column in the codelist.
        join_type: Of following types:
                - "read2" for GP data
                - "icd10" for HES data
                - "opcs4" for HES OPER
    Returns:
        A dataframe with all code hits in long format. Each patient has multiple rows.

    """

    df = df_data_clean
    df[col_evdt_data] = pd.to_datetime(df[col_evdt_data])
    if col_codelist_multicategory is None or "":
        col_list = [col_code_codelist, col_vocab_codelist]
    else:
        col_list = [col_code_codelist, col_vocab_codelist, col_codelist_multicategory]
    codelist_sel = df_codelist[col_list]
    codelist_sel = codelist_sel[codelist_sel[col_vocab_codelist] == use_vocab]
    codelist_sel.loc[:, col_assign_pheno_name] = assign_pheno_name

    if join_type == 'read2':
        df_long = pd.merge(df, codelist_sel,
                           left_on=df[col_code_data].str.strip().str[:5],
                           right_on=codelist_sel[col_code_codelist].str.strip().str[:5],
                           how="inner")
    elif join_type == 'icd10':
        df_long = pd.merge(df, codelist_sel,
                           left_on=df[col_code_data].str.strip().str.lower().str.replace(".", ""),
                           right_on=codelist_sel[col_code_codelist].str.strip().str.lower().str.replace(".", ""),
                           how="inner"
                           )
    else:
        df_long = pd.merge(df, codelist_sel,
                           left_on=df[col_code_data],
                           right_on=codelist_sel[col_code_codelist],
                           how="inner")

    return df_long


def __old_pheno_all_evdt_extractor(df_data_clean: DataFrame,
                                   col_evdt_data: str,
                                   col_code_data: str,
                                   df_codelist: DataFrame,
                                   col_code_codelist: str,
                                   col_vocab_codelist: str,
                                   use_vocab: str,
                                   col_assign_pheno_name: str,
                                   assign_pheno_name: str,
                                   col_codelist_multicategory: str = None,
                                   join_type: str = 'any'
                                   ) -> DataFrame:
    """ Extracts all event dates where there is an exact code hit

    Args:
        df_data_clean: Clean input data (event dates are clean, between date of birth and death)
        col_evdt_data: The name of the column in the data holding the event dates (e.g. diagnosis date). For example
            epistart in HES
        col_code_data: The name of the column in data holding the code. For example, diag_icd10 in HES
        df_codelist: The codelist in Pandas dataframe
        col_code_codelist: The code column in the codelist
        col_vocab_codelist: The column specifying the vocabulary or coding system in the codelist
        use_vocab: The only vocabulary that is going to be used in the extraction.
            If multiple vocabularies are needed, consolidate them into a single vocabulary label before this function.
        col_assign_pheno_name: The new column specifying the phenotype name (e.g. pheno, or pheno_name)
        assign_pheno_name: The value to assing to the col_assign_pheno_name (e.g. asthma  or diabetes)
        col_codelist_multicategory: If the phenotype is multi-category (such as smoking),
            specify the name of the category column in the codelist.
        join_type: Of following types:
                - "read2" for GP data
                - "icd10" for HES data
                - "opcs4" for HES OPER
    Returns:
        A dataframe with all code hits in long format. Each patient has multiple rows.

    """

    df = df_data_clean
    df[col_evdt_data] = pd.to_datetime(df[col_evdt_data])
    if col_codelist_multicategory is None or "":
        col_list = [col_code_codelist, col_vocab_codelist]
    else:
        col_list = [col_code_codelist, col_vocab_codelist, col_codelist_multicategory]
    codelist_sel = df_codelist[col_list]
    codelist_sel = codelist_sel[codelist_sel[col_vocab_codelist] == use_vocab]
    codelist_sel.loc[:, col_assign_pheno_name] = assign_pheno_name

    if join_type == 'read2':
        df_long = pd.merge(df, codelist_sel,
                           left_on=df[col_code_data].str.strip().str.lower().str[:5],
                           right_on=codelist_sel[col_code_codelist].str.strip().str.lower().str[:5],
                           how="inner")
    elif join_type == 'icd10':
        df_long = pd.merge(df, codelist_sel,
                           left_on=df[col_code_data].str.strip().str.lower().str.replace(".", ""),
                           right_on=codelist_sel[col_code_codelist].str.strip().str.lower().str.replace(".", ""),
                           how="inner"
                           )
    else:
        df_long = pd.merge(df, codelist_sel,
                           left_on=df[col_code_data],
                           right_on=codelist_sel[col_code_codelist],
                           how="inner")

    return df_long


def pheno_rank_and_filter(df_pheno_long: DataFrame,
                          col_evdt: str,
                          col_eid: str = "eid",
                          earliest_ranks_1: bool = True) -> DataFrame:
    """ Takes the output of pheno_all_evdt_extractor and adds a row number based on event date

    Args:
        df_pheno_long: The output of pheno_all_evdt_extractor, a dataframe with all eventdates of a code hit
             for a specific phenotype.
        col_evdt: The column holding the eventdate in the data.
        col_eid: The name of the eid column
        earliest_ranks_1: If True, the earliest date will be ranked as 1. If False, the latest date will be ranked as 1.

    Returns:
        A data frame with ranked row_number baed on earliest_ranks_1

    """
    df = df_pheno_long
    df.loc[:, col_evdt] = pd.to_datetime(df[col_evdt])
    df = df.sort_values(by=[col_evdt], ascending=earliest_ranks_1)
    df['row_number'] = df.groupby(col_eid).cumcount() + 1
    return df


def pheno_keep_one_row(df_ranked_long: DataFrame,
                       col_row_number: str = 'row_number') -> DataFrame:
    """ Keeps only row_number= 1 in the output of pheno_rank_and_filter

    Args:
        df_ranked_long: The output of pheno_rank_and_filter
        col_row_number: The name of the rank column

    Returns:
        A dataframe with a single row per person with a code hit

    """
    df_out = df_ranked_long[df_ranked_long[col_row_number] == 1]
    df_out = df_out.drop(columns=[col_row_number], axis=1)
    return df_out


def clean_biobank_ado_pheno(df_ado: DataFrame,
                            col_evdt: str,
                            col_source: str,
                            df_cohort: DataFrame,
                            pheno_name: str = "",
                            col_dob: str = "dob",
                            col_dod: str = "dod",
                            col_eid: str = "eid") -> DataFrame:
    """ Prepares the algorithmically defined output (ADO) files for phenotype extraction

    Args:
        df_ado: the raw ADO file
        col_evdt: The event date column of the ADO file, usually in the form of field_number-0.0
        df_cohort: The cohort file with date of birth (dob) and date of death (dod) columns
        pheno_name: The name to be assigned to the event date column
        col_dob: The name of the dob in the cohort file
        col_dod: The name of the dod in the cohort file
        col_eid: the name of the eid in the cohort file

    Returns:
        A clean ADO file where all eventdates are valid, and between date of birth and date of death

    """
    # check uniquenss
    assert df_ado[col_eid].count() == df_ado[col_eid].nunique(), "eid is not unique"
    df_ado_temp = df_ado[df_ado[col_evdt].notnull()]
    df_ado_temp[col_evdt] = pd.to_datetime(df_ado_temp[col_evdt])
    df_cohort[col_dob] = pd.to_datetime(df_cohort[col_dob])
    df_cohort[col_dod] = pd.to_datetime(df_cohort[col_dod])
    new_col_name = f'''evdt_ado_{pheno_name}'''
    new_source_col_name = f'''source_ado_{pheno_name}'''
    df_ado_cohort = pd.merge(df_cohort[[col_eid, col_dob, col_dod]],
                             df_ado_temp.rename(columns={col_evdt: new_col_name,
                                                         col_source: new_source_col_name}),
                             on=col_eid,
                             how="inner")
    df_ado_clean = df_ado_cohort[(df_ado_cohort[new_col_name] >= df_ado_cohort[col_dob]) &
                                 ((df_ado_cohort[col_dod].isnull()) |
                                  (df_ado_cohort[col_dod] >= df_ado_cohort[new_col_name]))]
    return df_ado_clean[[col_eid, new_col_name, new_source_col_name]]


def join_gp_hes_biobank_single_row_dfs(pheno_gp: DataFrame,
                                       pheno_hes: DataFrame,
                                       pheno_biobank: DataFrame = None,
                                       col_evdt_gp: str = "evdt_gp",
                                       col_evdt_hes: str = "epistart",
                                       col_evdt_biobank: str = None,
                                       col_source_biobank: str = None,
                                       pheno_name: str = "pheno_name",
                                       gp_and_hes_only: bool = True,
                                       keep_minimum: bool = True,
                                       col_eid: str = "eid") -> DataFrame:
    """ Makes a single event date column from the single row phenotype tables from GP, HES and Biobank ADO files

    Args:
        pheno_gp: The dataframe of the phenotypes from GP. Single row per patient.
        pheno_hes: The dataframe of the phenotypes from HES. Single row per patient.
        pheno_biobank: None or The dataframe of the phenotypes from GP. Single row per patient.
        col_evdt_gp: The event date column in the GP phenotype table
        col_evdt_hes: The event date column in the HES phenotype table
        col_evdt_biobank: The event date column in the Biobank ADO phenotype table
        pheno_name: The assigned name of the phenotype
        gp_and_hes_only: Is it GP and HES phenotypes only or GP+HES+Biobank ADO
        keep_minimum: Whether to keep the minimum or maximum event date when more than one event date is available.
        col_eid: The eid column

    Returns:
        A dataframe with a new single event date column.

    """

    sel_gp = pheno_gp[['eid', col_evdt_gp]]
    sel_hes = pheno_hes[['eid', col_evdt_hes]]
    assert sel_gp['eid'].count() == sel_gp['eid'].nunique(), "GP phenotype has multiple eids"
    sel_gp.loc[:, col_evdt_gp] = pd.to_datetime(sel_gp[col_evdt_gp])
    assert sel_hes["eid"].count() == sel_hes['eid'].nunique(), "HES phenoytpe has multiple eids"
    sel_hes.loc[:, col_evdt_hes] = pd.to_datetime(sel_hes[col_evdt_hes])
    if not gp_and_hes_only:
        sel_biobank = pheno_biobank[['eid', col_evdt_biobank, col_source_biobank]]

        # sel_biobank['biobank_source'] = 'ado'
        assert sel_biobank['eid'].count() == sel_biobank['eid'].nunique(), "UK Biobank phenotype has multiple eids"
        sel_biobank.loc[:, col_evdt_biobank] = pd.to_datetime(sel_biobank[col_evdt_biobank])

    df = pd.merge(sel_gp, sel_hes,
                  on=col_eid,
                  how="outer")
    df = df[["eid", col_evdt_gp, col_evdt_hes]]

    if not gp_and_hes_only:
        df = pd.merge(df, sel_biobank,
                      on=col_eid,
                      how="outer")
        df = df[[col_eid, col_evdt_gp, col_evdt_hes, col_evdt_biobank, col_source_biobank]]

    if gp_and_hes_only:
        if keep_minimum:
            df[f'''evdt_{pheno_name}'''] = df[[col_evdt_gp, col_evdt_hes]].min(axis=1, skipna=True)
        else:
            df[f'''evdt_{pheno_name}'''] = df[[col_evdt_gp, col_evdt_hes]].max(axis=1, skipna=True)
    else:
        if keep_minimum:
            df[f'''evdt_{pheno_name}'''] = df[[col_evdt_gp, col_evdt_hes, col_evdt_biobank]].min(axis=1, skipna=True)
        else:
            df[f'''evdt_{pheno_name}'''] = df[[col_evdt_gp, col_evdt_hes, col_evdt_biobank]].max(axis=1, skipna=True)

    return df


def join_single_row_dfs(pheno_1: DataFrame,
                        pheno_2: DataFrame,
                        col_evdt_1: str,
                        col_evdt_2: str,
                        pheno_name: str,
                        keep_extra_cols_1: List = [],
                        keep_extra_cols_2: List = [],
                        keep_minimum: bool = True,
                        col_eid: str = "eid"):
    sel_1 = pheno_1[[col_eid, col_evdt_1] + keep_extra_cols_1]
    assert sel_1[col_eid].count() == sel_1[col_eid].nunique(), "The first phenotype dataframe has multiple eids"
    sel_2 = pheno_2[[col_eid, col_evdt_2] + keep_extra_cols_2]
    assert sel_2[col_eid].count() == sel_2[col_eid].nunique(), "The second phenotype dataframe has multiple eids"
    df = pd.merge(sel_1, sel_2,
                  on=col_eid,
                  how="outer")
    if keep_minimum:
        df[f'''evdt_{pheno_name}'''] = df[[col_evdt_1, col_evdt_2]].min(axis=1, skipna=True)
    else:
        df[f'''evdt_{pheno_name}'''] = df[[col_evdt_1, col_evdt_2]].max(axis=1, skipna=True)
    return df
