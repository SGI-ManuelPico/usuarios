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
        cursor2 = conn2.cursor(dictionary=True)

        # 1) Traer todos los registros de la tabla origen
        cursor1.execute(f"SELECT {', '.join(columnas)} FROM {tabla}")
        registros_origen = cursor1.fetchall()

        if not registros_origen:
            print(f"No se encontraron registros en la tabla {tabla} en la BD origen.")
            return

        # 2) Obtener todas las claves primarias existentes en la BD destino de una sola vez
        cursor2.execute(f"SELECT {clave_primaria} FROM {tabla}")
        claves_destino = cursor2.fetchall()

        # Convertir a un set para búsqueda rápida en O(1)
        claves_existentes = {fila[clave_primaria] for fila in claves_destino}

        # 3) Preparar los registros que se deben insertar porque NO existen en destino
        registros_a_insertar = []
        for registro in registros_origen:
            if registro[clave_primaria] not in claves_existentes:
                valores = [registro[col] for col in columnas]
                registros_a_insertar.append(valores)

        if not registros_a_insertar:
            print(f"Todos los registros de {tabla} ya existen en destino. Nada que insertar.")
            return

        # 4) Insertar en lotes usando executemany
        columnas_insert = ", ".join(columnas)
        valores_insert = ", ".join(["%s"] * len(columnas))

        query_insert = f"""
            INSERT INTO {tabla} ({columnas_insert}) 
            VALUES ({valores_insert})
        """

        cursor2.executemany(query_insert, registros_a_insertar)

        # 5) Hacer commit solo una vez luego de la inserción
        conn2.commit()

        print(f"Insertados {cursor2.rowcount} registros nuevos en la tabla {tabla}.")

    except Exception as e:
        print(f"Error general al sincronizar la tabla {tabla}: {e}")
    finally:
        if cursor1:
            cursor1.close()
        if cursor2:
            cursor2.close()


def sincronizarTodo():
    """
    Sincroniza todas las tablas necesarias usando una sola conexión
    a la BD de origen y otra a la BD de destino.
    """
    # Define las tablas a sincronizar y sus columnas
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

    # Configuración de conexiones de origen y destino
    db_config = {
        "destino": {
            "host": "srv1182.hstgr.io",
            "user": "u438914854_prueba",
            "password": "!Tn3X(_mp@Kio[h",
            "database": "u438914854_prueba"
        },
        "origen": {
            "host": "srv1182.hstgr.io",
            "user": "u438914854_dsoftwaresgi",
            "password": "C'M9UTwDBMkowe+A#",
            "database": "u438914854_baseDatosSGI"
        }
    }

    # Abrir las conexiones sólo una vez
    db_origen = ConexionDB(**db_config['origen'])
    db_destino = ConexionDB(**db_config['destino'])

    conn1 = db_origen.establecerConexion()
    conn2 = db_destino.establecerConexion()

    # Verificar que se pudo conectar a ambas bases de datos
    if not conn1 or not conn2:
        print("Error al conectar con la base de datos de origen o destino.")
        return

    try:
        # Recorrer cada tabla y sincronizar
        for config in tablas:
            try:
                sincronizar_tabla(
                    conn1,
                    conn2,
                    tabla=config["tabla"],
                    clave_primaria=config["clave_primaria"],
                    columnas=config["columnas"]
                )
            except Exception as e:
                print(f"Error al sincronizar la tabla {config['tabla']}: {e}")

    finally:
        # Cerrar las conexiones al terminar
        db_origen.cerrarConexion()
        db_destino.cerrarConexion()
        print("Proceso de sincronización finalizado.")
