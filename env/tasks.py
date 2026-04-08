from typing import Dict, Any


def get_tasks() -> Dict[str, Dict[str, Any]]:
    return {
        "easy": {"description": "Remove duplicate rows", "eval_metrics": ["accuracy"]},
        "medium": {
            "description": "Handle missing values and formatting",
            "eval_metrics": ["accuracy"],
        },
        "hard": {"description": "Full ETL pipeline", "eval_metrics": ["accuracy"]},
    }
