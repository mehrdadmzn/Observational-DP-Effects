# Introduction

Observational studies refer to the use of healthcare data, including electronic health records (EHR), to examine associations between risk factors and health outcomes. However, ensuring patients' privacy within these datasets remains an ongoing challenge. The application of differential privacy (DP) in the context of observational studies is largely underexplored. This project aims to investigate the impact of DP on a case-control analysis using data from the UK Biobank (https://www.ukbiobank.ac.uk/).


# UK Biobank data

The UK Biobank is a [biomedical database](https://www.ukbiobank.ac.uk/enable-your-research/about-our-data) containing information on 500,000 participants. It includes baseline assessments, questionnaires, physical measurements, disease histories, imaging data, genetic information, and linked healthcare records (including primary care and hospital data). The [UK Biobank Showcase](https://biobank.ndph.ox.ac.uk/showcase/) provides detailed information about available resources and fields.

The data is accessible to approved researchers and projects. Previously, researchers were allowed to download the data to secure local systems for analysis. Currently, access is limited to the cloud-based UK Biobank [Research Analysis Platform (RAP)](https://www.ukbiobank.ac.uk/enable-your-research/research-analysis-platform).

This project was conducted during the period when local data downloads were permitted. The provided code can still be adapted for use within RAP.

# Differential privacy (DP)
We used IBM's [Diffprivlib](http://diffprivlib.readthedocs.io/en/latest/index.html) library to apply DP on [logistic regression](https://diffprivlib.readthedocs.io/en/latest/modules/models.html#logistic-regression). The logistic regression results were used to find the odds ratio (OR) of risk factors. 


# Step by step guide to the packages and Jupyter notebooks


In this section we describe the steps to run the code and the required packages.


## 1. Settings and general utils

All constant parameters, including file paths, are defined using a Python data class in `env/parameters.py`

The `util` package contains modules for handling Dask, Parquet, and logging. 

## 2. Data preparation

The downloaded data from UK Biobank is available in various formats, including CSV. These are large files with columns representing different [fields](https://biobank.ndph.ox.ac.uk/ukb/help.cgi?cd=data_field). Each variable is split across multiple fields. These fields may correspond to data collected at different time points ([instances](https://biobank.ndph.ox.ac.uk/ukb/help.cgi?cd=instances)) or to multi-value variables.

The initial set of code and modules is used to merge data from various UK Biobank baskets (i.e., sets of data requested at different times) and to aggregate multiple fields into single variables.

These include:


* `data_metadata_input` module: contains functions for importing patient pseudonyms from the downloaded CSV file, listing available fields, and loading them. It also provides tools to convert CSV files into Parquet format. The CSV files can be quite large, and loading them into memory may cause performance issues on local systems with limited memory. Parquet format helps alleviate this by enabling a column-based structure for more efficient data handling.

* `1_data_input_code`: contains Python scripts used to import and convert the CSV files into Parquet format.


## 2. Phenotyping and cohort creation

We derived diagnostic and medication-related phenotypes from the [linked primary care and hospital inpatient data](https://www.ukbiobank.ac.uk/enable-your-research/about-our-data/health-related-outcomes-data). Diagnostic codes in primary care are based on Read v2 and CTV3 terminologies, while prescribed medications use BNF codes of varying lengths. Hospital inpatient diagnoses are recorded using ICD-10 codes.

We used validated and published code lists from the [HDR UK Phenotype Library](https://phenotypes.healthdatagateway.org/) and peer-reviewed publications (e.g., [Mukherjee et al., 2024](https://www.thelancet.com/journals/lanepe/article/PIIS2666-7762(24)00105-4/fulltext)). All code lists used in this project are available in the `phenotyping` folder.

- Phenotyping (code lists):
  - `phenotyping`
    - `codebase_phenotyping`: includes functions to extract event dates, rank events by date, and retain the first incident date.
  - `self_reported_phenotyping`: includes functions to extract relevant information from the [self-reported conditions field](https://biobank.ndph.ox.ac.uk/ukb/field.cgi?id=20002).

  - `2_data_preparation_notebooks/b1_codelist_maker_updated.ipynb`: loads and processes the code lists.

- Cohort creation:
The following notebooks are used to build the base cohort:
  - `2_data_preparation_notebooks/c1_make_cohort_dask_based.ipynb`: creates the base cohort using a single-node [Dask](https://github.com/dask/dask).
  - `2_data_preparation_notebooks/c2_advanced_cohort_dask_based.ipynb`: extends the base cohort by adding additional fields.

- Phenotype extraction: 
Example phenotype extraction notebooks for asthma, hypertension, stroke, and Acute Myocardial Infarction (AMI) are available in the `2_data_preparation_notebooks` directory.

## 3. Final analysis

The `3_final_analysis` directory includes notebooks for preprocessing, feature engineering, and the final analytical steps:

- `01_Data_preprocess.ipynb`: handles data preprocessing and feature engineering, including multiple imputation for missing values.
- `02_Descriptive_and_outlier.ipynb`: performs descriptive analysis and identifies outliers.
- `05_compare_adjusted_models`: Sensitivity analysis for choosing the covariates for logistic regression. 
- `10_adjusted_0747`: conducts a differentially private adjusted case-control analysis of risk factors for the outcome of interest (one-year asthma exacerbation) using random seeds `07` and `47`.
- `11_matched_0747`: performs a differentially private, propensity score-matched case-control analysis for the same outcome, using K-Nearest Neighbour matching without replacement.
- `12_unadjusted_0747`: runs a differentially private unadjusted case-control analysis using a 2x2 contingency table based on Diffprivlib’s [histogram2d](https://diffprivlib.readthedocs.io/en/latest/modules/tools.html#diffprivlib.tools.histogram2d)
