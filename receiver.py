import json
import pika

from main import bot
from handlers import get_event_subscribers


def callback(ch, method, properties, body):
    event = json.loads(body)[0]
    data = json.loads(body)[1]

    if event == 'tasks':
        msg = f"*New task has been added:*\n\n" \
              f"*Name:* {data.get('task_name')}\n" \
              f"*Dashboard:* {data.get('dashboard')}\n" \
              f"*Admin:* {data.get('admin_name')}\n" \
              f"*Current status:* {data.get('status')}\n" \
              f"*Description:* {data.get('text')}\n"

        for chat_id in get_event_subscribers(data.get('dashboard_id'), event):
            bot.send_message(chat_id.get('chat_id'), msg, parse_mode='Markdown')

    elif event == 'status':
        msg = f"Task *{data.get('task_name')}* has changed its status to:\n\n" \
              f"*{data.get('status')}*"

        for chat_id in get_event_subscribers(data.get('dashboard_id'), 'tasks'):
            bot.send_message(chat_id.get('chat_id'), msg, parse_mode='Markdown')

    elif event == 'comments':
        msg = f"*New comment has been posted:*\n\n" \
              f"*Task:* {data.get('task')}\n"\
              f"*Title:* {data.get('title')}\n"\
              f"*Author:* {data.get('sender')}\n"\
              f"*Comment:* {data.get('comment')}"

        for chat_id in get_event_subscribers(data.get('task_id'), event):
            bot.send_message(chat_id.get('chat_id'), msg, parse_mode='Markdown')


connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='127.0.0.1'
))
channel = connection.channel()

channel.queue_declare(queue='message')

channel.basic_consume(queue='message',
                      on_message_callback=callback)


if __name__ == '__main__':
    channel.start_consuming()
