
import streamlit as st
import pandas as pd
import numpy as np

from hosted_database import (
    save_applicants_if_empty,
    load_applicants,
    save_document_statuses,
    load_document_statuses,
    save_officer_decision,
    load_officer_decision,
)


st.set_page_config(
    page_title="Agentic AI Loan Approval",
    page_icon="🏦",
    layout="wide"
)


# =====================================================
# 1. SESSION STATE
# =====================================================

defaults = {
    "assessment": None,
    "officer_decision": "Pending",
    "officer_reason": "",
    "document_statuses": {
        "KYC Documents": "Pending",
        "Salary Slips": "Pending",
        "Bank Statements": "Pending",
        "Mock Credit Bureau": "Pending"
    }
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =====================================================
# 2. EMI CALCULATION
# =====================================================

def calculate_emi(principal, annual_rate, months):
    if months <= 0:
        return 0.0

    monthly_rate = annual_rate / 1200

    if monthly_rate == 0:
        return principal / months

    factor = (1 + monthly_rate) ** months

    return principal * monthly_rate * factor / (factor - 1)


# =====================================================
# 3. GENERATE SYNTHETIC APPLICANTS
# =====================================================

@st.cache_data
def generate_applicants(n=100):
    rng = np.random.default_rng(42)

    first_names = [
        "Aarav", "Priya", "Rahul", "Ananya", "Arjun",
        "Meera", "Karthik", "Sneha", "Rohan", "Divya",
        "Vikram", "Nisha", "Aditya", "Kavya", "Sanjay",
        "Ishita", "Varun", "Aditi", "Harish", "Pooja"
    ]

    last_names = [
        "Sharma", "Rao", "Kumar", "Nair", "Reddy",
        "Iyer", "Patel", "Das", "Singh", "Menon"
    ]

    records = []

    for i in range(n):
        income = int(rng.integers(20000, 150001))
        existing_emi = int(income * rng.uniform(0.00, 0.25))
        loan_amount = int(rng.integers(100000, 1500001))
        tenure = int(rng.choice([12, 24, 36, 48, 60]))
        credit_score = int(rng.integers(550, 851))

        kyc = str(rng.choice(
            ["Verified", "Pending", "Failed"],
            p=[0.82, 0.13, 0.05]
        ))

        salary = str(rng.choice(
            ["Verified", "Pending", "Failed"],
            p=[0.78, 0.17, 0.05]
        ))

        bank = str(rng.choice(
            ["Verified", "Pending", "Failed"],
            p=[0.76, 0.19, 0.05]
        ))

        bureau = str(rng.choice(
            ["Verified", "Pending", "Flagged"],
            p=[0.80, 0.15, 0.05]
        ))

        emi = calculate_emi(loan_amount, 12.0, tenure)
        total_emi = existing_emi + emi
        dti = total_emi / income

        documents_verified = all(
            status == "Verified"
            for status in [kyc, salary, bank, bureau]
        )

        policy_ok = loan_amount <= income * 20
        credit_ok = credit_score >= 700
        affordability_ok = dti <= 0.40

        if (
            documents_verified
            and policy_ok
            and credit_ok
            and affordability_ok
        ):
            application_status = "Ready for human review"
        else:
            application_status = "Further review"

        if (
            dti > 0.50
            or credit_score < 650
            or "Failed" in [kyc, salary, bank]
            or bureau == "Flagged"
        ):
            risk_level = "High"

        elif (
            dti > 0.40
            or credit_score < 700
            or not documents_verified
            or not policy_ok
        ):
            risk_level = "Moderate"

        else:
            risk_level = "Low"

        records.append({
            "Application ID": f"APP{i + 1:04d}",

            "Applicant Name": (
                f"{first_names[i % len(first_names)]} "
                f"{last_names[(i // 2) % len(last_names)]} "
                f"{i + 1}"
            ),

            "Monthly Income": income,
            "Existing EMI": existing_emi,
            "Loan Amount": loan_amount,
            "Tenure (Months)": tenure,
            "Estimated EMI": round(emi, 2),
            "Credit Score": credit_score,
            "EMI Ratio (%)": round(dti * 100, 2),
            "KYC Status": kyc,
            "Salary Slips Status": salary,
            "Bank Statement Status": bank,
            "Bureau Status": bureau,
            "Risk Level": risk_level,
            "Application Status": application_status
        })

    return pd.DataFrame(records)


# =====================================================
# 4. MYSQL INITIALIZATION AND DATA LOADING
# =====================================================

try:
    generated_applicants = generate_applicants(100)

    # Insert the generated data only when the table is empty.
    save_applicants_if_empty(generated_applicants)

    # Load the applicant records from MySQL.
    applicants = load_applicants()

    if applicants is None or applicants.empty:
        st.error("No applicant records were loaded from MySQL.")
        st.stop()

except Exception as error:
    st.error("Unable to load the fictional applicant data for this demo.")
    st.exception(error)
    st.stop() 

try:
    saved_statuses = load_document_statuses("MANUAL-DEMO")
    if saved_statuses is not None:
        st.session_state.document_statuses = saved_statuses
except Exception as error:
    st.error("Unable to load document verification statuses.")
    st.exception(error)

try:
    saved_officer_decision = load_officer_decision("MANUAL-DEMO")
    if saved_officer_decision is not None:
        st.session_state.officer_decision = saved_officer_decision["decision"]
        st.session_state.officer_reason = saved_officer_decision["rationale"]
except Exception as error:
    st.error("Unable to load the saved officer decision.")
    st.exception(error)


# =====================================================
# 5. NAVIGATION
# =====================================================

st.title("🏦 Agentic AI Loan Approval")
st.caption("Retail Lending Intelligence | Synthetic Portfolio Demo")

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select page",
    [
        "Dashboard",
        "Applicant Explorer",
        "Loan Assessment",
        "Document Verification",
        "Agent Activity",
        "About"
    ]
)

