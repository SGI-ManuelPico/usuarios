import pandas as pd
from sqlalchemy import create_engine
from db import get_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import update
from usuario import Usuario 
from actualizarUsuarios import getCodigoSubcentro, getIdProyecto

# Load the Excel file
excel_df = pd.read_excel(r"files\Usuarios Noviembre 6.xlsx")  # Replace with actual path

# Calculate 'codigoSubcentroCostos' and 'idProyecto' for each row in the Excel data
excel_df['codigoSubcentroCostos'] = excel_df['CENTRO_COSTO'].apply(getCodigoSubcentro)
excel_df['idProyecto'] = excel_df['codigoSubcentroCostos'].apply(getIdProyecto)
# Replace NaN with None in the DataFrame to ensure no NaN values are passed to SQL
excel_df = excel_df.where(pd.notnull(excel_df), None)

# Get a new session
session = get_session()

# Iterate over each row in the Excel file
# for index, row in excel_df.iterrows():
#     # Query the usuario table for the matching cedula
#     usuario = session.query(Usuario).filter_by(cedula=row['IDENTIFICACION']).first()
    
#     if usuario:
#         # Update fechaIngreso and fechaVencimiento if they exist in Excel
#         if pd.notnull(row['FECHA INGRESO']):
#             usuario.fechaIngreso = row['FECHA INGRESO']
#         if pd.notnull(row['FECHA VENCIMIENTO']):
#             usuario.fechaVencimiento = row['FECHA VENCIMIENTO']
        
#         # Commit changes to the session
#         session.commit()


# Iterate over each row in the Excel DataFrame
# for index, row in excel_df.iterrows():
#     # Find the existing user by 'cedula'
#     usuario = session.query(Usuario).filter_by(cedula=row['IDENTIFICACION']).first()
    
#     if usuario:
#         # Update only the fields if they are not None
#         if row['codigoSubcentroCostos'] is not None:
#             usuario.codigoSubcentroCostos = row['codigoSubcentroCostos']
#         if row['idProyecto'] is not None:
#             usuario.idProyecto = row['idProyecto']
#         session.commit()  # Commit after each update

# Close the session
session.close()
print(excel_df)
print("Database updated with new codigoSubcentroCostos and idProyecto where applicable.")


