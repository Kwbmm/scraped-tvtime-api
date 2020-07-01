import json
import random
import unittest

import requests

from src.etc import Config
from src.main import app
from tests import TestUtil


class ShowsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._cookies, cls._username, cls._password = TestUtil.create_user()
        print('OK')
        cls._cookies = TestUtil.add_shows(cls._cookies)

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
        with open('tests/config.json', 'r') as fp:
            expected_data = json.load(fp)

        # Test
        response = self.client.get('/shows')

        # Verify
        json_data = response.json
        self.assertEqual(json_data['count'], len(expected_data['series']))
        output_ids = [series['id'] for series in json_data['series']]
        unmatched_ids = []
        for series in expected_data['series']:
            expected_id = series['id']
            if expected_id not in output_ids:
                unmatched_ids.append(expected_id)
        self.assertEqual(0, len(unmatched_ids), "The following IDs are not in the output: {}".format(unmatched_ids))

    def test_when_not_logged_in_show_should_ko(self):
        # Test
        response = self.client.get('/show/42')

        # Verify
        self.assertEqual('KO', response.json['status'])

    def test_when_fetching_single_show_should_return_episodes(self):
        # Given
        self.client.post('/login', data={'username': self._username, 'password': self._password})
        with open('tests/config.json', 'r') as fp:
            expected_data = json.load(fp)

        selected_series = expected_data['series'][random.randint(0, len(expected_data['series']))]
        # TODO: This should be logged
        print("Testing with series {}".format(selected_series['name']))
        selected_series_id = selected_series['id']

        # Test
        response = self.client.get('/show/{}'.format(selected_series_id))
        json_data = response.json

        # Verify
        watched_episodes = sum(
            [episode['watched'] for season in json_data['seasons'] for episode in season['episodes']])
        self.assertEqual(selected_series['count_watched'], watched_episodes)


if __name__ == '__main__':
    unittest.main()