st.sidebar.divider()
st.sidebar.caption(f"Dataset: {len(applicants)} fictional applicants")
st.sidebar.caption("Interest rate assumption: 12% annually")
st.sidebar.caption("Storage: Streamlit session (demo only)")


# =====================================================
# 6. DASHBOARD
# =====================================================

if page == "Dashboard":

    st.header("Loan Portfolio Dashboard")

    total_apps = len(applicants)

    further_review = int(
        (applicants["Application Status"] == "Further review").sum()
    )

    ready_review = int(
        (
            applicants["Application Status"]
            == "Ready for human review"
        ).sum()
    )

    high_risk = int(
        (applicants["Risk Level"] == "High").sum()
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Applications", total_apps)
    c2.metric("Further Review", further_review)
    c3.metric("High Risk", high_risk)
    c4.metric("Ready for Human Review", ready_review)

    st.caption(
        "'Ready for human review' does not mean approved. "
        "All figures use simulated data."
    )

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Application Status")

        status_counts = (
            applicants["Application Status"]
            .value_counts()
            .rename_axis("Status")
            .reset_index(name="Applications")
        )

        st.bar_chart(
            status_counts,
            x="Status",
            y="Applications",
            horizontal=True
        )

    with right:
        st.subheader("Risk Distribution")

        risk_counts = (
            applicants["Risk Level"]
            .value_counts()
            .rename_axis("Risk")
            .reset_index(name="Applications")
        )

        st.bar_chart(
            risk_counts,
            x="Risk",
            y="Applications",
            horizontal=True
        )

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Credit Score Distribution")

        score_counts = pd.cut(
            applicants["Credit Score"],
            bins=[549, 600, 650, 700, 750, 800, 851],
            labels=[
                "550–600",
                "601–650",
                "651–700",
                "701–750",
                "751–800",
                "801–850"
            ]
        ).value_counts(sort=False)

        score_data = score_counts.rename_axis(
            "Score Range"
        ).reset_index(name="Applicants")

        st.bar_chart(
            score_data,
            x="Score Range",
            y="Applicants"
        )

    with right:
        st.subheader("Affordability Analysis")

        chart_data = applicants[
            ["Monthly Income", "EMI Ratio (%)"]
        ].copy()

        chart_data["Income Band"] = pd.cut(
            chart_data["Monthly Income"],
            bins=[0, 40000, 70000, 100000, float("inf")],
            labels=[
                "Below ₹40k",
                "₹40k–₹70k",
                "₹70k–₹100k",
                "Above ₹100k"
            ]
        )

        affordability_summary = (
            chart_data.groupby(
                "Income Band",
                observed=False
            )["EMI Ratio (%)"]
            .mean()
            .reset_index()
        )

        st.bar_chart(
            affordability_summary,
            x="Income Band",
            y="EMI Ratio (%)"
        )

    st.divider()
    st.subheader("Recent Synthetic Applications")

    st.dataframe(
        applicants.head(10),
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Download Applicant Dataset (CSV)",
        data=applicants.to_csv(index=False).encode("utf-8"),
        file_name="synthetic_loan_applicants.csv",
        mime="text/csv"
    )


# =====================================================
# 7. APPLICANT EXPLORER
# =====================================================

elif page == "Applicant Explorer":

    st.header("Applicant Explorer")

    search = st.text_input(
        "Search by application ID or applicant name"
    )

    risk_filter = st.multiselect(
        "Filter by Risk Level",
        ["Low", "Moderate", "High"],
        default=["Low", "Moderate", "High"]
    )

    status_filter = st.multiselect(
        "Filter by Application Status",
        ["Ready for human review", "Further review"],
        default=["Ready for human review", "Further review"]
    )

    filtered = applicants[
        applicants["Risk Level"].isin(risk_filter)
        & applicants["Application Status"].isin(status_filter)
    ].copy()

    if search.strip():
        term = search.strip()

        filtered = filtered[
            filtered["Application ID"].str.contains(
                term, case=False, na=False
            )
            | filtered["Applicant Name"].str.contains(
                term, case=False, na=False
            )
        ]

    st.write(f"Matching applications: {len(filtered)}")

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True
    )

    if not filtered.empty:

        selected_id = st.selectbox(
            "Inspect an application",
            filtered["Application ID"].tolist()
        )

        record = filtered[
            filtered["Application ID"] == selected_id
        ].iloc[0]

        st.subheader(f"Application {selected_id}")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Monthly Income",
            f"₹{record['Monthly Income']:,.0f}"
        )

        c2.metric(
            "Requested Loan",
            f"₹{record['Loan Amount']:,.0f}"
        )

        c3.metric(
            "Credit Score",
            int(record["Credit Score"])
        )

        st.write(
            "**Application status:**",
            record["Application Status"]
        )

        st.write("**Risk level:**", record["Risk Level"])

        st.write(
            f"**EMI ratio:** {record['EMI Ratio (%)']:.2f}%"
        )

        st.subheader("Verification Statuses")

        for label, column in [
            ("KYC", "KYC Status"),
            ("Salary Slips", "Salary Slips Status"),
            ("Bank Statements", "Bank Statement Status"),
            ("Mock Credit Bureau", "Bureau Status")
        ]:
            st.write(f"**{label}:** {record[column]}")

    st.download_button(
        "Download Filtered Results (CSV)",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="filtered_loan_applicants.csv",
        mime="text/csv"
    )


