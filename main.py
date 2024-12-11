# uvicorn main:app --reload
from app import *
from db import Base, engine

Base.metadata.create_all(engine)