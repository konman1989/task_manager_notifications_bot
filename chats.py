import sqlite3


def create_table_users():
    with sqlite3.connect('chat_users.db') as conn:
        conn.execute("""create table users (
        id integer primary key autoincrement,
        chat_id integer unique)
        """)


def create_table_events():
    with sqlite3.connect('chat_users.db') as conn:
        conn.execute("""create table events (
        id integer primary key autoincrement,
        event varchar(32) unique)
        """)


def create_table_subscriptions():
    with sqlite3.connect('chat_users.db') as conn:
        conn.execute("""create table subscriptions (
        chat_id integer,
        event varchar(32),
        primary key (chat_id, event),
        foreign key(chat_id) references users(chat_id),
        foreign key(event) references events(event))
        """)


def add_event(event):
    with sqlite3.connect('chat_users.db') as conn:
        curs = conn.cursor()
        t = (event,)
        curs.execute(
            f"insert into events (event) values(?)", t)


def add_user_to_db(chat_id):
    with sqlite3.connect('chat_users.db') as conn:
        curs = conn.cursor()
        t = (chat_id,)

        try:
            curs.execute(
                "insert into users (chat_id) values(?)", t)
        except sqlite3.IntegrityError:
            return


def subscribe_to_event(chat_id, event):
    with sqlite3.connect('chat_users.db') as conn:
        curs = conn.cursor()
        t = (chat_id, event)

        try:
            curs.execute(
                "insert into subscriptions (chat_id, event) values (?, ?)", t
            )
            return f'You have subscribed to receive notifications about {event}.'
        except sqlite3.IntegrityError:
            return f'You are already subscribed to receive notifications from ' \
                   f'{event}'


def unsubscribe_from_events(chat_id, event):
    with sqlite3.connect('chat_users.db') as conn:
        curs = conn.cursor()
        t = (chat_id, event)

        curs.execute(
            "delete from subscriptions where chat_id=? and event=?", t
        )


def get_user_subscriptions(chat_id):
    with sqlite3.connect('chat_users.db') as conn:
        t = (chat_id,)
        curs = conn.cursor()
        subs = curs.execute(
            'select event from subscriptions where chat_id=?', t)

        return [n[0].title() for n in subs.fetchall()]


def get_chat_ids(event):
    with sqlite3.connect('chat_users.db') as conn:
        curs = conn.cursor()
        t = (event,)
        users = curs.execute('select chat_id from subscriptions where event=?',
                             t)
        for chat_id in users:
            yield chat_id[0]


if __name__ == '__main__':
    # create_table_users()
    # create_table_events()
    # create_table_subscriptions()
    # #
    # add_event('tasks')
    # add_event('comments')
    # print(subscribe_to_event(12111, 'comments'))
    # subscribe_to_event(22222, 'comments')
    # subscribe_to_event(33333, 'comments')
    # subscribe_to_event(33333, 'tasks')
    # print(subscribe_to_event(555, 'tasks'))
    # print(unsubscribe_from_events(4444, 'tasks'))
    # print(unsubscribe_from_events(555, 'tasks'))
    for i in get_chat_ids('comments'):
        print(i)