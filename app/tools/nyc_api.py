import requests
from datetime import datetime, timedelta
import re

BASE_URL = "https://data.cityofnewyork.us/resource/erm2-nwe9.json"


def fetch_nyc_data(query: str, limit: int = 20000):
    query = query.lower()

    complaint_filter = "complaint_type LIKE '%Noise%'"
    time_filter = None

    # priority: between > specific date > last X days > fallback
    # between
    range_match = re.search(
        r"between (\d{4})[.\-/](\d{1,2})[.\-/](\d{1,2}) and (\d{4})[.\-/](\d{1,2})[.\-/](\d{1,2})",
        query
    )

    # specific date
    date_match = re.search(r"(\d{4})[.\-/](\d{1,2})[.\-/](\d{1,2})", query)
    # today / yesterday
    today_match = "today" in query
    yesterday_match = "yesterday" in query
    # last X days
    match = re.search(r"last (\d+) days", query)


    if range_match:
        y1, m1, d1, y2, m2, d2 = range_match.groups()

        start = f"{y1}-{int(m1):02d}-{int(d1):02d}T00:00:00"
        end   = f"{y2}-{int(m2):02d}-{int(d2):02d}T23:59:59"

        time_filter = f"created_date >= '{start}' AND created_date <= '{end}'"

    elif today_match:
        today = datetime.now().strftime("%Y-%m-%d")
        start = f"{today}T00:00:00"
        end   = f"{today}T23:59:59"

        time_filter = f"created_date >= '{start}' AND created_date <= '{end}'"

    elif yesterday_match:
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        start = f"{yesterday}T00:00:00"
        end   = f"{yesterday}T23:59:59"

        time_filter = f"created_date >= '{start}' AND created_date <= '{end}'"


    elif date_match:
        year, month, day = date_match.groups()

        start = f"{year}-{int(month):02d}-{int(day):02d}T00:00:00"
        end   = f"{year}-{int(month):02d}-{int(day):02d}T23:59:59"

        time_filter = f"created_date >= '{start}' AND created_date <= '{end}'"

    elif match:
        days = int(match.group(1))
        date = datetime.now() - timedelta(days=days)

        time_filter = f"created_date >= '{date.strftime('%Y-%m-%dT%H:%M:%S')}'"

    elif "trend" in query or "change" in query:
        date = datetime.now() - timedelta(days=30)

        time_filter = f"created_date >= '{date.strftime('%Y-%m-%dT%H:%M:%S')}'"
    

    if time_filter:
        where_clause = f"{complaint_filter} AND {time_filter}"
    else:
        where_clause = complaint_filter

    all_data = []
    offset = 0
    batch_size = 1000

    while True:
        params = {
            "$limit": batch_size,
            "$offset": offset,
            "$where": where_clause,
            "$order": "created_date DESC"   
        }

        response = requests.get(BASE_URL, params=params)

        if response.status_code != 200:
            print("API failed")
            break

        batch = response.json()

        if not batch:
            break

        all_data.extend(batch)
        offset += batch_size

        if len(all_data) >= limit:
            break
        if offset > 50000:
            break

    return all_data[:limit]


# TEST
if __name__ == "__main__":
    print("Running NYC API test...")

    data = fetch_nyc_data("noise complaints last 7 days")

    print("Number of records:", len(data))

    if len(data) > 0:
        print("Sample record:", data[0])