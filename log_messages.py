import requests
import logging
import sys
from rate_check import rate_check
import redis
from urlparse import urlparse
import os
import time
import csv
from pymongo import MongoClient
import datetime
from pprint import pprint
import json

#Setup Logger
logger = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
        '%(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

#Set Environment Variables
ROOM_ID = os.getenv('ROOM_ID')
MONGODB_URI = os.getenv('MONGODB_URI')
USER_KEY = os.getenv('USER_KEY')
REDIS_URL = os.getenv('REDIS_URL')

base_url = "https://api.hipchat.com/v2/"
message_log_file = 'message_log.csv'


#get messages and add to csv
def get_messages():
	uri = urlparse(REDIS_URL)
	r = redis.StrictRedis(host = uri.hostname, port = uri.port, password = uri.password)
	last_run = r.get('last_run')
	if last_run:
		pass
	else:
		last_run = 1
	now = int(time.time())
	f = open(message_log_file, 'wb')
	writer = csv.writer(f)
	writer.writerow( ('user_id', 'user_name', 'message'))
	f.close()
	url = base_url + 'room/' + str(ROOM_ID) + '/history'
	payload = {
		'auth_token': USER_KEY,
		'max-results': 999,
		'reverse': 'true',
		'date': now,
		'include_deleted': 'false',
		'end-date': last_run
	}
	get_room_history = requests.get(url, params = payload)
	rate_check(get_room_history.headers)
	write_to_log(get_room_history.text)
	response = json.loads(get_room_history.text)
	while 'next' in response['links']:
		url = response['links']['next']
		payload = {'auth_token': USER_KEY}
		get_room_history = requests.get(url, params = payload)
		rate_check(get_room_history.headers)
		response = get_room_history.json()
		write_to_log(get_room_history.text)
		logger.debug('iteration ' + str(response['startIndex']))
		time.sleep(.1)
	r.set('last_run', now)
		
def write_to_log(response):
	message_log = open(message_log_file, 'ab')
	log = json.loads(response)
	for item in log['items']:
		if 'id' in item['from']:
			user_id = item['from']['id']
			name = item['from']['name']
			name = name.encode('utf-8').strip()
			message = item['message']
			if message:
				message = message.encode('utf-8').strip()
			else:
				message = ''
			messages = open(message_log_file, 'ab')
			unicodewriter = csv.writer(messages)
			unicodewriter.writerow((user_id, name, message))
			messages.close()

def update_trainer():
	client = MongoClient(MONGODB_URI)
	db = client.get_default_database()
	collection = client.messages
	posts = db.posts
	user_ids = []
	#https://api.mongodb.com/python/current/tutorial.html
	with open(message_log_file, 'rb') as message_file:
		messagereader = csv.DictReader(message_file)
		for row in messagereader:
			user_id = row['user_id']
			if user_id not in user_ids:
				user_ids.append(user_id)
		for user_id in iter(user_ids):
			logger.debug('starting user_id: ' + str(user_id))
			messages = ''
			entry = posts.find_one({"_id": user_id})
			if entry:
				messages = entry['text']
				messages = messages.encode('utf-8').strip()
			message_file.seek(0)
			for row in messagereader:
				if row['user_id'] == str(user_id):
					messages += '\n'
					messages += row['message']
			post = {
				'author': 'imitationBot',
				'text': messages,
				'tags': ['messages', str(user_id)],
				'date': datetime.datetime.utcnow(),
				'_id': user_id
			}
			post_id = posts.update_one({'_id': user_id}, {'$set':post}, upsert = True)
			logger.debug('inserted mongodb document ' + str(user_id))
	logger.info('trainers updated')
	os.remove(message_log_file)
			
if __name__ == '__main__':
    get_messages()
    update_trainer()