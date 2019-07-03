import json
import os
import unittest
import dotenv

from src.twitter import TweepyStreamingInterface

class TestTwitterStream(unittest.TestCase):
    def setUp(self):
        # default .env code, untested
        project_dir = os.path.join(os.path.dirname(__file__), os.pardir)
        dotenv_path = os.path.join(project_dir, '.env')
        dotenv.load_dotenv(dotenv_path)
        
        auth_config = {
            'CONSUMER_KEY': os.environ.get('CONSUMER_KEY'),
            'CONSUMER_SECRET': os.environ.get('CONSUMER_SECRET'),
            'ACCESS_TOKEN_KEY': os.environ.get('ACCESS_TOKEN_KEY'),
            'ACCESS_TOKEN_SECRET': os.environ.get('ACCESS_TOKEN_SECRET')
        }

        self.api = TweepyStreamingInterface(**auth_config)


    def test_interface_login(self):
        self.assertTrue(self.api._connect())