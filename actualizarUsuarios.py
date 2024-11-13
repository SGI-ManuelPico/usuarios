import pandas as pd
from db import get_session_db1
from usuario import Base, Usuario
from difflib import get_close_matches
import re
import bcrypt

# Función para cargar datos
def cargarDatos():
    codigosSubcentros = r'files\SubcentrosF.xlsx'
    refDf = pd.read_excel(codigosSubcentros)
    
    excelUsuariosNuevos = r'files\Usuarios Noviembre 6.xlsx'
    df = pd.read_excel(excelUsuariosNuevos)
    
    # Normalizar los nombres en los datos de referencia a minúsculas y eliminar espacios adicionales
    refDf['Subcentro de Costo'] = refDf['Subcentro de Costo'].str.lower().str.strip()
    df['CENTRO_COSTO'] = df['CENTRO_COSTO'].str.lower().str.strip()
    
    return refDf, df

# Función para crear diccionario de subcentros
def crearDiccionarioSubcentro(refDf):
    return {k: v.upper() for k, v in zip(refDf['Subcentro de Costo'], refDf['Código'])}

# Función para encontrar la coincidencia más cercana para el código del subcentro
def mejorCoincidencia(nombreSubcentro, diccionarioSubcentro, umbral=0.8):
    if nombreSubcentro in diccionarioSubcentro:
        return diccionarioSubcentro[nombreSubcentro]
    coincidencias = get_close_matches(nombreSubcentro, diccionarioSubcentro.keys(), n=1, cutoff=umbral)
    return diccionarioSubcentro[coincidencias[0]].upper() if coincidencias else None

# Función para obtener `codigoSubcentroCostos` de `CENTRO_COSTO`
def obtenerCodigoSubcentro(centroCosto, diccionarioSubcentro):
    casosEspeciales = ['labotatorio frontera-c2217', 'frontera quifa y cajua cto c-856']
    if '-' in centroCosto and centroCosto not in casosEspeciales and 'perenco' not in centroCosto:
        # Extraer el código si tiene un guion pero no está en casos especiales ni contiene "perenco"
        codigo = centroCosto.split('-')[0].strip().upper()
        if re.match(r'^[EAIOLeaio][0-9]+', codigo):
            return codigo
    elif 'perenco' in centroCosto:
        return 'L21510201'  
    elif 'transversal' in centroCosto:
        return 'E2100'  
    elif 'labotatorio frontera-c2217' in centroCosto:
        return 'L241223' 
    elif 'frontera quifa y cajua cto c-856' in centroCosto:
        return mejorCoincidencia('frontera quifa y cajua cto c-856', diccionarioSubcentro)
    else:
        return mejorCoincidencia(centroCosto, diccionarioSubcentro)

def obtenerIdProyecto(codigoSubcentro):
    if codigoSubcentro is None:
        return None 
    if codigoSubcentro.startswith('A'):
        return 1
    elif codigoSubcentro.startswith('E'):
        return 2
    elif codigoSubcentro.startswith('L'):
        return 3
    elif codigoSubcentro.startswith('I'):
        return 4
    elif codigoSubcentro.startswith('O'):
        return 5
    else:
        return None

# Preparar datos de nuevos usuarios
def prepararNuevosUsuarios(df, idsExistentes, diccionarioSubcentro):
    df['codigoSubcentroCostos'] = df['CENTRO_COSTO'].apply(lambda x: obtenerCodigoSubcentro(x, diccionarioSubcentro))
    df['idProyecto'] = df['codigoSubcentroCostos'].apply(obtenerIdProyecto)

    # Filtrar nuevos usuarios basados en IDs existentes
    nuevosUsuarios = df[~df['IDENTIFICACION'].isin(idsExistentes)]
    
    # Crear DataFrame para nuevos usuarios con las columnas necesarias
    nuevosUsuariosAct = pd.DataFrame({
        'cedula': nuevosUsuarios['IDENTIFICACION'],
        'nombre': nuevosUsuarios['NOMBRE COMPLETO'],
        'cargo': nuevosUsuarios['CARGO'],
        'correoPersonal': nuevosUsuarios['CORREO ELECTRONICO'],
        'correo': None,
        'celular': nuevosUsuarios['CELULAR'],
        'codigoSubcentroCostos': nuevosUsuarios['codigoSubcentroCostos'],
        'direccion': nuevosUsuarios['DIRECCION'],
        'idProyecto': nuevosUsuarios['codigoSubcentroCostos'].apply(obtenerIdProyecto),
        'estado': 1,
        'tipoDocumento': 'Cédula de ciudadanía',
        'genero': None,
        'foto': None,
        'fechaIngreso': pd.to_datetime(nuevosUsuarios['FECHA INGRESO'], errors='coerce'),
        'fechaVencimiento': pd.to_datetime(nuevosUsuarios['FECHA VENCIMIENTO'], errors='coerce')
    })

    return nuevosUsuariosAct

