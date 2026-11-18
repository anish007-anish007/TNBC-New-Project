
import pandas as pd


def calculate_data_quality():
    metadata_path = (
        "data/raw/GSE31519_TNBC_SampleInfo_BCR.txt.gz"
    )

    expression_path = (
        "data/raw/GSE31519_complete_dataset.txt.gz"
    )

    # Read metadata: first row contains sample names.
    metadata = pd.read_csv(
        metadata_path,
        sep="\t",
        dtype=str,
        header=None
    )

    metadata_samples = [
        str(x).strip()
        for x in metadata.iloc[0, 1:]
    ]

    # Read the four original header lines.
    with pd.io.common.get_handle(
        expression_path, "r", compression="infer"
    ) as handle:
        header_lines = [
            next(handle.handle).rstrip("\r\n")
            for _ in range(4)
        ]

    expression_samples = (
        header_lines[1].split("\t")
    )

    # Keep only columns with verified sample names.
    valid_columns = [
        i for i, name in enumerate(expression_samples)
        if i > 0 and name.strip()
    ]

    expression_sample_names = [
        expression_samples[i].strip()
        for i in valid_columns
    ]

    # Validate sample identities before calculating metrics.
    if len(metadata_samples) != 579:
        raise ValueError("Unexpected metadata sample count.")

    if len(set(metadata_samples)) != len(metadata_samples):
        raise ValueError("Duplicate metadata sample names found.")

    if set(metadata_samples) != set(expression_sample_names):
        raise ValueError(
            "Metadata and expression sample names do not match."
        )

    if len(expression_sample_names) != 579:
        raise ValueError("Expected 579 expression samples.")

    # Read expression measurements after the four header lines.
    expression = pd.read_csv(
        expression_path,
        sep="\t",
        skiprows=4,
        header=None,
        dtype=str,
        keep_default_na=False
    )

    probes = len(expression)

    # Select only the 579 verified sample columns.
    sample_data = expression.iloc[:, valid_columns]

    # Convert expression measurements to numeric values.
    numeric_data = sample_data.apply(
        lambda column: pd.to_numeric(
            column.str.strip(),
            errors="coerce"
        )
    )

    # Count missing and invalid values.
    missing_values = int(numeric_data.isna().sum().sum())

    non_numeric_values = int(
        (
            sample_data.apply(
                lambda column: column.str.strip().ne("")
            )
            & numeric_data.isna()
        ).sum().sum()
    )

    expected_values = probes * len(valid_columns)
    observed_values = expected_values - missing_values

    incomplete_probes = int(
        numeric_data.isna().any(axis=1).sum()
    )

    missing_percentage = (
        missing_values / expected_values * 100
        if expected_values else 0
    )

    return {
        "samples": len(valid_columns),
        "probes": probes,
        "expected_values": expected_values,
        "observed_values": observed_values,
        "missing_values": missing_values,
        "incomplete_probes": incomplete_probes,
        "missing_percentage": missing_percentage,
        "non_numeric_values": non_numeric_values
    }



