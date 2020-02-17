import os
from time import sleep
from telebot import TeleBot, types, logger

import handlers

TOKEN = os.getenv('TASK_NOTIFICATIONS_BOT_TOKEN')
bot = TeleBot(TOKEN)


EMOJI = {
    'subscription': '\U0001F4F2',
    'subscribe': '\U0001F449',
    'unsubscribe': '\U0001F448',
    'back': '\u21A9',
    'comment': '\U0001F4DD',
    'task': '\U0001F4CB',
}


@bot.message_handler(commands=['start'])
def subscribe_menu(message):
    text = 'This is a notification channel. You can subscribe to receive ' \
           'updates about tasks or comments from the menu below. ' \
           'You can also unsubscribe from receiving notifications.'

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    markup.add(f'{EMOJI["subscribe"]} Subscribe',
               f'{EMOJI["subscription"]} My subscriptions',
               f'{EMOJI["unsubscribe"]} Unsubscribe')

    bot.send_message(message.chat.id,
                     text=text,
                     reply_markup=markup)


@bot.message_handler(
    func=lambda x: x.text == f'{EMOJI["subscribe"]} Subscribe')
def subscribe_to_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    rows = [f'{EMOJI["task"]} Tasks', f'{EMOJI["comment"]} Comments']
    markup.add(*rows, f'{EMOJI["back"]} Back to main menu', )
    bot.send_message(message.chat.id,
                     f'You can subscribe to receive notifications below.',
                     reply_markup=markup)


@bot.message_handler(func=lambda x: x.text == f'{EMOJI["task"]} Tasks'
                                    or x.text == f'{EMOJI["comment"]} Comments')
def subscribe_to_events(message):
    event = message.text.split()[-1]
    res = handlers.subscribe_user(message.chat.id, event.lower())

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(f'{EMOJI["task"]} Tasks',
               f'{EMOJI["comment"]} Comments',
               f'{EMOJI["back"]} Back to main menu'
               )
    if res == 201:
        bot.send_message(message.chat.id,
                         f"You have subscribed to receive notifications about"
                         f" {event.lower()}.",
                         reply_markup=markup)

    elif res == 409:
        bot.send_message(message.chat.id,
                         f"You are already subscribed to receive notifications "
                         f"about {event.lower()}.",
                         reply_markup=markup)

    elif res == 403:
        bot.send_message(message.chat.id,
                         "You are not registered with @BestTaskManagerBot. "
                         "You need to create an account first.",
                         reply_markup=markup)


@bot.message_handler(
    func=lambda x: x.text == f'{EMOJI["subscription"]} My subscriptions')
def get_subscriptions(message):
    events = handlers.get_user_subscriptions(message.chat.id)

    if not events:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add(f'{EMOJI["task"]} Tasks',
                   f'{EMOJI["comment"]} Comments',
                   f'{EMOJI["back"]} Back to main menu'
                   )
        bot.send_message(message.chat.id,
                         'You have no active subscriptions.'
                         ' You can subscribe below.',
                         reply_markup=markup)
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(f'{EMOJI["task"]} Tasks',
               f'{EMOJI["comment"]} Comments',
               f'{EMOJI["back"]} Back to main menu'
               )

    events = [e.get('event').title() for e in events]

    bot.send_message(message.chat.id,
                     f'You are subscribed to receive '
                     f'notifications about {", ".join(events).lower()}',
                     reply_markup=markup)


@bot.message_handler(
    func=lambda x: x.text == f'{EMOJI["unsubscribe"]} Unsubscribe')
def unsubscribe(message):
    events = handlers.get_user_subscriptions(message.chat.id)

    if not events:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add(f'{EMOJI["task"]} Tasks',
                   f'{EMOJI["comment"]} Comments',
                   f'{EMOJI["back"]} Back to main menu'
                   )
        bot.send_message(
            message.chat.id,
            'You have no active subscriptions You can subscribe below.',
            reply_markup=markup)
        return

    events = [e.get('event').title() for e in events]
    rows = [f'{EMOJI["unsubscribe"]} Unsubscribe {n}' for n in events]

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*rows, f'{EMOJI["back"]} Back to main menu')

    bot.send_message(message.chat.id,
                     f'You are currently subscribed to '
                     f'{", ".join(events).lower()}. '
                     f'Choose notifications to unsubscribe from.',
                     reply_markup=markup)


@bot.message_handler(
    func=lambda
            x: x.text == f'{EMOJI["unsubscribe"]} Unsubscribe Tasks' or
               x.text == f'{EMOJI["unsubscribe"]} Unsubscribe Comments')
def unsubscribe_user(message):
    event = message.text.split()[-1]
    res = handlers.unsubscribe_user(message.chat.id, event.lower())

    events = handlers.get_user_subscriptions(message.chat.id)
    events = [e.get('event').title() for e in events]

    rows = [f'{EMOJI["unsubscribe"]} Unsubscribe {n}' for n in events]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*rows, f'{EMOJI["back"]} Back to main menu')

    if res == 200:
        button = f'{EMOJI["unsubscribe"]} Unsubscribe '
        bot.send_message(message.chat.id,
                         f"You have unsubscribed from "
                         f"{message.text.replace(button, '').lower()}.",
                         reply_markup=markup)
        return

@bot.message_handler(
    func=lambda x: x.text == f'{EMOJI["back"]} Back to main menu')
def main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(f'{EMOJI["subscribe"]} Subscribe',
               f'{EMOJI["subscription"]} My subscriptions',
               f'{EMOJI["unsubscribe"]} Unsubscribe')

    bot.send_message(message.chat.id, 'Main Menu', reply_markup=markup)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def unknown_command(message):
    bot.send_message(message.chat.id,
                     "Sorry, I didn't understand that command.")


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            logger.error(e)
            sleep(15)