# Agregar nuevos usuarios
def agregarNuevosUsuarios(session, nuevosUsuariosAct):
    inserted_users = []  # Lista para almacenar usuarios insertados para verificación

    for _, row in nuevosUsuariosAct.iterrows():
        # Reemplazar valores NaT con None para las columnas de fecha
        fechaIngreso = row['fechaIngreso'] if pd.notnull(row['fechaIngreso']) else None
        fechaVencimiento = row['fechaVencimiento'] if pd.notnull(row['fechaVencimiento']) else None

        nuevoUsuario = Usuario(
            cedula=row['cedula'],
            nombre=row['nombre'],
            cargo=row['cargo'],
            correoPersonal=row['correoPersonal'],
            correo=row['correo'],
            celular=row['celular'],
            codigoSubcentroCostos=row['codigoSubcentroCostos'],
            direccion=row['direccion'],
            idProyecto=row['idProyecto'],
            idArea = 1,
            idSede = 1,
            estado=row['estado'],
            tipoDocumento=row['tipoDocumento'],
            genero=row['genero'],
            foto=row['foto'],
            fechaIngreso=fechaIngreso,
            fechaVencimiento=fechaVencimiento,
            password=None  # Dejar en None para asignar después
        )
        session.add(nuevoUsuario)
        # Agregar a la lista de verificación
        inserted_users.append(nuevoUsuario)
    session.commit()

    # Mostrar usuarios insertados
    print("\nUsuarios insertados:")
    for user in inserted_users:
        print(f"ID: {user.cedula}, Nombre: {user.nombre}")
    
    return inserted_users

# Función para asignar contraseña a los usuarios sin contraseña
def asignarContrasena(session):
    usuariosSinContrasena = session.query(Usuario).filter_by(password=None).all()
    
    print("\nAsignando contraseñas a usuarios sin contraseña:")
    for usuario in usuariosSinContrasena:
        # Crear la contraseña en el formato SGI<cedula>@
        contrasena = f"SGI{usuario.cedula}@"
        # Encriptar la contraseña con bcrypt
        hashedContrasena = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt())
        # Asignar la contraseña encriptada al usuario
        usuario.password = hashedContrasena
        # Imprimir para verificación
        print(f"Usuario ID: {usuario.cedula}, Contraseña asignada: {contrasena}")

    session.commit()

# Función para desactivar usuarios que ya no están en la empresa
def desactivarUsuariosAusentes(session, idsExistentes, idsExcel):
    # Encontrar usuarios en la base de datos pero no en el archivo Excel
    idsUsuariosAusentes = idsExistentes - idsExcel
    
    # Actualizar el campo `estado` a 0 para cada usuario ausente
    for cedula in idsUsuariosAusentes:
        usuario = session.query(Usuario).filter_by(cedula=cedula).first()
        if usuario:
            usuario.estado = 0
            session.commit()

def actualizarUsuariosExistentes(session, df):
    for _, row in df.iterrows():
        usuario = session.query(Usuario).filter_by(cedula=row['IDENTIFICACION']).first()
        if usuario:
            # Actualizar codigoSubcentroCostos y idProyecto si existen
            if row['codigoSubcentroCostos'] is not None:
                usuario.codigoSubcentroCostos = row['codigoSubcentroCostos']
            if row['idProyecto'] is not None:
                usuario.idProyecto = row['idProyecto']
            
            # Actualizar fechaIngreso y fechaVencimiento si existen
            fechaIngreso = row['FECHA INGRESO'] if pd.notnull(row['FECHA INGRESO']) else None
            fechaVencimiento = row['FECHA VENCIMIENTO'] if pd.notnull(row['FECHA VENCIMIENTO']) else None

            if fechaIngreso is not None:
                usuario.fechaIngreso = pd.to_datetime(fechaIngreso, errors='coerce')
            if fechaVencimiento is not None:
                usuario.fechaVencimiento = pd.to_datetime(fechaVencimiento, errors='coerce')
            
            session.commit()  # Guardar los cambios después de cada actualización
            print(f"Usuario {usuario.cedula} actualizado con fechaIngreso {usuario.fechaIngreso} y fechaVencimiento {usuario.fechaVencimiento}")


# Ejecución principal
if __name__ == "__main__":
    # Cargar datos y crear diccionario de subcentros
    refDf, df = cargarDatos()
    diccionarioSubcentro = crearDiccionarioSubcentro(refDf)
    
    # Iniciar sesión y obtener IDs de usuarios existentes
    session = get_session_db1()
    idsExistentes = {usuario.cedula for usuario in session.query(Usuario.cedula).all()}
    session.close()
    
    # Obtener IDs del archivo Excel
    idsExcel = set(df['IDENTIFICACION'].unique())
    
    # Preparar nuevos usuarios y actualizar los existentes
    nuevosUsuariosAct = prepararNuevosUsuarios(df, idsExistentes, diccionarioSubcentro)
    
    # Agregar nuevos usuarios a la base de datos y verificar los insertados
    session = get_session_db1()
    usuariosInsertados = agregarNuevosUsuarios(session, nuevosUsuariosAct)
    
    # Asignar contraseñas a usuarios sin contraseña
    asignarContrasena(session)
    
    # Desactivar usuarios que ya no están en la empresa
    desactivarUsuariosAusentes(session, idsExistentes, idsExcel)
    
    # Actualizar usuarios existentes en la base de datos
    actualizarUsuariosExistentes(session, df)
    
    session.close()