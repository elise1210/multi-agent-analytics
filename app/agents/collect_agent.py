from app.tools.nyc_api import fetch_nyc_data


def collect_data(query: str):
    data = fetch_nyc_data(query)
    return data


if __name__ == "__main__":
    data = collect_data("noise complaints")
    print("Collected:", len(data))