# =====================================================
# 8. LOAN ASSESSMENT
# =====================================================

elif page == "Loan Assessment":

    st.header("Applicant Details")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input(
            "Applicant Name",
            "Demo Applicant",
            key="applicant_name"
        )

        income = st.number_input(
            "Monthly Income (₹)",
            min_value=0,
            value=60000,
            step=1000
        )

        existing_emi = st.number_input(
            "Existing Monthly EMI (₹)",
            min_value=0,
            value=5000,
            step=500
        )

    with col2:
        loan_amount = st.number_input(
            "Loan Amount Requested (₹)",
            min_value=10000,
            value=500000,
            step=10000
        )

        tenure = st.selectbox(
            "Loan Tenure (months)",
            [12, 24, 36, 48, 60]
        )

        credit_score = st.number_input(
            "Mock Credit Score",
            min_value=300,
            max_value=900,
            value=760
        )

    annual_rate = 12.0

    emi = calculate_emi(
        loan_amount,
        annual_rate,
        tenure
    )

    total_emi = existing_emi + emi

    dti = total_emi / income if income > 0 else None

    st.caption(
        "Illustrative interest rate: 12% per annum. "
        "Affordability threshold: 40% of monthly income."
    )

    st.divider()
    st.subheader("Estimated Affordability")

    c1, c2, c3 = st.columns(3)

    c1.metric("Estimated Monthly EMI", f"₹{emi:,.0f}")
    c2.metric("Total Monthly EMI", f"₹{total_emi:,.0f}")

    c3.metric(
        "EMI / Monthly Income",
        f"{dti:.1%}" if dti is not None else "Unavailable"
    )

    if st.button("Run Preliminary Assessment", type="primary"):

        statuses = st.session_state.document_statuses

        name_ok = bool(name.strip())
        policy_ok = loan_amount <= income * 20
        credit_ok = credit_score >= 700
        affordability_ok = dti is not None and dti <= 0.40

        findings = [
            {
                "agent": "Applicant Information Check",
                "passed": name_ok,
                "reason": "Applicant name provided" if name_ok else "Applicant name is missing",
                "evidence": f"Applicant name entered: {name.strip()!r}" if name_ok else "The applicant-name field is blank.",
                "policy": "A non-empty applicant name is required to identify the case in this demo.",
                "next_action": "Continue with the case." if name_ok else "Enter the applicant's name before assessment."
            },
            {
                "agent": "Loan Amount Policy Check",
                "passed": policy_ok,
                "reason": "Illustrative loan amount rule passed" if policy_ok else "Demo loan amount rule failed",
                "evidence": f"Requested loan ₹{loan_amount:,.0f}; monthly income ₹{income:,.0f}; demo limit ₹{income * 20:,.0f}.",
                "policy": "Demo rule: requested loan amount must not exceed 20 times monthly income. This is an illustrative threshold, not a bank policy.",
                "next_action": "Continue to the next check." if policy_ok else "Review the requested amount and income evidence with a credit officer."
            },
            {
                "agent": "Credit Risk Check",
                "passed": credit_ok,
                "reason": "Mock score meets demo threshold" if credit_ok else "Mock score below demo threshold",
                "evidence": f"Entered mock credit score: {credit_score}.",
                "policy": "Demo rule: mock credit score must be at least 700. No credit bureau is contacted.",
                "next_action": "Continue to the next check." if credit_ok else "Verify the credit information through an authorised source and refer for human review."
            },
            {
                "agent": "Affordability Check",
                "passed": affordability_ok,
                "reason": "EMI ratio is within demo threshold" if affordability_ok else "EMI ratio exceeds demo threshold or income is unavailable",
                "evidence": (
                    f"Estimated new EMI ₹{emi:,.0f} + existing EMI ₹{existing_emi:,.0f} "
                    f"= total monthly EMI ₹{total_emi:,.0f}; monthly income ₹{income:,.0f}; "
                    + (f"EMI-to-income ratio {dti:.1%}." if dti is not None else "EMI-to-income ratio unavailable because income is zero.")
                ),
                "policy": "Demo affordability rule: total monthly EMI must be no more than 40% of monthly income.",
                "next_action": "Continue to the next check." if affordability_ok else "Review income and existing obligations; consider a lower loan amount or longer tenure, then reassess."
            }
        ]

        for document, status in statuses.items():
            passed = status == "Verified"
            findings.append({
                "agent": f"Document Verification Check — {document}",
                "passed": passed,
                "reason": f"Status: {status}",
                "evidence": f"Manually selected demo verification status for {document}: {status}.",
                "policy": "Demo rule: each listed verification status must be Verified to pass this check. No actual document is inspected.",
                "next_action": "Continue to the next check." if passed else f"Review {document.lower()} and update its status only after the required verification is completed."
            })

        blockers = []

        if not name_ok:
            blockers.append("Applicant name is missing")

        if not policy_ok:
            blockers.append("Demo loan amount rule failed")

        if not credit_ok:
            blockers.append("Mock credit score below threshold")

        if not affordability_ok:
            blockers.append("Affordability check failed")

        for document, status in statuses.items():
            if status != "Verified":
                blockers.append(f"{document}: {status}")

        st.session_state.assessment = {
            "name": name,
            "income": income,
            "loan_amount": loan_amount,
            "tenure": tenure,
            "emi": emi,
            "dti": dti,
            "findings": findings,
            "blockers": blockers
        }

        st.session_state.officer_decision = "Pending"
        st.session_state.officer_reason = ""

    result = st.session_state.assessment

    if result is None and st.session_state.officer_decision != "Pending":
        st.divider()
        st.subheader("Previously Recorded Officer Decision")
        st.info(
            "This decision was loaded from MySQL. "
            "Run a new preliminary assessment to review the current inputs."
        )
        st.write("**Recorded decision:**", st.session_state.officer_decision)
        if st.session_state.officer_reason:
            st.write("**Officer rationale:**", st.session_state.officer_reason)

    if result is not None:

        st.divider()
        st.subheader("Explainable Assessment Findings")
        st.caption(
            "Each finding shows the evidence used, the illustrative demo rule, "
            "and a suggested next action. These are rule-based checks, not live AI agents."
        )

        for finding in result["findings"]:
            # Support an assessment created before this version was loaded.
            if isinstance(finding, dict):
                agent = finding["agent"]
                passed = finding["passed"]
                reason = finding["reason"]
                evidence = finding["evidence"]
                policy = finding["policy"]
                next_action = finding["next_action"]
            else:
                agent, passed, reason = finding
                evidence = "Details were generated by an earlier version of this demo."
                policy = "Rule details were not stored for this earlier assessment."
                next_action = "Run the preliminary assessment again to generate evidence-linked findings."

            if passed:
                st.success(f"{agent}: {reason}")
            else:
                st.warning(f"{agent}: {reason}")

            with st.expander(f"Evidence and next action — {agent}"):
                st.markdown(f"**Evidence**  \n{evidence}")
                st.markdown(f"**Rule applied**  \n{policy}")
                st.markdown(f"**Suggested next action**  \n{next_action}")

        st.subheader("Preliminary Recommendation")
        st.caption(
            "This is a preliminary demo outcome only. It is not a lending decision "
            "and must be reviewed by an authorised human decision-maker."
        )

        if result["blockers"]:
            st.warning("Further review required.")

            for blocker in result["blockers"]:
                st.write(f"- {blocker}")

        else:
            st.success(
                "Configured demo checks passed. "
                "Proceed to human credit review."
            )

        st.divider()
        st.subheader("Credit Officer Review")

        if result["blockers"]:
            st.warning(
                "Approval cannot be recorded while assessment blockers remain."
            )

        with st.form("officer_review_form"):

            choices = [
                "Pending",
                "Request More Information",
                "Approve Subject to Checks",
                "Reject"
            ]

            decision = st.selectbox(
                "Record a demo decision",
                choices,
                index=choices.index(
                    st.session_state.officer_decision
                )
            )

            reason = st.text_area(
                "Officer rationale",
                value=st.session_state.officer_reason
            )

            submit = st.form_submit_button(
                "Record Officer Decision"
            )

            if submit:

                if not reason.strip():
                    st.error(
                        "Enter a rationale before recording the decision."
                    )

                elif (
                    decision == "Approve Subject to Checks"
                    and result["blockers"]
                ):
                    st.error(
                        "Resolve all assessment blockers and rerun "
                        "the assessment before recording this decision."
                    )

                else:
                    try:
                        save_officer_decision(
                            "MANUAL-DEMO",
                            decision,
                            reason.strip()
                        )
                        st.session_state.officer_decision = decision
                        st.session_state.officer_reason = reason.strip()

                        st.success(
                            "Officer decision and rationale saved for this demo session."
                        )
                    except Exception as error:
                        st.error(
                            "Unable to save the officer decision to MySQL."
                        )
                        st.exception(error)

        st.write(
            "**Recorded decision:**",
            st.session_state.officer_decision
        )

        if st.session_state.officer_reason:
            st.write(
                "**Officer rationale:**",
                st.session_state.officer_reason
            )


