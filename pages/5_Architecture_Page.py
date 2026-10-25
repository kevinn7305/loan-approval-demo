import streamlit as st

st.set_page_config(
    page_title="Architecture | Loan Approval Demo",
    page_icon="🏗️",
    layout="wide",
)

st.title("Solution Architecture")
st.caption(
    "Agentic AI Loan Approval Demo | Current implementation and proposed future state"
)

st.info(
    "This page documents the current prototype honestly. It uses fictional data, "
    "MySQL, CSV, and Python rule-based checks. BigQuery and LLM-powered agents "
    "are not connected in the current implementation."
)

st.header("1. Current architecture")

st.markdown(
    """
    <style>
    .arch-card {
        border: 1px solid rgba(128,128,128,.35);
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
        min-height: 105px;
    }
    .arch-title {
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 6px;
    }
    .arch-subtitle {
        font-size: .92rem;
        opacity: .88;
    }
    .arch-arrow {
        text-align: center;
        font-size: 1.6rem;
        padding: 0;
        opacity: .75;
    }
    </style>
    <div class="arch-card">
      <div class="arch-title">1. Data sources</div>
      <div class="arch-subtitle">100 fictional applicants · MySQL tables · CSV export</div>
    </div>
    <div class="arch-arrow">↓</div>
    <div class="arch-card">
      <div class="arch-title">2. Data preparation</div>
      <div class="arch-subtitle">Python and Pandas · Structured fields · CSV validation</div>
    </div>
    <div class="arch-arrow">↓</div>
    <div class="arch-card">
      <div class="arch-title">3. Loan assessment workflow</div>
      <div class="arch-subtitle">Python rule-based checks · Affordability · Mock credit score · Simulated document statuses</div>
    </div>
    <div class="arch-arrow">↓</div>
    <div class="arch-card">
      <div class="arch-title">4. Streamlit user interface</div>
      <div class="arch-subtitle">Dashboard · Applicant Explorer · Loan Assessment · Document Verification · Agent Activity</div>
    </div>
    <div class="arch-arrow">↓</div>
    <div class="arch-card">
      <div class="arch-title">5. Human review and persistence</div>
      <div class="arch-subtitle">Credit officer reviews findings and records a decision in MySQL</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption(
    "The current workflow is a rule-based demonstration, not a live autonomous "
    "AI system. External credit bureau, banking, and document extraction APIs are not connected."
)

st.header("2. Current technology and data")

left, right = st.columns(2)

with left:
    st.subheader("Implemented")
    st.markdown(
        """
        - **Python / Pandas:** data preparation and assessment logic
        - **MySQL:** applicant records, document verification statuses, and officer decisions
        - **CSV:** portable structured export (`lakehouse_applicants.csv`)
        - **Streamlit:** interactive demonstration UI
        - **Fictional data:** 100 generated applicant records
        """
    )

with right:
    st.subheader("Not connected or not implemented")
    st.markdown(
        """
        - **Google BigQuery:** not connected
        - **LLM-powered agents:** not implemented
        - **Live credit bureau APIs:** not connected
        - **Automated real-document extraction:** not implemented
        - **Real loan sanction or disbursement:** not performed
        """
    )

st.header("3. Proposed future architecture")

st.warning(
    "The following is a proposal, not the current deployed implementation. "
    "Cloud services should only be added after access, security, and costs are reviewed."
)

future_steps = [
    ("Data ingestion", "Ingest approved structured data and document metadata from controlled sources."),
    ("Cloud analytical layer", "Use Google BigQuery for curated analytical tables if access and billing are acceptable."),
    ("Data quality and governance", "Apply schema checks, validation rules, access controls, and audit logging."),
    ("Agent orchestration", "Add separately tested agents for document checks, policy lookup, credit assessment, and risk flagging."),
    ("Human-in-the-loop", "Require an authorised credit officer to review evidence and make the final decision."),
    ("Monitoring", "Log agent actions, errors, decision rationale, and changes for audit and evaluation."),
]

for title, description in future_steps:
    with st.container(border=True):
        st.markdown(f"**{title}**")
        st.write(description)

st.header("4. Human oversight and responsible use")
st.markdown(
    """
    - Automated findings are advisory and must be supported by visible evidence.
    - A failed or uncertain check should trigger review rather than an automatic final rejection.
    - Only authorised personnel should record final lending decisions.
    - This prototype uses fictional data and must not be used to approve real loans.
    - Credentials and API keys should remain outside source control.
    """
)

st.header("5. Data flow summary")
st.code(
    "Fictional applicant records\\n"
    "        ↓\\n"
    "MySQL database ──→ Python/Pandas export ──→ lakehouse_applicants.csv\\n"
    "        ↓\\n"
    "Streamlit assessment workflow (Python rules and simulated checks)\\n"
    "        ↓\\n"
    "Assessment findings and preliminary recommendation\\n"
    "        ↓\\n"
    "Human credit officer review → decision and rationale saved in MySQL",
    language="text",
)

st.caption(
    "Architecture status: current prototype uses MySQL + CSV. BigQuery and LLM integrations remain future enhancements."
)
