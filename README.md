## NYC Noise Complaint Analytics Agent

Live Application

**Service URL:**
https://multi-agent-analytics-git-1018522235899.europe-west1.run.app

Health check:
https://multi-agent-analytics-git-1018522235899.europe-west1.run.app/health

## Overview

This project implements a **multi-agent analytics system** that reproduces the first three steps of a real-world data analysis workflow:

1. Collect real-world data dynamically
2. Perform exploratory data analysis (EDA)
3. Generate a data-driven hypothesis 

The system analyzes NYC 311 noise complaint data using real-time API queries and produces structured analytical insights.

## Architecture (Multi-Agent Pattern)

The system uses a pipeline (orchestrator-handoff) multi-agent design:

- Collect Agent (collect_agent.py, collect_data)
- EDA Agent (eda_agent.py, run_eda)
- Hypothesis Agent (hypothesis_agent.py, generate_hypothesis)

Orchestrated in app/main.py:

data = collect_tool.func(query)

eda = eda_tool.func(data, query)

answer = hypothesis_tool.func(eda, query, mode="api")

## Project Structure
```text
multi-agent-analytics/
│
├── app/
│   ├── main.py                  # FastAPI entrypoint (orchestration)
│   ├── agents/
│   │   ├── collect_agent.py     # Data collection agent
│   │   ├── eda_agent.py         # EDA agent
│   │   └── hypothesis_agent.py  # Hypothesis agent
│   │
│   ├── tools/
│   │   ├── nyc_api.py           # NYC Open Data API integration
│   │   └── python_eda.py        # Pandas + matplotlib analysis
│   │
│   └── static/                 # Generated visualization files
│
├── frontend/
│   └── index.html              # Frontend UI
│
├── assets/
│   └── trend_example.png       # Example visualization (README)
│
├── requirements.txt 
├── Dockerfile
└── README.md
```

## Run Locally

### Install Dependencies
```bash
pip install -r requirements.txt
```

### 1. Start Backend
```bash
uvicorn app.main:app --reload --port 8001
```
### 2. Start Frontend
```bash
cd frontend
python -m http.server 3000
```

### 3. Open in Browser
http://127.0.0.1:3000

## Sample Queries

Try the following example queries to explore different analysis scenarios:

- which borough has highest complaints in last 30 days  
- which type of noise complaints is highest in last 30 days  
- how does noise trend change in last 30 days  
- noise complaints last 7 days  
- which type of noise complaints is highest between 2024-01-01 and 2024-01-15    

## Step 1: **Collect (API Integration)**

- File: app/tools/nyc_api.py  
- Function: fetch_nyc_data   

Retrieves real-time data from NYC Open Data API.

Supports:

- last X days
- specific date
- between dates
- today / yesterday

## Step 2: **EDA (Tool Calling)**

- File: app/tools/python_eda.py
- Function: analyze_data

Uses pandas and matplotlib to compute and visualize:

- complaint distribution
- borough aggregation
- time trends (groupby)
- peak day
- top vs second comparison
- trend visualization (saved as images)

The EDA process dynamically adapts to the user's query (e.g., time ranges such as "last 7 days", "between dates", or "today"), ensuring that analysis is performed over the relevant subset of data.
This ensures that the analysis is not static, but responsive to different analytical questions and time-based constraints.

### Example Visualization

![Trend Example](assets/trend_example.png)

## Step 3: **Hypothesis (Data Memo)**

- File: app/agents/hypothesis_agent.py  
- Function: generate_hypothesis  

Outputs structured insights:

- Analysis Summary
- Key Insight
- Interpretation
- Supporting Evidence
- Temporal Evidence


## Core Requirements

**Frontend** → frontend/index.html

**Agent Framework** → LangChain (Tool-based agent framework)

- File: app/main.py  
- Components: Tool (collect_tool, eda_tool, hypothesis_tool)

The system uses LangChain's Tool abstraction to wrap each agent (collect, EDA, hypothesis) as callable components.

These tools are orchestrated through a structured pipeline in the FastAPI backend, implementing an orchestrator-handoff multi-agent pattern.

**Tool Calling** → Python EDA tool

- File: app/tools/python_eda.py  
- Function: analyze_data()

The EDA tool performs statistical aggregation and grouping operations (e.g., complaint distribution, borough aggregation, and time trends) over the collected data and returns structured results used for hypothesis generation.

**Non-trivial Data** → NYC Open Data API  

- File: app/tools/nyc_api.py  
- Function: fetch_nyc_data()

**Multi-agent Pattern** → 3 agents (collect_agent.py / eda_agent.py / hypothesis_agent.py)

**Deployed** → Cloud Run (URL above)



## Elective Features

- **Code Execution**  
  - File: app/tools/python_eda.py  
  - Uses pandas and matplotlib to compute statistics and generate visualizations at runtime  

- **Data Visualization**  
  - File: app/tools/python_eda.py  
  - Generates time-series plots with continuous date indexing, missing-day handling, and peak highlighting (annotated maximum values) to improve interpretability  

- **Artifacts (Visualization Files)**  
  - File: app/static/  
  - Generated plots are saved as PNG files and reused by the frontend   

## Summary

This system simulates a real analytics workflow:

- dynamic data retrieval
- programmatic analysis
- evidence-based reasoning

and produces structured, interpretable insights including visualization-based evidence.
