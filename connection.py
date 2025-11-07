import mysql.connector
from mysql.connector import Error
import pandas as pd
import streamlit as st

# Initialize connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host=st.secrets["mysql"]["host"],
            user=st.secrets["mysql"]["user"],
            password=st.secrets["mysql"]["password"],
            database=st.secrets["mysql"]["database"],
            port=st.secrets["mysql"]["port"]
        )
        return connection
    except Error as e:
        st.error(f"Error connecting to MySQL: {e}")
        return None

# Perform query
def run_query(query, params=None, fetch=True):
    """
    Runs a SQL query with optional parameters.
    
    - `query`: The SQL query string.
    - `params`: Optional parameters to be passed with the query.
    - `fetch`: If True, fetches results (used for SELECT queries).
    """
    conn = create_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # For SELECT queries, fetch results
            if fetch:
                result = cursor.fetchall()
                return pd.DataFrame(result) if result else pd.DataFrame()
            
            # For INSERT, UPDATE, DELETE queries
            else:
                conn.commit()
                return None
        except mysql.connector.Error as e:
            st.error(f"Error executing query: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
    else:
        st.error("Failed to connect to the database.")
        return None
    
def init_db():
    """
    Membuat tabel users jika belum ada.
    """
    run_query("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        salt VARCHAR(32) NOT NULL,
        role VARCHAR(50) DEFAULT 'user'
    );
    """, fetch=False)

def init_db_reports():
    """
    Membuat tabel reports jika belum ada.
    """
    run_query("""
    CREATE TABLE IF NOT EXISTS reports (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        subject VARCHAR(255) NOT NULL,
        description TEXT,
        mode VARCHAR(50) NOT NULL,
        file_path VARCHAR(500),
        image_path VARCHAR(500),
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """, fetch=False)
