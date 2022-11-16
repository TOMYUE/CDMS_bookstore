from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123456@localhost/tangyue"

# initialization
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# connect to local database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# create declarative_base instance
Base = declarative_base()


def conn_db():
    db_session = SessionLocal()
    try:
        return db_session
    except:
        db_session.close()


def create_table():
    Base.metadata.create_all(engine)


db_session = conn_db()
create_table()