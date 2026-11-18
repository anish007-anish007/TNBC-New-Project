\# TNBC Research Project

\## Data Quality Assessment Report



\### 1. Objective

Assess the integrity, completeness, consistency and expression-profile characteristics of the 579-sample TNBC dataset before downstream biomarker analysis.



\### 2. Dataset Overview

\- Dataset: GSE31519 combined TNBC cohort

\- Organism: Homo sapiens

\- Samples: 579

\- Expression probes: 22,283

\- Platforms represented: GPL96, GPL570 and GPL96 \& GPL97

\- Data type: Affymetrix gene expression microarray

\- Normalization: Median-centered and magnitude-normalized data, as documented in the downloaded expression file.



\### 3. Data Integrity and Sample Alignment

\- Metadata samples: 579

\- Unique metadata samples: 579

\- Expression samples: 579

\- Unique expression sample names: 579

\- Missing sample identities: 0

\- Extra sample identities: 0

\- Duplicate expression sample identities: 0



All 579 metadata sample names matched the expression matrix sample names.



\### 4. Missing-Value Assessment

\- Expected expression values: 12,901,857

\- Observed expression values: 12,900,804

\- Missing values: 1,053

\- Missing percentage: 0.00816%

\- Incomplete probes: 15

\- Non-numeric values: 0

\- Samples with zero missing values: 438

\- Samples with missing values: 141



Missingness was concentrated in a small number of probe sets and varied across platform groups.



\### 5. Platform and Probe-Level Findings

Missingness patterns differed between GPL570, GPL96 and GPL96 \& GPL97 samples.



The six ribosomal RNA control probes had 141 missing values each. Nine additional Affymetrix control probes accounted for the remaining 207 missing values.



These patterns suggest an association with platform or cohort structure. The underlying technical cause has not been established.



\### 6. Expression Distribution

Expression distributions were examined using sample-level mean, median, standard deviation, minimum, maximum and quartiles.



The mean sample standard deviation was approximately 0.006673.



No sample was classified as technically invalid based on standard deviation alone.



\### 7. PCA and Sample Correlation

Principal component analysis was performed using NumPy SVD.



\- PC1 variance explained: 11.10%

\- PC2 variance explained: 4.28%

\- Combined variance explained: 15.38%



Platform groups overlapped in the first two principal components. This does not establish the absence of batch effects.



Mean sample-to-sample correlation was approximately 0.8226.



\### 8. Potential Expression Outliers

Global correlation-based screening identified 19 potential outliers using an exploratory IQR threshold.



Within-cohort screening identified 19 potential outliers.



These are screening results, not confirmed low-quality samples. No samples should be automatically removed based on these results alone.



\### 9. Cohort-Level Findings

Cohorts 21 and 31 showed comparatively low within-cohort mean correlations.



Biopsy method 3 was present exclusively in these two cohorts. Therefore, biopsy method and cohort are confounded in this dataset, and their individual effects cannot be separated using these comparisons alone.



\### 10. TNBC\_119 Investigation

TNBC\_119 showed unusual expression characteristics within cohort 9.



\- It had the lowest mean expression among the 22 cohort 9 samples.

\- Its mean expression was approximately 3.23 standard deviations below the mean of the other 21 samples.

\- Its standard deviation was approximately 2.60 standard deviations above the average of the other 21 samples.

\- Approximately 61.78% of probes had lower expression than the cohort 9 median.



Twenty highly differentially expressed probe sets were annotated using the official GPL570 annotation.



Notable differences included higher GRIA2, REG1A, DLK1 and COL2A1 expression, and lower HMMR, MMP7 and CD24 expression.



These are exploratory observations. They do not establish biological significance, clinical relevance or biomarker validity.



\### 11. Limitations

\- The dataset combines multiple cohorts and array platforms.

\- Cohort, platform and biopsy-method effects may be confounded.

\- Correlation and IQR thresholds are exploratory.

\- Probe annotations may be ambiguous or affected by cross-hybridization.

\- No independent validation has yet been performed.

\- No clinical biomarker performance has been established.



\### 12. Recommendations

1\. Investigate cohort-specific expression shifts.

2\. Assess batch effects using appropriate statistical methods.

3\. Review potential outliers without automatically excluding them.

4\. Verify probe annotations and probe-to-gene mappings.

5\. Document all preprocessing and filtering decisions.

6\. Perform downstream biomarker analysis only after appropriate QC decisions.



\### 13. Overall Conclusion

The dataset passed the structural sample-alignment checks and demonstrated very low overall missingness.



However, cohort-specific expression differences and potential outliers require further investigation. The dataset is suitable for continued exploratory quality assessment, but additional validation and batch-effect evaluation are required before drawing biological or clinical conclusions.

