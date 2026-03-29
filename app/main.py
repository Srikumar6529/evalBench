from fastapi import FastAPI, HTTPException

from app.run_benchmark import run_benchmark
from app.schemas import EvaluateResponse

app = FastAPI(title="EvalBench")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/evaluate", response_model=EvaluateResponse)
def evaluate():
    try:
        result = run_benchmark()
        return result
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))