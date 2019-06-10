'''
Created on May 27, 2019

@author: Gabriel Torrandella
'''
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', heartbeat=5))
channel = connection.channel()

deadLetterArgs = {"x-dead-letter-exchange": "dead-letter",
                  "x-dead-letter-routing-key": "maxRequeue"}
channel.queue_declare(queue='maxRequeue', arguments= deadLetterArgs)

channel.basic_qos(prefetch_size=0, prefetch_count=1)

def callback(channel, method, properties, body):
    if body.decode() == "Broken":
        requeueCount = properties.headers['x-requeue-count']
        print(" [x] Received %r" % body)
        print("  --> Requeue Count %i" % requeueCount)
        if  requeueCount <= 0:
            channel.basic_nack(delivery_tag = method.delivery_tag,
                               requeue = False)
            print("  --> Sent to Dead-Letter")
        else:
            channel.basic_ack(delivery_tag = method.delivery_tag)
            customProperties = pika.BasicProperties(headers = {'x-requeue-count': requeueCount - 1})
            channel.basic_publish(exchange = '', 
                                  routing_key = 'maxRequeue', 
                                  body = body,
                                  properties = customProperties)
            print("  --> Requeued Broken")
    else:
        channel.basic_ack(delivery_tag = method.delivery_tag)
        print(" [x] Working Message")
        print("  --> Acknowledge %r" % body)
    print("-----------------")

channel.basic_consume(queue='maxRequeue', on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
connection.close()
