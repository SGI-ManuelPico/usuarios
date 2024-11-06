from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "mysql+mysqlconnector://root:12345678@localhost/test"

engine = create_engine(DATABASE_URL)


Session = sessionmaker(bind=engine)

def get_session():
    return Session()
