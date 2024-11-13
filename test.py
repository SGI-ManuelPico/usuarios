from dbTest import ConexionDB
from mysql.connector import Error

# Configuración de las bases de datos
db1 = ConexionDB(
    host="srv1182.hstgr.io",
    user="u438914854_prueba",
    password="!Tn3X(_mp@Kio[h",
    database="u438914854_prueba"  #
)

db2 = ConexionDB(
    host="srv1182.hstgr.io",
    user="u438914854_dsoftwaresgi",
    password="C'M9UTwDBMkowe+A#",
    database="u438914854_baseDatosSGI" 
)

con1 = db1.establecerConexion()
con2 = db2.establecerConexion()

if con2:
    print("Conexión exitosa a la base de datos destino.")