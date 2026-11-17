
import streamlit as st
import pandas as pd
from datetime import date

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

researcher = st.sidebar.text_input(
    "Researcher name",
    value="Research Team"
)

project_description = st.sidebar.text_area(
    "Project description",
    value="TNBC biomarker discovery and validation research."
)

st.sidebar.divider()

st.sidebar.caption("TNBC Research Demo | Version 1.0")

# --------------------------------------------------
# PROJECT OVERVIEW
# --------------------------------------------------

st.header("Research Project Details")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Project", project_name)

with col2:
    st.metric("Dataset accession", geo_accession)

with col3:
    st.metric("Workspace sections", "05")

st.write("**Research description:**", project_description)
st.write("**Researcher:**", researcher)

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
        "Technology / Platform",
        value="Microarray (demo)"
    )

    sample_count = st.number_input(
        "Number of samples",
        min_value=0,
        value=579
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

    st.subheader("02 | Data Quality")

    st.write(
        "Record missing values, sample balance, "
        "batch effects and technical replicates."
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Demo samples", "579")

    with c2:
        st.metric("Demo features", "22,283")

    with c3:
        st.metric("Missing expression", "0.0082%")

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
        ["Not assessed", "No major effect detected",
         "Potential batch effect", "Batch effect detected"]
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
        "The displayed metrics are example values, not live QC calculations."
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
        "Summarize the research findings, evidence strength "
        "and remaining limitations."
    )

    findings = st.text_area(
        "Key research findings",
        placeholder="Summarize the findings supported by your analysis..."
    )

    evidence_strength = st.selectbox(
        "Overall evidence strength",
        [
            "Not assessed",
            "Exploratory",
            "Preliminary",
            "Supported by independent validation"
        ]
    )

    limitations = st.text_area(
        "Research limitations",
        value=(
            "This demonstration does not establish clinical validity. "
            "Independent validation and further statistical assessment "
            "are required."
        )
    )

    next_steps = st.text_area(
        "Next research steps",
        placeholder="Describe the next steps..."
    )

    st.divider()

    st.markdown("### Research report preview")

    report = f"""
# {project_name}

## Dataset
Accession: {geo_accession}

## Key findings
{findings}

## Evidence strength
{evidence_strength}

## Limitations
{limitations}

## Next steps
{next_steps}

---
Generated on: {date.today()}
Research demonstration only. Not for clinical decision-making.
"""

    st.download_button(
        label="Download Evidence Report",
        data=report,
        file_name="TNBC_research_evidence_report.md",
        mime="text/markdown"
    )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "TNBC New Project | Research prototype | "
    "For academic and exploratory research only."
)
