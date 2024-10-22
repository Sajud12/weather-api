import logging
import uvicorn
from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, Annotated
from models import models
from ingest_data.data_ingestion import IngestData
from database.session.session import get_database_session
from src.services import fetch_statistics, fetch_records, initialize_database

app = FastAPI()

@app.on_event("startup") # pragma: no cover
async def on_startup():
    """
    Executes on startup of the application and initializes the data ingestion process into the database.
    """
    try:
        dbs = IngestData()
        db = next(get_database_session())
        initialize_database(dbs, db)
    except Exception as e:
        logging.error(f"Error during startup of application: {e}")

@app.get('/api/weather')
async def fetch_weather_data(
    db: Annotated[Session, Depends(get_database_session)], 
    station_id: Optional[int] = None, 
    date: Optional[str] = None, 
    page: int = Query(0, ge=0), 
    limit: int = Query(10, ge=1)
):
    """
    Fetch weather records based on station ID and date.
    """
    try:
        if date:
            date = date.replace("-", "").replace("/", "")
            if len(date) != 8:
                raise ValueError("Invalid date format. Date must be in 'YYYYMMDD' format.")
        query = db.query(models.RecordData)
        return fetch_records(query, station_id, date, page, limit)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except HTTPException as he:
        raise he
    except Exception as e: # All types of exceptions handled here
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get('/api/weather/stats')
async def fetch_weather_stats(
    db: Annotated[Session, Depends(get_database_session)], 
    station_id: Optional[int] = None, 
    year: Optional[int] = None, 
    page: int = Query(0, ge=0), 
    limit: int = Query(10, ge=1)
):
    """
    Fetch weather statistics based on station ID and year.
    """
    try:
        query = db.query(models.StatisticsData)
        return fetch_statistics(query, station_id, year, page, limit)
    except HTTPException as he:
        raise he
    except Exception as e: # All types of exceptions handled here
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) # pragma: no cover