
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

Base = declarative_base()

def initialize_database(session):
    # This could include scripts to create tables if they don't exist, or migrate
    Base.metadata.create_all(bind=session.get_bind())


def get_db_session(database_url=None):
    if database_url is None:
        database_url = os.getenv("STACKOVERFLOW_DATA_PATH", "sqlite:///./data/stackoverflow.db")
    engine = create_engine(database_url, connect_args={"check_same_thread": False} if "sqlite" in database_url else {})
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    return SessionLocal()
```

```plaintext