def calculate_sample_missingness():
    metadata_path = "data/raw/GSE31519_TNBC_SampleInfo_BCR.txt.gz"
    expression_path = "data/raw/GSE31519_complete_dataset.txt.gz"

    import pandas as pd

    # Read sample names from metadata
    metadata = pd.read_csv(
        metadata_path,
        sep="\t",
        dtype=str,
        header=None
    )

    metadata_samples = [
        str(x).strip() for x in metadata.iloc[0, 1:]
    ]

    # Read sample names from expression file
    with pd.io.common.get_handle(
        expression_path, "r", compression="infer"
    ) as handle:
        header_lines = [
            next(handle.handle).rstrip("\r\n")
            for _ in range(4)
        ]

    expression_samples = header_lines[1].split("\t")

    valid_columns = [
        i for i, name in enumerate(expression_samples)
        if i > 0 and name.strip()
    ]

    # Check sample identity
    selected_names = [
        expression_samples[i].strip()
        for i in valid_columns
    ]

    if set(metadata_samples) != set(selected_names):
        raise ValueError("Sample names do not match.")

    # Read expression measurements
    expression = pd.read_csv(
        expression_path,
        sep="\t",
        skiprows=4,
        header=None,
        dtype=str,
        keep_default_na=False
    )

    sample_data = expression.iloc[:, valid_columns]

    numeric_data = sample_data.apply(
        lambda column: pd.to_numeric(
            column.str.strip(),
            errors="coerce"
        )
    )

    # Calculate missingness for each sample
    missing_counts = numeric_data.isna().sum(axis=0)

    missing_percentages = (
        missing_counts / len(numeric_data) * 100
    )

    results = pd.DataFrame({
        "Sample": selected_names,
        "Missing Values": missing_counts.values,
        "Missing Percentage": missing_percentages.values
    })

    return results.sort_values(
        by="Missing Percentage",
        ascending=False
    ).reset_index(drop=True)
def calculate_probe_missingness():
    expression_path = "data/raw/GSE31519_complete_dataset.txt.gz"

    import pandas as pd

    # Read expression data
    expression = pd.read_csv(
        expression_path,
        sep="\t",
        skiprows=4,
        header=None,
        dtype=str,
        keep_default_na=False
    )

    # Select the 579 valid sample columns
    with pd.io.common.get_handle(
        expression_path, "r", compression="infer"
    ) as handle:
        header_lines = [
            next(handle.handle).rstrip("\r\n")
            for _ in range(4)
        ]

    expression_samples = header_lines[1].split("\t")

    valid_columns = [
        i for i, name in enumerate(expression_samples)
        if i > 0 and name.strip()
    ]

    sample_data = expression.iloc[:, valid_columns]

    # Convert measurements to numeric values
    numeric_data = sample_data.apply(
        lambda column: pd.to_numeric(
            column.str.strip(),
            errors="coerce"
        )
    )

    # Calculate missingness for each probe
    missing_counts = numeric_data.isna().sum(axis=1)

    missing_percentages = (
        missing_counts / numeric_data.shape[1] * 100
    )

    results = pd.DataFrame({
        "Probe_ID": expression.iloc[:, 0],
        "Missing_Values": missing_counts,
        "Missing_Percentage": missing_percentages
    })

    return results.sort_values(
        by="Missing_Percentage",
        ascending=False
    ).reset_index(drop=True)
def compare_probe_missingness_by_platform():
    import pandas as pd

    metadata_path = "data/raw/GSE31519_TNBC_SampleInfo_BCR.txt.gz"
    expression_path = "data/raw/GSE31519_complete_dataset.txt.gz"

    # Read metadata
    metadata = pd.read_csv(
        metadata_path,
        sep="\t",
        header=None,
        dtype=str
    )

    sample_info = pd.DataFrame({
        "Sample": metadata.iloc[0, 1:].str.strip().values,
        "Array_type": metadata.iloc[2, 1:].str.strip().values
    })

    # Read expression data
    expression = pd.read_csv(
        expression_path,
        sep="\t",
        skiprows=4,
        header=None,
        dtype=str,
        keep_default_na=False
    )

    # Identify the 579 valid sample columns
    with pd.io.common.get_handle(
        expression_path, "r", compression="infer"
    ) as handle:
        header_lines = [
            next(handle.handle).rstrip("\r\n")
            for _ in range(4)
        ]

    expression_samples = header_lines[1].split("\t")

    valid_columns = [
        i for i, name in enumerate(expression_samples)
        if i > 0 and name.strip()
    ]

    sample_names = [
        expression_samples[i].strip()
        for i in valid_columns
    ]

    # Convert expression measurements
    numeric_data = expression.iloc[:, valid_columns].apply(
        lambda column: pd.to_numeric(
            column.str.strip(),
            errors="coerce"
        )
    )

    numeric_data.columns = sample_names

    # Select the six ribosomal RNA-related probes
    probe_ids = expression.iloc[:, 0].str.strip()

    selected_ids = [
        "AFFX-r2-Hs18SrRNA-3_s_at",
        "AFFX-r2-Hs18SrRNA-5_at",
        "AFFX-r2-Hs18SrRNA-M_x_at",
        "AFFX-r2-Hs28SrRNA-3_at",
        "AFFX-r2-Hs28SrRNA-5_at",
        "AFFX-r2-Hs28SrRNA-M_at"
    ]

    probe_data = numeric_data.loc[
        probe_ids.isin(selected_ids)
    ].copy()

    probe_data.index = probe_ids[probe_ids.isin(selected_ids)]

    # Combine probe measurements with platform information
    results = []

    for platform in sample_info["Array_type"].unique():
        platform_samples = sample_info.loc[
            sample_info["Array_type"] == platform,
            "Sample"
        ].tolist()

        platform_data = probe_data[platform_samples]

        for probe in selected_ids:
            if probe in platform_data.index:
                missing = platform_data.loc[probe].isna().sum()
                total = len(platform_samples)

                results.append({
                    "Array_type": platform,
                    "Probe_ID": probe,
                    "Missing_Values": int(missing),
                    "Total_Samples": total,
                    "Missing_Percentage": missing / total * 100
                })

    return pd.DataFrame(results)
