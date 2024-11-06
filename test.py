from db import get_session
from usuario import Usuario

# Start a new session
session = get_session()

# Fetch all records from the usuario table using ORM
existing_users = session.query(Usuario).all()

user_data = [
    {
        "cedula": user.cedula,
        "nombre": user.nombre,
        "cargo": user.cargo,
        "correoPersonal": user.correoPersonal,
        "correo": user.correo,
        "celular": user.celular,
        "password": user.password,
        "direccion": user.direccion,
        "idProyecto": user.idProyecto,
        "codigoSubcentroCostos": user.codigoSubcentroCostos,
        "idSede": user.idSede,
        "idArea": user.idArea,
        "estado": user.estado,
        "tipoDocumento": user.tipoDocumento,
        "genero": user.genero,
        "foto": user.foto,
        "fechaIngreso": user.fechaIngreso,
        "fechaVencimiento": user.fechaVencimiento
    }
    for user in existing_users
]

# Convert to a DataFrame if needed
import pandas as pd
df = pd.DataFrame(user_data)

# Close the session
session.close()

# Display the DataFrame (optional)
print(df)