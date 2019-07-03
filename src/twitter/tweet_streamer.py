import sys
import os
import logging
import json
import pika
from tweepy import OAuthHandler, StreamListener

from src.utilities import RabbitConnection

class TweepyStreamingInterface:
    def __init__(self, auth_config):
        # TODO list out kwargs once final
        self.auth_config = auth_config 
        self.data = self.cache = iter([])
        
        try:
            self._connect()
            print('connected') # replace with logging
        except Error as e:
            print(e)

        self.publisher = RabbitConnection()

    def __iter__(self):
        import itertools as it
        self.data, self.cache = it.tee(self.cache)
        return iter(self.data)
    

    def __next__(self):
        return _pushUpdates(next(self.data))

    
    def _connect(self):
        try:
            self.auth = OAuthHandler(self.auth_config['CONSUMER_KEY'], self.auth_config['CONSUMER_SECRET'])
            self.auth.set_access_token(self.auth_config['ACCESS_TOKEN_KEY'], self.auth_config['ACCESS_TOKEN_SECRET'])
            return True
        except:
            return False

    def _pushUpdates(self, data):
        """
        Batch run stored updates here
        """
        return data