import psycopg2
from fastapi import HTTPException, status

class Voos:
    def __init__(self, conexao):
        self.conexao = conexao

    # metodo para obter voos
    def obter_voos(self, data):
        connection = self.conexao.conectar()
        if connection is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Não foi possível conectar ao banco de dados")
        cursor = connection.cursor()

        cursor = connection.cursor()
        try:
            cursor.execute("""
                SELECT v.rota_id, v.codigo_voo, r.aeroporto_origem, r.aeroporto_destino, v.data, v.horario, v.tarifa
                FROM voos v
                INNER JOIN rotas r ON v.rota_id = r.id
                WHERE v.data = %s
            """, (data,))
            voos = cursor.fetchall()

            if not voos: # se nao retornou nenhum dado
                return "Nenhum voo encontrado para a data informada"
            
            else:
                # formatando voos para mostrar a chave
                voos_formatados = [] 
                for voo in voos:
                    voo_formatado = {
                        "rota_id": voo[0],
                        "codigo_voo": voo[1],
                        "aeroporto_origem": voo[2],
                        "aeroporto_destino": voo[3],
                        "data": voo[4].strftime("%d-%m-%Y"),
                        "horario": voo[5],
                        "tarifa": voo[6]
                    }
                    voos_formatados.append(voo_formatado)
                
                return voos_formatados                    
            
        except psycopg2.Error as e:
            print("Erro ao obter voos:", e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ocorreu um erro ao processar a solicitação")
        
        finally:
            cursor.close()
            connection.close()

    # metodo para pesquisar voos por data e numero de passageiros
    def pesquisar_voos(self, data, numero_passageiros):
        connection = self.conexao.conectar()
        if connection is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Não foi possível conectar ao banco de dados")
        cursor = connection.cursor()

        cursor = connection.cursor()
        try:
            cursor.execute("""
                SELECT v.rota_id, v.codigo_voo, r.aeroporto_origem, r.aeroporto_destino, v.data, v.horario, v.tarifa
                FROM voos v
                INNER JOIN rotas r ON v.rota_id = r.id
                WHERE v.data = %s
                AND v.tarifa = (SELECT MIN(tarifa) FROM voos WHERE data = %s)
            """, (data, data))
            voos = cursor.fetchall()

            if not voos:
                return "Nenhum voo encontrado para a data informada"
            
            else:
                # formatando voos para mostrar a chave
                voos_formatados = []
                for voo in voos:
                    tarifa = voo[6]
                    valor_total = tarifa * numero_passageiros
                    voo_formatado = {
                        "rota_id": voo[0],
                        "codigo_voo": voo[1],
                        "aeroporto_origem": voo[2],
                        "aeroporto_destino": voo[3],
                        "data": voo[4].strftime("%d-%m-%Y"),
                        "horario": voo[5],
                        "tarifa": tarifa,
                        f"valor_para_{numero_passageiros}_passageiros": valor_total
                    }
                    voos_formatados.append(voo_formatado)
                
                return voos_formatados                    
            
        except psycopg2.Error as e:
            print("Erro ao pesquisar voos:", e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ocorreu um erro ao processar a solicitação")
        finally:
            cursor.close()
            connection.close()
