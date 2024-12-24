from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


DATABASE_URL = 'sqlite:///app.db'

engine = create_engine(DATABASE_URL)

Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ModelDateDataMixin(Base):
    __abstract__ = True

    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    modified_at = Column(DateTime(timezone=True), default=datetime.utcnow)


class User(ModelDateDataMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    is_admin = Column(Integer, default=False)


class Post(ModelDateDataMixin):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    country = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    group_size = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)

