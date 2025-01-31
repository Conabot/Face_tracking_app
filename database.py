import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgres://your_postgres_url")

def connect_db():
    return psycopg2.connect(DATABASE_URL)

def create_table():
    """Creates table to store face encodings."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS faces (
            id SERIAL PRIMARY KEY,
            name TEXT,
            encoding BYTEA
        )
    """)
    conn.commit()
    conn.close()
