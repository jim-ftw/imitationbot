import requests
import json
import logging
import os
from pprint import pprint
from rate_check import rate_check

USER_KEY = os.getenv('USER_KEY')
ROOM_ID = os.getenv('ROOM_ID')
IMITATIONBOT_KEY = os.getenv('IMITATIONBOT_KEY')

hipchat_url = 'https://api.hipchat.com/v2/'

logger = logging.getLogger(__name__)


def get_user_info(user_name):
    url = hipchat_url + 'user/@' + user_name 
    payload = {
        'auth_token': USER_KEY
    }
    r = requests.get(url, params = payload)
    response = json.loads(r.text)
    headers = r.headers
    user_info = {}
    if r.status_code == 200:
        user_info['user_id'] = response['id']
        user_info['name'] = response['name']
        return user_info
    else:
        logger.info('error {0}; message: {1}'.format(response['error']['code'], response['error']['message']))
    rate_check(headers)

def send_notification(msg, sent_from):
    url = hipchat_url + 'room/{0}/notification'.format(str(ROOM_ID))
    payload = {
        'auth_token': IMITATIONBOT_KEY,
        'color': 'green',
		'message': msg,
		'message_format': 'text',
		'from': sent_from
    }
    r = requests.post(url, data = payload)
    headers = r.headers
    rate_check(headers)
    logger.debug('Posted Message')