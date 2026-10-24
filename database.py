
import json
import streamlit as st
import mysql.connector
import pandas as pd


def get_connection():
    return mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        port=int(st.secrets["mysql"]["port"]),
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"],
    )


def initialize_tables():
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS applicants (
                applicant_id INT AUTO_INCREMENT PRIMARY KEY,
                applicant_data JSON NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS document_verifications (
                application_id VARCHAR(100) PRIMARY KEY,
                statuses JSON NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    ON UPDATE CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS officer_decisions (
                application_id VARCHAR(100) PRIMARY KEY,
                decision VARCHAR(100) NOT NULL,
                rationale TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    ON UPDATE CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        cursor.close()

    finally:
        conn.close()


def save_applicants_if_empty(df):
    initialize_tables()

    conn = get_connection()

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM applicants")
        count = cursor.fetchone()[0]

        if count == 0:
            sql = """
                INSERT INTO applicants (applicant_data)
                VALUES (%s)
            """

            records = [
                (
                    json.dumps(
                        record,
                        default=str,
                        ensure_ascii=False
                    ),
                )
                for record in df.to_dict(orient="records")
            ]

            cursor.executemany(sql, records)
            conn.commit()

        cursor.close()

    finally:
        conn.close()


def load_applicants():
    initialize_tables()

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT applicant_data
            FROM applicants
            ORDER BY applicant_id
        """)

        rows = cursor.fetchall()
        cursor.close()

        if not rows:
            return None

        records = []

        for row in rows:
            value = row[0]

            if isinstance(value, (bytes, bytearray)):
                value = value.decode("utf-8")

            if isinstance(value, dict):
                record = value
            else:
                record = json.loads(value)

            records.append(record)

        return pd.DataFrame(records)

    finally:
        conn.close()


def save_document_statuses(application_id, statuses):
    initialize_tables()

    conn = get_connection()

    try:
        cursor = conn.cursor()

        sql = """
            INSERT INTO document_verifications
                (application_id, statuses)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE
                statuses = VALUES(statuses)
        """

        cursor.execute(
            sql,
            (
                str(application_id),
                json.dumps(statuses, ensure_ascii=False),
            ),
        )

        conn.commit()
        cursor.close()

    finally:
        conn.close()


def load_document_statuses(application_id):
    initialize_tables()

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT statuses
            FROM document_verifications
            WHERE application_id = %s
            """,
            (str(application_id),),
        )

        row = cursor.fetchone()
        cursor.close()

        if row is None:
            return None

        value = row[0]

        if isinstance(value, (bytes, bytearray)):
            value = value.decode("utf-8")

        if isinstance(value, dict):
            return value

        if isinstance(value, str):
            return json.loads(value)

        raise ValueError(
            "Unexpected format for saved document statuses."
        )

    finally:
        conn.close()


def save_officer_decision(application_id, decision, rationale):
    """Save or update a human credit officer's decision in MySQL."""
    initialize_tables()
    conn = get_connection()

    try:
        cursor = conn.cursor()
        sql = """
            INSERT INTO officer_decisions
                (application_id, decision, rationale)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE
                decision = VALUES(decision),
                rationale = VALUES(rationale)
        """
        cursor.execute(
            sql,
            (str(application_id), str(decision), str(rationale)),
        )
        conn.commit()
        cursor.close()
    finally:
        conn.close()


def load_officer_decision(application_id):
    """Load the most recently saved officer decision from MySQL."""
    initialize_tables()
    conn = get_connection()

    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT decision, rationale
            FROM officer_decisions
            WHERE application_id = %s
            """,
            (str(application_id),),
        )
        row = cursor.fetchone()
        cursor.close()

        if row is None:
            return None

        return {
            "decision": row[0],
            "rationale": row[1],
        }
    finally:
        conn.close()
