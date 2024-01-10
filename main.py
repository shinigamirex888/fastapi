# from sqlalchemy import engine_from_config
from certifi import contents
from fastapi import Depends, FastAPI, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from  openpyxl import workbook

from openpyxl import load_workbook
import io
import csv
import xlsxwriter

import crud, models, schemas , fileoperation
# import crud
from database import SessionLocal, engine

# models.Base.metadata.create_all(bind=engine)

import pandas as pd


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/events/", response_model=list[schemas.Event])
def get_all_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    events = crud.all_events(db, skip=skip, limit=limit)
    return events

@app.get("/events/{event_id}", response_model=schemas.Event)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = crud.get_event_by_id(db, event_id=event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@app.get("/events/del/{event_id}", response_model=schemas.Event)
def del_event(event_id: int, db: Session = Depends(get_db)):
    event = crud.delete_event_by_id(db, event_id=event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return "Event Deleted"


@app.put("/events/update/{event_id}", response_model=schemas.Event)
def update_event(event_id: int, db: Session = Depends(get_db)):
    event = crud.update_event_status(db, event_id=event_id)
    # return event
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@app.post("/users/new/", response_model=schemas.Event)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    # db_event = crud.get_event_by_id(db, id=event.id)
    # if db_event:
    #     raise HTTPException(status_code=400, detail="Event already registered")
    return crud.create_event(db=db, event=event)





@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file sent")
    else:
        file_contents = await file.read()
        if file.filename.endswith('.xlsx'):
            fileoperation.read_excel_and_print(file_contents)
            return {"message": "Excel content printed"}    

        elif file.filename.endswith('.csv'):
            fileoperation.convert_csv_to_xlsx_and_print(file_contents)
            return {"message": "Csv content printed"}

        else:
            raise HTTPException(status_code=405, detail="File format not supported")



@app.get("/excel/")
def create_excel():
    workbook = xlsxwriter.Workbook('Example.xlsx')
    worksheet = workbook.add_worksheet("My sheet")
    scores = (
    ['ankit', 1000],
    ['rahul',   100],
    ['priya',  300],
    ['harshita',    50],
    )
    headers = ['name', 'external id', 'dob', 'seeding', 'email', 'gender']
    bold_format = workbook.add_format({'bold': True,'bg_color':'yellow'})
    # for row, data in enumerate(scores, start=1):
    #     for col, value in enumerate(data):
    #         worksheet.write(row, col, value)
   

    for col, header in enumerate(headers):
        worksheet.write(0, col, header, bold_format)  
         


    for row, data in enumerate(scores, start=1):
        for col, value in enumerate(data):
            worksheet.write(row, col, value)

    workbook.close()


@app.get("/check")
def read_root():
    return {"Hello": "World"}






