from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


from app.config import env_variables
# from app.features.aws.secretKey import get_secret_keys

env_data = env_variables()


engine = create_engine(env_data["DATABASE_URI"], pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def db_connection():
    db = SessionLocal()
    try:
        print("Opening db connection", db)
        yield db
    except Exception as e:
        print("Error in db_connection", e)
        db.rollback()
        raise
    finally:
        print("Closing db connection")
        db.close()
