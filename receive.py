#!/usr/bin/env python
import pika
import json
import psycopg2

def registrar_novo_usuario(msg):
    print("Registering new user")
    data = json.loads(msg.decode('utf-8'))
    print(data)

    # Código para registrar o novo usuário no sistema de autenticação
    try:
        connection = psycopg2.connect(
            host='localhost',
            user='seu_usuario',
            password='sua_senha',
            database='seu_banco_de_dados'
        )
        cursor = connection.cursor()
        cursor.execute("INSERT INTO usuarios (email, senha) VALUES (%s, %s)", (data['email'], data['senha']))
        connection.commit()
        print("New user registered successfully")
    except psycopg2.Error as e:
        print("Error registering new user:", e)
    finally:
        if connection:
            connection.close()

def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='novo_usuario')

    def callback(ch, method, properties, body):
        registrar_novo_usuario(body)

    channel.basic_consume(queue='novo_usuario', on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    main()
