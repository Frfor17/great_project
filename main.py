#внешние импорты
import asyncio
from sqlalchemy.future import select
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, AsyncGenerator, List

# Импорты из локальных файлов
from schemas import UserCreate, UserOut, GoodCreate, GoodOut
from database import SessionLocal, engine
from models import User, Base, Good

app = FastAPI()

@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

#какая-то странная функция
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

# создание юзера
@app.post("/users/", response_model=UserCreate)
async def create_user(name: str, password: str, db: AsyncSession = Depends(get_db)) -> Any:
    new_user = User(name=name, password=password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

# чтение юзера 
@app.get("/users/", response_model=List[UserOut])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()

# добавление товара
@app.post("/goods/", response_model=GoodCreate)
async def create_good(name:str, desc: str, db:AsyncSession = Depends(get_db)) -> Any:
    new_good = Good(name=name, desc=desc)
    db.add(new_good)
    await db.commit()
    await db.refresh(new_good)
    return new_good
    
#показать все товары
@app.get("/goods/", response_model=List[GoodOut])
async def get_all_goods(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Good))
    return result.scalars().all()