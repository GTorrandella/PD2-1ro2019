'''
Created on Jun 10, 2019

@author: gabo
'''
import unittest
import pika

class Test(unittest.TestCase):

    def setUp(self):
        # Se crea la conección con RabbitMQ
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        
        # Se declara el exchange example y la cola maxRequeue
        self.channel.exchange_declare('example', exchange_type="direct")
        
        deadLetterArgs = {"x-dead-letter-exchange": "dead-letter",
                          "x-dead-letter-routing-key": "maxRequeue"}
        self.channel.queue_declare(queue='maxRequeue', arguments= deadLetterArgs)
        
        # Se une maxRequeue a example, con la routing key example.maxRequeue
        self.channel.queue_bind('maxRequeue', 'example', routing_key="example.maxRequeue")

        # Se declara el exchange que funcionará como dead letter
        self.channel.exchange_declare("dead-letter", exchange_type="direct")

        self.channel.queue_declare(queue='maxedRequeues')
        self.channel.queue_bind(queue='maxedRequeues', 
                           exchange='dead-letter', 
                           routing_key='maxRequeue')
        
        customProperties = pika.BasicProperties(headers = {'x-requeue-count': 2})
            
        self.channel.basic_publish(exchange='example', routing_key='example.maxRequeue', body='Broken', properties = customProperties)
        self.channel.basic_publish(exchange='example', routing_key='example.maxRequeue', body='Working', properties = customProperties)
        

    def tearDown(self):
        self.channel.exchange_delete('example')
        self.channel.exchange_delete('dead-letter')
        self.channel.queue_delete('maxRequeue')
        self.channel.queue_delete('maxedRequeues')
        self.connection.close()
        

    def test_CustomHeaders(self):
        method, properties, body = self.channel.basic_get(queue="maxRequeue", auto_ack=True)
        
        self.assertEqual(method.exchange, "example")
        self.assertEqual(method.routing_key, "example.maxRequeue")
        
        self.assertEqual(body.decode(), "Broken")
        
        self.assertTrue('x-requeue-count' in properties.headers.keys())
        self.assertEqual(properties.headers['x-requeue-count'], 2)
    
    def _dequeueLogic(self):
        flag = True
        while(flag):
            method, properties, body = self.channel.basic_get(queue="maxRequeue")
            if method == None:
                flag = False
            else:
                if body.decode() == "Broken":
                    requeueCount = properties.headers['x-requeue-count']
                    if requeueCount <= 0:
                        self.channel.basic_nack(delivery_tag = method.delivery_tag,
                                                requeue = False)
                    else:
                        self.channel.basic_ack(delivery_tag = method.delivery_tag)
                        customProperties = pika.BasicProperties(headers = {'x-requeue-count': requeueCount - 1})
                        self.channel.basic_publish(exchange = '', 
                                              routing_key = 'maxRequeue', 
                                              body = body,
                                              properties = customProperties)
                else:
                    self.channel.basic_ack(delivery_tag = method.delivery_tag)
                    
                    
    def test_DeadLetter(self):
        self._dequeueLogic()
        method, properties, body = self.channel.basic_get(queue='maxedRequeues')
        
        self.assertEqual(method.exchange, "dead-letter")
        
        self.assertEqual(properties.headers['x-requeue-count'], 0)
        self.assertEqual(properties.headers['x-first-death-reason'], 'rejected')
        self.assertEqual(properties.headers['x-first-death-queue'], 'maxRequeue')
        
        self.assertEqual(body.decode(), "Broken")
                 

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()