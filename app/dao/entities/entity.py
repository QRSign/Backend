from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#from app.app.router import app


db_url = 'localhost:5432'
db_name = 'qrsign'
db_user = 'postgres'
db_password = 'root'
#engine = create_engine(f'postgres://ggqoskolpxtanp:13a0257a5f12b9d5dd0d57c1d993ff7b27e7c774746ce1661aa90f3082a17aaf@ec2-3-211-245-154.compute-1.amazonaws.com:5432/d516q9uaepdk5u')
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_url}/{db_name}')
Session = sessionmaker(bind=engine)

Base = declarative_base()


class Entity():
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    def __init__(self):
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
