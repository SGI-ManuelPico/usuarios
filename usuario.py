from sqlalchemy import Column, Integer, String, Date, BigInteger, Text, LargeBinary
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Usuario(Base):
    __tablename__ = 'usuario'
    
    cedula = Column(Integer, primary_key=True)                
    nombre = Column(String(60))                               
    cargo = Column(String(80))                                
    correoPersonal = Column(String(50))                    
    correo = Column(String(50))                               
    celular = Column(String(20))                              
    password = Column(String(150))                            
    direccion = Column(String(255))                           
    idProyecto = Column(Integer)                              
    codigoSubcentroCostos = Column(String(10))                
    idSede = Column(Integer)                                  
    idArea = Column(Integer)                                  
    estado = Column(Integer)                                  
    tipoDocumento = Column(String(50))                       
    genero = Column(String(15))                               
    foto = Column(LargeBinary)                              
    fechaIngreso = Column(Date)                              
    fechaVencimiento = Column(Date)


                          
