from telebot import types

from chats import add_user_to_db, subscribe_to_event, get_user_subscriptions, \
    unsubscribe_from_events
from main import bot


@bot.message_handler(commands=['start'])
def subscribe_menu(message):
    text = 'This is a notification channel. You can subscribe to receive ' \
           'updates about tasks or comments from the menu below. ' \
           'You can also unsubscribe from receiving notifications.'
    add_user_to_db(message.chat.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    markup.add('Subscribe', 'My subscriptions', 'Unsubscribe')

    bot.send_message(message.chat.id,
                     text=text,
                     reply_markup=markup)


@bot.message_handler(func=lambda x: x.text == 'Subscribe')
def subscribe_to_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    rows = ['Tasks', 'Comments']
    markup.add(*rows, '<< Back to main menu',)
    bot.send_message(message.chat.id,
                     f'You can subscribe to receive notifications below.',
                     reply_markup=markup)


@bot.message_handler(func=lambda x: x.text == 'Tasks' or x.text == 'Comments')
def subscribe_to_events(message):
    response = subscribe_to_event(message.chat.id, message.text.lower())

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add('Tasks', 'Comments', '<< Back to main menu')

    bot.send_message(message.chat.id,
                     response,
                     reply_markup=markup)


@bot.message_handler(func=lambda x: x.text == 'My subscriptions')
def get_subscriptions(message):
    events = get_user_subscriptions(message.chat.id)

    if not events:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add('Tasks', 'Comments', '<< Back to main menu')
        bot.send_message(message.chat.id,
                         'You have no active subscriptions.'
                         ' You can subscribe below.',
                         reply_markup=markup)
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add('Subscribe', 'My subscriptions', 'Unsubscribe')

    bot.send_message(message.chat.id,
                     f'You are subscribed to receive '
                     f'notifications about {", ".join(events).lower()}',
                     reply_markup=markup)


@bot.message_handler(func=lambda x: x.text == 'Unsubscribe')
def unsubscribe(message):
    events = get_user_subscriptions(message.chat.id)
    if not events:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add('Tasks', 'Comments', '<< Back to main menu')
        bot.send_message(
            message.chat.id,
            'You have no active subscriptions You can subscribe below.',
            reply_markup=markup)
        return

    rows = [f"Unsubscribe {n}" for n in events]

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*rows, '<< Back to main menu')

    bot.send_message(message.chat.id,
                     f'You are currently subscribed to '
                     f'{", ".join(events).lower()}. '
                     f'Choose notifications to unsubscribe from.',
                     reply_markup=markup)


@bot.message_handler(func=lambda x: x.text == 'Unsubscribe Tasks' or
                                    x.text == 'Unsubscribe Comments')
def delete_event_from_db(message):
    event = message.text.split()
    unsubscribe_from_events(message.chat.id, event[1].lower())

    events = get_user_subscriptions(message.chat.id)
    rows = [f"Unsubscribe {n}" for n in events]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*rows, '<< Back to main menu')

    bot.send_message(message.chat.id,
                     f"You have unsubscribed from "
                     f"{message.text.replace('Unsubscribe ', '').lower()}.",
                     reply_markup=markup)


@bot.message_handler(func=lambda x: x.text == '<< Back to main menu')
def main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add('Subscribe', 'My subscriptions', 'Unsubscribe')

    bot.send_message(message.chat.id, 'Main menu', reply_markup=markup)


if __name__ == '__main__':
    bot.polling(none_stop=True)
