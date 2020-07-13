import json
import unittest

import requests

from src.etc import Config
from src.main import app
from test import TestUtil


class ShowsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._cookies, cls._username, cls._password = TestUtil.create_user()
        print('OK')

        # Load the shows in memory
        with open('test/config.json', 'r') as config_fp:
            cls._expected_data = json.load(config_fp)

        cls._cookies = TestUtil.add_shows(cls._cookies, cls._expected_data)

    @classmethod
    def tearDownClass(cls) -> None:
        print("Deleting {}... ".format(cls._username), end='')
        res = requests.delete('https://www.tvtime.com/settings/delete_account', headers=Config.HEADERS,
                              cookies=cls._cookies)
        res.raise_for_status()
        print("OK")

    def setUp(self) -> None:
        app.config['SECRET_KEY'] = 'test_key'
        self.client = app.test_client()

    def test_when_not_logged_in_shows_should_ko(self):
        # Test
        response = self.client.get('/shows')

        # Verify
        self.assertEqual('KO', response.json['status'])

    def test_when_fetching_shows_should_return_correct_data(self):
        # Given
        self.client.post('/login', data={'username': self._username, 'password': self._password})

        # Test
        response = self.client.get('/shows')

        # Verify
        json_data = response.json
        self.assertEqual(json_data['count'], len(self._expected_data['series']))
        output_ids = [series['id'] for series in json_data['series']]
        unmatched_ids = []
        for series in self._expected_data['series']:
            expected_id = series['id']
            if expected_id not in output_ids:
                unmatched_ids.append(expected_id)
        self.assertEqual(0, len(unmatched_ids), "The following IDs are not in the output: {}".format(unmatched_ids))


if __name__ == '__main__':
    unittest.main()
