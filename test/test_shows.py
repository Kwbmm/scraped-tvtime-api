import unittest

from src.main import app
from test.BaseTestClass import BaseTestClass


class ShowsTestCase(BaseTestClass):
    def setUp(self) -> None:
        app.config['SECRET_KEY'] = 'test_key'
        self.client = app.test_client()

    def test_when_not_logged_in_shows_should_ko(self):
        # Test
        response = self.client.get('/shows')

        # Verify
        self.assertEqual(401, response.status_code)

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
