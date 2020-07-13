from flask import Flask, jsonify, request, session

from src.endpoints_processors import Login, Shows
from src.etc import Config, Utils
from src.etc.Utils import ko_response

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
        return Utils.ok_response()
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


@app.route('/show/<int:show_id>/follow', methods=['PUT', 'DELETE'])
def follow_show(show_id: int):
    if 'username' not in session:
        return ko_response('Not logged in')
    url_endpoint = 'https://www.tvtime.com/followed_shows'
    response = {}
    show_payload = {'show_id': show_id}

    if request.method == 'PUT':
        response = Utils.put(url_endpoint, show_payload, cookies=Utils.get_tvtime_cookies()).json()
    elif request.method == 'DELETE':
        response = Utils.delete(url_endpoint, show_payload, cookies=Utils.get_tvtime_cookies()).json()

    if 'result' not in response or response['result'] != 'OK':
        return Utils.ko_response('{} request failed!'.format(request.method))
    return Utils.ok_response()


@app.route('/episode/<int:episode_id>/watched', methods=['PUT', 'DELETE'])
def mark_watched(episode_id: int):
    if 'username' not in session:
        return ko_response('Not logged in')
    url_endpoint = 'https://www.tvtime.com/watched_episodes'
    response = {}
    episode_payload = {'episode_id': episode_id}

    if request.method == 'PUT':
        response = Utils.put(url_endpoint, episode_payload,
                             cookies=Utils.get_tvtime_cookies()).json()
    elif request.method == 'DELETE':
        response = Utils.delete(url_endpoint, episode_payload,
                                cookies=Utils.get_tvtime_cookies()).json()

    if 'result' not in response or response['result'] != 'OK':
        return Utils.ko_response('{} request failed!'.format(request.method))
    return Utils.ok_response()
