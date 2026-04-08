from pydantic import BaseModel, Field
from typing import Optional, Any


class Action(BaseModel):
    action_type: str = Field(
        ...,
        description="Type of action: remove_duplicates, fill_nulls, convert_date, drop_column, drop_row, stop_cleaning",
    )
    column: Optional[str] = Field(
        None, description="Column name to apply the action to"
    )
    value: Optional[Any] = Field(None, description="Value to use for filling nulls, or index/value for dropping rows")
