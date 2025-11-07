import psycopg2
import pandas as pd
import streamlit as st

# Buat koneksi ke PostgreSQL Railway
def create_connection():
    try:
        conn = psycopg2.connect(st.secrets["postgres"]["url"])
        return conn
    except Exception as e:
        st.error(f"Error connecting to PostgreSQL: {e}")
        return None

# Eksekusi query (SELECT / INSERT / UPDATE / DELETE)
def run_query(query, params=None, fetch=True):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            if fetch:
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                return pd.DataFrame(rows, columns=columns)
            else:
                conn.commit()
                return None
        except Exception as e:
            st.error(f"Error executing query: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
    else:
        st.error("Failed to connect to the database.")
        return None


def init_db():
    """Membuat tabel users jika belum ada."""
    run_query("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            salt VARCHAR(32) NOT NULL,
            role VARCHAR(50) DEFAULT 'user'
        );
    """, fetch=False)


def init_db_reports():
    """Membuat tabel reports jika belum ada."""
    run_query("""
        CREATE TABLE IF NOT EXISTS reports (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            subject VARCHAR(255) NOT NULL,
            description TEXT,
            mode VARCHAR(50) NOT NULL,
            file_path VARCHAR(500),
            image_path VARCHAR(500),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """, fetch=False)
