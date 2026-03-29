import json


def is_valid_json_object(text: str) -> bool:
    text = text.strip()

    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()

    try:
        parsed = json.loads(text)
        return isinstance(parsed, dict)
    except Exception:
        return False


def evaluate_format(task_type: str, predicted_output: str) -> dict:
    if task_type == "json_extraction":
        passed = is_valid_json_object(predicted_output)
        return {
            "passed": passed,
            "reason": "Valid JSON object." if passed else "Output is not a valid JSON object.",
        }

    return {
        "passed": True,
        "reason": "No strict format requirement for this task type.",
    }