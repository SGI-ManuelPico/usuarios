from dbTest import ConexionDB
from mysql.connector import Error

# Configuración de las bases de datos
db1 = ConexionDB(
    host="srv1182.hstgr.io",
    user="u438914854_prueba",
    password="!Tn3X(_mp@Kio[h",
    database="u438914854_prueba"  
)

db2 = ConexionDB(
    host="srv1182.hstgr.io",
    user="u438914854_dsoftwaresgi",
    password="C'M9UTwDBMkowe+A#",
    database="u438914854_baseDatosSGI"  
)

def sincronizar_tablas():
    """
    Sincroniza los datos de la tabla `usuario` entre dos bases de datos.
    """

    conn1 = db1.establecerConexion()
    conn2 = db2.establecerConexion()

    if conn1 and conn2:
        try:
            cursor1 = conn1.cursor(dictionary=True)
            cursor2 = conn2.cursor()

            # Obtener todos los registros de la tabla `usuario` de la base desarrolloSGI
            cursor1.execute("SELECT * FROM usuario")
            usuarios_origen = cursor1.fetchall()

            for usuario in usuarios_origen:
                # Verificar si el registro ya existe en la base prueba
                cursor2.execute(
                    "SELECT * FROM usuario WHERE cedula = %s",
                    (usuario['cedula'],)
                )
                usuario_destino = cursor2.fetchone()

                if usuario_destino:
                    # Actualizar el registro si ya existe
                    cursor2.execute(
                        """
                        UPDATE usuario SET
                            nombre = %s,
                            cargo = %s,
                            correoPersonal = %s,
                            correo = %s,
                            celular = %s,
                            direccion = %s,
                            idProyecto = %s,
                            codigoSubcentroCostos = %s,
                            idSede = %s,
                            idArea = %s,
                            estado = %s,
                            tipoDocumento = %s,
                            genero = %s,
                            fechaIngreso = %s,
                            fechaVencimiento = %s,
                            password = %s
                        WHERE cedula = %s
                        """,
                        (
                            usuario['nombre'], usuario['cargo'], usuario['correoPersonal'],
                            usuario['correo'], usuario['celular'], usuario['direccion'],
                            usuario['idProyecto'], usuario['codigoSubcentroCostos'],
                            usuario['idSede'], usuario['idArea'], usuario['estado'],
                            usuario['tipoDocumento'], usuario['genero'],
                            usuario['fechaIngreso'], usuario['fechaVencimiento'],
                            usuario['password'], usuario['cedula']
                        )
                    )
                else:
                    # Insertar el registro si no existe
                    cursor2.execute(
                        """
                        INSERT INTO usuario (
                            cedula, nombre, cargo, correoPersonal, correo, celular,
                            direccion, idProyecto, codigoSubcentroCostos, idSede,
                            idArea, estado, tipoDocumento, genero, fechaIngreso,
                            fechaVencimiento, password
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            usuario['cedula'], usuario['nombre'], usuario['cargo'],
                            usuario['correoPersonal'], usuario['correo'], usuario['celular'],
                            usuario['direccion'], usuario['idProyecto'], usuario['codigoSubcentroCostos'],
                            usuario['idSede'], usuario['idArea'], usuario['estado'],
                            usuario['tipoDocumento'], usuario['genero'],
                            usuario['fechaIngreso'], usuario['fechaVencimiento'],
                            usuario['password']
                        )
                    )

            conn2.commit()

        except Error as e:
            print(f"Error durante la sincronización: {e}")
        finally:
            cursor1.close()
            cursor2.close()
            db1.cerrarConexion()
            db2.cerrarConexion()
    else:
        print("No se pudo establecer la conexión con una o ambas bases de datos.")

# Llamar a la función de sincronización
sincronizar_tablas()
