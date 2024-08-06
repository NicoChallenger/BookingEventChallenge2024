from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# use local sqlite db 
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# setup engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# create session class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create base class
Base = declarative_base()

# Handle for dependency injection of database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()