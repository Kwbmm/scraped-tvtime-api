import json
import logging
import unittest

import requests

from src.etc import Config
from test import TestUtil


class BaseTestClass(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._cookies, cls._username, cls._password = TestUtil.create_user()

        # Load the shows in memory
        with open('test/config.json', 'r') as config_fp:
            cls._expected_data = json.load(config_fp)

        cls._cookies = TestUtil.add_shows(cls._cookies, cls._expected_data)

    @classmethod
    def tearDownClass(cls) -> None:
        logging.info("Deleting {}... ".format(cls._username))
        res = requests.delete('https://www.tvtime.com/settings/delete_account', headers=Config.HEADERS,
                              cookies=cls._cookies)
        res.raise_for_status()


if __name__ == '__main__':
    unittest.main()
