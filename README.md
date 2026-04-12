## NYC Noise Complaint Analytics Agent

Live Application

**Service URL:**
https://multi-agent-analytics-git-1018522235899.europe-west1.run.app

Health check:
https://multi-agent-analytics-git-1018522235899.europe-west1.run.app/health

Overview

This project implements a **multi-agent analytics system** that reproduces the first three steps of a real-world data analysis workflow:
	1.	Collect real-world data dynamically
	2.	Perform exploratory data analysis (EDA)
	3.	Generate a data-driven hypothesis 

The system analyzes NYC 311 noise complaint data using real-time API queries and produces structured analytical insights.

Architecture (Multi-Agent Pattern)

The system uses a pipeline (orchestrator-handoff) multi-agent design:
	•	Collect Agent (collect_agent.py, collect_data)
	•	EDA Agent (eda_agent.py, run_eda)
	•	Hypothesis Agent (hypothesis_agent.py, generate_hypothesis)

Orchestrated in app/main.py:
data = collect_data(query)
eda = run_eda(data)
answer = generate_hypothesis(eda, query)

## Step 1: **Collect (API Integration)**
	•	File: app/tools/nyc_api.py
	•	Function: fetch_nyc_data

Retrieves real-time data from NYC Open Data API.
Supports:
	•	last X days
	•	specific date
	•	between dates
	•	today / yesterday

## Step 2: **EDA (Tool Calling)**
	•	File: app/tools/python_eda.py
	•	Function: analyze_data

Uses pandas and matplotlib to compute and visualize:
	•	complaint distribution
	•	borough aggregation
	•	time trends (groupby)
	•	peak day#
	•	top vs second comparison
    • trend visualization (saved as images)
### Example Visualization

![Trend Example](assets/trend_example.png)

## Step 3: **Hypothesis (Data Memo)**
	•	File: app/agents/hypothesis_agent.py
	•	Function: generate_hypothesis

Outputs structured insights:
	•	Key Finding
	•	Supporting Evidence
	•	Trend Insight
	•	Interpretation


## Core Requirements

**Frontend** → frontend/index.html
**Tool Calling** → python_eda.py
**Non-trivial Data** → NYC Open Data API
**Multi-agent Pattern** → 3 agents (collect_agent.py / eda_agent.py / hypothesis_agent.py)
**Deployed** → Cloud Run URL above
**Agent Framework** → FastAPI (app/main.py)

Elective Features

Data visualization (matplotlib)
Dynamic query parsing
Data Memo style output

Summary

This system simulates a real analytics workflow:
	•	dynamic data retrieval
	•	programmatic analysis
	•	evidence-based reasoning

and produces structured, interpretable insights including visualization-based evidence.
