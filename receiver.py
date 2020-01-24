import json
import pika

from chats import get_chat_ids
from main import bot


def callback(ch, method, properties, body):
    message = json.loads(body)

    for chat_id in get_chat_ids():
        bot.send_message(chat_id,
                         f'New {message[0]} been added\n{message[1]}')


connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='127.0.0.1'
))
channel = connection.channel()

channel.queue_declare(queue='message')

channel.basic_consume(queue='message',
                      on_message_callback=callback)


if __name__ == '__main__':
    channel.start_consuming()
