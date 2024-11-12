from fastapi import FastAPI
from database import Base, engine
from diary.controller.controllers import router

app = FastAPI()
Base.metadata.create_all(engine)
app.include_router(router)