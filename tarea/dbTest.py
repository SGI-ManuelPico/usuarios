import mysql.connector

class ConexionDB:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None

    def establecerConexion(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return self.conn
        except mysql.connector.Error as e:
            print(f"Error de conexión: {e}")
            return None

    def cerrarConexion(self):
        if self.conn:
            self.conn.close()
