from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import get_settings

settings = get_settings()

engine = create_engine(
    settings.database_url,
    echo = settings.debug,
    pool_pre_ping= True,
)

SessionLocal = sessionmaker(
    bind = engine,
    autoflush=False,
    autocommit = False,
)


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()