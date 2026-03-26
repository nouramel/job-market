from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import json
import psycopg2
import os

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def fetch_and_load_jobs():
    # Fetch from The Muse
    url = "https://www.themuse.com/api/public/jobs"
    response = requests.get(url, params={"page": 1, "limit": 100})
    muse_jobs = response.json().get("results", []) if response.status_code == 200 else []

    # Fetch from Adzuna
    app_id = os.getenv("ADZUNA_APP_ID", "")
    app_key = os.getenv("ADZUNA_APP_KEY", "")
    adzuna_url = f"https://api.adzuna.com/v1/api/jobs/gb/search/1"
    adzuna_response = requests.get(adzuna_url, params={
        "app_id": app_id,
        "app_key": app_key,
        "results_per_page": 50,
        "what": "data engineer"
    })
    adzuna_jobs = adzuna_response.json().get("results", []) if adzuna_response.status_code == 200 else []

    # Load to PostgreSQL
    conn = psycopg2.connect(
        host="postgres",
        port="5432",
        database="job_market",
        user="admin",
        password="admin123"
    )
    cursor = conn.cursor()

    for job in muse_jobs:
        location = job.get("locations", [{}])
        location_name = location[0].get("name", "Unknown") if location else "Unknown"
        cursor.execute("""
            INSERT INTO jobs (source, title, company, location, url)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """, (
            "the_muse",
            job.get("name", ""),
            job.get("company", {}).get("name", ""),
            location_name,
            job.get("refs", {}).get("landing_page", "")
        ))

    for job in adzuna_jobs:
        cursor.execute("""
            INSERT INTO jobs (source, title, company, location, description, url, salary_min, salary_max)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """, (
            "adzuna",
            job.get("title", ""),
            job.get("company", {}).get("display_name", ""),
            job.get("location", {}).get("display_name", ""),
            job.get("description", ""),
            job.get("redirect_url", ""),
            job.get("salary_min", None),
            job.get("salary_max", None)
        ))

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Loaded {len(muse_jobs)} Muse jobs and {len(adzuna_jobs)} Adzuna jobs")

with DAG(
    'job_market_etl',
    default_args=default_args,
    description='ETL pipeline for job market data',
    schedule_interval='@daily',
    start_date=datetime(2026, 1, 1),
    catchup=False,
) as dag:

    fetch_load_task = PythonOperator(
        task_id='fetch_and_load_jobs',
        python_callable=fetch_and_load_jobs,
    )