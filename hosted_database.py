
import streamlit as st
import pandas as pd


def save_applicants_if_empty(df):
    """Keep fictional applicant data in the current Streamlit session."""
    if "hosted_applicants" not in st.session_state:
        st.session_state["hosted_applicants"] = df.copy()


def load_applicants():
    """Load fictional applicant data from the current session."""
    applicants = st.session_state.get("hosted_applicants")

    if applicants is None:
        return None

    return applicants.copy()


def save_document_statuses(application_id, statuses):
    """Save demo verification statuses for the current session."""
    all_statuses = st.session_state.get(
        "hosted_document_statuses", {}
    ).copy()

    all_statuses[str(application_id)] = dict(statuses)
    st.session_state["hosted_document_statuses"] = all_statuses


def load_document_statuses(application_id):
    """Load demo verification statuses for the current session."""
    all_statuses = st.session_state.get(
        "hosted_document_statuses", {}
    )

    statuses = all_statuses.get(str(application_id))

    return dict(statuses) if statuses is not None else None


def save_officer_decision(application_id, decision, rationale):
    """Save a demo officer decision for the current session."""
    all_decisions = st.session_state.get(
        "hosted_officer_decisions", {}
    ).copy()

    all_decisions[str(application_id)] = {
        "decision": str(decision),
        "rationale": str(rationale),
    }

    st.session_state["hosted_officer_decisions"] = all_decisions


def load_officer_decision(application_id):
    """Load a demo officer decision from the current session."""
    all_decisions = st.session_state.get(
        "hosted_officer_decisions", {}
    )

    decision = all_decisions.get(str(application_id))

    return dict(decision) if decision is not None else None
