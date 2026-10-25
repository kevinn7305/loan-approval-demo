# Loan Approval Demo — Data & AI Presales Assessment

A Streamlit-based loan approval demonstration built with Python and fictional applicant data. The project showcases a loan assessment workflow, affordability analysis, simulated document verification, and human credit officer review.

## Features

- **Loan Portfolio Dashboard:** View portfolio metrics and applicant risk indicators.
- **Applicant Explorer:** Search and explore fictional loan applicants.
- **Loan Assessment:** Calculate EMI, evaluate affordability, and identify assessment blockers.
- **Document Verification:** Demonstrate simulated document status checks.
- **Agent Activity:** Review assessment findings and workflow activity.
- **Human-in-the-Loop Review:** Record an officer decision and rationale.
- **Supporting Pages:** Explore the approach story, architecture, FAQ, and contact information.

## Technology Stack

- Python
- Streamlit
- Pandas
- NumPy
- Plotly

## Run Locally

### 1. Prerequisites

Install Python and Git.

### 2. Clone the repository

```bash
git clone https://github.com/kevinn7305/loan-approval-demo.git
cd loan-approval-demo
```

### 3. Install dependencies

```bash
py -m pip install -r requirements.txt
```

### 4. Start the application

```bash
py -m streamlit run app.py
```

Open the local URL displayed in the terminal.

## Data and Storage

The hosted demonstration uses fictional applicant data generated in Python. In the hosted version, applicant data, document verification statuses, and officer decisions are managed through Streamlit session-based storage.

**Storage limitation:** Changes may reset when the session ends or a new session starts. The hosted version does not require MySQL credentials.

The original local version uses MySQL for persistent storage. The hosted version uses a separate storage implementation to avoid requiring database credentials during deployment.

## Architecture and AI Approach

The project demonstrates a loan assessment workflow using Python-based rules, affordability calculations, simulated verification checks, assessment findings, and human review.

The supporting architecture page distinguishes the current implementation from the proposed future architecture involving a consolidated data layer and agentic AI capabilities.

## Important Limitations

- All applicant records are fictional.
- Document verification is simulated.
- Assessment findings are generated using Python-based rules.
- The hosted version is not connected to a live banking system, BigQuery, external verification APIs, or a real LLM agent.
- The application does not independently make final lending decisions.
- Human credit officer review remains essential.

This project is an educational demonstration, not a production-ready lending system.

## Responsible Use

No real customer data, passwords, database credentials, or API keys should be committed to the repository.

## Project Purpose

The project demonstrates an understanding of loan assessment workflows, financial affordability, data processing, application development, human oversight, and the potential future application of AI in financial services.
