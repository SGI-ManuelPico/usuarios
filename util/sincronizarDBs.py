from util.db import get_session_db1, get_session_db2
from sqlalchemy import MetaData, Table

session_db1 = get_session_db1()
session_db2 = get_session_db2()

metadata = MetaData()

tabla_usuarios_db1 = Table('usuario', metadata, autoload_with=session_db1.bind)
tabla_usuarios_db2 = Table('usuario', metadata, autoload_with=session_db2.bind)

# Sincronización de datos
def sincronizar_tablas():
    usuarios_db1 = session_db1.execute(tabla_usuarios_db1.select()).fetchall()

    for usuario in usuarios_db1:
        existe = session_db2.execute(
            tabla_usuarios_db2.select().where(tabla_usuarios_db2.c.cedula == usuario.cedula)
        ).fetchone()

        if existe:

            session_db2.execute(
                tabla_usuarios_db2.update()
                .where(tabla_usuarios_db2.c.cedula == usuario.cedula)
                .values(
                    nombre=usuario.nombre,
                    cargo=usuario.cargo,
                    correoPersonal=usuario.correoPersonal,
                    correo=usuario.correo,
                    celular=usuario.celular,
                    direccion=usuario.direccion,
                    idProyecto=usuario.idProyecto,
                    codigoSubcentroCostos=usuario.codigoSubcentroCostos,
                    idSede=usuario.idSede,
                    idArea=usuario.idArea,
                    estado=usuario.estado,
                    tipoDocumento=usuario.tipoDocumento,
                    genero=usuario.genero,
                    fechaIngreso=usuario.fechaIngreso,
                    fechaVencimiento=usuario.fechaVencimiento,
                    password=usuario.password,  
                )
            )
        else:
           
            session_db2.execute(
                tabla_usuarios_db2.insert().values(
                    cedula=usuario.cedula,
                    nombre=usuario.nombre,
                    cargo=usuario.cargo,
                    correoPersonal=usuario.correoPersonal,
                    correo=usuario.correo,
                    celular=usuario.celular,
                    direccion=usuario.direccion,
                    idProyecto=usuario.idProyecto,
                    codigoSubcentroCostos=usuario.codigoSubcentroCostos,
                    idSede=usuario.idSede,
                    idArea=usuario.idArea,
                    estado=usuario.estado,
                    tipoDocumento=usuario.tipoDocumento,
                    genero=usuario.genero,
                    fechaIngreso=usuario.fechaIngreso,
                    fechaVencimiento=usuario.fechaVencimiento,
                    password=usuario.password,
                )
            )

    session_db2.commit()

# Ejecutar la sincronización
sincronizar_tablas()

# Cerrar las sesiones
session_db1.close()
session_db2.close()
