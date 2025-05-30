from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str 
    password: str

class UserOut(BaseModel):
    id: int 
    name: str

    class Config:
        orm_mode = True

class GoodCreate(BaseModel):
    name: str
    desc: str

class GoodOut(BaseModel):
    id: int 
    name: str

    class Config:
        orm_mode = True