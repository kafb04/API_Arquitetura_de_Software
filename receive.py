#!/usr/bin/env python
import pika
import json
import hashlib

def main():
    credenciais = pika.PlainCredentials('guest', 'guest')
    parametros = pika.ConnectionParameters('localhost',
                                       5672,
                                       '/',
                                       credenciais)

    conexao = pika.BlockingConnection(parametros)
    canal = conexao.channel()

    canal.queue_declare(queue='cadastro_usuario')

    def callback(ch, method, properties, body):
        dados_usuario = json.loads(body.decode('utf-8'))
        hash_usuario = hashlib.sha256(json.dumps(dados_usuario).encode()).hexdigest()
        if hash_usuario == dados_usuario['hash']:
            print(" [x] Mensagem de cadastro de usuário recebida:", body)
        else:
            print(" [x] Mensagem de cadastro de usuário recebida com hash inválido.")

    canal.basic_consume(queue='cadastro_usuario',
                          on_message_callback=callback, auto_ack=True)

    print(' [*] Aguardando mensagens de cadastro de usuário. Para sair, pressione CTRL+C')
    canal.start_consuming()

if __name__ == '__main__':
    main()
