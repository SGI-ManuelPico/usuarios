from dbTest import ConexionDB
import bcrypt

def actualizar_password(db, cedula, password_decrypted):
    # Encrypt the password
    password_encrypted = bcrypt.hashpw(password_decrypted.encode('utf-8'), bcrypt.gensalt())
    conn = db.establecerConexion()
    cursor = conn.cursor()
    # Update the password in the database
    query = "UPDATE usuario SET password = %s WHERE cedula = %s"
    cursor.execute(query, (password_encrypted, cedula))
    conn.commit()
    print("Password actualizado correctamente.")

    # Close the connection
    db.cerrarConexion()

if __name__ == "__main__":
        db_config = {
            "host": "srv1182.hstgr.io",
            "user": "u438914854_prueba",
            "password": "!Tn3X(_mp@Kio[h",
            "database": "u438914854_prueba"
        }

        db = ConexionDB(**db_config)
        cedula = 0000
        password_decrypted = "antiguos"
        actualizar_password(db, cedula, password_decrypted)

