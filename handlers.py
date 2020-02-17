import os
import requests

SERVER_IP_PATH = os.getenv('SERVER_IP_PATH')


def _get_events():
    req = requests.get(f'{SERVER_IP_PATH}/events')
    return req.json()


def _post_events(data):
    req = requests.post(f'{SERVER_IP_PATH}/events', json=data)
    return req.status_code


def get_user_subscriptions(user_id):
    req = requests.get(f'{SERVER_IP_PATH}/users/{user_id}/subscriptions')
    return req.json()


def subscribe_user(user_id, event):
    req = requests.post(f'{SERVER_IP_PATH}/users/{user_id}/subscriptions',
                        json={'event': event})
    return req.status_code


def unsubscribe_user(user_id, event):
    req = requests.delete(
        f'{SERVER_IP_PATH}/users/{user_id}/subscriptions',
        json={'event': event})
    return req.status_code


def get_dashboard_users(d_id):
    req = requests.get(
        f'{SERVER_IP_PATH}/dashboards/{d_id}/users')
    return req.json()


def get_event_subscribers(event_id, event):
    req = requests.get(
        f'{SERVER_IP_PATH}/events/{event_id}/subscribers?query={event}')
    return req.json()

