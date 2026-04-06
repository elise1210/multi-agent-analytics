import requests

BASE_URL = "https://data.cityofnewyork.us/resource/erm2-nwe9.json"


def fetch_nyc_data(query: str, limit: int = 100):
    """
    Fetch NYC 311 noise complaint data
    """

    params = {
        "$limit": limit,
        "$where": "complaint_type LIKE '%Noise%'"
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        print("API failed")
        return []

    return response.json()


# ✅ TEST
if __name__ == "__main__":
    print("Running NYC API test...")

    data = fetch_nyc_data("noise complaints")

    print("Number of records:", len(data))

    if len(data) > 0:
        print("Sample record:", data[0])