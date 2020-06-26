from typing import Dict

from bs4 import BeautifulSoup
from flask import session

from src.etc import Utils


def check_login_data(params: Dict) -> bool:
    if not Utils.are_form_data_keys_valid(params, ['username', 'password']):
        return False
    return Utils.are_form_data_values_valid(params)


def do_login(username: str, password: str) -> bool:
    resp_login = Utils.get('https://www.tvtime.com/login', False)
    symfony_cookie = resp_login.cookies['symfony']
    post_data = {'symfony': symfony_cookie, 'username': username, 'password': password}
    resp_signin = Utils.post('https://www.tvtime.com/signin', post_data, False)
    if len(resp_signin.history) == 0 or 'symfony' not in resp_signin.history[0].cookies or 'tvstRemember' not in \
            resp_signin.history[0].cookies:
        return False
    user_id = __get_user_id(resp_signin.text)
    if len(user_id) > 0:
        session['username'] = {'symfony': resp_signin.history[0].cookies['symfony'],
                               'tvstRemember': resp_signin.history[0].cookies['tvstRemember'],
                               'user_id': user_id}
        return True
    return False


def __get_user_id(html_page: str) -> str:
    parser = BeautifulSoup(html_page, 'html.parser')
    return parser.select_one('li.profile > a[href*="user/"]')['href'].split('/')[3]
