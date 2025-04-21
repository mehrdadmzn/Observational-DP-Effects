# Introduction

Observational studies refer to the use of healthcare data, including electronic health records (EHR), to examine associations between risk factors and health outcomes. However, ensuring patients' privacy within these datasets remains an ongoing challenge. The application of differential privacy (DP) in the context of observational studies is largely underexplored. This project aims to investigate the impact of DP on a case-control analysis using data from the UK Biobank (https://www.ukbiobank.ac.uk/).

# UK Biobank data

The UK Biobank is a biomedical database (https://www.ukbiobank.ac.uk/enable-your-research/about-our-data) containing information on 500,000 participants. It includes baseline assessments, questionnaires, physical measurements, disease histories, imaging data, genetic information, and linked healthcare records (including primary care and hospital data). The UK Biobank Showcase (https://biobank.ndph.ox.ac.uk/showcase/) provides detailed information about available resources and fields.

The data is accessible to approved researchers and projects. Previously, researchers were allowed to download the data to secure local systems for analysis. Currently, access is limited to the cloud-based UK Biobank Research Analysis Platform (RAP) (https://www.ukbiobank.ac.uk/enable-your-research/research-analysis-platform).

This project was conducted during the period when local data downloads were permitted. The provided code can still be adapted for use within RAP.

# Differential privacy (DP)
We used IBM's [diffprivlib](http://diffprivlib.readthedocs.io/en/latest/index.html) library to apply DP on [logistic regression](https://diffprivlib.readthedocs.io/en/latest/modules/models.html#logistic-regression). The logistic regression results were used to find the odds ratio (OR) of risk factors. 


# Step by step guide to the packages and Jupyter notebooks

In this section we describe the steps to run the codes and rquired packages. 

In this section we describe the steps to run the code and the required packages.

## 1. Data preparation

The downloaded data from UK Biobank is available in various formats, including CSV. These are large files with columns representing different [fields](https://biobank.ndph.ox.ac.uk/ukb/help.cgi?cd=data_field). Each variable is split across multiple fields. These fields may correspond to data collected at different time points ([instances](https://biobank.ndph.ox.ac.uk/ukb/help.cgi?cd=instances)) or to multi-value variables.

The initial set of code and modules is used to merge data from various UK Biobank baskets (i.e., sets of data requested at different times) and to aggregate multiple fields into single variables.

These include:

..* 
..* data_metadata_input module: contains functions for importing patient pseudonyms from the downloaded CSV file, listing available fields, and loading them. It also provides tools to convert CSV files into Parquet format. The CSV files can be quite large, and loading them into memory may cause performance issues on local systems with limited memory. Parquet format helps alleviate this by enabling a column-based structure for more efficient data handling.

..* 1_data_input_code: contains Python scripts used to import and convert the CSV files into Parquet format.




## 2. Phenotyping

## 3. Cohort preparation

## 4. Final analysis

