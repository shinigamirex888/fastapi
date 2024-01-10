from sqlalchemy.orm import Session

import models, schemas


def create_event(db: Session, event: schemas.EventCreate):
    new_description = "Stupa-Event" + event.description 
    db_event = models.Event(name=event.name, description=new_description)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def get_event_by_id(db: Session, event_id: int):
    return db.query(models.Event).filter(models.Event.id == event_id).first()


def all_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Event).offset(skip).limit(limit).all()    

def delete_event_by_id(db: Session, event_id: int):
    db.query(models.Event).delete(models.Event.id == event_id).first()


def update_event_status(db: Session, event_id: int):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if event:
        event.is_active = True
        db.commit()
    return event
  