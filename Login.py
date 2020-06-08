from typing import Dict

import requests
from bs4 import BeautifulSoup


def do_login(username: str, password: str) -> Dict[str, str]:
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
    resp_login = requests.get('https://www.tvtime.com/login', headers=headers)
    resp_login.raise_for_status()
    symfony_cookie = resp_login.cookies['symfony']
    post_data = {'symfony': symfony_cookie, 'username': username, 'password': password}
    resp_signin = requests.post('https://www.tvtime.com/signin', data=post_data, headers=headers)
    resp_signin.raise_for_status()
    if len(resp_signin.history) == 0 or 'symfony' not in resp_signin.history[0].cookies or 'tvstRemember' not in \
            resp_signin.history[0].cookies:
        return {'symfony': '', 'tvstRemember': ''}
    user_id = __get_user_id(resp_signin.text)
    return {'symfony': resp_signin.history[0].cookies['symfony'],
            'tvstRemember': resp_signin.history[0].cookies['tvstRemember'],
            'user_id': user_id}


def __get_user_id(html_page: str) -> str:
    parser = BeautifulSoup(html_page, 'html.parser')
    return parser.select_one('li.profile > a[href*="user/"]')['href'].split('/')[3]
