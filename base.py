from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from external_API import *
import os

db_hots = os.getenv("DB_HOST")
# If host run
# engine = create_engine('postgresql://admin:admin@localhost:5432/amcef')
# If run in docker
engine = create_engine(f'postgresql://admin:admin@{db_hots}:5432/amcef')


Session = sessionmaker(bind=engine)

Base = declarative_base()
external_user = EUsers()
external_posts = EPosts()


