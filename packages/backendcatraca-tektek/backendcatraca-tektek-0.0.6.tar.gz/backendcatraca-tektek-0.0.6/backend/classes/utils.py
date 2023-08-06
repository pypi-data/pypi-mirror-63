from os import system, name

from termcolor import colored
import pika
from decouple import config


RABBIT_MQ_HOST = config('RABBIT_MQ_HOST')
RABBIT_MQ_PORT = config('RABBIT_MQ_PORT')


class Utils:
    

    def printStart():
        programName = """
               _____ _____ _  ___   _ ___ ____    _      ___    _    
              |_   _| ____| |/ | \ | |_ _/ ___|  / \    |_ _|  / \   
                | | |  _| | ' /|  \| || |\___ \ / _ \    | |  / _ \  
                | | | |___| . \| |\  || | ___) / ___ \   | | / ___ \ 
                |_| |_____|_|\_|_| \_|___|____/_/   \_\ |___/_/   \_\ 
        """

        print(colored(programName, 'green'))

    def clearConsole():  
        # for windows 
        if name == 'nt': 
            _ = system('cls') 

        # for mac and linux(here, os.name is 'posix') 
        else: 
            _ = system('clear')

    def send_message_rabbitmq(rabbitmq_queue, message):

        print("Enviando mensagem")
        print(message)

        global RABBIT_MQ_HOST
        global RABBIT_MQ_PORT

        connection = pika.BlockingConnection(pika.ConnectionParameters(host = RABBIT_MQ_HOST, port = RABBIT_MQ_PORT))
        channel = connection.channel()

        channel.queue_declare(queue = rabbitmq_queue)

        channel.basic_publish(exchange = '', routing_key = rabbitmq_queue, body = message)
        connection.close()