import psycopg2
from psycopg2 import sql

def init_db():
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="job_market",
        user="admin",
        password="admin123"
    )
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id SERIAL PRIMARY KEY,
            source VARCHAR(50),
            title VARCHAR(255),
            company VARCHAR(255),
            location VARCHAR(255),
            description TEXT,
            url TEXT,
            salary_min FLOAT,
            salary_max FLOAT,
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()