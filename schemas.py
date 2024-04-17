from pydantic import BaseModel, Field
from datetime import date


class PersonBaseSchema(BaseModel):
    name: str = ...
    birth_date: date = Field(..., description="Date of birth", gt=date(1950, 1, 1))
    extra_info: str = None