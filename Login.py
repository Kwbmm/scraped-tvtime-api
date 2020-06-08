from typing import Dict
from bs4 import BeautifulSoup
import requests
import Utils


def check_login_data(params: Dict) -> bool:
    if not Utils.are_form_data_keys_valid(params, ['username', 'password']):
        return False
    return Utils.are_form_data_values_valid(params)


def do_login(username: str, password: str) -> Dict[str, str]:
    resp_login = requests.get('https://www.tvtime.com/login', headers=Utils.HEADERS)
    resp_login.raise_for_status()
    symfony_cookie = resp_login.cookies['symfony']
    post_data = {'symfony': symfony_cookie, 'username': username, 'password': password}
    resp_signin = requests.post('https://www.tvtime.com/signin', data=post_data, headers=Utils.HEADERS)
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
