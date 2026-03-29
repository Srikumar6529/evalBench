import json
from pathlib import Path

from app.llm.client import generate_response
from app.evaluators.correctness import evaluate_correctness
from app.evaluators.format_checks import evaluate_format
from app.evaluators.aggregate import aggregate_results


BENCHMARK_PATH = Path(__file__).resolve().parent / "data" / "benchmark.json"


def load_benchmark():
    with open(BENCHMARK_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def run_benchmark():
    benchmark_examples = load_benchmark()
    results = []

    print("=" * 100)
    print("RUNNING EVALBENCH")
    print("=" * 100)

    for example in benchmark_examples:
        example_id = example["id"]
        task_type = example["task_type"]
        user_input = example["input"]
        expected_output = example["expected_output"]

        llm_result = generate_response(user_input)
        predicted_output = llm_result["response"]
        latency_seconds = llm_result["latency_seconds"]

        correctness = evaluate_correctness(
            task_type=task_type,
            predicted_output=predicted_output,
            expected_output=expected_output,
        )

        format_check = evaluate_format(
            task_type=task_type,
            predicted_output=predicted_output,
        )

        result = {
            "id": example_id,
            "task_type": task_type,
            "input": user_input,
            "expected_output": expected_output,
            "predicted_output": predicted_output,
            "latency_seconds": latency_seconds,
            "correctness": correctness,
            "format_check": format_check,
        }

        results.append(result)

        print("-" * 100)
        print(f"Example ID: {example_id}")
        print(f"Task Type: {task_type}")
        print(f"Latency: {latency_seconds}s")
        print(f"Predicted Output: {predicted_output}")
        print(f"Correctness Passed: {correctness['passed']}")
        print(f"Correctness Reason: {correctness['reason']}")
        print(f"Format Passed: {format_check['passed']}")
        print(f"Format Reason: {format_check['reason']}")

    summary = aggregate_results(results)

    print("\n" + "=" * 100)
    print("SUMMARY")
    print("=" * 100)
    print(json.dumps(summary, indent=2))

    return {
        "results": results,
        "summary": summary,
    }


if __name__ == "__main__":
    run_benchmark()