import os
import logging
import psycopg2
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from tqdm import tqdm  # Import TQDM

from database.queries.records_query import QUERY_INSERT_RECORDS
from database.queries.stations_query import QUERY_INSERT_STATION, QUERY_BY_STATION_ID
from database.queries.statistics_query import QUERY_INSERT_STATISTICS

MISSING_VALUE_HANDLING = '-9999'

class IngestData:
    def __init__(self):
        load_dotenv()
        self.db_params = self._get_db_config()
        self.generate_logger_file()
        
    def _get_db_config(self):
        return {
            'dbname': os.getenv("DB_NAME"),
            'user': os.getenv("DB_USER"),
            'password': os.getenv("DB_PASSWORD"),
            'host': os.getenv("DB_HOST"),
            'port': os.getenv("DB_PORT")
        }
            
    def database_connection(self):
        return psycopg2.connect(**self.db_params)
               
    def generate_logger_file(self):
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='logger.log'
        )

    def calculate_statistics_data(self):
        try:
            with self.database_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(QUERY_INSERT_STATISTICS)
                connection.commit()
        except Exception as e:
            logging.error(f"Error observed while performing statistics calculation: {e}")
            
    def data_loading_from_input_files(self, folder_path: str = 'data/wx_data'):
        start_time = datetime.now()
        file_list = os.listdir(folder_path)
        
        with self.database_connection() as connection:
            cursor = connection.cursor()
            
            # Use TQDM to show progress for file processing
            for file_name in tqdm(file_list, desc='Processing files', unit='file'):
                if file_name.endswith('.txt'):
                    self.file_processing(cursor, folder_path, file_name)
                    
            connection.commit()

        end_time = datetime.now()
        logging.info(f'Logging: Data Load process started at :: {start_time} and ended at :: {end_time}')

    def file_processing(self, cursor, folder_path, file_name):
        file_path = Path(folder_path) / file_name
        station_name = file_path.stem

        station_id = self.insert_data_into_station_table(cursor, station_name)
        records = self.read_data_from_files(file_path, station_id)
        
        for record in records:
            self.insert_data_into_table(cursor, record)
    
    def insert_data_into_station_table(self, cursor, station_name: str) -> int:
        cursor.execute(QUERY_INSERT_STATION, (station_name,))
        station_id = cursor.fetchone()
        
        if not station_id:
            cursor.execute(QUERY_BY_STATION_ID, (station_name,))
            station_id = cursor.fetchone()
        
        return station_id[0]

    def read_data_from_files(self, file_path: Path, station_id: int) -> list:
        records = []
        with open(file_path, 'r') as file:
            for line in file:
                data = line.strip().split('\t')
                if MISSING_VALUE_HANDLING not in data:
                    date = datetime.strptime(data[0], '%Y%m%d').date()
                    record = [date] + [int(cell) for cell in data[1:]] + [station_id]
                    records.append(record)
        return records

    def insert_data_into_table(self, cursor, record: list):
        cursor.execute(QUERY_INSERT_RECORDS, record)
