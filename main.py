import requests
from flask import Flask, jsonify, request, session

import Config
import Login
import Shows
import Utils
from Utils import ko_response

app = Flask(__name__)
app.secret_key = Config.SESSION_KEY


@app.route('/')
def index():
    return jsonify({})


@app.route('/login', methods=['POST'])
def login():
    session.pop('username', None)
    if not Login.check_login_data(request.form):
        return ko_response('Invalid POST data')
    if Login.do_login(request.form['username'], request.form['password']):
        return jsonify({'status': 'OK'})
    return ko_response('Not logged in')


@app.route('/shows')
def shows():
    if 'username' not in session:
        return ko_response('Not logged in')
    data = Shows.get_shows()
    return jsonify(data)


@app.route('/show/<int:show_id>')
def show(show_id: int):
    if 'username' not in session:
        return ko_response('Not logged in')
    return jsonify(Shows.get_show(show_id))


@app.route('/episode/<int:episode_id>/watched', methods=['PUT', 'DELETE'])
def mark_watched(episode_id: int):
    episode_payload = {'episode_id': episode_id}
    if request.method == 'PUT':
        result = requests.put('https://www.tvtime.com/watched_episodes', headers=Config.HEADERS,
                              cookies=Utils.get_tvtime_cookies(), data=episode_payload)
        result.raise_for_status()
        return jsonify(result.json())
    elif request.method == 'DELETE':
        result = requests.delete('https://www.tvtime.com/watched_episodes', headers=Config.HEADERS,
                                 cookies=Utils.get_tvtime_cookies(), data=episode_payload)
        result.raise_for_status()
        return jsonify(result.json())
    return jsonify({})
