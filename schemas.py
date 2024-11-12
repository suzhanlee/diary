from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CreateDiaryRq(BaseModel):
    user_id: int
    time: datetime
    plan: str

class UpdateDiaryRq(BaseModel):
    time: Optional[datetime]
    plan: Optional[str]
