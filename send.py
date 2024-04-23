#!/usr/bin/env python
import pika
import json
import hashlib

def main():
    conexao = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    canal = conexao.channel()

    canal.queue_declare(queue='cadastro_usuario')

    id_usuario = 2
    nome_usuario = "Maria"
    email_usuario = "maria@example.com"
    dados_usuario = {"id": id_usuario, "nome": nome_usuario, "email": email_usuario}
    hash_usuario = hashlib.sha256(json.dumps(dados_usuario).encode()).hexdigest()
    dados_usuario['hash'] = hash_usuario
    canal.basic_publish(exchange='', routing_key='cadastro_usuario', body=json.dumps(dados_usuario))
    print("[x] Dados de cadastro de usuário enviados:", dados_usuario)

    conexao.close()

if __name__ == '__main__':
    main()
