import streamlit as st

st.set_page_config(
    page_title="Contact Us | Loan Approval Demo",
    page_icon="✉️",
    layout="wide",
)

st.title("Contact Us")
st.caption("Project information and demo enquiries")

st.write(
    "Thank you for exploring the Agentic AI Loan Approval Demo. "
    "This academic proof of concept demonstrates a fictional retail lending "
    "workflow using synthetic applicant data, MySQL, CSV, Streamlit, and "
    "Python rule-based checks."
)

st.header("About this project")
st.markdown(
    """
    **Project:** Agentic AI Loan Approval Demo

    **Purpose:** Demonstrate how structured applicant data, explainable checks,
    document-status review, preliminary recommendations, and human oversight
    can fit into a simplified loan assessment journey.

    **Current implementation:** MySQL data storage, CSV export, Streamlit pages,
    Python-based assessment rules, simulated document statuses, and human
    decision recording.

    **Not currently connected:** Google BigQuery, live credit bureau or banking
    APIs, automated real-document extraction, and LLM-powered agents.
    """
)

st.header("Project scope")
st.info(
    "This is a demonstration prototype using fictional data. It does not "
    "approve or reject real loan applications, issue loan sanctions, or "
    "disburse funds. Preliminary findings require review by an authorised human."
)

st.header("Enquiries")
st.write(
    "For questions about this demonstration, please contact the project owner "
    "through the communication channel provided by your course or assessment "
    "coordinator."
)

st.caption(
    "No personal contact details are displayed on this page. Do not enter or "
    "share real applicant information, passwords, database credentials, or API keys."
)
