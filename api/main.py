from fastapi import FastAPI, Query
from typing import Optional
import psycopg2
import psycopg2.extras
import os

app = FastAPI(title="Job Market API", version="1.0.0")

def get_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "job_market"),
        user=os.getenv("DB_USER", "admin"),
        password=os.getenv("DB_PASSWORD", "admin123")
    )

@app.get("/")
def root():
    return {"message": "Job Market API is running!"}

@app.get("/jobs")
def get_jobs(
    source: Optional[str] = None,
    company: Optional[str] = None,
    location: Optional[str] = None,
    limit: int = 20
):
    conn = get_db()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    query = "SELECT * FROM jobs WHERE 1=1"
    params = []
    
    if source:
        query += " AND source = %s"
        params.append(source)
    if company:
        query += " AND company ILIKE %s"
        params.append(f"%{company}%")
    if location:
        query += " AND location ILIKE %s"
        params.append(f"%{location}%")
    
    query += " LIMIT %s"
    params.append(limit)
    
    cursor.execute(query, params)
    jobs = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return {"total": len(jobs), "jobs": [dict(j) for j in jobs]}

@app.get("/stats")
def get_stats():
    conn = get_db()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    cursor.execute("SELECT source, COUNT(*) as count FROM jobs GROUP BY source")
    by_source = cursor.fetchall()
    
    cursor.execute("SELECT company, COUNT(*) as count FROM jobs GROUP BY company ORDER BY count DESC LIMIT 10")
    top_companies = cursor.fetchall()
    
    cursor.execute("SELECT location, COUNT(*) as count FROM jobs GROUP BY location ORDER BY count DESC LIMIT 10")
    top_locations = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return {
        "by_source": [dict(r) for r in by_source],
        "top_companies": [dict(r) for r in top_companies],
        "top_locations": [dict(r) for r in top_locations]
    }

@app.get("/recommend")
def recommend_jobs(
    skills: str = Query(..., description="Comma-separated skills, e.g. python,sql,docker"),
    location: Optional[str] = None,
    limit: int = 10
):
    conn = get_db()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    skill_list = [s.strip().lower() for s in skills.split(",")]
    
    query = "SELECT * FROM jobs WHERE 1=1"
    params = []
    
    if skill_list:
        conditions = " OR ".join(["LOWER(description) LIKE %s OR LOWER(title) LIKE %s" for _ in skill_list])
        query += f" AND ({conditions})"
        for skill in skill_list:
            params.extend([f"%{skill}%", f"%{skill}%"])
    
    if location:
        query += " AND location ILIKE %s"
        params.append(f"%{location}%")
    
    query += " LIMIT %s"
    params.append(limit)
    
    cursor.execute(query, params)
    jobs = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return {"skills": skill_list, "total": len(jobs), "recommendations": [dict(j) for j in jobs]}