def compare_control_probe_missingness():
    import pandas as pd

    metadata_path = "data/raw/GSE31519_TNBC_SampleInfo_BCR.txt.gz"
    expression_path = "data/raw/GSE31519_complete_dataset.txt.gz"

    metadata = pd.read_csv(
        metadata_path,
        sep="\t",
        header=None,
        dtype=str
    )

    sample_info = pd.DataFrame({
        "Sample": metadata.iloc[0, 1:].str.strip().values,
        "Array_type": metadata.iloc[2, 1:].str.strip().values
    })

    expression = pd.read_csv(
        expression_path,
        sep="\t",
        skiprows=4,
        header=None,
        dtype=str,
        keep_default_na=False
    )

    with pd.io.common.get_handle(
        expression_path, "r", compression="infer"
    ) as handle:
        header_lines = [
            next(handle.handle).rstrip("\r\n")
            for _ in range(4)
        ]

    expression_samples = header_lines[1].split("\t")

    valid_columns = [
        i for i, name in enumerate(expression_samples)
        if i > 0 and name.strip()
    ]

    sample_names = [
        expression_samples[i].strip()
        for i in valid_columns
    ]

    numeric_data = expression.iloc[:, valid_columns].apply(
        lambda column: pd.to_numeric(
            column.str.strip(),
            errors="coerce"
        )
    )

    numeric_data.columns = sample_names

    probe_ids = expression.iloc[:, 0].str.strip()

    selected_ids = [
        "AFFX-BioB-3_at",
        "AFFX-BioB-5_at",
        "AFFX-BioB-M_at",
        "AFFX-BioC-3_at",
        "AFFX-BioC-5_at",
        "AFFX-BioC-5_st"
    ]

    probe_mask = probe_ids.isin(selected_ids)
    probe_data = numeric_data.loc[probe_mask].copy()
    probe_data.index = probe_ids[probe_mask]

    results = []

    for platform in sample_info["Array_type"].unique():
        platform_samples = sample_info.loc[
            sample_info["Array_type"] == platform,
            "Sample"
        ].tolist()

        platform_data = probe_data[platform_samples]

        for probe in selected_ids:
            if probe in platform_data.index:
                missing = platform_data.loc[probe].isna().sum()
                total = len(platform_samples)

                results.append({
                    "Array_type": platform,
                    "Probe_ID": probe,
                    "Missing_Values": int(missing),
                    "Total_Samples": total,
                    "Missing_Percentage": round(
                        missing / total * 100, 4
                    )
                })

    return pd.DataFrame(results)
