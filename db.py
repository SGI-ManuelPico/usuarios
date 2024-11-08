from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Conexión a la base de datos
HOST = 'localhost'
USER = 'root'
PASSWORD = '12345678'
DATABASE = 'test2'

DATABASE_URL = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DATABASE}"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def get_session():
    return Session()
