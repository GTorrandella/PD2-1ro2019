'''
Created on May 27, 2019

@author: Gabriel Torrandella
'''
import pika

# Se crea la conección con RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Se declara el exchange example y la cola maxRequeue
channel.exchange_declare('example', exchange_type="direct")

deadLetterArgs = {"x-dead-letter-exchange": "dead-letter",
                  "x-dead-letter-routing-key": "maxRequeue"}
channel.queue_declare(queue='maxRequeue', arguments= deadLetterArgs)

# Se une maxRequeue a example, con la routing key example.maxRequeue
channel.queue_bind('maxRequeue', 'example', routing_key="example.maxRequeue")

# x-requeue-count es un header propio 
customProperties = pika.BasicProperties(headers = {'x-requeue-count': 2})
            
channel.basic_publish(exchange='example', routing_key='example.maxRequeue', body='Broken', properties = customProperties)
print(" [x] Sent BROKEN message")

channel.basic_publish(exchange='example', routing_key='example.maxRequeue', body='Working', properties = customProperties)
print(" [x] Sent WORKING message")

channel.basic_publish(exchange='example', routing_key='example.maxRequeue', body='Working', properties = customProperties)
print(" [x] Sent WORKING message")

channel.basic_publish(exchange='example', routing_key='example.maxRequeue', body='Working', properties = customProperties)
print(" [x] Sent WORKING message")


connection.close()
