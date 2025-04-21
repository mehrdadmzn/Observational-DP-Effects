# Introduction

Observational studies refer to the use of healthcare data, including electronic health records (EHR), to examine associations between risk factors and health outcomes. However, ensuring patients' privacy within these datasets remains an ongoing challenge. The application of differential privacy (DP) in the context of observational studies is largely underexplored. This project aims to investigate the impact of DP on a case-control analysis using data from the UK Biobank (https://www.ukbiobank.ac.uk/).

# UK Biobank data

The UK Biobank is a biomedical database (https://www.ukbiobank.ac.uk/enable-your-research/about-our-data) containing information on 500,000 participants. It includes baseline assessments, questionnaires, physical measurements, disease histories, imaging data, genetic information, and linked healthcare records (including primary care and hospital data). The UK Biobank Showcase (https://biobank.ndph.ox.ac.uk/showcase/) provides detailed information about available resources and fields.

The data is accessible to approved researchers and projects. Previously, researchers were allowed to download the data to secure local systems for analysis. Currently, access is limited to the cloud-based UK Biobank Research Analysis Platform (RAP) (https://www.ukbiobank.ac.uk/enable-your-research/research-analysis-platform).

This project was conducted during the period when local data downloads were permitted. The provided code can still be adapted for use within RAP.

# Differential privacy (DP)
We used IBM's [diffprivlib](http://diffprivlib.readthedocs.io/en/latest/index.html) library to apply DP on [logistic regression](https://diffprivlib.readthedocs.io/en/latest/modules/models.html#logistic-regression). The logistic regression results were used to find the odds ratio (OR) of risk factors. 


# Step by step guide to the packages and Jupyter notebooks


In this section we describe the steps to run the code and the required packages.


## 1. Settings

All constant parameters, including file paths, are defined using a Python data class in `env/parameters.py`

## 2. Data preparation

The downloaded data from UK Biobank is available in various formats, including CSV. These are large files with columns representing different [fields](https://biobank.ndph.ox.ac.uk/ukb/help.cgi?cd=data_field). Each variable is split across multiple fields. These fields may correspond to data collected at different time points ([instances](https://biobank.ndph.ox.ac.uk/ukb/help.cgi?cd=instances)) or to multi-value variables.

The initial set of code and modules is used to merge data from various UK Biobank baskets (i.e., sets of data requested at different times) and to aggregate multiple fields into single variables.

These include:


* `data_metadata_input` module: contains functions for importing patient pseudonyms from the downloaded CSV file, listing available fields, and loading them. It also provides tools to convert CSV files into Parquet format. The CSV files can be quite large, and loading them into memory may cause performance issues on local systems with limited memory. Parquet format helps alleviate this by enabling a column-based structure for more efficient data handling.

* `1_data_input_code`: contains Python scripts used to import and convert the CSV files into Parquet format.


## 2. Phenotyping and cohort creation

We extracted diagnostic and prescribed medication phenotypes from the [linked primary care and hospital inpatient data](https://www.ukbiobank.ac.uk/enable-your-research/about-our-data/health-related-outcomes-data). The primary care data is based on Read v2 and CTV3 terminologies for diagnostic codes. The prescribed medication in the primary care data is based on BNF codes of varying lengths. Hospital inpatient diagnoses are based on ICD-10 terminology. 

We used published and validated code lists from [HDR UK Phenotype Library]() and publications (e.g., [Mukherjee et al., 2024](https://www.thelancet.com/journals/lanepe/article/PIIS2666-7762(24)00105-4/fulltext)). The code lists can be found under `phenotyping`.

- Phenotyping:
  - `phenotyping module`:
    - `codebase_phenotyping`: includes functions for extracting event dates, ranking based on date, and keeping the first incident date. 
 -`self_reported_phenotyping`: functions to extract relevant fields from the [self-reported conditions field](https://biobank.ndph.ox.ac.uk/ukb/field.cgi?id=20002).

  - `2_data_preparation_notebooks/b1_codelist_maker_updated.ipynb`: loads and cleans the code-lists. 

- Cohort creation:
The following notebooks are used to create the base cohort:
  - `2_data_preparation_notebooks/c1_make_cohort_dask_based.ipynb`: Creates the base cohort based on Dask
  


## 3. Cohort preparation

## 4. Final analysis

