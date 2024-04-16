#!/usr/bin/env python
import pika
import json
import psycopg2

def obter_dados_novo_usuario():
    # Conectar ao banco de dados para obter os dados do novo usuário
    try:
        connection = psycopg2.connect(
            host='localhost',
            user='seu_usuario',
            password='sua_senha',
            database='seu_banco_de_dados'
        )
        cursor = connection.cursor()
        cursor.execute("SELECT email, senha FROM novos_usuarios ORDER BY id DESC LIMIT 1")
        novo_usuario = cursor.fetchone()
        if novo_usuario:
            return {"email": novo_usuario[0], "senha": novo_usuario[1]}
        else:
            return None
    except psycopg2.Error as e:
        print("Erro ao obter dados do novo usuário:", e)
        return None
    finally:
        if connection:
            connection.close()

def enviar_novo_usuario():
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='novo_usuario')

    dados_novo_usuario = obter_dados_novo_usuario()
    if dados_novo_usuario:
        channel.basic_publish(exchange='', routing_key='novo_usuario', body=json.dumps(dados_novo_usuario).encode())
        print(" [x] Sent 'New User Registration'")
    else:
        print("No new user data found.")

    connection.close()

if __name__ == '__main__':
    enviar_novo_usuario()
