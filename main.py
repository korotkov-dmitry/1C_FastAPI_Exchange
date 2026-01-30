from contextlib import asynccontextmanager
from typing import List
# import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

import db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    db.init_db()
    yield
    # shutdown
    # здесь потом можно закрывать пулы, соединения и т.п.

app = FastAPI(
    title="Обмен данными 1С - Веб сервер",
    description="Бэк-энд обмена",
    tags=["Обмен с 1С"],
    summary="Приём данных из 1С",
    lifespan=lifespan
)

class Data1c(BaseModel):
    uid: str
    title: str
    done: bool

class Data1cIn(BaseModel):
    uid: str
    title: str
    done: bool

TAGS_1C = ["1С: обмен данными"]

@app.get("/",
         tags=["It works!"],
         summary="It works!", )
async def root():
    return {"status": "Exchange backend is running"}

@app.get("/api/get_data",
         response_model=List[Data1c],
         tags=TAGS_1C,)
def get_data():
    return db.get_data()

@app.post("/api/add_data",
          tags=TAGS_1C,)
def add_data(item: Data1cIn):
    db.add_data(item.model_dump())
    return {"status": "ok"}


# if __name__ == '__main__':
#     uvicorn.run("main:app", host='localhost', port=8000, reload=True)