def calculate_expression_distribution():
    import pandas as pd

    expression_path = "data/raw/GSE31519_complete_dataset.txt.gz"

    # Read the four expression-file header lines
    with pd.io.common.get_handle(
        expression_path, "r", compression="infer"
    ) as handle:
        header_lines = [
            next(handle.handle).rstrip("\r\n")
            for _ in range(4)
        ]

    expression_samples = header_lines[1].split("\t")

    valid_columns = [
        i for i, name in enumerate(expression_samples)
        if i > 0 and name.strip()
    ]

    sample_names = [
        expression_samples[i].strip()
        for i in valid_columns
    ]

    # Read expression measurements
    expression = pd.read_csv(
        expression_path,
        sep="\t",
        skiprows=4,
        header=None,
        dtype=str,
        keep_default_na=False
    )

    sample_data = expression.iloc[:, valid_columns]

    numeric_data = sample_data.apply(
        lambda column: pd.to_numeric(
            column.str.strip(),
            errors="coerce"
        )
    )

    numeric_data.columns = sample_names

    # Calculate distribution statistics for each sample
    results = pd.DataFrame({
        "Sample": sample_names,
        "Mean": numeric_data.mean().values,
        "Median": numeric_data.median().values,
        "Std_Dev": numeric_data.std().values,
        "Minimum": numeric_data.min().values,
        "Maximum": numeric_data.max().values,
        "Q1": numeric_data.quantile(0.25).values,
        "Q3": numeric_data.quantile(0.75).values
    })

    return results
def compare_expression_distribution_by_platform():
    import pandas as pd

    metadata_path = "data/raw/GSE31519_TNBC_SampleInfo_BCR.txt.gz"
    expression_path = "data/raw/GSE31519_complete_dataset.txt.gz"

    # Read sample metadata
    metadata = pd.read_csv(
        metadata_path,
        sep="\t",
        header=None,
        dtype=str
    )

    sample_info = pd.DataFrame({
        "Sample": metadata.iloc[0, 1:].str.strip().values,
        "Array_type": metadata.iloc[2, 1:].str.strip().values
    })

    # Read expression file headers
    with pd.io.common.get_handle(
        expression_path, "r", compression="infer"
    ) as handle:
        header_lines = [
            next(handle.handle).rstrip("\r\n")
            for _ in range(4)
        ]

    expression_samples = header_lines[1].split("\t")

    valid_columns = [
        i for i, name in enumerate(expression_samples)
        if i > 0 and name.strip()
    ]

    sample_names = [
        expression_samples[i].strip()
        for i in valid_columns
    ]

    # Read expression measurements
    expression = pd.read_csv(
        expression_path,
        sep="\t",
        skiprows=4,
        header=None,
        dtype=str,
        keep_default_na=False
    )

    numeric_data = expression.iloc[:, valid_columns].apply(
        lambda column: pd.to_numeric(
            column.str.strip(),
            errors="coerce"
        )
    )

    numeric_data.columns = sample_names

    # Calculate distribution statistics for each sample
    sample_stats = pd.DataFrame({
        "Sample": sample_names,
        "Mean": numeric_data.mean().values,
        "Median": numeric_data.median().values,
        "Std_Dev": numeric_data.std().values
    })

    # Attach array platform information
    combined = sample_stats.merge(
        sample_info,
        on="Sample",
        validate="one_to_one"
    )

    # Summarize statistics by platform
    results = combined.groupby("Array_type").agg(
        Samples=("Sample", "count"),
        Mean_Expression=("Mean", "mean"),
        Median_Expression=("Median", "median"),
        Mean_Std_Dev=("Std_Dev", "mean"),
        Min_Std_Dev=("Std_Dev", "min"),
        Max_Std_Dev=("Std_Dev", "max")
    ).reset_index()

    return results
