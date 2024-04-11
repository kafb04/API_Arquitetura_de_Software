import psycopg2
import random
import string
from fastapi import HTTPException, status

class Reserva:
    def __init__(self, conexao):
        self.conexao = conexao

    # metodo responsavel por efetuar a compra das passagens
    def efetuar_compra(self, codigo_voo, qtd_passageiros):
        connection = self.conexao.conectar()
        if connection is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Não foi possível conectar ao banco de dados")
        cursor = connection.cursor()

        cursor = connection.cursor()
        try:
            cursor.execute("SELECT id, tarifa FROM voos WHERE codigo_voo = %s", (codigo_voo,))
            id_voo, tarifa = cursor.fetchone()
            valor = tarifa * qtd_passageiros

            # forma encontrada na internet para gerar numero aleatorio para o localizador da reserva e para os etickets
            caracteres = string.ascii_uppercase + string.digits
            localizador_reserva = ''.join(random.choice(caracteres) for _ in range(6))

            etickets = [] # etickets eh uma lista, pois deve conter um eticket para cada passageiro
            for _ in range(qtd_passageiros):
                eticket = ''.join(random.choice(string.digits) for _ in range(6))
                etickets.append(eticket)

            cursor.execute("""
                INSERT INTO reservas (id_voo, qtd_passageiros, valor, localizador_reserva, etickets)
                VALUES (%s, %s, %s, %s, %s)
            """, (id_voo, qtd_passageiros, valor, localizador_reserva, etickets))
            connection.commit()

            dados_reserva = [
                {
                    "localizador_reserva": localizador_reserva,
                    "e-tickets": etickets
                }
            ]
            return dados_reserva
                
        except psycopg2.Error as e:
            print("Erro ao criar reserva:", e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ocorreu um erro ao processar a solicitação")
        
        finally:
            cursor.close()
            connection.close()
