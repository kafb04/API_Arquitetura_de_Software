#!/usr/bin/env python
import pika
import json
import time
import hashlib

def processar_cadastro_usuario(msg):
    print("Processamento de Cadastro de Usuário")
    print("[x] Dados de cadastro de usuário recebidos:", msg)
    dados_usuario = json.loads(msg.decode('utf-8'))
    print("ID do Usuário: {0}".format(dados_usuario['id']))
    print("Nome do Usuário: {0}".format(dados_usuario['nome']))
    print("E-mail do Usuário: {0}".format(dados_usuario['email']))

    # Verifica o hash
    hash_usuario = hashlib.sha256(json.dumps(dados_usuario).encode()).hexdigest()
    if hash_usuario == dados_usuario['hash']:
        print("Hash verificado: válido")
    else:
        print("Hash verificado: inválido")

    # Aqui você pode adicionar a lógica para salvar os dados do usuário no banco de dados, enviar e-mails, etc.
    time.sleep(2)  # Simula algum processamento
    print("Processamento de Cadastro de Usuário Finalizado\n")

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
        processar_cadastro_usuario(body)

    canal.basic_consume(queue='cadastro_usuario',
                          on_message_callback=callback, auto_ack=True)

    print(' [*] Aguardando mensagens de cadastro de usuário. Para sair, pressione CTRL+C')
    canal.start_consuming()

if __name__ == '__main__':
    main()
