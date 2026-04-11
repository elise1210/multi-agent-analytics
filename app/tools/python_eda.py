import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import time  

def analyze_data(data):
    """
    Perform EDA on NYC 311 data
    """
    filename = None
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

    # 4. Time trend
    if "created_date" in df.columns:
        df["created_date"] = pd.to_datetime(df["created_date"], errors="coerce")
        df = df.dropna(subset=["created_date"])

        daily_counts = (
            df.groupby(df["created_date"].dt.date)
            .size()
            .sort_index()
            .to_dict()
        )

        if daily_counts:
            peak_day = max(daily_counts, key=daily_counts.get)
            peak_value = daily_counts[peak_day]

            # ✅ only plot if >= 2 days
            if len(daily_counts) >= 2:
                dates = list(daily_counts.keys())
                values = list(daily_counts.values())

                filename = f"trend_{int(time.time())}.png"
                filepath = f"app/static/{filename}"

                plt.figure()
                plt.plot(dates, values)
                plt.xticks(rotation=45)
                plt.title("Noise Complaints Trend")
                plt.tight_layout()

                plt.savefig(filepath)
                plt.close()
            else:
                filename = None  # if single day no plot

        else:
            peak_day = None
            peak_value = 0
            filename = None

    else:
        daily_counts = {}
        peak_day = None
        peak_value = 0
        filename = None

    result = {
        "total_count": total_count,
        "top_complaints": top_complaints,
        "borough_distribution": borough_counts,
        "daily_trend": daily_counts,
        "peak_day": peak_day,
        "peak_value": peak_value,
        "plot": filename 
    }

    return result


# TEST
if __name__ == "__main__":
    from app.tools.nyc_api import fetch_nyc_data

    data = fetch_nyc_data("noise complaints", 200)

    result = analyze_data(data)

    print("EDA Result:")
    print(result)