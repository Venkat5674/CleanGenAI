from typing import Dict, Any
from env.grader import grade

def get_tasks() -> Dict[str, Dict[str, Any]]:
    return {
        "easy": {"description": "Remove duplicate rows", "eval_metrics": ["accuracy"], "grader": grade},
        "medium": {
            "description": "Handle missing values and formatting",
            "eval_metrics": ["accuracy"],
            "grader": grade
        },
        "hard": {"description": "Full ETL pipeline", "eval_metrics": ["accuracy"], "grader": grade},
    }
