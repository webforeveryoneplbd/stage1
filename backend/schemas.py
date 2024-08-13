from pydantic import BaseModel

class RecorBase(BaseModel):
    name: str
    description: str

class RecorCreate(RecorBase):
    pass

class Recor(RecorBase):
    id: int

    class Config:
        orm_mode = True
