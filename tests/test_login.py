import unittest

import flask
import requests

from src.etc import Config
from src.main import app
from tests import TestUtil


class LoginTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._cookies, cls._username, cls._password = TestUtil.create_user()
        print('OK')

    @classmethod
    def tearDownClass(cls) -> None:
        res = requests.delete('https://www.tvtime.com/settings/delete_account', headers=Config.HEADERS,
                              cookies=cls._cookies)
        res.raise_for_status()

    def setUp(self) -> None:
        app.config['SECRET_KEY'] = 'test_key'
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

    def test_when_correct_user_and_pass_should_ok(self):
        # Given
        payload = {'username': self._username, 'password': self._password}

        with self.client as c:
            with c.session_transaction() as s:
                s['username'] = {'dummy': '42'}
            # Test
            result = c.post('/login', data=payload)
            has_dummy_key = 'dummy' in flask.session['username']
            has_userdata = 'user_id' in flask.session['username'] and 'symfony' in flask.session[
                'username'] and 'tvstRemember' in flask.session['username']

        # Verify
        self.assertEqual(result.json['status'], 'OK')
        self.assertFalse(has_dummy_key)
        self.assertTrue(has_userdata)


if __name__ == '__main__':
    unittest.main()
