# Build FastAPI backend
from fastapi import FastAPI
from pydantic import BaseModel

from app.agents.collect_agent import collect_data
from app.agents.eda_agent import run_eda
from app.agents.hypothesis_agent import generate_hypothesis

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from langchain.tools import Tool
from pathlib import Path

app = FastAPI()

collect_tool = Tool(
    name="collect_data",
    func=collect_data,
    description="Fetch NYC noise complaint data from API"
)

eda_tool = Tool(
    name="run_eda",
    func=run_eda,
    description="Perform EDA analysis on collected data"
)

hypothesis_tool = Tool(
    name="generate_hypothesis",
    func=generate_hypothesis,
    description="Generate data-driven hypothesis from EDA results"
)

@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    html_path = Path("frontend/index.html")
    return html_path.read_text(encoding="utf-8")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# request schema
class QueryRequest(BaseModel):
    question: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(request: QueryRequest):
    query = request.question

    # Step 1: Collect
    data = collect_tool.func(query)

    # Step 2: EDA
    eda_result = eda_tool.func(data)

    # Step 3: Hypothesis
    hypothesis = hypothesis_tool.func(eda_result, query, mode="api")

    return {
        "question": query,
        "eda_result": eda_result,
        "answer": hypothesis
    }