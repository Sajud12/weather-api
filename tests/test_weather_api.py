import pytest
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from src.app import app, get_database_session
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

load_dotenv()
engine = create_engine(os.getenv('TEST_URL'))
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_database_session] = override_get_db

@pytest.fixture()
def test_client():
    client = TestClient(app)
    yield client

def test_weather_api_default_endpoint(test_client):
    response = test_client.get('/api/weather/')
    assert response.status_code == 200
    assert response.json()['count'] == 10
    
def test_weather_api_with_pagination(test_client):
    response = test_client.get('/api/weather/?page=1&limit=5')
    assert response.status_code == 200
    assert response.json()['count'] == 5

def test_weather_api_with_all_filters(test_client):
    response = test_client.get('/api/weather/?station_id=1&date=1985-01-01')
    assert response.status_code == 200
    assert response.json()['data'][0]['date'] == '1985-01-01'
    assert response.json()['data'][0]['station_id'] == 1

def test_weather_api_with_date_param_filter(test_client):
    response = test_client.get('/api/weather/?date=1985-01-01')
    assert response.status_code == 200
    assert response.json()['data'][0]['date'] == '1985-01-01'

def test_weather_api_with_station_id_param_filter(test_client):
    response = test_client.get('/api/weather/?station_id=1')
    assert response.status_code == 200
    assert response.json()['data'][0]['station_id'] == 1
    
def test_weather_stats_api_default_endpoint(test_client):
    response = test_client.get('/api/weather/stats/')
    assert response.status_code == 200
    assert response.json()['count'] == 10

def test_weather_stats_api_with_pagination(test_client):
    response = test_client.get('/api/weather/stats/?page=0&limit=5')
    assert response.json()['count'] == 5

def test_weather_stats_api_with_all_filters(test_client):
    response = test_client.get('/api/weather/stats/?year=2001&station_id=1')
    assert response.status_code == 200
    assert response.json()['count'] == 1
    assert response.json()['data'][0]['year'] == 2001
    assert response.json()['data'][0]['station_id'] == 1
    
def test_weather_stats_api_with_year_param_filter(test_client):
    response = test_client.get('/api/weather/stats/?year=2001')
    assert response.status_code == 200
    assert response.json()['count'] == 10
    assert response.json()['data'][0]['year'] == 2001
    
def test_weather_stats_api_with_station_id_param_filter(test_client):
    response = test_client.get('/api/weather/stats?station_id=12')
    assert response.status_code == 200
    assert response.json()['count'] == 10
    assert response.json()['data'][0]['station_id'] == 12
    
def test_weather_api_with_station_id_param_filter_1(test_client):
    response = test_client.get('/api/weather/?station_id=-1')
    assert response.status_code == 404
    
def test_weather_api_with_date_param_filter_1(test_client):
    response = test_client.get('/api/weather/?date=-1')
    assert response.status_code == 400
   
def test_weather_api_with_page_param_filter_1(test_client):
    response = test_client.get('/api/weather/?page=abc')
    assert response.status_code == 422
     
def test_weather_stats_api_with_station_id_param_filter_1(test_client):
    response = test_client.get('/api/weather/stats?station_id=-1')
    assert response.status_code == 404

def test_weather_stats_api_with_year_param_filter_1(test_client):
    response = test_client.get('/api/weather/stats?year=-1')
    assert response.status_code == 404
    
def test_weather_stats_api_with_page_param_filter_1(test_client):
    response = test_client.get('/api/weather/stats?page=abc')
    assert response.status_code == 422
