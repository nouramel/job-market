import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def fetch_muse_jobs(max_pages=10):
    all_jobs = []
    for page in range(1, max_pages + 1):
        url = "https://www.themuse.com/api/public/jobs"
        params = {"page": page, "limit": 100}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            jobs = response.json().get("results", [])
            if not jobs:
                break
            all_jobs.extend(jobs)
            print(f"The Muse page {page}: {len(jobs)} jobs")
        else:
            break
    return all_jobs

def fetch_adzuna_jobs(app_id, app_key, max_pages=2):
    all_jobs = []
    keywords = [
        "developpeur", "data analyst", "product owner", "chef de projet",
        "marketing", "comptable", "infirmier", "commercial", "juriste",
        "ressources humaines", "ingenieur", "architecte", "medecin",
        "enseignant", "finance", "graphiste", "logisticien", "pharmacien",
        "consultant", "devops"
    ]
    
    for keyword in keywords:
        for page in range(1, max_pages + 1):
            url = f"https://api.adzuna.com/v1/api/jobs/fr/search/{page}"
            params = {
                "app_id": app_id,
                "app_key": app_key,
                "results_per_page": 50,
                "what": keyword
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                jobs = response.json().get("results", [])
                if not jobs:
                    break
                all_jobs.extend(jobs)
                print(f"Adzuna '{keyword}' page {page}: {len(jobs)} jobs")
            else:
                print(f"Adzuna '{keyword}' page {page}: erreur {response.status_code}")
                break
    return all_jobs

def save_to_json(data, filename):
    os.makedirs("data", exist_ok=True)
    with open(f"data/{filename}", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(data)} records to data/{filename}")

if __name__ == "__main__":
    print("Fetching from The Muse...")
    muse_jobs = fetch_muse_jobs(max_pages=10)
    save_to_json(muse_jobs, "muse_jobs.json")

    print("\nFetching from Adzuna France...")
    app_id = os.getenv("ADZUNA_APP_ID", "your_id")
    app_key = os.getenv("ADZUNA_APP_KEY", "your_key")
    adzuna_jobs = fetch_adzuna_jobs(app_id, app_key, max_pages=2)
    save_to_json(adzuna_jobs, "adzuna_jobs.json")

    print("\nDone!")