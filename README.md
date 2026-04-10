# NYC Noise Complaint Analytics Agent

## Overview

This project implements a multi-agent analytics system that performs the first three steps of a real-world data analysis workflow:

1. Collect real-world data dynamically  
2. Explore and analyze (EDA) the data  
3. Form and communicate a hypothesis with evidence  

The system focuses on analyzing NYC 311 noise complaint data using a combination of backend agents and a simple frontend interface.

---

## System Architecture

The system follows a multi-agent design pattern, where each agent has a distinct responsibility:

- Collect Agent (`collect_agent.py`)  
  Retrieves real-time data from the NYC Open Data API  

- EDA Agent (`eda_agent.py`, `python_eda.py`)  
  Performs data analysis using pandas  

- Hypothesis Agent (`hypothesis_agent.py`)  
  Generates insights and explanations from analyzed data  

These agents are orchestrated by a FastAPI backend.

---

## Step 1: Data Collection

The system retrieves data from the NYC Open Data API:

- Dataset: 311 Service Requests (Noise Complaints)  
- Method: API integration with dynamic queries at runtime  
- Supported queries:
  - last X days  
  - specific date (e.g., 2024-01-01)  
  - date ranges (between ... and ...)  

Example queries:

- noise complaints last 7 days  
- which type of noise complaints is highest between 2024-01-01 and 2024-01-15  

---

## Step 2: Exploratory Data Analysis (EDA)

EDA is performed using a Python-based tool (pandas and matplotlib).

Key analyses include:

- Total complaint count  
- Top complaint types  
- Borough-level distribution  
- Time-based trends (daily aggregation)  

This step uses tool execution to compute statistics dynamically based on the retrieved data.

---

## Step 3: Hypothesis Generation

The system generates a data-driven hypothesis based on EDA results.

Example:

"Noise - Residential accounts for 60% of complaints, suggesting that residential environments are the primary source of noise issues in the analyzed period."

Each hypothesis:

- is grounded in computed statistics  
- includes quantitative evidence  
- adapts to the user’s query  

---

## Knowledge-Augmented Insights (Lightweight RAG)

To improve interpretability, the system incorporates a lightweight retrieval-based knowledge layer.

- A small domain-specific knowledge base maps complaint types to explanations  
- Relevant context is retrieved based on EDA results  
- Retrieved information is injected into the final response  

Example:

Context:  
Residential noise complaints are commonly caused by loud music, parties, or neighbor disturbances.

This design simulates a retrieval-augmented generation (RAG)-like mechanism, where external knowledge is used to enrich analytical outputs.
## Frontend Interface

A simple HTML frontend allows users to interact with the system.

Features include:

- Input field for natural language queries  
- Predefined sample queries for guidance  
- Dynamic rendering of responses from the backend  
- Visualization display for trend-related queries  

The frontend communicates with the FastAPI backend through HTTP requests and displays both textual insights and generated plots.

---

## Data Visualization

The system generates visualizations as part of the EDA process.

- Daily complaint counts are plotted using matplotlib  
- Each query produces a timestamped image file  
- Images are saved in `app/static/`  
- Visualizations are dynamically returned and rendered in the frontend  

### Example

![Trend Example](assets/trend_example.png)

---

## Artifacts

The system produces persistent artifacts to support analysis:

- Visualization files (PNG format)  
- Each file is uniquely timestamped to avoid overwriting  
- Artifacts serve as evidence supporting analytical conclusions  

---

## Query Understanding

The system supports flexible natural language queries through rule-based parsing.

Supported query types include:

- Time filters:
  - last 7 days  
  - last 30 days  

- Specific date:
  - on 2024-01-01  

- Date range:
  - between 2024-01-01 and 2024-01-15  

These patterns allow the system to dynamically construct API queries and perform targeted analysis.

---

## Tech Stack

- Backend: FastAPI  
- Data Processing: pandas  
- Visualization: matplotlib  
- Frontend: HTML and JavaScript  
- Data Source: NYC Open Data API  

---

## How to Run

### 1. Start Backend

```bash
uvicorn app.main:app --reload --port 8001

### 2. Start Frontend
```bash
cd frontend
python -m http.server 3000
### 3. Open in Browser
http://127.0.0.1:3000

 ## Sample Queries
	•	which borough has highest complaints in last 30 days
	•	which type of noise complaints is highest in last 30 days
	•	how does noise trend change in last 30 days
	•	noise complaints last 7 days
	•	which type of noise complaints is highest between 2024-01-01 and 2024-01-15

## Summary

This project demonstrates a complete data analysis agent pipeline, combining:
	•	dynamic data retrieval
	•	programmatic analysis
	•	interpretable insight generation
	•	user interaction

It mimics the workflow of a real data analyst and showcases how agent-based systems can support data-driven decision making.


##  Limitations & Future Work

- Currently relies on a single data source (NYC Open Data API) and rule-based query parsing.  
- Visualization is limited to basic trend plots.  

**Future Improvements:**
- Integrate LLM-based query understanding for more flexible inputs  
- Add advanced analytics (e.g., comparisons, anomaly detection)  
- Support interactive visualizations  
- Expand to multiple data sources  