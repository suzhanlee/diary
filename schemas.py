from datetime import datetime
from pydantic import BaseModel


class CreateDiaryRq(BaseModel):
    user_id: int
    time: datetime
    plan: str
