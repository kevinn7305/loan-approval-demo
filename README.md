# Loan Approval Demo

A Streamlit demonstration of a loan assessment workflow using Python, MySQL, fictional applicant data, and rule-based checks.

## Features

- Loan portfolio dashboard and applicant exploration
- EMI and affordability assessment
- Simulated document verification
- Preliminary recommendations with reasons
- Human credit officer decisions and rationale
- CSV export and supporting architecture pages

## Technology

Python, Streamlit, MySQL, Pandas, NumPy, and Plotly.

## Run Locally

1. Install Python and MySQL Server.
2. Create a MySQL database named `loan_approval_demo`.
3. Configure your own MySQL connection details in `.streamlit/secrets.toml` using the structure documented in the database setup instructions.
4. Install dependencies:

   `py -m pip install -r requirements.txt`

5. Start the app:

   `py -m streamlit run app.py`

## Important Limitations

The application uses fictional data, Python-based rules, and simulated checks. It is not connected to a live banking system, BigQuery, external verification APIs, or an autonomous LLM agent. All lending recommendations require human review.

Never publish database credentials or real customer data.
