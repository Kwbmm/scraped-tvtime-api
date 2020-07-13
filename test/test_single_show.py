import logging
import random
import unittest

from src.main import app
from test.BaseTestClass import BaseTestClass


class TestSingleShow(BaseTestClass):
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
        login_resp = self.client.post('/login', data={'username': self._username, 'password': self._password})
        self.assertEqual('OK', login_resp.json['status'])
        selected_show_index = random.randrange(0, len(self._expected_data['series']))
        selected_series = self._expected_data['series'][selected_show_index]
        logging.info("Testing with series {}".format(selected_series['name']))
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
        login_resp = self.client.post('/login', data={'username': self._username, 'password': self._password})
        self.assertEqual('OK', login_resp.json['status'])
        expected_shows = self.client.get('/shows').json
        expected_count = expected_shows['count'] + 1
        to_follow_data = {'id': 295829, 'name': 'The Man in the High Castle'}

        # Test
        response = self.client.put('/show/{}/follow'.format(to_follow_data['id'])).json

        # Verify
        self.assertEqual('OK', response['status'])
        followed_shows = self.client.get('/shows')
        self.assertEqual(expected_count, followed_shows.json['count'])

        fetched_show_ids = [series['id'] for series in followed_shows.json['series']]
        self.assertTrue(to_follow_data['id'] in fetched_show_ids)

    def test_when_unfollowing_show_should_ok(self):
        # Given
        login_resp = self.client.post('/login', data={'username': self._username, 'password': self._password})
        self.assertEqual('OK', login_resp.json['status'])
        expected_shows = self.client.get('/shows').json
        expected_count = expected_shows['count'] - 1
        to_unfollow_show_id = expected_shows['series'][random.randrange(0, expected_shows['count'])]['id']

        # Test
        response = self.client.delete('/show/{}/follow'.format(to_unfollow_show_id)).json

        # Verify
        self.assertEqual('OK', response['status'])
        followed_shows = self.client.get('/shows')
        self.assertEqual(expected_count, followed_shows.json['count'])

        fetched_show_ids = [series['id'] for series in followed_shows.json['series']]
        self.assertFalse(to_unfollow_show_id in fetched_show_ids)


if __name__ == '__main__':
    unittest.main()
