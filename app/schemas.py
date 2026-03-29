from typing import Any, Dict, List
from pydantic import BaseModel


class BenchmarkExampleResult(BaseModel):
    id: int
    task_type: str
    input: str
    expected_output: Any
    predicted_output: str
    latency_seconds: float
    correctness: Dict[str, Any]
    format_check: Dict[str, Any]


class BenchmarkSummary(BaseModel):
    total_examples: int
    correctness_pass_rate: float
    format_pass_rate: float
    average_latency_seconds: float
    task_type_breakdown: Dict[str, Any]


class EvaluateResponse(BaseModel):
    results: List[BenchmarkExampleResult]
    summary: BenchmarkSummary