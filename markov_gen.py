import markovify
from pymongo import MongoClient
import logging
import os
import re
import nltk
import requests

logger = logging.getLogger(__name__)

MONGODB_URI = os.getenv('MONGODB_URI')
USER_KEY = os.getenv('USER_KEY')

class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        words = [ "::".join(tag) for tag in nltk.pos_tag(words) ]
        return words

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence

def get_user_id(mention_name):
    pass

def gen_markov(user_id):
    client = MongoClient(MONGODB_URI)
    db = client.get_default_database()
    posts = db.posts
    entry = posts.find_one({"_id": user_id})
    corpus = entry['text']
    text_model = markovify.Text(corpus)
    return text_model.make_sentence()