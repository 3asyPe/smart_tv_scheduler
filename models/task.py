from pydantic import BaseModel, field_validator
from croniter import croniter

from services.functions import TASKS


class Task(BaseModel):
    name: str
    start_at: str
    function: str
    run_statuses: list[str]
    params: dict

    @field_validator("start_at")
    @classmethod
    def validate_cron(cls, value):
        if not croniter.is_valid(value):
            raise ValueError(f"'{value}' is not a valid cron expression")
        return value

    @field_validator("function")
    @classmethod
    def validate_function(cls, value):
        if value not in TASKS:
            raise ValueError(f"Function '{value}' does not exist")
        return value
