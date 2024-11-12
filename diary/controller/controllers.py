from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from schemas import CreateDiaryRq
from domain import Member
from domain.Diary import Diary
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/diary")
def create_diary(createDiaryRq: CreateDiaryRq, db: Session = Depends(get_db)):
    member: Member = db.query(Member).filter(Member.id == createDiaryRq.user_id).first()

    if member is None:
        raise HTTPException(400, detail="존재하지 않는 사용자입니다.")

    diary: Diary = Diary(
        user_id=createDiaryRq.user_id,
        time=createDiaryRq.time,
        plan=createDiaryRq.time,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    diary.member = member
    db.add(diary)
    db.commit()
    db.refresh(diary)

    return {"diary_id": diary.id, "time": diary.time, "plan": diary.plan}


@router.get("/diary/{user_id}")
def get_diarites(user_id: int, db: Session = Depends(get_db)):
    diaries: list[Diary] = db.query(Diary).filter(Diary.user_id == user_id).all()
    if diaries.size() == 0:
        return {"message": "사용자의 다이어리는 비어있습니다."}

    return [
        {"diary_id": diary_id, "time": time, "plan": plan}
        for diary_id, time, plan in diaries
    ]

