import psycopg2
from fastapi import HTTPException, status

class Aeroporto:
    def __init__(self, conexao):
        self.conexao = conexao

    # Metodo para obter a lista de aeroportos
    def obter_aeroportos(self):
        # estabelecendo conexao
        connection = self.conexao.conectar()
        if connection is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Não foi possível conectar ao banco de dados")
        cursor = connection.cursor()

        try:
            cursor.execute("SELECT codigo, nome, cidade, estado FROM aeroportos")
            aeroportos = cursor.fetchall()

            # se nao retornou aeroportos
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
        
        # Caso de erro
        except psycopg2.Error as e:
            print("Erro ao obter aeroportos:", e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ocorreu um erro ao processar a solicitação")
        
        # Fechando a conexao
        finally:
            cursor.close()
            connection.close()

    # Metodo para obter a lista de aeroportos por origem
    def obter_aeroportos_por_origem(self, aeroporto_origem):
        # estabelecendo conexao
        connection = self.conexao.conectar()
        if connection is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Não foi possível conectar ao banco de dados")
        cursor = connection.cursor()
        try:
            cursor.execute("""
                SELECT a.codigo, a.nome, a.cidade, a.estado
                FROM rotas r
                INNER JOIN aeroportos a ON r.aeroporto_destino = a.codigo
                WHERE r.aeroporto_origem = %s
            """, (aeroporto_origem.upper(),)) # virgula necessaria apos o upper() pois o cursor.execute espera uma tupla como parametro
            aeroportos_destino = cursor.fetchall()
            
            # se nao retornou aeroportos
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
            
        # Caso de erro
        except psycopg2.Error as e:
            print("Erro ao obter aeroportos de destino por origem:", e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ocorreu um erro ao processar a solicitação")
        
        # Fechando a conexao
        finally:
            cursor.close()
            connection.close()