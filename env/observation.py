from pydantic import BaseModel
from typing import List, Dict, Any


class Observation(BaseModel):
    table_preview: List[Dict[str, Any]]
    num_missing: int
    num_duplicates: int
    data_schema: Dict[str, str]
    steps_taken: int
