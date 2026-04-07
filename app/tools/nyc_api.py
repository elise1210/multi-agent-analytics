import requests
from datetime import datetime, timedelta

BASE_URL = "https://data.cityofnewyork.us/resource/erm2-nwe9.json"


def fetch_nyc_data(query: str, limit: int = 1000):
    """
    Fetch NYC 311 noise complaint data dynamically
    """

    query = query.lower()

    # Default filter (noise)
    complaint_filter = "complaint_type LIKE '%Noise%'"

    # Default time (recent baseline)
    time_filter = None

    # Dynamic time handling
    if "last 7 days" in query:
        date = datetime.now() - timedelta(days=7)
        time_filter = f"created_date >= '{date.strftime('%Y-%m-%dT%H:%M:%S')}'"

    elif "last 30 days" in query:
        date = datetime.now() - timedelta(days=30)
        time_filter = f"created_date >= '{date.strftime('%Y-%m-%dT%H:%M:%S')}'"

    elif "2023" in query:
        time_filter = (
            "created_date >= '2023-01-01T00:00:00' AND "
            "created_date <= '2023-12-31T23:59:59'"
        )

    # Combine filters
    if time_filter:
        where_clause = f"{complaint_filter} AND {time_filter}"
    else:
        where_clause = complaint_filter
    
    params = {
        "$limit": limit,
        "$where": where_clause,
        "$order": "created_date DESC"
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        print("API failed")
        return []

    return response.json()


# TEST
if __name__ == "__main__":
    print("Running NYC API test...")

    data = fetch_nyc_data("noise complaints last 7 days")

    print("Number of records:", len(data))

    if len(data) > 0:
        print("Sample record:", data[0])