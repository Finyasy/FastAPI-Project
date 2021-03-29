from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#database uri
SQLALCHEMY_DATABASE_URI = 'sqlite:///tododb.db'

engine = create_engine(SQLALCHEMY_DATABASE_URI,connect_args={"check_same_thread":False},echo=True)

#Talk to db
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

#class to describe our db
Base = declarative_base()

#dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()