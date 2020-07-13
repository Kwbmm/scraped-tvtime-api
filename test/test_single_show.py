import json
import random
import unittest

import requests

from src.etc import Config
from src.main import app
from test import TestUtil


class TestSingleShow(unittest.TestCase):
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

    def test_when_not_logged_in_show_should_ko(self):
        # Test
        response = self.client.get('/show/42')

        # Verify
        self.assertEqual('KO', response.json['status'])

    def test_when_fetching_single_show_should_return_episodes(self):
        # Given
        self.client.post('/login', data={'username': self._username, 'password': self._password})

        selected_show_index = random.randrange(0, len(self._expected_data['series']))
        selected_series = self._expected_data['series'][selected_show_index]
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

    def test_when_following_show_should_ok(self):
        # Given
        self.client.post('/login', data={'username': self._username, 'password': self._password})
        to_follow_data = {'id': 295829, 'name': 'The Man in the High Castle'}

        # Test
        response = self.client.put('/show/{}/follow'.format(to_follow_data['id']))
        json_data = response.json

        # Verify
        self.assertEqual('OK', json_data['status'])
        followed_shows = self.client.get('/shows')
        self.assertEqual(len(self._expected_data['series']) + 1, followed_shows.json['count'])

        fetched_show_ids = [series['id'] for series in followed_shows.json['series']]
        self.assertTrue(to_follow_data['id'] in fetched_show_ids)

    def test_when_unfollowing_show_should_ok(self):
        # Given
        self.client.post('/login', data={'username': self._username, 'password': self._password})
        selected_series_to_unfollow = random.randrange(0, len(self._expected_data['series']))
        show_id_to_unfollow = self._expected_data['series'][selected_series_to_unfollow]['id']

        # Test
        response = self.client.delete('/show/{}/follow'.format(show_id_to_unfollow))
        json_data = response.json

        # Verify
        self.assertEqual('OK', json_data['status'])
        followed_shows = self.client.get('/shows')
        self.assertEqual(len(self._expected_data['series']) - 1, followed_shows.json['count'])

        fetched_show_ids = [series['id'] for series in followed_shows.json['series']]
        self.assertFalse(show_id_to_unfollow in fetched_show_ids)


if __name__ == '__main__':
    unittest.main()
