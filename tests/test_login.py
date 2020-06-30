import json
import time
import unittest

import requests

from src.etc import Config
from src.main import app


class LoginTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        with open('tests/config.json', 'r') as config_fp:
            test_shows = json.load(config_fp)
        current_time = int(time.time())
        username = 'user{}'.format(current_time)
        password = username
        email_address = '{username}@asd.asd'.format(username=username)
        print('Creating {}'.format(username))
        resp = requests.post('https://www.tvtime.com/signup', headers=Config.HEADERS,
                             data={'username': username, 'password': password, 'email': email_address})
        resp.raise_for_status()
        history_cookies = {'symfony': resp.history[0].cookies.get('symfony', ''),
                           'tvstRemember': resp.history[0].cookies.get('tvstRemember', '')}
        cookies = {'symfony': resp.cookies.get('symfony', ''), 'tvstRemember': resp.cookies.get('tvstRemember', '')}
        cls._cookies = {}
        if all(cookies.values()):
            cls._cookies = cookies
        elif all(history_cookies.values()):
            cls._cookies = history_cookies
        else:
            error = "Failed to create user\n\tStatus code={code}\nNo cookies found!".format(code=resp.status_code)
            raise ConnectionError(error)
        # TODO: This should be logged
        print('Created user {}'.format(username))

        # Add shows
        for series in test_shows['series']:
            # TODO: This should be logged
            print('Adding {}'.format(series['name']))
            cls.put_and_update_cookies('https://www.tvtime.com/followed_shows', {'show_id': series['id']})
            watched_until_payload = {'season': series['watched']['season'], 'episode': series['watched']['episode'],
                                     'show_id': series['id']}
            cls.put_and_update_cookies('https://www.tvtime.com/show_watch_until', watched_until_payload)
            # TODO: This should be logged
            print('Added {}'.format(series['name']))

    @classmethod
    def put_and_update_cookies(cls, url, payload):
        add_show_resp = requests.put(url, headers=Config.HEADERS,
                                     data=payload, cookies=cls._cookies)
        add_show_resp.raise_for_status()
        cls._cookies = {'symfony': add_show_resp.cookies.get('symfony', cls._cookies['symfony']),
                        'tvstRemember': add_show_resp.cookies.get('tvstRemember', cls._cookies['tvstRemember'])}

    @classmethod
    def tearDownClass(cls) -> None:
        res = requests.delete('https://www.tvtime.com/settings/delete_account', headers=Config.HEADERS,
                              cookies=cls._cookies)
        res.raise_for_status()

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
