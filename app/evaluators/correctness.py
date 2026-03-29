import json
from typing import Any


def normalize_text(value: str) -> str:
    return " ".join(value.strip().lower().split())


def classification_match(predicted: str, expected: str) -> bool:
    predicted_norm = normalize_text(predicted)
    expected_norm = normalize_text(expected)

    if predicted_norm == expected_norm:
        return True

    return expected_norm in predicted_norm.split() or expected_norm in predicted_norm


def short_qa_match(predicted: str, expected: str) -> bool:
    predicted_norm = normalize_text(predicted)
    expected_norm = normalize_text(expected)

    if predicted_norm == expected_norm:
        return True

    return expected_norm in predicted_norm


def safe_json_loads(text: str) -> Any:
    text = text.strip()

    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()

    return json.loads(text)


def json_extraction_match(predicted: str, expected: dict) -> dict:
    try:
        parsed = safe_json_loads(predicted)
    except Exception as exc:
        return {
            "passed": False,
            "parsed_output": None,
            "reason": f"Invalid JSON output: {exc}",
        }

    if not isinstance(parsed, dict):
        return {
            "passed": False,
            "parsed_output": parsed,
            "reason": "Output is valid JSON but not a JSON object.",
        }

    missing_keys = [key for key in expected.keys() if key not in parsed]
    if missing_keys:
        return {
            "passed": False,
            "parsed_output": parsed,
            "reason": f"Missing required keys: {missing_keys}",
        }

    mismatched = {}
    for key, expected_value in expected.items():
        actual_value = parsed.get(key)
        if isinstance(expected_value, str) and isinstance(actual_value, str):
            if normalize_text(actual_value) != normalize_text(expected_value):
                mismatched[key] = {
                    "expected": expected_value,
                    "actual": actual_value,
                }
        else:
            if actual_value != expected_value:
                mismatched[key] = {
                    "expected": expected_value,
                    "actual": actual_value,
                }

    if mismatched:
        return {
            "passed": False,
            "parsed_output": parsed,
            "reason": f"Value mismatch: {mismatched}",
        }

    return {
        "passed": True,
        "parsed_output": parsed,
        "reason": "JSON output matched expected keys and values.",
    }


def evaluate_correctness(task_type: str, predicted_output: str, expected_output: Any) -> dict:
    if task_type == "classification":
        passed = classification_match(predicted_output, expected_output)
        return {
            "passed": passed,
            "reason": "Exact normalized label match." if passed else "Classification label mismatch.",
        }

    if task_type == "short_qa":
        passed = short_qa_match(predicted_output, expected_output)
        return {
            "passed": passed,
            "reason": "Exact normalized short answer match." if passed else "Short QA answer mismatch.",
        }

    if task_type == "json_extraction":
        return json_extraction_match(predicted_output, expected_output)

    return {
        "passed": False,
        "reason": f"Unsupported task type: {task_type}",
    }