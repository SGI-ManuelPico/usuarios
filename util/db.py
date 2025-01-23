from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dataclasses import dataclass

@dataclass
class db:
    host: str
    user: str
    password: str   
    database: str
    conexion = None

    def establecerConexion(self):
        try:
            self.conexion = create_engine(
                f"mysql+mysqlconnector://{self.user}:{self.password}@{self.host}/{self.database}"
            )
            return self.conexion
        except Exception as e:
            print(f"Error de conexión: {e}")
            return None
    
    def cerrarConexion(self):
        if self.conexion:
            self.conexion.close()     

    def getSession(self):
        if self.conexion:
            return sessionmaker(bind=self.conexion)()
        else:
            return None  

    
