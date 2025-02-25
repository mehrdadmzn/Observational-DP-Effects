from typing import Final

from data_metadata_input.csv_basic_imports import csv_field_list
from data_metadata_input.parquet_basic_imports import parquet_field_list
from env.user_parameters import data_path
from  datetime import datetime
from dataclasses import dataclass


@dataclass
class Parameters:

    data_path = "PATH_TO_UK_BIOBANK_DATA_FOLDER"

    raw_data_path= f'''{data_path}/raw_data'''
    data_portal_path = f'''{data_path}/data_portal'''
    processed_data_path = f'''{data_path}/processed_data'''
    output_parquet_path = f'''{processed_data_path}/parquet'''
    output_csv_path = f'''{processed_data_path}/csv'''
    analysis_data_path = f'''{processed_data_path}/analysis_data''' # holds metadata and models in pickle and other formats related to the analysis phase
    codelist_path = f'''{data_path}/codelists'''
    codings_path = f'''{data_path}/codings'''
    withdrawal_path = f'''{data_path}/withdrawals'''
    output_path = f'''{data_path}/output'''
    log_path = f'''{output_path}/log'''
    output_phenotypes_csv_path = f'''{output_csv_path}/phenotypes'''
    output_phenotypes_parquet_path = f'''{output_parquet_path}/phenotypes'''
    cohorts_path = f'''{processed_data_path}/cohorts'''
    cohorts_ukb_start_path = f'''{cohorts_path}/ukb_start'''
    cohorts_ukb_start_gphesonly_path = f'''{cohorts_path}/ukb_start_gphesonly'''
    cohorts_asthma_incident_gphesonly_path = f'''{cohorts_path}/asthma_incident_start_gphesonly'''
    cohorts_covid_path = f'''{cohorts_path}/covid'''
    cohorts_pandemic_path = f'''{cohorts_path}/pandemic'''

    logging_project_prefix = "PHHDS"
    csv_1_filename = "FILE1.csv" # The first downloaded basket
    core_1_name = "core_1"
    csv_2_filename = "FILE2.csv"
    core_2_name = "core_2"
    csv_3_filename = "FILE#.csv"
    core_3_name = "core_3"
    csv_4_filename = "FILE4.csv"
    core_4_name = "core_4"
    core_all_name = "core_all"
    eid_included_name = "eid_included"

    data_end_date = "2023-10-26" # MAximum study end date

    input_file_dict = {
        "csv_1": {
            "path": f'''{raw_data_path}/{csv_1_filename}''',
            "fields": [],
            "df": None
        },
        "csv_2": {
            "path": f'''{raw_data_path}/{csv_2_filename}''',
            "fields": [],
            "df": None
        },
        "csv_3": {
            "path": f'''{raw_data_path}/{csv_3_filename}''',
            "fields": [],
            "df": None
        },
        "csv_4": {
            "path": f'''{raw_data_path}/{csv_4_filename}''',
            "fields": [],
            "df": None
        },
        "core_1": {
            "path": f'''{processed_data_path}/parquet/{core_1_name}''',
            "fields": []
        },
        "core_2": {
            "path": f'''{processed_data_path}/parquet/{core_2_name}''',
            "fields": []
        },
        "core_3": {
            "path": f'''{processed_data_path}/parquet/{core_3_name}''',
            "fields": []
        },
        "core_4": {
            "path": f'''{processed_data_path}/parquet/{core_4_name}''',
            "fields": []
        },
        "core_all": {
            "path": f'''{processed_data_path}/parquet/{core_all_name}''',
            "fields": []
        },
        "withdrawals":
            {
                "path": f'''{withdrawal_path}/withdraw49708_281_20231221.txt'''
            },
        "death":
            {
                "path": f'''{data_portal_path}/death.txt'''
            },

    }

    field_encoding_dict = {
        "sex":
            {
                "field": "31",
                "data_coding": "9",
                "coding_file_path": f'''{codings_path}/coding9.tsv'''
            },
        "eth":
            {
                "field": "21000",
                "data_coding": "1001",
                "coding_file_path": f'''{codings_path}/coding1001.tsv'''
            },
        "smoking":
            {
                "field": "20116",
                "data_coding": "90",
                "coding_file_path": f'''{codings_path}/coding90.tsv'''
            },
        "alcohol":
            {
                "field": "1558",
                "data_coding": "100402",
                "coding_file_path": f'''{codings_path}/coding100402.tsv'''

            },
        "non_cancer_self_reported":
            {
                "field": "20002",
                "data_coding": "6",
                "coding_file_path": f'''{codings_path}/coding6.tsv'''
            },
        "yes_no_unknown":
            {
                "field": "",
                "data_coding": "100349",
                "coding_file_path": f'''{codings_path}/coding100349.tsv'''
            },
        "yes_no":
            {
                "field": "",
                "data_coding": "7",
                "coding_file_path": f'''{codings_path}/coding7.tsv'''
            }
    }

    codelist_dict = {
        "diabetes": {
            "name": "Diabetes",
            "ph": 152,
            "version": 304,
            "file_name": f'''{codelist_path}/Diabetes_phenotype_PH152_ver_304_concepts_20231110T202045.csv'''
        },
        "ami": {
            "name": "AMI",
            "ph": 949,
            "version": 2127,
            "file_name": f'''{codelist_path}/AMI_phenotype_PH949_ver_2127_concepts_20231109T105016.csv'''
        },

    }


P = Parameters(



def set_codelist_dict():
    """Sets the codelist path for each condition"""
    dict_out = {
        "diabetes": {
            "name": "Diabetes",
            "ph": 152,
            "version": 304,
            "file_name": f'''{codelist_path}/Diabetes_phenotype_PH152_ver_304_concepts_20231110T202045.csv'''
        },
        "ami": {
            "name": "AMI",
            "ph": 949,
            "version": 2127,
            "file_name": f'''{codelist_path}/AMI_phenotype_PH949_ver_2127_concepts_20231109T105016.csv'''
        },

    }



