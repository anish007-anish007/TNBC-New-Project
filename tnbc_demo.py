import streamlit as st
from datetime import datetime

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="TNBC AI",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# BIOINFORMATICS-INSPIRED BACKGROUND AND CSS
# --------------------------------------------------

st.markdown("""
<style>

/* Main application background */
.stApp {
    background:
        radial-gradient(circle at 10% 15%, rgba(0, 220, 200, 0.16), transparent 28%),
        radial-gradient(circle at 90% 80%, rgba(90, 100, 255, 0.20), transparent 30%),
        linear-gradient(135deg, #061321 0%, #0b1e35 50%, #10152e 100%);
    color: #f1f5f9;
}

/* Keep content comfortably wide */
.block-container {
    padding-top: 2.5rem;
    padding-bottom: 3rem;
    max-width: 1150px;
}

/* Main title */
.main-title {
    text-align: center;
    font-size:  fifty;
    font-size: 52px;
    font-weight: 800;
    letter-spacing: 4px;
    color: #ffffff;
    text-shadow: 0 0 22px rgba(0, 230, 210, 0.45);
    margin-bottom: 5px;
}

/* Subtitle below title */
.main-subtitle {
    text-align: center;
    color: #a9c7dc;
    font-size: 17px;
    margin-bottom: 28px;
}

/* Demo status */
.demo-label {
    text-align: center;
    color: #53e6d1;
    font-size: 12px;
    letter-spacing: 3px;
    font-weight: bold;
    margin-bottom: 10px;
}

/* Section cards */
.section-card {
    background: rgba(15, 35, 58, 0.82);
    border: 1px solid rgba(82, 220, 210, 0.28);
    border-radius: 15px;
    padding: 18px 20px 8px 20px;
    margin-top: 14px;
    margin-bottom: 12px;
    box-shadow: 0 8px 28px rgba(0, 0, 0, 0.18);
}

/* Section headings */
.section-heading {
    color: #65e6d5;
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 5px;
}

/* Section descriptions */
.section-description {
    color: #b5c9d9;
    font-size: 13px;
    margin-bottom: 12px;
}

/* Text input labels */
label {
    color: #e6f1f8 !important;
}

/* Text areas */
.stTextArea textarea {
    background-color: rgba(5, 19, 34, 0.92) !important;
    color: #ffffff !important;
    border: 1px solid #31546b !important;
    border-radius: 10px !important;
}

/* Text input boxes */
.stTextInput input {
    background-color: rgba(5, 19, 34, 0.92) !important;
    color: #ffffff !important;
    border: 1px solid #31546b !important;
    border-radius: 8px !important;
}

/* Buttons */
.stButton button, .stDownloadButton button {
    background: linear-gradient(90deg, #087f8c, #12b8a6);
    color: white;
    border: none;
    border-radius: 9px;
    padding: 10px 22px;
    font-weight: 700;
}

.stButton button:hover, .stDownloadButton button:hover {
    background: linear-gradient(90deg, #0ba5a9, #38d9c5);
    color: white;
    border: none;
}

/* Divider */
hr {
    border-color: rgba(120, 210, 220, 0.25);
}

/* Footer */
.footer {
    text-align: center;
    color: #7895aa;
    font-size: 12px;
    padding-top: 28px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="demo-label">BIOINFORMATICS • CANCER RESEARCH • AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-title">🧬 TNBC AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-subtitle">'
    'An AI-assisted research workspace for Triple-Negative Breast Cancer biomarker evidence'
    '</div>',
    unsafe_allow_html=True
)

st.info(
    "DEMO MODE: Enter sample or illustrative research information below. "
    "This prototype does not perform clinical diagnosis or establish validated biomarkers."
)


# --------------------------------------------------
# PROJECT DETAILS
# --------------------------------------------------

st.markdown("### Research project details")

col1, col2 = st.columns(2)

with col1:
    project_name = st.text_input(
        "Project name",
        placeholder="Example: TNBC biomarker research"
    )

with col2:
    dataset_accession = st.text_input(
        "GEO / dataset accession",
        placeholder="Example: GSE12345"
    )

st.divider()


# --------------------------------------------------
# RESEARCH SECTIONS
# --------------------------------------------------

st.markdown("## Research evidence workspace")

with st.form("tnbc_research_form"):

    # 1. DATASET PROVENANCE
    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    st.markdown(
        '<div class="section-heading">01 | Dataset provenance</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Record where the dataset came from and how the samples were collected.'
        '</div>',
        unsafe_allow_html=True
    )

    provenance = st.text_area(
        "Dataset provenance details",
        placeholder=(
            "Enter dataset accession, source repository, platform, "
            "publication, sample count, tissue type and collection details..."
        ),
        height=120,
        key="provenance"
    )

    st.markdown('</div>', unsafe_allow_html=True)


    # 2. DATA QUALITY
    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    st.markdown(
        '<div class="section-heading">02 | Data quality</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Describe missing values, sample balance, batch effects and technical replicates.'
        '</div>',
        unsafe_allow_html=True
    )

    data_quality = st.text_area(
        "Data quality assessment",
        placeholder=(
            "Enter number of samples, missing-value percentage, "
            "class distribution, batch information, outlier observations "
            "and quality-control findings..."
        ),
        height=120,
        key="data_quality"
    )

    st.markdown('</div>', unsafe_allow_html=True)


    # 3. CANDIDATE SIGNALS
    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    st.markdown(
        '<div class="section-heading">03 | Candidate signals</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Record candidate genes and the statistical evidence supporting further investigation.'
        '</div>',
        unsafe_allow_html=True
    )

    candidate_signals = st.text_area(
        "Candidate biomarker details",
        placeholder=(
            "Enter candidate gene symbols, log2 fold change, "
            "adjusted p-values, effect sizes, analysis method "
            "and whether the findings are exploratory..."
        ),
        height=120,
        key="candidate_signals"
    )

    st.markdown('</div>', unsafe_allow_html=True)


    # 4. INDEPENDENT VALIDATION
    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    st.markdown(
        '<div class="section-heading">04 | Independent validation</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Document external cohort testing and whether the candidate signals replicate.'
        '</div>',
        unsafe_allow_html=True
    )

    independent_validation = st.text_area(
        "Independent validation details",
        placeholder=(
            "Enter external dataset accession, validation sample count, "
            "model evaluation metrics, replication of gene-expression direction "
            "and any limitations. If not performed, state 'Not yet performed'."
        ),
        height=120,
        key="independent_validation"
    )

    st.markdown('</div>', unsafe_allow_html=True)


    # 5. EVIDENCE REPORT
    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    st.markdown(
        '<div class="section-heading">05 | Evidence report</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Summarize the research findings, evidence strength and remaining limitations.'
        '</div>',
        unsafe_allow_html=True
    )

    evidence_report = st.text_area(
        "Research evidence summary",
        placeholder=(
            "Summarize the research objective, major observations, "
            "strength of evidence, limitations, next steps and conclusions..."
        ),
        height=140,
        key="evidence_report"
    )

    st.markdown('</div>', unsafe_allow_html=True)


    # SUBMIT BUTTON
    st.markdown("")
    submitted = st.form_submit_button(
        "Generate Research Evidence Report",
        use_container_width=True
    )


# --------------------------------------------------
# REPORT GENERATION
# --------------------------------------------------

if submitted:

    report = f"""
TNBC AI — RESEARCH EVIDENCE REPORT
=================================

Generated: {datetime.now().strftime("%d-%m-%Y %H:%M")}

PROJECT DETAILS
---------------
Project name: {project_name or "Not provided"}
Dataset accession: {dataset_accession or "Not provided"}

1. DATASET PROVENANCE
--------------------
{provenance or "Not provided"}

2. DATA QUALITY
---------------
{data_quality or "Not provided"}

3. CANDIDATE SIGNALS
-------------------
{candidate_signals or "Not provided"}

4. INDEPENDENT VALIDATION
-------------------------
{independent_validation or "Not provided"}

5. EVIDENCE REPORT
------------------
{evidence_report or "Not provided"}

IMPORTANT DISCLAIMER
--------------------
This is a research demonstration report.
It does not establish clinical validity, diagnose cancer,
or recommend treatment.
All findings require appropriate scientific validation.
"""

    st.session_state["generated_report"] = report

    st.success("Research evidence report generated successfully.")


# --------------------------------------------------
# DOWNLOAD REPORT
# --------------------------------------------------

if "generated_report" in st.session_state:

    st.markdown("## Your generated report")

    st.download_button(
        label="⬇ Download Research Report",
        data=st.session_state["generated_report"],
        file_name="TNBC_AI_Evidence_Report.txt",
        mime="text/plain",
        use_container_width=True
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.markdown(
    '<div class="footer">'
    'TNBC AI | AI-assisted bioinformatics research demo<br>'
    'Research use only • Not intended for clinical decision-making'
    '</div>',
    unsafe_allow_html=True
)