# =====================================================
# 9. DOCUMENT VERIFICATION
# =====================================================

elif page == "Document Verification":

    st.header("Document Verification")

    st.write(
        "Set simulated verification statuses. "
        "No actual documents or external services are checked."
    )

    options = ["Pending", "Verified", "Failed", "Flagged"]

    with st.form("document_verification_form"):

        new_statuses = {}

        for document, current in (
            st.session_state.document_statuses.items()
        ):
            new_statuses[document] = st.selectbox(
                document,
                options,
                index=options.index(current),
                key=f"verify_{document}"
            )

        submitted = st.form_submit_button(
            "Save Verification Statuses",
            type="primary"
        )

    if submitted:
        try:
            save_document_statuses("MANUAL-DEMO", new_statuses)

            st.session_state.document_statuses = new_statuses
            st.session_state.assessment = None
            st.session_state.officer_decision = "Pending"
            st.session_state.officer_reason = ""

            st.success("Verification statuses saved for this demo session.")

        except Exception as error:
            st.error("Unable to save verification statuses to MySQL.")
            st.exception(error)

    st.subheader("Current Verification Summary")
    for document, status in st.session_state.document_statuses.items():
        if status == "Verified":
            st.success(f"{document}: {status}")
        elif status == "Pending":
            st.warning(f"{document}: {status}")
        else:
            st.error(f"{document}: {status}")

