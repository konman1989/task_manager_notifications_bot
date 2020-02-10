import requests


def _get_events():
    req = requests.get('http://127.0.0.1:5000/events')
    return req.json()


def _post_events(data):
    req = requests.post('http://127.0.0.1:5000/events', json=data)
    return req.status_code


def get_user_subscriptions(user_id):
    req = requests.get(f'http://127.0.0.1:5000/users/{user_id}/subscriptions')
    return req.json()


def subscribe_user(user_id, event):
    req = requests.post(f'http://127.0.0.1:5000/users/{user_id}/subscriptions',
                        json={'event': event})
    return req.status_code


def unsubscribe_user(user_id, event):
    req = requests.delete(
        f'http://127.0.0.1:5000/users/{user_id}/subscriptions',
        json={'event': event})
    return req.status_code

