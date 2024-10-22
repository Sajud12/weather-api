# Weather Api Challenge

## Description
This is a Weather API Application to perform api calls to fetch respective weather records and weather statistics data of different stations.

## Framework
 - FastAPI

## API Endpoints
 - `/api/weather/`
 - `/api/weather/stats/`
 - `/docs`

## Requirements
- Python 3.10 or higher

## Running the project

1. Clone the Github repository

2. Move to project directory
```bash
  cd weather_api
```

3. Creation of virtual environment
- Command to create a virtual environment.
```bash
  python -m venv venv
```
- Command to activate virtual environment
```bash
  source venv/bin/activate #(For Mac and Linux)
  venv\Scripts\activate #(For Windows)
```

4. Installation of project requirements
```bash
  pip install -r requirements.txt
```

## Steps for Database Setup and Installation.
1. Firstly, need to download and install database - PostgreSQL in your system. Refer to link `https://www.postgresql.org/download/` for same.
2. Now create a database using command below:-
```bash
CREATE DATABASE database_name;
```

## Setup environment variables.
Create a .env file in root directory of project and accordingly store your database credentials in given format:-
```bash
DB_USER='user_name_for_db'
DB_PASSWORD='password_of_db'
DB_NAME='name_of_db'
DB_HOST='host_of_db'
DB_PORT='port_number_of_db'
DB_URL='f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"'
TEST_URL='f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"'
```

### Step to run the api server
```bash
uvicorn src.app:app --host 127.0.0.1 --port 8000 --reload
```
# Screenshots of Api server running

![Alt text](static/app-start.png?raw=true "api server")

### Data Ingestion Process Info:
- Data ingestion process starts automatically when application starts running.
- All info wrt ingestion is logged into logger file at run time.
- In terminal process, ingestion process could be seen as:
- INFO: Waiting for application startup -> Indicates initiation of ingestion process.
- INFO: Application startup complete -> Indicates ingestion process is completed and application is started successfully.

# Screenshots of Logger

![Alt text](static/logger.png?raw=true "logger")

# Troubleshoot 
### When api server is unable to start due to port issue / port already in use, proceed to kill port and then restart server again.
```bash
kill -9 $(lsof -t -i:8000)
```


### Running tests cases
```bash
pytest --cov
```

# Screenshots of test cases

![Alt text](static/testing.png?raw=true "test cases")

## API Documentation
After running the project and use following URL to access the API documentation.
```
http://localhost:8000/docs
```


### Example Response
```json
{
    "status": "Success"
}
```
- GET `/api/weather`
    - Returns the list of  weather
    - Query Parameters:
        - `station_id`: The station id to filter the records.
        - `date`: The date to filter the records. `(Format: YYYYMMDD)`
        - `offset`: The offset of the first record to return.
        - `limit`: The number of records to return.
    - Example: `/api//weather?offset=0&limit=50`
    - Example: `/api//weather?station_id=USC00114198&date=19850103`
    - Example: `/api//weather?station_id=USC00114198`

### Example Response
```json
[
  {
    "id": 1,
    "station_id": "USC00257715",
    "date": "19850101",
    "maximum_temp": -83,
    "minimum_temp": -144,
    "precipitation": 0
  }
]
```
- GET `/weather/stats`
    - Returns the weather stats.
    - Query Parameters:
        - `station_id`: The station id to filter the records.
        - `year`: The year to filter the records.
        - `offset`: The offset of the first record to return.
        - `limit`: The number of records to return.
    - Example: `/api/weather/stats`
    - Example: `/api/weather/stats?offset=0&limit=50&year=1985&station_id=USC00113879`

### Example Response
```json
[
  {
    "id": 30,
    "station_id": "USC00113879",
    "year": 1985,
    "avg_max_temp": 193.6904109589041,
    "avg_min_temp": 74.82191780821918,
    "total_precipitation": 14473
  }
]
```

# Screenshots of Postman Collection

![Alt text](static/postman-1.png?raw=true "weather-1")

<br><br>
![Alt text](static/postman-2.png?raw=true "weather-2")

<br><br>
![Alt text](static/postman-3.png?raw=true "weather-3")

<br><br>
![Alt text](static/postman-4.png?raw=true "weather-4")

<br><br>
![Alt text](static/postman-5.png?raw=true "weather-5")


# Screenshots of Swagger API Collection

![Alt text](static/swagger-1.png?raw=true "swagger-1")

<br><br>
![Alt text](static/swagger-2.png?raw=true "swagger-2")

<br><br>
![Alt text](static/swagger-3.png?raw=true "swagger-3")

<br><br>
![Alt text](static/swagger-4.png?raw=true "swagger-4")

<br><br>
![Alt text](static/swagger-5.png?raw=true "swagger-5")


## AWS Deployment Strategy: FastAPI API on AWS

To deploy weather api application developed using Fastapi framework in python on AWS cloud would require usage of several AWS services and thus create scalable, maintainable system.

## Services Utilized
- AWS Elastic Beanstalk
- Application Load Balancer (ALB)
- Amazon RDS(PostgreSQL)
- AWS S3
- AWS EFS
- Cloudwatch Events
- AWS Fargate


### Application Layer

#### Set Up for Backend
- Use AWS Elastic Beanstalk to deploy and manage your FastAPI application with ease.
- Elastic Beanstalk natively supports Python, making it ideal for FastAPI deployments.
- Configure an Application Load Balancer (ALB) to manage incoming traffic and distribute it across FastAPI instances.
- Enable auto-scaling to handle traffic spikes and improve reliability.
- Set up health checks on the `/health` endpoint to ensure application health and availability.


#### Deploy Amazon RDS (PostgreSQL)
- Deploy a fully managed PostgreSQL database using Amazon RDS to store and manage your data.
- Utilize Multi-AZ deployment for high availability and automatic failover.
- Enable auto-scaling for database storage to adjust based on demand.
- Recommended instance class: `t3.medium` for balancing cost and performance.
- Configure a 7-day backup retention policy to ensure data durability.

#### Use Amazon S3 and EFS for Storage
- Use Amazon S3 for storing static assets, application logs, and backups efficiently.
- Optionally, use Amazon EFS as a shared file system for persistent, scalable file storage.

### ETL Pipeline

#### Configure AWS ECS Fargate
- Deploy containerized Python workers using AWS ECS Fargate for ETL tasks.
- Store Docker images in Amazon ECR (Elastic Container Registry) for easy access.
- Use Amazon CloudWatch Events to automate and schedule ETL tasks on ECS Fargate.
- Enable automatic data ingestion into the Amazon RDS PostgreSQL database.

## Security Considerations

#### Set Up VPC and Security Groups
- Configure VPC with private subnets for RDS and public subnets for ALB to restrict database access.
- Set security groups to allow only necessary access to RDS and ALB for improved security.

#### Manage Secrets with AWS Secrets Manager
- Store sensitive credentials such as database passwords in AWS Secrets Manager.
- Assign IAM roles to services for secure and seamless access control.
- Ensure SSL/TLS is enabled for encrypting data in transit.

---

## Monitoring and Logging

#### Use CloudWatch for Monitoring
- Set up CloudWatch Logs for collecting application, access, and error logs.
- Monitor key metrics like request latency, error rates, and CPU/memory usage.
- Set up alarms to notify on key thresholds like database connections and application errors.

---

## Deployment Pipeline

#### Automate with CI/CD
- Use infrastructure-as-code tools (e.g., CloudFormation, Terraform) to automate AWS resource provisioning.
- Automate FastAPI application deployment to Elastic Beanstalk using continuous deployment.

