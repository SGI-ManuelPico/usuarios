import pandas as pd
import re
from difflib import SequenceMatcher

# Función para normalizar nombres
def normalizarNombre(name):
    name = name.lower()
    name = re.sub(r'\s+', ' ', name)
    name = re.sub(r'[^a-z\s]', '', name)
    return name.strip()

# Función para calcular la similitud entre dos nombres
def similar(a, b):
    return SequenceMatcher(None, normalizarNombre(a), normalizarNombre(b)).ratio()

# Función para encontrar coincidencias entre dos dataframes (esta es más para debuggear)
def find_matches(df1, df2, threshold):
    matches = []
    for i, row1 in df1.iterrows():
        name1 = str(row1['Nombre'])
        for j, row2 in df2.iterrows():
            name2 = str(row2['Nombre'])
            try:
                similarity = similar(name1, name2)
                if similarity >= threshold:
                    matches.append((name1, name2, similarity))
            except Exception as e:
                print(f"Error comparando {name1} y {name2}: {e}")
    return pd.DataFrame(matches, columns=['Nombre_df1', 'Nombre_df2', 'Similitud']), matches

# Función para encontrar las mejores coincidencias de correos electrónicos basados en la similitud de nombres
def matchesCorreo(df1, df2, threshold=0.8):
    matches = []
    for i, row1 in df1.iterrows():
        name1 = str(row1['Nombre'])
        mejorMatch = ""
        mejorSimilitud = 0
        for j, row2 in df2.iterrows():
            name2 = str(row2['Nombre'])
            try:
                similarity = similar(name1, name2)
                if similarity > mejorSimilitud and similarity >= threshold:
                    mejorMatch = row2['CorreoCorp']
                    mejorSimilitud = similarity
            except Exception as e:
                print(f"Error comparando {name1} y {name2}: {e}")
        matches.append(mejorMatch if mejorMatch else "")
    return matches

# Función principal
def main():
    # Cargar datos (cambiar por la más reciente)
    rutaUsuarios = 'Usuarios_Completos1.csv'
    
    usuario_comp = pd.read_csv(rutaUsuarios)

    # Modificar estructura del dataframe
    usuario_comp.insert(usuario_comp.columns.get_loc('Correo') + 1, 'CorreoSgi', '')
    usuario_comp.rename(columns={'Correo': 'correoPersonal'}, inplace=True)
   

    df1 = usuario_comp

    # Cargar datos externos para comparación (cambiar por la más reciente)
    rutaCorreos = r"C:\Users\Soporte\Downloads\Libro3.xlsx"

    df2 = pd.read_excel(rutaCorreos)[['Nombre para mostrar', 'Nombre principal de usuario']]
    df2.rename(columns={'Nombre principal de usuario': 'CorreoCorp', 'Nombre para mostrar':'Nombre'}, inplace=True)

    # Encontrar coincidencias con un umbral de similitud del 80%
    # matches_df, matches = find_matches(df1, df2, threshold=0.8)
    matches_correo = matchesCorreo(df1, df2, threshold=0.8)

    # Actualizar df1 con correos electrónicos corporativos coincidentes
    df1['CorreoCorp'] = matches_correo

    # Reemplazar correos electrónicos corporativos vacíos con correos electrónicos personales
    df1['CorreoCorp'] = df1.apply(
        lambda row: row['correoPersonal'] if pd.isna(row['CorreoCorp']) or row['CorreoCorp'] == "" else row['CorreoCorp'],
        axis=1
    )

    # Obtener la posición de la columna 'CorreoSgi' y eliminarla
    col_position = df1.columns.get_loc('CorreoSgi')
    df1 = df1.drop(columns=['CorreoSgi'])

    # Insertar 'CorreoCorp' en la posición original de 'CorreoSgi'
    df1.insert(col_position, 'CorreoCorp', df1.pop('CorreoCorp'))

    # Renombrar 'CorreoCorp' a 'correoSGI'
    df1 = df1.rename(columns={'CorreoCorp': 'correoSGI'})

    df_S = df1[['Nombre', 'Cargo', 'correoSGI']]

    df_S.to_excel('usuarios.xlsx', index=False)

    print(df1['correoSGI'])

if __name__ == "__main__":
    main()
