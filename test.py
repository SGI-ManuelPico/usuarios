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

# Establecer conexiones
conn1 = db1.establecerConexion()
conn2 = db2.establecerConexion()

cursor1 = conn1.cursor(dictionary=True)
cursor2 = conn2.cursor()

# Obtener todos los registros de la tabla informacionbancaria en la base origen
cursor1.execute("SELECT * FROM informacionbancaria")
registros_origen = cursor1.fetchall()

if not registros_origen:
    print("No se encontraron registros en la tabla origen (informacionbancaria).")
else:
    for registro in registros_origen:
        try:
            # Verificar si el registro ya existe en la base destino
            cursor2.execute(
                "SELECT cedula FROM informacionbancaria WHERE cedula = %s",
                (registro['cedula'],)
            )
            registro_destino = cursor2.fetchone()

            if not registro_destino:
                # Insertar el registro si no existe
                print(f"Insertando registro con cedula = {registro['cedula']}...")
                columnas_insert = ", ".join([
                    "cedula", "idBanco", "cuentaBancaria", "tipoTransaccion", "tipoCuenta"
                ])
                valores_insert = ", ".join(["%s"] * 5)
                valores = [
                    registro['cedula'], registro['idBanco'], registro['cuentaBancaria'],
                    registro['tipoTransaccion'], registro['tipoCuenta']
                ]
                cursor2.execute(
                    f"INSERT INTO informacionbancaria ({columnas_insert}) VALUES ({valores_insert})",
                    valores
                )
                conn2.commit()  # Confirmar después de cada inserción

        except Exception as e:
            print(f"Error al procesar el registro con cedula = {registro['cedula']}: {e}")

# Cerrar cursores
cursor1.close()
cursor2.close()
