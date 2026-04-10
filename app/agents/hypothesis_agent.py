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

    # Get top complaint
    if top:
        top_complaint = max(top, key=top.get)
        top_value = top[top_complaint]
    else:
        top_complaint = "Unknown"
        top_value = 0

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
    clean_complaint = top_complaint.replace("Noise - ", "").lower()
    extra_info = KNOWLEDGE_BASE.get(top_complaint.lower(), "")

    # Intent detection
    # Only use intent logic in API mode
    if mode == "api":
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

        # =========================
        # CASE 1: Borough question
        # =========================
        if intent == "borough":
            return f"""
    📊 Answer
    The borough with the highest number of noise complaints is **{top_borough}**.

    📌 Evidence
    - {top_borough}: {borough_value} complaints ({borough_pct:.1f}% of total)

    💡 Insight
    This suggests that noise complaints are most concentrated in {top_borough}, 
    reflecting localized urban activity patterns.
    """

        # =========================
        # CASE 2: Complaint type question
        # =========================
        elif intent == "complaint":
            return f"""
        📊 Answer
        The most common type of noise complaint is **{top_complaint}**.

        📌 Evidence
        - {top_complaint}: {top_value} complaints ({top_pct:.1f}% of total)

        📌 Context
        {extra_info}

        💡 Insight
        This indicates that {clean_complaint} is the dominant noise issue in the dataset.

        ---

        📊 Additional Context
        - Total complaints analyzed: {total}
        - Borough with highest complaints: {top_borough} ({borough_value} cases, {borough_pct:.1f}%)
        """

        # =========================
        # CASE 3: Trend question
        # =========================
        elif intent == "trend":
            if trend:
                dates = list(trend.keys())
                values = list(trend.values())

                if len(values) >= 2:
                    return f"""
    📅 Trend Analysis
    Complaint volume changed from {values[0]} to {values[-1]} between {dates[0]} and {dates[-1]}.

    💡 Insight
    This suggests short-term variation in noise reporting behavior.
    """
        
        return "Trend data is not available for this query."



    # Build hypothesis
    hypothesis = f"""
    📊 Analysis Summary
    - Total complaints analyzed: {total}
    - Most common complaint: {top_complaint} ({top_value} cases, {top_pct:.1f}%)
    - Borough with highest complaints: {top_borough} ({borough_value} cases, {borough_pct:.1f}%)

    💡 Key Insight
    The data shows a strong concentration of complaints in {top_borough}, where 
    {clean_complaint} alone accounts for a significant share of all reported issues. 
    This indicates that complaint patterns are not evenly distributed, but instead 
    dominated by specific categories and geographic areas.

    📈 Interpretation
    The dominance of {clean_complaint} suggests localized environmental or behavioral 
    factors driving complaint frequency. In {top_borough}, higher population density, 
    urban infrastructure, and activity patterns likely contribute to elevated noise levels.

    📌 Supporting Evidence
    - {top_complaint} accounts for {top_pct:.1f}% of all complaints
    - {top_borough} contributes {borough_pct:.1f}% of total complaints
    """

    if trend:
        dates = list(trend.keys())
        values = list(trend.values())

        if len(values) >= 2:
            hypothesis += f"\n📅 Temporal Insight\nComplaint volume changed from {values[0]} to {values[-1]} between {dates[0]} and {dates[-1]}, indicating short-term variation in reporting activity."

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