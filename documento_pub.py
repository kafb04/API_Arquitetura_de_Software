#!/usr/bin/env python
import pika
import json
import time
import sys
import hashlib

def main():
    if len(sys.argv) < 4:
        print("Uso: {} <id> <nome> <email>".format(sys.argv[0]))
        sys.exit(1)

    id_usuario = int(sys.argv[1])
    nome_usuario = sys.argv[2]
    email_usuario = sys.argv[3]

    # Calcula o hash dos dados do usuário
    dados_usuario = {"id": id_usuario, "nome": nome_usuario, "email": email_usuario}
    hash_usuario = hashlib.sha256(json.dumps(dados_usuario).encode()).hexdigest()

    credenciais = pika.PlainCredentials('guest', 'guest')
    parametros = pika.ConnectionParameters('localhost',
                                       5672,
                                       '/',
                                       credenciais)

    conexao = pika.BlockingConnection(parametros)
    canal = conexao.channel()

    canal.queue_declare(queue='cadastro_usuario')

    dados_usuario_com_hash = {"id": id_usuario, "nome": nome_usuario, "email": email_usuario, "hash": hash_usuario}
    canal.basic_publish(exchange='', routing_key='cadastro_usuario', body=json.dumps(dados_usuario_com_hash))
    print("[x] Dados de cadastro de usuário enviados:", dados_usuario_com_hash)

    conexao.close()

if __name__ == '__main__':
    main()