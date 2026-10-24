import streamlit as st

st.set_page_config(
    page_title="Approach Story | Loan Approval Demo",
    page_icon="🧭",
    layout="wide",
)

st.title("Our Approach")
st.caption("From fragmented loan data to explainable, human-supervised decisions")

st.markdown(
    """
    This proof of concept explores how a loan approval journey can become more
    organised, transparent and easier to review. The story has two acts: first,
    establish a usable data foundation; second, design an agentic workflow around
    that foundation.
    """
)

st.divider()

st.header("Act 1 — Build the data foundation")
st.write(
    "A lending decision depends on information from several places: applicant "
    "details, income and repayment obligations, identity documents, bank "
    "statements, credit information and lending policies. When information is "
    "inconsistent or difficult to find, reviewers spend time collecting and "
    "rechecking evidence before they can assess the application."
)

a1, a2, a3 = st.columns(3)

with a1:
    with st.container(border=True):
        st.subheader("Collect")
        st.write(
            "Bring applicant attributes and verification statuses into a "
            "consistent structure."
        )
        st.caption("Current demo: 100 fictional applicant records in MySQL.")

with a2:
    with st.container(border=True):
        st.subheader("Prepare")
        st.write(
            "Organise key fields and create a portable dataset for inspection "
            "and analysis."
        )
        st.caption("Current demo: Python/Pandas and lakehouse_applicants.csv.")

with a3:
    with st.container(border=True):
        st.subheader("Validate")
        st.write(
            "Check relevant fields and surface issues that may need attention "
            "before a decision."
        )
        st.caption(
            "Current demo: rule-based assessment checks and simulated document statuses."
        )

st.success(
    "Act 1 outcome: a structured, inspectable dataset that supports a more "
    "consistent demonstration of the loan assessment workflow."
)

st.info(
    "Current-state note: MySQL and CSV are implemented. Google BigQuery is not "
    "connected, and the CSV is an exported file rather than a live-synchronised lakehouse."
)

st.divider()

st.header("Act 2 — Design the agentic loan assessment")
st.write(
    "With a reliable data foundation, a future agentic workflow could coordinate "
    "specialised tasks. Each task should return evidence and a reason, while "
    "uncertain or adverse findings are routed to an authorised human reviewer."
)

agents = [
    (
        "1. Application and document checks",
        "Check required fields and document status; identify missing or inconsistent evidence.",
        "Current demo: simulated document statuses and Python-based checks.",
    ),
    (
        "2. Policy lookup",
        "Retrieve the relevant lending rule and show the rule used for a check.",
        "Future enhancement: a controlled policy knowledge source is not connected.",
    ),
    (
        "3. Credit and affordability assessment",
        "Review income, existing obligations, requested amount, tenure and available credit indicators.",
        "Current demo: rule-based affordability checks and a mock credit score.",
    ),
    (
        "4. Risk flagging and explanation",
        "Summarise potential concerns, supporting evidence and the next recommended action.",
        "Current demo: assessment findings and a preliminary recommendation.",
    ),
    (
        "5. Human review",
        "Present the findings for an authorised credit officer to review and record a decision.",
        "Current demo: officer decision and rationale can be saved in MySQL.",
    ),
]

for title, description, status in agents:
    with st.container(border=True):
        st.markdown(f"**{title}**")
        st.write(description)
        st.caption(status)

st.warning(
    "These are workflow roles, not proof that autonomous LLM agents are running. "
    "The current prototype uses Python rules and simulated checks; LLM-powered "
    "agents and live external integrations have not been implemented."
)

st.divider()

st.header("The end-to-end journey")
st.code(
    "Application data\\n"
    "   ↓\\n"
    "Data preparation and validation\\n"
    "   ↓\\n"
    "Document-status and policy checks\\n"
    "   ↓\\n"
    "Credit / affordability assessment\\n"
    "   ↓\\n"
    "Risk flags, evidence and preliminary recommendation\\n"
    "   ↓\\n"
    "Authorised human review\\n"
    "   ↓\\n"
    "Decision and rationale recorded",
    language="text",
)

st.header("Design principles")
p1, p2 = st.columns(2)

with p1:
    st.markdown(
        """
        - **Explainability:** show evidence and rules behind findings.
        - **Human oversight:** keep final lending decisions with authorised staff.
        - **Traceability:** record decisions and rationale.
        """
    )

with p2:
    st.markdown(
        """
        - **Data quality:** validate inputs before relying on them.
        - **Privacy and security:** protect credentials and restrict data access.
        - **Honest scope:** label proposed integrations separately from implemented features.
        """
    )

st.caption(
    "This is a fictional proof of concept for demonstration and learning. "
    "It does not approve real loans, connect to live credit bureaus, or disburse funds."
)
