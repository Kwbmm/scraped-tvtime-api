from typing import Dict, List, Any

import requests
from flask import session

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}


def are_form_data_keys_valid(params: Dict[str, any], expected_keys: List[str]) -> bool:
    for key in expected_keys:
        if key not in params:
            return False
    return True


def are_form_data_values_valid(params: Dict[str, str]) -> bool:
    for value in params.values():
        if len(value.strip()) == 0:
            return False
    return True


def update_cookies(cookies: Any) -> None:
    old_session_cookie = session['username']['symfony']
    old_remember_cookie = session['username']['tvstRemember']
    session['username']['symfony'] = cookies.get('symfony', old_session_cookie)
    session['username']['tvstRemember'] = cookies.get('tvstRemember', old_remember_cookie)
