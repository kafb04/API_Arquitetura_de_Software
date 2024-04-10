import psycopg2

class Aeroporto:
    def __init__(self, conexao):
        self.conexao = conexao

    def obter_aeroportos(self):
        connection = self.conexao.conectar()
        if connection is None:
            return None

        cursor = connection.cursor()
        try:
            cursor.execute("SELECT codigo, nome, cidade, estado FROM aeroportos")
            aeroportos = cursor.fetchall()

            if not aeroportos:
                return "Nenhum aeroporto encontrado"
            
            else:
                aeroportos_formatados = []
                for aeroporto in aeroportos:
                    aeroporto_formatado = {
                        "codigo": aeroporto[0],
                        "nome": aeroporto[1],
                        "cidade": aeroporto[2],
                        "estado": aeroporto[3]
                    }
                    aeroportos_formatados.append(aeroporto_formatado)
                
                return aeroportos_formatados                                
            
        except psycopg2.Error as e:
            print("Erro ao obter aeroportos:", e)
            return None
        finally:
            cursor.close()
            connection.close()

    def obter_aeroportos_por_origem(self, aeroporto_origem):
        connection = self.conexao.conectar()
        if connection is None:
            return None

        cursor = connection.cursor()
        try:
            cursor.execute("""
                SELECT a.codigo, a.nome, a.cidade, a.estado
                FROM rotas r
                INNER JOIN aeroportos a ON r.aeroporto_destino = a.codigo
                WHERE r.aeroporto_origem = %s
            """, (aeroporto_origem.upper(),))
            aeroportos_destino = cursor.fetchall()

            if not aeroportos_destino:
                return "Nenhum aeroporto encontrado"
            
            else:
                aeroportos_destino_formatado = []
                for aeroporto in aeroportos_destino:
                    aeroporto_formatado = {
                        "codigo": aeroporto[0],
                        "nome": aeroporto[1],
                        "cidade": aeroporto[2],
                        "estado": aeroporto[3]
                    }
                    aeroportos_destino_formatado.append(aeroporto_formatado)
                
                return aeroportos_destino_formatado                    
            
            
        except psycopg2.Error as e:
            print("Erro ao obter aeroportos de destino por origem:", e)
            return None
        finally:
            cursor.close()
            connection.close()


