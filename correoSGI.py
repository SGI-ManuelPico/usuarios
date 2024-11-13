import pandas as pd
import re
from difflib import SequenceMatcher
from db import get_session_db1
from usuario import Usuario

# Función para normalizar nombres
def normalizarNombre(nombre):
    nombre = nombre.lower()
    nombre = re.sub(r'\s+', ' ', nombre)
    nombre = re.sub(r'[^a-z\s]', '', nombre)
    return nombre.strip()

# Función para calcular la similitud entre dos nombres
def similitudNombres(nombreA, nombreB):
    return SequenceMatcher(None, normalizarNombre(nombreA), normalizarNombre(nombreB)).ratio()

# Función para encontrar y asignar correos corporativos a usuarios en la base de datos
def actualizarCorreosCorporativos(rutaCorreos, umbral=0.8):
    # Cargar datos externos para comparación
    dfCorreos = pd.read_excel(rutaCorreos)[['Nombre para mostrar', 'Nombre principal de usuario']]
    dfCorreos.rename(columns={'Nombre para mostrar': 'nombre', 'Nombre principal de usuario': 'correoCorp'}, inplace=True)
    
    # Iniciar sesión con la base de datos
    session = get_session_db1()
    
    # Obtener todos los usuarios de la tabla `usuario`
    usuariosBD = session.query(Usuario).all()
    
    # Lista para almacenar coincidencias para verificación
    coincidencias = []

    # Recorrer cada usuario en la base de datos
    for usuario in usuariosBD:
        mejorCorreo = None
        mejorSimilitud = 0

        # Comparar el nombre del usuario con cada nombre en el archivo de correos
        for _, row in dfCorreos.iterrows():
            nombreCorreo = row['nombre']
            correoCorporativo = row['correoCorp']
            
            # Calcular la similitud
            similitud = similitudNombres(usuario.nombre, nombreCorreo)
            
            # Asignar el mejor correo basado en el umbral de similitud
            if similitud > mejorSimilitud and similitud >= umbral:
                mejorCorreo = correoCorporativo
                mejorSimilitud = similitud

        # Si se encontró una coincidencia, actualizar el campo de correo en la base de datos
        if mejorCorreo:
            usuario.correo = mejorCorreo
            coincidencias.append((usuario.nombre, mejorCorreo, mejorSimilitud))
            print(f"Actualizado correo de {usuario.nombre} a {mejorCorreo} (Similitud: {mejorSimilitud:.2f})")

    # Confirmar los cambios en la base de datos
    session.commit()
    session.close()

    # Mostrar las coincidencias encontradas
    print("\nCoincidencias encontradas:")
    for nombre, correo, similitud in coincidencias:
        print(f"Nombre: {nombre}, Correo Corporativo: {correo}, Similitud: {similitud:.2f}")

# Ejecución principal
if __name__ == "__main__":
    # Ruta al archivo de correos corporativos
    rutaCorreos = r'files\CorreosSGI.xlsx'  

    # Actualizar correos corporativos en la base de datos
    actualizarCorreosCorporativos(rutaCorreos)
