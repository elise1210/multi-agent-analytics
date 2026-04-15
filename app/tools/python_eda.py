import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import time  
import re
from datetime import datetime, timedelta

def analyze_data(data, query=None):
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

        # group first
        trend_series = df.groupby(df["created_date"].dt.date).size()

        end_date = datetime.now().date()
        start_date = None

        match = re.search(r"last (\d+) days", query or "")
        if match:
            days = int(match.group(1))
            start_date = end_date - timedelta(days=days)

        range_match = re.search(
            r"between (\d{4})[.\-/](\d{1,2})[.\-/](\d{1,2}) and (\d{4})[.\-/](\d{1,2})[.\-/](\d{1,2})",
            query or ""
        )
        if range_match:
            y1, m1, d1, y2, m2, d2 = range_match.groups()
            start_date = datetime(int(y1), int(m1), int(d1)).date()
            end_date   = datetime(int(y2), int(m2), int(d2)).date()

        elif "today" in (query or ""):
            start_date = end_date

        elif "yesterday" in (query or ""):
            start_date = end_date - timedelta(days=1)
            end_date = start_date

        if start_date is None:
            start_date = trend_series.index.min()
            end_date = trend_series.index.max()

        full_range = pd.date_range(start=start_date, end=end_date)

        trend_series = trend_series.reindex(full_range.date, fill_value=0)

        daily_counts = trend_series.to_dict()
        

        if daily_counts:
            peak_day = max(daily_counts, key=daily_counts.get)
            peak_value = daily_counts[peak_day]

            # ✅ only plot if >= 2 days
            if len(daily_counts) >= 2:
                dates = list(daily_counts.keys())
                values = list(daily_counts.values())

                filename = f"trend_{int(time.time())}.png"
                filepath = f"app/static/{filename}"

                plt.figure(figsize=(10, 4))
                plt.plot(dates, values, marker='o', linewidth=2)
                plt.grid(True, linestyle='--', alpha=0.5)
                if peak_day in dates:
                    peak_index = dates.index(peak_day)

                    plt.scatter(
                        dates[peak_index],
                        values[peak_index],
                        color='red',
                        s=80,
                        zorder=5,
                        label='Peak'
                    )

                    plt.annotate(
                        f"{peak_value}",
                        (dates[peak_index], values[peak_index]),
                        textcoords="offset points",
                        xytext=(0,10),
                        ha='center',
                        fontsize=9,
                        color='red'
                    )

                if len(dates) > 0:
                    plt.title(f"Noise Complaints Trend ({dates[0]} → {dates[-1]})")
                else:
                    plt.title("Noise Complaints Trend")

                plt.xlabel("Date")
                plt.ylabel("Number of Complaints")

                plt.xticks(rotation=45)

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