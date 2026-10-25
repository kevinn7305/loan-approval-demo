# Loan Approval Demo — Data & AI Presales Assessment

**A Streamlit-based loan assessment prototype built with Python and fictional applicant data.**

🚀 **[Launch Live Demo](https://loan-approval-demo-kevinn.streamlit.app)** | 💻 **[View Source Code on GitHub](https://github.com/kevinn7305/loan-approval-demo)**

🎥 **[Watch the Demo Recording](https://drive.google.com/file/d/1hXgaEyeBjZQItkISLfbAv3OMOo7P0EP8/view?usp=sharing)**

The project demonstrates a loan assessment workflow covering affordability analysis, simulated document verification, rule-based assessment findings, and human credit officer review.

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

## Live Application

**Live Demo:** https://loan-approval-demo-kevinn.streamlit.app

The application is deployed using Streamlit Community Cloud and uses fictional applicant data.

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

The hosted demonstration uses fictional applicant data generated in Python. Applicant data, document verification statuses, and officer decisions are managed through Streamlit session-based storage.

**Storage limitation:** Changes may reset when the session ends or a new session starts. The hosted version does not require MySQL credentials.

The original local implementation uses MySQL for persistent storage. The hosted implementation uses a separate session-based storage module to simplify deployment.

## Architecture and AI Approach

The prototype demonstrates a structured loan assessment workflow using Python-based rules, affordability calculations, simulated verification checks, assessment findings, and human review.

The supporting architecture and approach-story pages describe the current implementation and a proposed future architecture involving consolidated data infrastructure and agentic AI capabilities.

The current hosted application **does not use a live LLM agent**. Its assessment findings are generated using Python-based rules, with simulated checks and human oversight.

## Important Limitations

- All applicant records are fictional.
- Document verification is simulated.
- Assessment findings are generated using Python-based rules.
- The hosted version is not connected to a live banking system, BigQuery, or external verification APIs.
- No real LLM agent is integrated into the hosted application.
- The application does not independently make final lending decisions.
- Human credit officer review remains essential.
- Session-based changes are not guaranteed to persist across sessions.

This project is an educational demonstration, not a production-ready lending system.

## Responsible Use

No real customer data, passwords, database credentials, or API keys should be committed to the repository.

## Project Purpose

This project demonstrates an understanding of loan assessment workflows, financial affordability, data processing, application development, human oversight, and potential future applications of AI in financial services.