def plot_expression_distribution_by_platform():
    import matplotlib.pyplot as plt
    import pandas as pd

    metadata_path = "data/raw/GSE31519_TNBC_SampleInfo_BCR.txt.gz"
    expression_path = "data/raw/GSE31519_complete_dataset.txt.gz"

    metadata = pd.read_csv(
        metadata_path,
        sep="\t",
        header=None,
        dtype=str
    )

    sample_info = pd.DataFrame({
        "Sample": metadata.iloc[0, 1:].str.strip().values,
        "Array_type": metadata.iloc[2, 1:].str.strip().values
    })

    expression = pd.read_csv(
        expression_path,
        sep="\t",
        skiprows=4,
        header=None,
        dtype=str,
        keep_default_na=False
    )

    with pd.io.common.get_handle(
        expression_path, "r", compression="infer"
    ) as handle:
        header_lines = [
            next(handle.handle).rstrip("\r\n")
            for _ in range(4)
        ]

    expression_samples = header_lines[1].split("\t")

    valid_columns = [
        i for i, name in enumerate(expression_samples)
        if i > 0 and name.strip()
    ]

    sample_names = [
        expression_samples[i].strip()
        for i in valid_columns
    ]

    numeric_data = expression.iloc[:, valid_columns].apply(
        lambda column: pd.to_numeric(
            column.str.strip(),
            errors="coerce"
        )
    )

    numeric_data.columns = sample_names

    plot_data = numeric_data.melt(
        var_name="Sample",
        value_name="Expression"
    )

    plot_data = plot_data.merge(
        sample_info,
        on="Sample",
        validate="many_to_one"
    )

    plt.figure(figsize=(10, 6))

    plot_data.boxplot(
        column="Expression",
        by="Array_type",
        grid=False,
        rot=15
    )

    plt.title("Expression Distribution by Array Platform")
    plt.suptitle("")
    plt.xlabel("Array Platform")
    plt.ylabel("Normalized Expression")
    plt.tight_layout()

    plt.show()



def plot_pca_by_platform():
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np

    metadata_path = "data/raw/GSE31519_TNBC_SampleInfo_BCR.txt.gz"
    expression_path = "data/raw/GSE31519_complete_dataset.txt.gz"

    # Read sample metadata
    metadata = pd.read_csv(
        metadata_path,
        sep="\t",
        header=None,
        dtype=str
    )

    sample_info = pd.DataFrame({
        "Sample": metadata.iloc[0, 1:].str.strip().values,
        "Array_type": metadata.iloc[2, 1:].str.strip().values
    })

    # Read expression file headers
    with pd.io.common.get_handle(
        expression_path, "r", compression="infer"
    ) as handle:
        header_lines = [
            next(handle.handle).rstrip("\r\n")
            for _ in range(4)
        ]

    expression_samples = header_lines[1].split("\t")

    valid_columns = [
        i for i, name in enumerate(expression_samples)
        if i > 0 and name.strip()
    ]

    sample_names = [
        expression_samples[i].strip()
        for i in valid_columns
    ]

    # Read expression measurements
    expression = pd.read_csv(
        expression_path,
        sep="\t",
        skiprows=4,
        header=None,
        dtype=str,
        keep_default_na=False
    )

    numeric_data = expression.iloc[:, valid_columns].apply(
        lambda column: pd.to_numeric(
            column.str.strip(),
            errors="coerce"
        )
    )

    numeric_data.columns = sample_names

    # Convert to samples x probes
    sample_matrix = numeric_data.T.to_numpy(dtype=float)

    # Remove probes that are entirely missing
    valid_probes = np.isfinite(sample_matrix).any(axis=0)
    sample_matrix = sample_matrix[:, valid_probes]

    # Replace missing values with each probe's median
    probe_medians = np.nanmedian(sample_matrix, axis=0)
    missing_rows, missing_cols = np.where(
        ~np.isfinite(sample_matrix)
    )
    sample_matrix[missing_rows, missing_cols] = (
        probe_medians[missing_cols]
    )

    # Center each probe before PCA
    sample_matrix = sample_matrix - sample_matrix.mean(axis=0)

    # Calculate PCA using NumPy SVD
    U, singular_values, Vt = np.linalg.svd(
        sample_matrix,
        full_matrices=False
    )

    pca_results = U[:, :2] * singular_values[:2]

    variance = singular_values ** 2
    explained_variance = variance / variance.sum() * 100

    # Prepare results
    pca_df = pd.DataFrame({
        "Sample": sample_names,
        "PC1": pca_results[:, 0],
        "PC2": pca_results[:, 1]
    })

    pca_df = pca_df.merge(
        sample_info,
        on="Sample",
        validate="one_to_one"
    )

    print("PCA samples:", len(pca_df))
    print("Platform counts:")
    print(pca_df["Array_type"].value_counts())
    print("PC1 variance:", round(explained_variance[0], 2), "%")
    print("PC2 variance:", round(explained_variance[1], 2), "%")
    print(
        "Combined variance:",
        round(explained_variance[:2].sum(), 2),
        "%"
    )

    # Plot PCA
    plt.figure(figsize=(10, 7))

    for platform, group in pca_df.groupby("Array_type"):
        plt.scatter(
            group["PC1"],
            group["PC2"],
            label=platform,
            alpha=0.7,
            s=35
        )

    plt.xlabel(
        f"PC1 ({explained_variance[0]:.2f}% variance)"
    )
    plt.ylabel(
        f"PC2 ({explained_variance[1]:.2f}% variance)"
    )
    plt.title("PCA of TNBC Expression Data by Array Platform")
    plt.legend(title="Array Platform")
    plt.grid(alpha=0.2)
    plt.tight_layout()
    plt.show()

