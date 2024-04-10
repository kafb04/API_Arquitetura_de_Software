import psycopg2

class Conexao(object):
    
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def conectar(self):
        try:
            connection = psycopg2.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return connection
        except psycopg2.Error as e:
            print("Erro ao conectar ao banco de dados:", e)
            return None
