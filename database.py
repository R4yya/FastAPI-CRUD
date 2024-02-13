from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# SQLALCHEMY_URL = 'sqlite:///./sql_app.db'
SQLALCHEMY_URL = 'sqlite:///./test_db.db'
engine = create_engine(SQLALCHEMY_URL, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
