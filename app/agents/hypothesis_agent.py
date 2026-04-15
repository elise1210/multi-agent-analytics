def generate_hypothesis(eda_result, query, mode="api"):
    """
    Generate hypothesis based on EDA results
    """
    query = query.lower()

    KNOWLEDGE_BASE = {
    "noise - residential": "Commonly caused by loud music, parties, or neighbor disturbances.",
    "noise - street": "Often related to traffic, construction, or public activity.",
    "noise - commercial": "Usually comes from businesses such as bars, restaurants, or shops.",
    "noise - vehicle": "Associated with car horns, engines, or traffic congestion."
    }
    if "error" in eda_result:
        return "Unable to generate hypothesis due to data issue."

    total = eda_result.get("total_count", 0)
    top = eda_result.get("top_complaints", {})
    borough = eda_result.get("borough_distribution", {})
    trend = eda_result.get("daily_trend", {})

    peak_day = eda_result.get("peak_day", None)
    peak_value = eda_result.get("peak_value", 0)

    # Get top complaint
    if top:
        top_complaint = max(top, key=top.get)
        top_value = top[top_complaint]
    else:
        top_complaint = "Unknown"
        top_value = 0

    # Method 1: compare with second highest
    if len(top) > 1:
        sorted_items = sorted(top.items(), key=lambda x: x[1], reverse=True)
        second_complaint, second_value = sorted_items[1]
        gap = top_value - second_value
    else:
        second_complaint = "Unknown"
        second_value = 0
        gap = 0

    # Get top borough
    if borough:
        top_borough = max(borough, key=borough.get)
        borough_value = borough[top_borough]
    else:
        top_borough = "Unknown"
        borough_value = 0
    # Percentages
    top_pct = (top_value / total * 100) if total > 0 else 0
    borough_pct = (borough_value / total * 100) if total > 0 else 0

    # Clean text
    #clean_complaint = top_complaint.replace("Noise - ", "").lower()
    extra_info = KNOWLEDGE_BASE.get(top_complaint.lower(), "")

    # Intent detection

    # Only use intent logic in API mode
    
    intent = "general"

    if "borough" in query:
        intent = "borough"

    elif "type" in query or "kind" in query:
        intent = "complaint"

    elif "trend" in query or "time" in query or "change" in query:
        intent = "trend"

    # time-based queries should ALSO trigger trend
    elif "last" in query or "days" in query or "week" in query or "month" in query:
        intent = "trend"

    # Dynamic Key Insight

    if intent == "borough":
        key_insight = f"""Because {top_borough} accounts for {borough_pct:.1f}% of all complaints, noise reports are geographically concentrated rather than evenly distributed.
    """
    elif intent == "complaint":
        key_insight = f"""Because {top_complaint} accounts for {top_pct:.1f}% of all complaints and exceeds {second_complaint} by {gap} cases, complaints are highly concentrated in a single category.
    """
    elif intent == "trend":
        key_insight = f"""Complaint activity shows noticeable variation over time rather than remaining stable.
    """
    else:
        key_insight = f"""Noise complaints show uneven distribution across categories and locations.
    """


    # Dynamic Interpretation

    if intent == "borough":
        interpretation = """This suggests that complaint activity is not evenly distributed across locations, indicating localized concentration of noise issues."""

    elif intent == "complaint":
        interpretation = "This suggests that a single source is disproportionately driving complaints rather than a balanced mix of noise types."

        if extra_info:
            interpretation += f" This aligns with known patterns where {extra_info.lower()}"

    elif intent == "trend":
        interpretation = """This indicates short-term fluctuations in reporting activity rather than a stable long-term trend."""

    else:
        interpretation = """This reflects underlying variation in how complaints are distributed across the dataset."""

    # Build unified Data Memo

    hypothesis = f"""
    📊 Analysis Summary
    - Total complaints analyzed: {total}
    - Most common complaint: {top_complaint} ({top_value} cases, {top_pct:.1f}%)
    - Borough with highest complaints: {top_borough} ({borough_value} cases, {borough_pct:.1f}%)

    💡 Key Insight
    {key_insight.strip()}

    📈 Interpretation
    {interpretation.strip()}

    📌 Supporting Evidence
    - {top_complaint}: {top_value} cases ({top_pct:.1f}%)
    - {top_borough}: {borough_value} cases ({borough_pct:.1f}%)
    - Difference vs {second_complaint}: {gap} cases
    """

    # Add trend evidence
    if trend and len(trend)>0:
        dates = list(trend.keys())
        values = list(trend.values())

        if len(values) >= 2:
            hypothesis += f"""

    📅 Temporal Evidence
    Complaint volume changed from {values[0]} to {values[-1]} between {dates[0]} and {dates[-1]}.
    """
            if peak_day:
                hypothesis += f"\nPeak occurred on {peak_day} with {peak_value} cases."


    return hypothesis


# Test
if __name__ == "__main__":
    from app.agents.eda_agent import run_eda
    from app.agents.collect_agent import collect_data

    query = "how does noise trend change"
    data = collect_data(query)
    eda = run_eda(data)

    hypothesis = generate_hypothesis(eda, query, mode="api")

    print(hypothesis)