# =====================================================
# 10. AGENT ACTIVITY
# =====================================================

elif page == "Agent Activity":

    st.header("Agent Activity")

    workflow = [
        "Capture applicant information",
        "Check document verification statuses",
        "Apply illustrative loan policy rules",
        "Calculate repayment affordability",
        "Review simulated credit bureau data",
        "Explain findings and escalate blockers",
        "Hand off the case to a human credit officer"
    ]

    for i, step in enumerate(workflow, start=1):
        st.write(f"{i}. {step}")

    if st.session_state.assessment is None:
        st.info("Run an assessment to see its agent findings.")

    else:
        st.subheader("Latest Assessment Findings")

        for finding in st.session_state.assessment["findings"]:
            if isinstance(finding, dict):
                agent = finding["agent"]
                passed = finding["passed"]
                reason = finding["reason"]
                evidence = finding["evidence"]
                next_action = finding["next_action"]
            else:
                agent, passed, reason = finding
                evidence = "Run the assessment again to generate evidence details."
                next_action = "Review the finding with the supporting case information."

            icon = "✅" if passed else "⚠️"
            st.write(f"{icon} **{agent}:** {reason}")
            st.caption(f"Evidence: {evidence}")
            st.caption(f"Suggested next action: {next_action}")

    st.caption(
        "The workflow currently uses Python rules and simulated data. "
        "It is not connected to an LLM or live external APIs."
    )


# =====================================================
# 11. ABOUT
# =====================================================

else:

    st.header("About This Demo")

    st.write(
        "A prototype of an AI-assisted loan assessment workflow "
        "for a fictional retail bank."
    )

    st.write("Current capabilities:")
    st.write("- Synthetic portfolio of 100 applicants")
    st.write("- Portfolio dashboard and searchable records")
    st.write("- EMI and affordability calculations")
    st.write("- Simulated document verification")
    st.write("- Rule-based preliminary assessment")
    st.write("- Human credit officer review")
    st.write("- Fictional applicant data generated in Python, with verification statuses and officer decisions stored in the current Streamlit session. Data is not persistently stored in the hosted demo.")
    st.write("- CSV export for further analysis")

    st.warning(
        "All applicant records, verification results, rates and "
        "thresholds are illustrative. No real lending decision is made. "
        "'Ready for human review' does not mean approved."
    )
