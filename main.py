from typing import Dict
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({})


@app.route('/login', methods=['POST'])
def login():
    if 'username' not in request.form or 'password' not in request.form:
        return jsonify({'status': 'KO', 'reason': 'No username or password provided'})
    username: str = request.form['username'].strip()
    password: str = request.form['password'].strip()
    if len(username) == 0 or len(password) == 0:
        return jsonify({'status': 'KO', 'reason': 'Empty username or password'})
    data = do_login(username, password)
    if data['symfony'] != '' and data['tvstRemember'] != '':
        data.update({'status': 'OK'})
        return jsonify(data)
    return jsonify({'status': 'KO', 'reason': 'Not logged in'})


def do_login(username: str, password: str) -> Dict[str, str]:
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
    resp_login = requests.get('https://www.tvtime.com/login', headers=headers)
    resp_login.raise_for_status()
    symfony_cookie = resp_login.cookies['symfony']
    post_data = {'symfony': symfony_cookie, 'username': username, 'password': password}
    resp_signin = requests.post('https://www.tvtime.com/signin', data=post_data, headers=headers)
    resp_signin.raise_for_status()
    if len(resp_signin.history) == 0 or 'symfony' not in resp_signin.history[0] or 'tvstRemember' not in \
            resp_signin.history[0]:
        return {'symfony': '', 'tvstRemember': ''}
    return {'symfony': resp_signin.history[0].cookies['symfony'],
            'tvstRemember': resp_signin.history[0].cookies['tvstRemember']}