def calculate_sample_correlation():
    import pandas as pd
    import numpy as np

    expression_path = "data/raw/GSE31519_complete_dataset.txt.gz"

    # Read expression header
    with pd.io.common.get_handle(
        expression_path, "r", compression="infer"
    ) as handle:
        header_lines = [
            next(handle.handle).rstrip("\r\n")
            for _ in range(4)
        ]

    expression_samples = header_lines[1].split("\t")

    valid_columns = [
        i for i, name in enumerate(expression_samples)
        if i > 0 and name.strip()
    ]

    sample_names = [
        expression_samples[i].strip()
        for i in valid_columns
    ]

    # Read expression measurements
    expression = pd.read_csv(
        expression_path,
        sep="\t",
        skiprows=4,
        header=None,
        dtype=str,
        keep_default_na=False
    )

    numeric_data = expression.iloc[:, valid_columns].apply(
        lambda column: pd.to_numeric(
            column.str.strip(),
            errors="coerce"
        )
    )

    numeric_data.columns = sample_names

    # Remove probes that are entirely missing
    numeric_data = numeric_data.dropna(axis=0, how="all")

    # Calculate correlations between samples
    correlation_matrix = numeric_data.corr(
    method="pearson",
    min_periods=100
    )

    # Summarize each sample's correlation with all other samples
    correlation_values = correlation_matrix.copy()
    np.fill_diagonal(correlation_values.values, np.nan)

    results = pd.DataFrame({
        "Sample": correlation_matrix.index,
        "Mean_Correlation": correlation_values.mean(axis=1),
        "Minimum_Correlation": correlation_values.min(axis=1),
        "Maximum_Correlation": correlation_values.max(axis=1)
    })

    results = results.sort_values(
        "Mean_Correlation",
        ascending=True
    )

    print("Samples analyzed:", len(results))
    print("\nCorrelation summary:")
    print(results[
        ["Mean_Correlation", "Minimum_Correlation",
         "Maximum_Correlation"]
    ].describe().round(4))

    print("\n10 samples with lowest mean correlation:")
    print(results.head(10).round(4).to_string(index=False))

    return results

