
import streamlit as st
import pandas as pd
from datetime import date
from data_quality import calculate_data_quality
# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="TNBC New Project",
    page_icon="🧬",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM STYLING
# --------------------------------------------------

st.markdown("""
<style>
.main {
    background-color: #f7f9fc;
}
.block-container {
    padding-top: 2rem;
}
h1, h2, h3 {
    color: #183153;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🧬 TNBC New Project")
st.subheader("Research Evidence Workspace")

st.write(
    "An interactive workspace for documenting, "
    "evaluating and reporting TNBC biomarker research."
)

st.info(
    "DEMO MODE: The information shown is illustrative. "
    "It is not a validated scientific result."
)

# --------------------------------------------------
# SIDEBAR - PROJECT CONFIGURATION
# --------------------------------------------------

st.sidebar.title("Project Configuration")

project_name = st.sidebar.text_input(
    "Project name",
    value="TNBC New Project"
)

geo_accession = st.sidebar.text_input(
    "GEO / Dataset accession",
    value="GSE31519"
)

st.sidebar.divider()

st.sidebar.caption("TNBC Research Demo | Version 1.0")

# --------------------------------------------------
# PROJECT OVERVIEW
# --------------------------------------------------

st.header("PROJECT OVERVIEW")

st.write(
    "**Research description:** "
    "TNBC biomarker discovery and validation research."
)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Project", project_name)

with col2:
    st.metric("Dataset accession", geo_accession)

with col3:
    st.metric("Workspace sections", "05")

st.divider()

# --------------------------------------------------
# RESEARCH EVIDENCE WORKSPACE
# --------------------------------------------------

st.header("Research Evidence Workspace")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "01 Dataset Provenance",
    "02 Data Quality",
    "03 Candidate Signals",
    "04 Independent Validation",
    "05 Evidence Report"
])

# --------------------------------------------------
# TAB 1 - DATASET PROVENANCE
# --------------------------------------------------

with tab1:

    st.subheader("01 | Dataset Provenance")

    st.write(
        "Document where the dataset originated "
        "and how the samples were collected."
    )

    source = st.text_input(
        "Dataset source",
        value="Gene Expression Omnibus (GEO)"
    )

    accession = st.text_input(
        "Dataset accession",
        value=geo_accession,
        key="provenance_accession"
    )

    organism = st.selectbox(
        "Organism",
        ["Homo sapiens", "Mus musculus", "Other"]
    )

    platform = st.text_input(
        "Experiment Type",
        value="Microarray (demo)"
    )

    sample_count = 579

    st.text_input(
        "Number of samples",
        value=str(sample_count),
        disabled=True
    )

    collection_details = st.text_area(
        "Sample collection details",
        value="Demonstration entry: TNBC-related gene expression cohort."
    )

    st.text_area(
        "Provenance notes",
        placeholder="Add publication, source URL, collection criteria..."
    )

    st.success("Dataset provenance workspace ready.")

# --------------------------------------------------
# TAB 2 - DATA QUALITY
# --------------------------------------------------

with tab2:

    quality = calculate_data_quality()

    st.subheader("02 | Data Quality")

    st.write(
        "Record missing values, sample balance, "
        "batch effects and technical replicates."
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Samples in metadata",
            f"{quality['samples']:,}"
        )

    with c2:
        st.metric(
            "Expression probes",
            f"{quality['probes']:,}"
        )

    with c3:
        st.metric(
            "Missing expression",
            f"{quality['missing_percentage']:.4f}%"
        )

    st.markdown("### Quality assessment")

    missing_values = st.selectbox(
        "Missing value assessment",
        ["Not assessed", "Low", "Moderate", "High"]
    )

    sample_balance = st.selectbox(
        "Sample balance",
        ["Not assessed", "Balanced", "Imbalanced"]
    )

    batch_effects = st.selectbox(
        "Batch effect assessment",
        [
            "Not assessed",
            "No major effect detected",
            "Potential batch effect",
            "Batch effect detected"
        ]
    )

    replicates = st.selectbox(
        "Technical replicate assessment",
        ["Not assessed", "Present", "Absent", "Unknown"]
    )

    quality_notes = st.text_area(
        "Quality control observations",
        placeholder="Describe QC findings and methods..."
    )

    st.caption(
        "Metrics are calculated from the downloaded files. "
        "Sample-column alignment and missing-value parsing "
        "still require scientific validation."
    )


# --------------------------------------------------
# TAB 3 - CANDIDATE SIGNALS
# --------------------------------------------------

with tab3:

    st.subheader("03 | Candidate Signals")

    st.write(
        "Document candidate genes and the statistical "
        "evidence supporting further investigation."
    )

    gene = st.text_input(
        "Candidate gene",
        value="BRCA1"
    )

    statistical_method = st.selectbox(
        "Statistical method",
        ["Welch t-test", "Log-rank test", "Cox regression", "Other"]
    )

    p_value = st.number_input(
        "P-value",
        min_value=0.0,
        max_value=1.0,
        value=0.01,
        format="%.6f"
    )

    adjusted_p = st.number_input(
        "Adjusted P-value (FDR)",
        min_value=0.0,
        max_value=1.0,
        value=0.05,
        format="%.6f"
    )

    effect_size = st.text_input(
        "Effect size / Hazard ratio",
        placeholder="Enter measured value"
    )

    interpretation = st.text_area(
        "Research interpretation",
        placeholder="Explain why this gene is a candidate..."
    )

    st.warning(
        "Candidate signals are hypotheses for further investigation, "
        "not confirmed biomarkers."
    )

# --------------------------------------------------
# TAB 4 - INDEPENDENT VALIDATION
# --------------------------------------------------

with tab4:

    st.subheader("04 | Independent Validation")

    st.write(
        "Record external cohort testing and whether "
        "candidate signals replicate."
    )

    external_dataset = st.text_input(
        "External dataset accession",
        placeholder="Example: Enter an independent GEO accession"
    )

    validation_status = st.selectbox(
        "Validation status",
        [
            "Not started",
            "Data collected",
            "Analysis in progress",
            "Replicated",
            "Not replicated"
        ]
    )

    validation_method = st.selectbox(
        "Validation method",
        [
            "Not selected",
            "Differential expression",
            "Survival analysis",
            "Cox regression",
            "Other"
        ]
    )

    validation_notes = st.text_area(
        "Validation findings",
        placeholder="Document independent cohort results..."
    )

    st.info(
        "External validation is a planned workflow until "
        "independent cohort results have actually been analyzed."
    )

# --------------------------------------------------
# TAB 5 - EVIDENCE REPORT
# --------------------------------------------------

with tab5:

    st.subheader("05 | Evidence Report")

    st.write(
        "Research findings generated from the TNBC dataset "
        "and completed data quality investigations."
    )

    # Dataset information
    st.markdown("### 1. Dataset overview")

    quality = calculate_data_quality()

    col1, col2, col3 = st.columns(3)

    col1.metric("Samples", f"{quality['samples']:,}")
    col2.metric("Expression probes", f"{quality['probes']:,}")
    col3.metric(
        "Missing values",
        f"{quality['missing_percentage']:.5f}%"
    )

    st.markdown("### 2. Verified findings")

    verified_findings = [
        "All 579 metadata sample names match the expression matrix.",
        "No duplicate expression sample identities were detected.",
        "The expression matrix contains 22,283 probes.",
        "Overall missingness is approximately 0.00816%.",
        "No non-numeric expression values were detected.",
        "Expression distributions and platform differences were investigated.",
        "PCA and sample correlation analyses were performed.",
        "Potential expression outliers were identified for further review.",
        "Cohort-specific expression differences require further investigation."
    ]

    for finding in verified_findings:
        st.markdown(f"- {finding}")

    st.markdown("### 3. TNBC_119 investigation")

    st.write(
        "TNBC_119 showed an unusual expression profile within cohort 9. "
        "Its mean expression was lower than that of the other cohort 9 "
        "samples, and its expression profile differed across multiple probes."
    )

    st.write(
        "Exploratory probe annotation identified differences involving "
        "GRIA2, REG1A, DLK1, COL2A1, HMMR, MMP7 and CD24."
    )

    st.warning(
        "These findings are exploratory. They do not establish "
        "biomarker validity or clinical significance."
    )

    st.markdown("### 4. Evidence strength")

    evidence_strength = st.selectbox(
        "Overall evidence strength",
        [
            "Exploratory",
            "Preliminary",
            "Supported by independent validation"
        ],
        index=0
    )

    if evidence_strength == "Supported by independent validation":
        st.warning(
            "Select this status only after independent validation "
            "has actually been completed."
        )

    st.markdown("### 5. Research limitations")

    limitations = st.text_area(
        "Research limitations",
        value=(
            "The dataset combines multiple cohorts and array platforms. "
            "Cohort and technical effects may be confounded. "
            "Potential outliers require further review. "
            "Independent validation has not yet been completed. "
            "No clinical biomarker performance has been established."
        ),
        height=140
    )

    st.markdown("### 6. Next research steps")

    next_steps = st.text_area(
        "Next research steps",
        value=(
            "1. Investigate cohort-specific expression differences.\n"
            "2. Evaluate potential batch effects.\n"
            "3. Complete exploratory candidate-gene analysis.\n"
            "4. Obtain independent validation datasets.\n"
            "5. Evaluate candidate biomarkers using appropriate "
            "statistical methods."
        ),
        height=140
    )

    st.divider()

    st.markdown("### 7. Research report preview")

    report = f"""
# {project_name}

## Dataset
Accession: {geo_accession}

Samples: {quality['samples']}
Expression probes: {quality['probes']}
Missing values: {quality['missing_values']}
Missing percentage: {quality['missing_percentage']:.5f}%

## Verified findings

{chr(10).join("- " + item for item in verified_findings)}

## TNBC_119 investigation

TNBC_119 showed an unusual expression profile within cohort 9.
Probe-level differences require further investigation.

## Evidence strength

{evidence_strength}

## Limitations

{limitations}

## Next research steps

{next_steps}

---
Generated on: {date.today()}

Research prototype only. Not for clinical decision-making.
"""

    st.download_button(
        label="Download Evidence Report",
        data=report,
        file_name="TNBC_research_evidence_report.md",
        mime="text/markdown"
    )
