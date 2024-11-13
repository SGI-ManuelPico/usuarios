from dbTest import ConexionDB

def sincronizar_tabla(conn1, conn2, tabla, clave_primaria, columnas):
    """
    Sincroniza una tabla entre dos bases de datos.
    Inserta únicamente registros nuevos y no actualiza registros existentes.

    Args:
        conn1: Conexión a la base de datos origen.
        conn2: Conexión a la base de datos destino.
        tabla: Nombre de la tabla a sincronizar.
        clave_primaria: Columna que actúa como clave primaria.
        columnas: Lista de columnas a sincronizar.
    """
    cursor1 = None
    cursor2 = None
    try:
        print(f"Iniciando sincronización de la tabla {tabla}...")
        cursor1 = conn1.cursor(dictionary=True)
        cursor2 = conn2.cursor()

        # Obtener todos los registros de la tabla en la base de datos origen
        cursor1.execute(f"SELECT {', '.join(columnas)} FROM {tabla}")
        registros_origen = cursor1.fetchall()

        if not registros_origen:
            print(f"No se encontraron registros en la tabla {tabla}.")
            return

        for registro in registros_origen:
            try:
                # Verificar si el registro ya existe en la tabla destino
                cursor2.execute(
                    f"SELECT {clave_primaria} FROM {tabla} WHERE {clave_primaria} = %s", 
                    (registro[clave_primaria],)
                )
                registro_destino = cursor2.fetchone()

                if not registro_destino:
                    # Insertar el registro si no existe
                    print(f"Insertando registro con {clave_primaria} = {registro[clave_primaria]}...")
                    columnas_insert = ", ".join(columnas)
                    valores_insert = ", ".join(["%s"] * len(columnas))
                    valores = [registro[col] for col in columnas]
                    cursor2.execute(
                        f"INSERT INTO {tabla} ({columnas_insert}) VALUES ({valores_insert})",
                        valores
                    )
                    conn2.commit()  # Confirmar los cambios después de cada inserción

            except Exception as e:
                print(f"Error al procesar el registro con {clave_primaria} = {registro[clave_primaria]}: {e}")

        print(f"Sincronización de la tabla {tabla} completada.")

    except Exception as e:
        print(f"Error general al sincronizar la tabla {tabla}: {e}")
    finally:
        if cursor1:
            cursor1.close()
        if cursor2:
            cursor2.close()


def sincronizarTablaConexion(config, db_config):
    """
    Sincroniza una tabla con su propia conexión.

    Args:
        config: Diccionario con la configuración de la tabla (nombre, clave primaria, columnas).
        db_config: Configuración para conectarse a la base de datos.
    """
    db_origen = ConexionDB(**db_config['origen'])
    db_destino = ConexionDB(**db_config['destino'])

    conn1 = db_origen.establecerConexion()
    conn2 = db_destino.establecerConexion()

    if conn1 and conn2:
        try:
            sincronizar_tabla(
                conn1, conn2,
                tabla=config["tabla"],
                clave_primaria=config["clave_primaria"],
                columnas=config["columnas"]
            )
        except Exception as e:
            print(f"Error al sincronizar la tabla {config['tabla']}: {e}")
        finally:
            db_origen.cerrarConexion()
            db_destino.cerrarConexion()
    else:
        print(f"Error al conectar para la tabla {config['tabla']}.")


def sincronizarTodo():
    """
    Sincroniza todas las tablas usando conexiones separadas para cada una.
    """
    tablas = [
        {
            "tabla": "usuario",
            "clave_primaria": "cedula",
            "columnas": [
                "cedula", "nombre", "cargo", "correoPersonal", "correo",
                "celular", "direccion", "idProyecto", "codigoSubcentroCostos",
                "idSede", "idArea", "estado", "tipoDocumento", "genero",
                "fechaIngreso", "fechaVencimiento", "password"
            ]
        },
        {
            "tabla": "informacionbancaria",
            "clave_primaria": "cedula",
            "columnas": [
                "cedula", "idBanco", "cuentaBancaria", "tipoTransaccion", "tipoCuenta"
            ]
        }
    ]

    db_config = {
        "origen": {
            "host": "srv1182.hstgr.io",
            "user": "u438914854_prueba",
            "password": "!Tn3X(_mp@Kio[h",
            "database": "u438914854_prueba"
        },
        "destino": {
            "host": "srv1182.hstgr.io",
            "user": "u438914854_dsoftwaresgi",
            "password": "C'M9UTwDBMkowe+A#",
            "database": "u438914854_baseDatosSGI"
        }
    }

    for config in tablas:
        sincronizarTablaConexion(config, db_config)
