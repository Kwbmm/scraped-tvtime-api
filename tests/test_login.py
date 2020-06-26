import time
import unittest

import requests

from src.etc import Config
from src.main import app


class LoginTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        current_time = int(time.time())
        username = 'user{}'.format(current_time)
        password = username
        email_address = '{username}@asd.asd'.format(username=username)
        resp = requests.post('https://www.tvtime.com/signup', headers=Config.HEADERS,
                             data={'username': username, 'password': password, 'email': email_address})
        resp.raise_for_status()
        if 'symfony' not in resp.cookies or 'tvstRemember' not in resp.cookies or len(
                resp.cookies['symfony']) == 0 or len(resp.cookies['tvstRemember']) == 0:
            raise ConnectionError("Failed to create user")
        # TODO: This should be removed
        print('Created user {}'.format(username))
        cls._cookies = {'symfony': resp.cookies['symfony'], 'tvstRemember': resp.cookies['tvstRemember']}
        # TODO: Should add series

    @classmethod
    def tearDownClass(cls) -> None:
        requests.delete('https://www.tvtime.com/settings/delete_account', headers=Config.HEADERS, cookies=cls._cookies)

    def setUp(self) -> None:
        self.client = app.test_client()

    def test_when_wrong_keys_should_ko(self):
        # Given
        payload = {'wrong': 'data'}

        # Test
        result = self.client.post('/login', data=payload)

        # Verify
        self.assertEqual(result.json['status'], 'KO')

    def test_when_empty_user_or_pass_should_ko(self):
        # Given
        payload = {'username': '      ', 'password': 'whatever'}

        # Test
        result = self.client.post('/login', data=payload)

        # Verify
        self.assertEqual(result.json['status'], 'KO')

    def test_when_wrong_user_or_pass_should_ko(self):
        # Given
        payload = {'username': 'dummy', 'password': 'still_dummy'}

        # Test
        result = self.client.post('/login', data=payload)

        # Verify
        self.assertEqual(result.json['status'], 'KO')


if __name__ == '__main__':
    unittest.main()
