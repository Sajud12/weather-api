import logging
from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from models import models
from ingest_data.data_ingestion import IngestData
from database.session.session import engine

def initialize_database(dbs: IngestData, db: Session): # pragma: no cover
    """
    Initializes the database by dropping and creating tables,
    and loading data if necessary.
    """
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    
    logging.info(f"Data Ingestion Process Started Successfully. Please wait until process is completed")
    
    if not db.query(models.RecordData).count() or not db.query(models.StationData).count():
        dbs.data_loading_from_input_files()
    if not db.query(models.StatisticsData).count():
        dbs.calculate_statistics_data()
    
    logging.info(f"Data Ingestion Process Completed Successfully. Application is ready")
        
def fetch_records(query, station_id: Optional[int], date: Optional[str], page: int, limit: int):
    """
    Applies filtering and pagination to the weather records query.
    """
    if station_id:
        query = query.filter(models.RecordData.station_id == station_id)
        if not query.count():
            raise HTTPException(status_code=404, detail=f'Station ID {station_id} does not exist. Please provide correct values.')

    if date:
        query = query.filter(models.RecordData.date == date)
        if not query.count():
            raise HTTPException(status_code=404, detail=f'Date {date} does not exist. Please provide correct values.')

    records = query.offset(page * limit).limit(limit).all()
    return {'count': len(records), 'data': records}

def fetch_statistics(query, station_id: Optional[int], year: Optional[int], page: int, limit: int):
    """
    Applies filtering and pagination to the weather statistics query.
    """
    if station_id:
        query = query.filter(models.StatisticsData.station_id == station_id)
        if not query.count():
            raise HTTPException(status_code=404, detail=f'Station ID {station_id} does not exist. Please provide correct values.')
    
    if year:
        query = query.filter(models.StatisticsData.year == year)
        if not query.count():
            raise HTTPException(status_code=404, detail=f'Year {year} does not exist. Please provide correct values.')

    stats = query.offset(page * limit).limit(limit).all()
    return {'count': len(stats), 'data': stats}

