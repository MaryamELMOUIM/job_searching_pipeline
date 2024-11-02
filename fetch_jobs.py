import os
import requests
import logging

logging.basicConfig(level=logging.INFO)

def fetch_jobs(keyword, location=None):
    api_key = os.getenv("JOOBLE_API_KEY")  # Fetch from environment variables
    if not api_key:
        raise ValueError("API key is missing. Make sure JOOBLE_API_KEY is set in the .env file.")

    api_endpoint = f"https://jooble.org/api/{api_key}"
    headers = {"Content-Type": "application/json"}
    query_params = {"keywords": keyword}
    if location:
        query_params["location"] = location

    try:
        response = requests.post(api_endpoint, json=query_params, headers=headers)
        response.raise_for_status()
        data = response.json()
        logging.info("Fetched jobs: %s", data)
        return data.get("jobs", []) if response.status_code == 200 else []
    except requests.exceptions.RequestException as e:
        logging.error("Error fetching jobs: %s", e)
        return []
