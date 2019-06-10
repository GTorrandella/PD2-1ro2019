'''
Created on May 27, 2019

@author: Gabriel Torrandella
'''
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', heartbeat=5))
channel = connection.channel()

channel.exchange_declare("dead-letter", exchange_type="direct")

channel.queue_declare(queue='maxedRequeues')
channel.queue_bind(queue='maxedRequeues', 
                   exchange='dead-letter', 
                   routing_key='maxRequeue')


channel.basic_qos(prefetch_size=0, prefetch_count=1)

def callback(channel, method, properties, body):
    print(" [x] Recived from dead letter %r" % body.decode)
    channel.basic_ack(delivery_tag = method.delivery_tag)
    
channel.basic_consume(queue='maxedRequeues', on_message_callback=callback)

print(' [*] Waiting for messages on Dead Letter. To exit press CTRL+C')

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
connection.close()
