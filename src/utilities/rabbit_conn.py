import logging
import pika


class RabbitConnection:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=15672))
        self.channel = connection.channel()
        self.logging = [] # TODO gen logging channel

    @classmethod
    def send(cls, queue, msg):
        cls.channel.queue_declare(queue=queue)
        cls.channel.basic_publish(exchange='', routing_key=queue, body=msg)
        cls.logging.push(f"Sent \n'{msg}' \nin {queue}")
        return cls


    @classmethod
    def receive(cls, queue, callback=None):
        if not callback:
            callback = lambda ch, method, properties, body: cls.logging.push(" [x] Received %r" % body)
        channel.queue_declare(queue=queue)
        channel.basic_consume(queue=queue,
                      auto_ack=True,
                      on_message_callback=callback)
        channel.start_consuming()
        return cls


    def __del__(self):
        self.connection.close()