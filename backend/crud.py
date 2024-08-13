from sqlalchemy.orm import Session
from . import models, schemas

def get_recor(db: Session, recor_id: int):
    return db.query(models.Recor).filter(models.Recor.id == recor_id).first()

def create_recor(db: Session, recor: schemas.RecorCreate):
    db_recor = models.Recor(name=recor.name, description=recor.description)
    db.add(db_recor)
    db.commit()
    db.refresh(db_recor)
    return db_recor