def detect_expression_outliers():
    import pandas as pd
    import matplotlib.pyplot as plt

    # Get sample correlation results
    correlation_results = calculate_sample_correlation()

    # Calculate statistical outlier threshold
    mean_correlation = correlation_results["Mean_Correlation"]

    q1 = mean_correlation.quantile(0.25)
    q3 = mean_correlation.quantile(0.75)
    iqr = q3 - q1

    lower_threshold = q1 - (1.5 * iqr)

    # Identify potential outliers
    correlation_results["Potential_Outlier"] = (
        mean_correlation < lower_threshold
    )

    print("OUTLIER DETECTION RESULTS")
    print("-------------------------")
    print("Samples analyzed:", len(correlation_results))
    print("Q1:", round(q1, 4))
    print("Q3:", round(q3, 4))
    print("IQR:", round(iqr, 4))
    print("Lower outlier threshold:", round(lower_threshold, 4))

    outliers = correlation_results[
        correlation_results["Potential_Outlier"]
    ]

    print("\nPotential outlier samples:", len(outliers))

    if len(outliers) > 0:
        print(
            outliers[
                ["Sample", "Mean_Correlation",
                 "Minimum_Correlation", "Maximum_Correlation"]
            ].to_string(index=False)
        )
    else:
        print("No samples crossed the IQR outlier threshold.")

    # Plot correlation distribution
    plt.figure(figsize=(10, 6))

    plt.hist(
        mean_correlation,
        bins=30,
        edgecolor="black"
    )

    plt.axvline(
        lower_threshold,
        linestyle="--",
        label="Lower outlier threshold"
    )

    plt.xlabel("Mean Sample Correlation")
    plt.ylabel("Number of Samples")
    plt.title("Distribution of Sample Correlations")
    plt.legend()
    plt.tight_layout()
    plt.show()

    return correlation_results


def calculate_within_cohort_correlation():
    import pandas as pd

    metadata_path = "data/raw/GSE31519_TNBC_SampleInfo_BCR.txt.gz"
    expression_path = "data/raw/GSE31519_complete_dataset.txt.gz"

    # Read metadata
    metadata = pd.read_csv(
        metadata_path,
        sep="\t",
        header=None,
        dtype=str
    )

    sample_info = pd.DataFrame({
        "Sample": metadata.iloc[0, 1:].values,
        "Cohort": metadata.iloc[1, 1:].values
    })

    # Read the actual sample-name header (second file line)
    sample_header = pd.read_csv(
        expression_path,
        sep="\t",
        skiprows=1,
        nrows=1,
        header=None,
        dtype=str,
        keep_default_na=False
    )

    expression_sample_names = sample_header.iloc[0, 1:].tolist()

    # Read expression values
    expression = pd.read_csv(
        expression_path,
        sep="\t",
        skiprows=4,
        header=None,
        dtype=str,
        keep_default_na=False
    )

    expression = expression.iloc[:, 1:]
    expression.columns = expression_sample_names

    # Keep only the 579 verified samples
    valid_samples = sample_info["Sample"].tolist()
    expression = expression[valid_samples]

    # Convert values to numeric
    expression = expression.apply(
        pd.to_numeric,
        errors="coerce"
    )

    # Remove probes with no usable values
    expression = expression.dropna(how="all")

    # Impute missing values using each probe's median
    expression = expression.T.fillna(
        expression.median(axis=1)
    ).T

    results = []

    # Calculate correlations within each cohort
    for cohort, group in sample_info.groupby("Cohort"):

        samples = group["Sample"].tolist()

        if len(samples) < 3:
            continue

        cohort_expression = expression[samples]
        correlation = cohort_expression.corr()

        # Exclude self-correlations
        correlation.values[
            range(len(samples)),
            range(len(samples))
        ] = float("nan")

        mean_correlations = correlation.mean(axis=1)

        for sample, mean_corr in mean_correlations.items():
            results.append({
                "Sample": sample,
                "Cohort": cohort,
                "Within_Cohort_Mean_Correlation": mean_corr
            })

    return pd.DataFrame(results)

