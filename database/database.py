from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine
import os
from dotenv import load_dotenv

load_dotenv()

postgres_url = os.getenv("DB_URL")

engine = create_engine(postgres_url)

def create_db_and_tables():
    """Creates tables for all table models"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Creates a session. A new session is provided for each request.
    
    This is used to create a session dependancy - a stored object in memory which
    keeps track of changes to data, then uses the engine to communicate to
    the database. """
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]