from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Replace with your actual PostgreSQL credentials and database name
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin@localhost:5432/vidyasaarthi_db"

# The engine manages the connection pool
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()