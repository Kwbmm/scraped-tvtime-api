import unittest

from src.main import app
from test.BaseTestClass import BaseTestClass


class EpisodeTestCase(BaseTestClass):
    def setUp(self) -> None:
        app.config['SECRET_KEY'] = 'test_key'
        self.client = app.test_client()

    def test_when_not_logged_in_episode_watched_should_ko(self):
        # Test
        response = self.client.put('/episode/42/watched')

        # Verify
        self.assertEqual('KO', response.json['status'])

    def test_when_episode_watched_should_ok(self):
        # Given
        login_resp = self.client.post('/login', data={'username': self._username, 'password': self._password})
        self.assertEqual('OK', login_resp.json['status'])
        selected_series = self._expected_data['series'][0]  # The Office
        retrieved_show_data = self.client.get('/show/{}'.format(selected_series['id'])).json
        expected_episode_id = self.get_expected_episode_id(retrieved_show_data, False)

        # Test
        response = self.client.put('/episode/{}/watched'.format(expected_episode_id))

        # Verify
        self.assertEqual('OK', response.json['status'])
        retrieved_show_data = self.client.get('/show/{}'.format(selected_series['id'])).json
        expected_watched_episode = self.get_expected_episode(expected_episode_id, retrieved_show_data)
        self.assertTrue(expected_watched_episode['watched'],
                        "Episode '{name}' with id {ep_id} and number {num} has not been marked as watched".format(
                            name=expected_watched_episode['name'], ep_id=expected_watched_episode['id'],
                            num=expected_watched_episode['number']))

    def test_when_episode_unwatched_should_ok(self):
        # Given
        login_resp = self.client.post('/login', data={'username': self._username, 'password': self._password})
        self.assertEqual('OK', login_resp.json['status'])
        selected_series = self._expected_data['series'][0]  # The Office
        retrieved_show_data = self.client.get('/show/{}'.format(selected_series['id'])).json
        expected_episode_id = self.get_expected_episode_id(retrieved_show_data, True)

        # Test
        response = self.client.delete('/episode/{}/watched'.format(expected_episode_id))

        # Verify
        self.assertEqual('OK', response.json['status'])
        retrieved_show_data = self.client.get('/show/{}'.format(selected_series['id'])).json
        expected_unwatched_episode = self.get_expected_episode(expected_episode_id, retrieved_show_data)
        self.assertFalse(expected_unwatched_episode['watched'],
                         "Episode '{name}' with id {ep_id} and number {num} is still marked as watched".format(
                             name=expected_unwatched_episode['name'], ep_id=expected_unwatched_episode['id'],
                             num=expected_unwatched_episode['number']))

    def get_expected_episode_id(self, retrieved_show_data, watched):
        for season in retrieved_show_data['seasons']:
            for episode in season['episodes']:
                if episode['watched'] == watched:
                    return episode['id']

    def get_expected_episode(self, expected_episode_id, retrieved_show_data):
        for season in retrieved_show_data['seasons']:
            for episode in season['episodes']:
                if episode['id'] == expected_episode_id:
                    return episode


if __name__ == '__main__':
    unittest.main()
