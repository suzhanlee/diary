from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from database import Base
from sqlalchemy.orm import relationship


class Diary(Base):
    __tablename__ = "diaries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("members.id"))
    time = Column(DateTime)
    plan = Column(String(1000))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    member = relationship("Member", back_populates="diaries")

    def update_diary(self, time, plan) -> None:
        if time is not None:
            self.time = time

        if plan is not None:
            self.plan = plan
