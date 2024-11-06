import pandas as pd
from db import get_session
from usuario import Usuario
from difflib import get_close_matches

codigosSubcentros = r'files\SubcentrosF.xlsx'
ref_df = pd.read_excel(codigosSubcentros)

excelUsuariosNuevos = r'files\Usuarios Noviembre 6.xlsx'
df = pd.read_excel(excelUsuariosNuevos)

# Create a dictionary for quick lookup by 'Subcentro de Costo' name
subcentro_dict = dict(zip(ref_df['Subcentro de Costo'], ref_df['Código']))

# Function to find the closest match using difflib
def mejorMatch(subcentro_name, threshold=0.87):
    # Check for an exact match first
    if subcentro_name in subcentro_dict:
        return subcentro_dict[subcentro_name]
    # Find close matches with a threshold
    matches = get_close_matches(subcentro_name, subcentro_dict.keys(), n=1, cutoff=threshold)
    # Return the code if a close match is found
    return subcentro_dict[matches[0]] if matches else None


# Apply function to get `codigoSubcentroCostos`
def getCodigoSubcentro(centro_costo):
    if '-' in centro_costo:
        # Extract code if present
        return centro_costo.split('-')[0]
    else:
        # Use sequence matching for approximate name matching
        return mejorMatch(centro_costo)

session = get_session()
ids_existentes = {usuario.cedula for usuario in session.query(Usuario.cedula).all()}
session.close()
df['codigoSubcentroCostos'] = df['CENTRO_COSTO'].apply(getCodigoSubcentro)


nuevosUsuarios = df[~df['IDENTIFICACION'].isin(ids_existentes)]


nuevosUsuariosAct = pd.DataFrame()
nuevosUsuariosAct['cedula'] = nuevosUsuarios['IDENTIFICACION']
nuevosUsuariosAct['nombre'] = nuevosUsuarios['NOMBRE COMPLETO']
nuevosUsuariosAct['cargo'] = nuevosUsuarios['CARGO']
nuevosUsuariosAct['correoPersonal'] = nuevosUsuarios['CORREO ELECTRONICO']
nuevosUsuariosAct['correo'] = None
nuevosUsuariosAct['celular'] = nuevosUsuarios['CELULAR']
nuevosUsuariosAct['codigoSubcentroCostos'] = nuevosUsuarios['codigoSubcentroCostos']
nuevosUsuariosAct['direccion'] = nuevosUsuarios['DIRECCION']
nuevosUsuariosAct['idProyecto'] = None
nuevosUsuariosAct['estado'] = None
nuevosUsuariosAct['tipoDocumento'] = None
nuevosUsuariosAct['genero'] = None
nuevosUsuariosAct['foto'] = None
nuevosUsuariosAct['fechaIngreso'] = pd.to_datetime(nuevosUsuarios['FECHA INGRESO'], errors='coerce')
nuevosUsuariosAct['fechaVencimiento'] = pd.to_datetime(nuevosUsuarios['FECHA VENCIMIENTO'], errors='coerce')

print(df[['CENTRO_COSTO', 'codigoSubcentroCostos']])

print(nuevosUsuariosAct['codigoSubcentroCostos'].head(20))
