import psycopg2
from datetime import datetime

class Voos:
    def __init__(self, conexao):
        self.conexao = conexao

    def obter_voos(self, data):
        connection = self.conexao.conectar()
        if connection is None:
            return None

        cursor = connection.cursor()
        try:
            cursor.execute("""
                SELECT v.rota_id, v.codigo_voo, r.aeroporto_origem, r.aeroporto_destino, v.data, v.horario, v.tarifa
                FROM voos v
                INNER JOIN rotas r ON v.rota_id = r.id
                WHERE v.data = %s
            """, (data,))
            voos = cursor.fetchall()

            if not voos:
                return "Nenhum voo encontrado para a data informada"
            
            else:
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
            return None
        finally:
            cursor.close()
            connection.close()

    def pesquisar_voos(self, data, numero_passageiros):
        connection = self.conexao.conectar()
        if connection is None:
            return None

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
            return None
        finally:
            cursor.close()
            connection.close()
