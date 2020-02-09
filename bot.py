from telebot import types

from chats import add_user_to_db, subscribe_to_event, get_user_subscriptions, \
    unsubscribe_from_events
from main import bot

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
    add_user_to_db(message.chat.id)
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
    response = subscribe_to_event(message.chat.id, event.lower())

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(f'{EMOJI["task"]} Tasks',
               f'{EMOJI["comment"]} Comments',
               f'{EMOJI["back"]} Back to main menu'
               )

    bot.send_message(message.chat.id,
                     response,
                     reply_markup=markup)


@bot.message_handler(
    func=lambda x: x.text == f'{EMOJI["subscription"]} My subscriptions')
def get_subscriptions(message):
    events = get_user_subscriptions(message.chat.id)

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

    bot.send_message(message.chat.id,
                     f'You are subscribed to receive '
                     f'notifications about {", ".join(events).lower()}',
                     reply_markup=markup)


@bot.message_handler(
    func=lambda x: x.text == f'{EMOJI["unsubscribe"]} Unsubscribe')
def unsubscribe(message):
    events = get_user_subscriptions(message.chat.id)
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
def delete_event_from_db(message):
    event = message.text.split()[-1]
    unsubscribe_from_events(message.chat.id, event.lower())

    events = get_user_subscriptions(message.chat.id)
    rows = [f'{EMOJI["unsubscribe"]} Unsubscribe {n}' for n in events]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*rows, f'{EMOJI["back"]} Back to main menu')

    bot.send_message(message.chat.id,
                     f"You have unsubscribed from "
                     f"{message.text.replace('Unsubscribe ', '').lower()}.",
                     reply_markup=markup)


@bot.message_handler(
    func=lambda x: x.text == f'{EMOJI["back"]} Back to main menu')
def main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(f'{EMOJI["subscribe"]} Subscribe',
               f'{EMOJI["subscription"]} My subscriptions',
               f'{EMOJI["unsubscribe"]} Unsubscribe')

    bot.send_message(message.chat.id, 'Main menu', reply_markup=markup)


if __name__ == '__main__':
    bot.polling(none_stop=True)
