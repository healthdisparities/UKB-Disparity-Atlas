# UK Biobank Atlas of Health Disparities

## Introduction

Hello! Welcome to the codebase for UK Biobank Health Disparities Browser hosted on [the link here](https://ukbatlas.health-disparities.org)

Documented here is a codebase and summarized data that powers the Health Disparities Atlas browser. 

The summary level data that is visualized in the browser is found in `data/summary_stats/` directory in this repository.

## Background

Health disparities (or inequalities) can be defined as differences in health outcomes between groups of people, where the groups can be delineated in a variety of ways. We created the UK Health Disparities Browser as a means for researchers to explore the landscape of health disparities in the United Kingdom, for groups defined by age, ethnicity, sex, and socioeconomic status. The browser includes prevalence data for 1,513 diseases based on a cohort of ~500,000 participants from the UK Biobank. Users can browse and sort by disease prevalence and differences to visualize health disparities for each of these four groups, and users can search for diseases of interest by disease names or codes.

Disease cohorts were defined by mapping ICD-10 disease codes from the UK Biobank to phenotype codes (phecodes). Phecodes aggregate one or more related ICD-10 codes into distinct diseases, and they use both inclusion and exclusion criteria to define disease case and control cohorts. For each disease phecode, prevalence values were calculated by dividing the number of cases by the sum of the number of cases and controls. For each of the four groups – age, ethnicity, sex, and socioeconomic status – disease percent prevalence values were computed for all subgroups, and the magnitude of the disparities were calculated by both the variances of the prevalence and the maximum prevalence differences among the subgroups.

## Methodology

We stratify case/control cohorts for different disease phenotypes:

1. Sex
2. Age
3. Ethnicity
4. Socio-economic status
5. Country of origin

All of the health disparities data published here are released freely for the benefit of the research community. It should be noted that the disease prevalence and disparities values were calculated using the UK Biobank Resource (project ID 65206), and use of these data are subject to the terms of the UK Biobank.


## Publications

Shashwat Deepali Nagar, I King Jordan, Leonardo Mariño-Ramírez, The landscape of health disparities in the UK Biobank, Database, Volume 2023, 2023, baad026, https://doi.org/10.1093/database/baad026 [[PubMed]](https://pubmed.ncbi.nlm.nih.gov/) [[Article]](https://academic.oup.com/database/article-pdf/doi/10.1093/database/baad026/50103027/baad026.pdf)
