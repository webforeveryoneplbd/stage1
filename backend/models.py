from sqlalchemy import Column, Integer, String
from .database import Base

class Recor(Base):
    __tablename__ = "recors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    