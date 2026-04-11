# Build FastAPI backend
from fastapi import FastAPI
from pydantic import BaseModel

from app.agents.collect_agent import collect_data
from app.agents.eda_agent import run_eda
from app.agents.hypothesis_agent import generate_hypothesis

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path

app = FastAPI()

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
    data = collect_data(query)

    # Step 2: EDA
    eda_result = run_eda(data)

    # Step 3: Hypothesis
    hypothesis = generate_hypothesis(eda_result, query, mode="api")

    return {
        "question": query,
        "eda_result": eda_result,
        "answer": hypothesis
    }