from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Conexión a la primera base de datos
HOST1 = 'srv1182.hstgr.io'
USER1 = 'u438914854_prueba	'
PASSWORD1 = '!Tn3X(_mp@Kio[h'
DATABASE1 = 'u438914854_prueba'

DATABASE_URL1 = f"mysql+pymysql://{USER1}:{PASSWORD1}@{HOST1}/{DATABASE1}"
engine_db1 = create_engine(DATABASE_URL1)
Session_db1 = sessionmaker(bind=engine_db1)

# Conexión a la segunda base de datos
HOST2 = 'srv1182.hstgr.io'
USER2 = 'u438914854_dsoftwaresgi'
PASSWORD2 = "C'M9UTwDBMkowe+A#"
DATABASE2 = 'u438914854_baseDatosSGI'

DATABASE_URL2 = f"mysql+pymysql://{USER2}:{PASSWORD2}@{HOST2}/{DATABASE2}"
engine_db2 = create_engine(DATABASE_URL2)
Session_db2 = sessionmaker(bind=engine_db2)

# Funciones para obtener las sesiones de cada base de datos
def get_session_db1():
    print(f'Conectando a la base de datos {DATABASE1}')
    return Session_db1()

def get_session_db2():
    print(f'Conectando a la base de datos {DATABASE2}')
    return Session_db2()
