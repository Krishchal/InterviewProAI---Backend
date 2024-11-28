import pika

def publish_message(queue_name, message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    
    # Declare a queue
    channel.queue_declare(queue=queue_name, durable=True)
    
    # Publish a message
    channel.basic_publish(exchange='',
                          routing_key=queue_name,
                          body=message,
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # Make message persistent
                          ))
    
    print("\n[x] Message published to RabbitMQ")
    connection.close()


if __name__=="__main__":
    queue_name = "transcribed-text"
    message = "Hello, World!"
    publish_message(queue_name, message)  # Publish a message to the queue