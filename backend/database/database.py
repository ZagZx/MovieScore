from sqlalchemy import create_engine, URL
from sqlalchemy.orm import Session, sessionmaker
from fastapi import Depends
from typing import Annotated
from os import getenv
from dotenv import load_dotenv

load_dotenv()

DATABASE=getenv("DATABASE")
USERNAME=getenv("DB_USERNAME")
PASSWORD=getenv("DB_PASSWORD")
HOST=getenv("DB_HOST")
PORT=int(getenv("DB_PORT", 3306))

DB_URL = URL.create(
    drivername="mysql+pymysql",
    database=DATABASE,
    username=USERNAME,
    password=PASSWORD,
    host=HOST,
    port=PORT
)

engine = create_engine(DB_URL)
SessionFactory = sessionmaker(bind=engine)

def get_session():
    with SessionFactory() as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]