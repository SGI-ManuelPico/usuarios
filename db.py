from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Conexión a la primera base de datos
HOST = 'localhost'
USER = 'root'
PASSWORD = '12345678'
DATABASE1 = 'test'

DATABASE_URL1 = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DATABASE1}"
engine_db1 = create_engine(DATABASE_URL1)
Session_db1 = sessionmaker(bind=engine_db1)

# Conexión a la segunda base de datos
DATABASE2 = 'test2'

DATABASE_URL2 = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DATABASE2}"
engine_db2 = create_engine(DATABASE_URL2)
Session_db2 = sessionmaker(bind=engine_db2)

# Funciones para obtener las sesiones de cada base de datos
def get_session_db1():
    return Session_db1()

def get_session_db2():
    return Session_db2()
