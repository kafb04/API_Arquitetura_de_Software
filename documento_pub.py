#!/usr/bin/env python
import pika
import json
import time
import psycopg2

def obter_dados_compra_passagem():
    # Conectar ao banco de dados para obter os dados da compra de passagem
    try:
        connection = psycopg2.connect(
            host='localhost',
            user='seu_usuario',
            password='sua_senha',
            database='seu_banco_de_dados'
        )
        cursor = connection.cursor()
        cursor.execute("SELECT codigo_voo, qtd_passageiros FROM compras_passagem ORDER BY id DESC LIMIT 1")
        compra_passagem = cursor.fetchone()
        if compra_passagem:
            return {"codigo_voo": compra_passagem[0], "qtd_passageiros": compra_passagem[1]}
        else:
            return None
    except psycopg2.Error as e:
        print("Erro ao obter dados da compra de passagem:", e)
        return None
    finally:
        if connection:
            connection.close()

def enviar_compra_passagem():
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='compra_passagem')

    while True:
        dados_compra = obter_dados_compra_passagem()
        if dados_compra:
            channel.basic_publish(exchange='', routing_key='compra_passagem', body=json.dumps(dados_compra).encode())
            print("[x] Message sent to consumer")
        else:
            print("No purchase data found.")
        time.sleep(5)  # delays for 5 seconds

    connection.close()

if __name__ == '__main__':
    enviar_compra_passagem()
