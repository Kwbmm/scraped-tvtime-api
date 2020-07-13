import logging
import time
from typing import Tuple, Dict, Any

import requests

from src.etc import Config


def create_user() -> Tuple[Dict, str, str]:
    current_time = int(time.time())
    username = 'user{}'.format(current_time)
    password = username
    email_address = '{username}@asd.asd'.format(username=username)
    logging.info('Creating {}... '.format(username))
    resp = requests.post('https://www.tvtime.com/signup', headers=Config.HEADERS,
                         data={'username': username, 'password': password, 'email': email_address})
    resp.raise_for_status()
    history_cookies = {'symfony': resp.history[0].cookies.get('symfony', ''),
                       'tvstRemember': resp.history[0].cookies.get('tvstRemember', '')}
    cookies = {'symfony': resp.cookies.get('symfony', ''), 'tvstRemember': resp.cookies.get('tvstRemember', '')}
    if all(cookies.values()):
        return cookies, username, password
    elif all(history_cookies.values()):
        return history_cookies, username, password
    else:
        error = "Failed to create user\n\tStatus code={code}\nNo cookies found!".format(code=resp.status_code)
        logging.error(error)
        raise ConnectionError(error)


def add_shows(cookies: Dict[str, Any], shows_data: Dict[str, Any]) -> Dict[str, Any]:
    # Add shows
    for series in shows_data['series']:
        logging.info('Adding {}... '.format(series['name']))
        cookies = _put_and_return_cookies('https://www.tvtime.com/followed_shows', {'show_id': series['id']}, cookies)

        watched_until_payload = {'season': series['watched']['season'], 'episode': series['watched']['episode'],
                                 'show_id': series['id']}
        cookies = _put_and_return_cookies('https://www.tvtime.com/show_watch_until', watched_until_payload, cookies)
    return cookies


def _put_and_return_cookies(url: str, payload: Dict[str, Any], cookies: Dict[str, Any]) -> Dict[str, Any]:
    response = requests.put(url, headers=Config.HEADERS, data=payload, cookies=cookies)
    response.raise_for_status()
    return {'symfony': response.cookies.get('symfony', cookies['symfony']),
            'tvstRemember': response.cookies.get('tvstRemember', cookies['tvstRemember'])}
