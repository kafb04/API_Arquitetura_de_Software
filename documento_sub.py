#!/usr/bin/env python
import pika
import json
import time
from fpdf import FPDF
import psycopg2

def processar_compra_passagem(msg):
    print("Processing purchase of airplane tickets")
    data = json.loads(msg.decode('utf-8'))
    print(data)

    # Processar os dados e gerar o PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Compra de Passagem Aérea", ln=1, align="C")
    pdf.cell(200, 20, txt=f"Código do Voo: {data['codigo_voo']}", ln=2, align="C")
    pdf.cell(200, 30, txt=f"Quantidade de Passageiros: {data['qtd_passageiros']}", ln=3, align="C")
    pdf.output("/path/to/pdf/file.pdf")

    time.sleep(5)
    print("Purchase processing finished")

def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='compra_passagem')

    def callback(ch, method, properties, body):
        processar_compra_passagem(body)

    channel.basic_consume(queue='compra_passagem', on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    main()
