import psycopg2
import json
from dotenv import load_dotenv

load_dotenv()

def load_muse_jobs():
    with open("data/muse_jobs.json", "r", encoding="utf-8") as f:
        jobs = json.load(f)
    
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="job_market",
        user="admin",
        password="admin123"
    )
    cursor = conn.cursor()

    for job in jobs:
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

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Loaded {len(jobs)} jobs from The Muse")

def load_adzuna_jobs():
    with open("data/adzuna_jobs.json", "r", encoding="utf-8") as f:
        jobs = json.load(f)
    
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="job_market",
        user="admin",
        password="admin123"
    )
    cursor = conn.cursor()

    for job in jobs:
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
    print(f"Loaded {len(jobs)} jobs from Adzuna")

if __name__ == "__main__":
    load_muse_jobs()
    load_adzuna_jobs()
    print("All jobs loaded!")