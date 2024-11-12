from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy.orm import relationship


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(10), unique=True, index=True)
    email = Column(String(20))
    hashed_password = Column(String(20))

    diaries = relationship("Diary", back_populates="member")
