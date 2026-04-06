import pandas as pd


def analyze_data(data):
    """
    Perform EDA on NYC 311 data
    """

    if not data:
        return {"error": "No data"}

    df = pd.DataFrame(data)

    # Basic cleaning
    df = df.dropna(subset=["complaint_type", "borough"])

    # 1. Count total
    total_count = len(df)

    # 2. Top complaint types
    top_complaints = df["complaint_type"].value_counts().head(5).to_dict()

    # 3. Complaints by borough
    borough_counts = df["borough"].value_counts().to_dict()

    result = {
        "total_count": total_count,
        "top_complaints": top_complaints,
        "borough_distribution": borough_counts
    }

    return result


# ✅ TEST
if __name__ == "__main__":
    from app.tools.nyc_api import fetch_nyc_data

    data = fetch_nyc_data("noise complaints", 200)

    result = analyze_data(data)

    print("EDA Result:")
    print(result)