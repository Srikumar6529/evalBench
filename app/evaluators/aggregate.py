from typing import List, Dict, Any


def aggregate_results(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    total_examples = len(results)
    if total_examples == 0:
        return {
            "total_examples": 0,
            "correctness_pass_rate": 0.0,
            "format_pass_rate": 0.0,
            "average_latency_seconds": 0.0,
            "task_type_breakdown": {},
        }

    correctness_passes = sum(1 for item in results if item["correctness"]["passed"])
    format_passes = sum(1 for item in results if item["format_check"]["passed"])
    avg_latency = sum(item["latency_seconds"] for item in results) / total_examples

    task_type_breakdown = {}
    for item in results:
        task_type = item["task_type"]
        if task_type not in task_type_breakdown:
            task_type_breakdown[task_type] = {
                "count": 0,
                "correctness_passes": 0,
                "format_passes": 0,
            }

        task_type_breakdown[task_type]["count"] += 1
        if item["correctness"]["passed"]:
            task_type_breakdown[task_type]["correctness_passes"] += 1
        if item["format_check"]["passed"]:
            task_type_breakdown[task_type]["format_passes"] += 1

    for task_type, stats in task_type_breakdown.items():
        count = stats["count"]
        stats["correctness_pass_rate"] = round(stats["correctness_passes"] / count, 3)
        stats["format_pass_rate"] = round(stats["format_passes"] / count, 3)

    return {
        "total_examples": total_examples,
        "correctness_pass_rate": round(correctness_passes / total_examples, 3),
        "format_pass_rate": round(format_passes / total_examples, 3),
        "average_latency_seconds": round(avg_latency, 3),
        "task_type_breakdown": task_type_breakdown,
    }