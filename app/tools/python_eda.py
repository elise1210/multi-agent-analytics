import pandas as pd


def analyze_data(data):
    """
    Perform EDA on NYC 311 data
    """

    if not data:
        return {"error": "No data"}

    df = pd.DataFrame(data)

    # check required columns
    required_cols = ["complaint_type", "borough"]

    for col in required_cols:
        if col not in df.columns:
            return {"error": f"Missing column: {col}"}

    # cleaning
    df = df.dropna(subset=required_cols)

    # 1. Total count
    total_count = len(df)

    # 2. Top complaint types
    top_complaints = df["complaint_type"].value_counts().head(5).to_dict()

    # 3. Borough distribution
    borough_counts = df["borough"].value_counts().to_dict()

    # 4. Time trend (strong addition)
    if "created_date" in df.columns:
        df["created_date"] = pd.to_datetime(df["created_date"], errors="coerce")
        df = df.dropna(subset=["created_date"])

        daily_counts = df.groupby(df["created_date"].dt.date).size().to_dict()
    else:
        daily_counts = {}

    result = {
        "total_count": total_count,
        "top_complaints": top_complaints,
        "borough_distribution": borough_counts,
        "daily_trend": daily_counts
    }

    return result


# TEST
if __name__ == "__main__":
    from app.tools.nyc_api import fetch_nyc_data

    data = fetch_nyc_data("noise complaints", 200)

    result = analyze_data(data)

    print("EDA Result:")
    print(result)