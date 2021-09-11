from flask import Flask, jsonify, request, session
from werkzeug.exceptions import abort

from src.endpoints_processors import Login, Shows
from src.etc import Config, Utils, ErrorHandlers

app = Flask(__name__)
app.secret_key = Config.SESSION_KEY

app.register_error_handler(400, ErrorHandlers.ko_error)
app.register_error_handler(401, ErrorHandlers.ko_error)
app.register_error_handler(404, ErrorHandlers.ko_error)
app.register_error_handler(502, ErrorHandlers.ko_error)


@app.route('/')
def index():
    return abort(404, 'Page not found')


@app.route('/login', methods=['POST'])
def login():
    session.pop('username', None)
    if not Login.check_login_data(request.form):
        return abort(400, 'Invalid POST data')
    if Login.do_login(request.form['username'], request.form['password']):
        return Utils.ok_response()
    return abort(401, 'Not logged in')


@app.route('/shows')
def shows():
    if 'username' not in session:
        return abort(401, 'Not logged in')
    data = Shows.get_shows()
    return jsonify(data)


@app.route('/show/<int:show_id>')
def show(show_id: int):
    if 'username' not in session:
        return abort(401, 'Not logged in')
    return jsonify(Shows.get_show(show_id))


@app.route('/show/<int:show_id>/follow', methods=['PUT', 'DELETE'])
def follow_show(show_id: int):
    if 'username' not in session:
        return abort(401, 'Not logged in')
    url_endpoint = 'https://www.tvtime.com/followed_shows'
    response = {}
    show_payload = {'show_id': show_id}

    if request.method == 'PUT':
        response = Utils.put(url_endpoint, show_payload, cookies=Utils.get_tvtime_cookies()).json()
        if 'result' not in response or response['result'] != 'OK':
            return abort(502, '{} request failed!'.format(request.method))
    elif request.method == 'DELETE':
        response = Utils.delete(url_endpoint, show_payload, cookies=Utils.get_tvtime_cookies())
        if not response.ok:
            return abort(502, '{} request failed!'.format(request.method))

    return Utils.ok_response()


@app.route('/episode/<int:episode_id>/watched', methods=['PUT', 'DELETE'])
def mark_watched(episode_id: int):
    if 'username' not in session:
        return abort(401, 'Not logged in')
    url_endpoint = 'https://www.tvtime.com/watched_episodes'
    response = {}
    episode_payload = {'episode_id': episode_id}

    if request.method == 'PUT':
        response = Utils.put(url_endpoint, episode_payload,
                             cookies=Utils.get_tvtime_cookies()).json()
        if 'result' not in response or response['result'] != 'OK':
            return abort(502, '{} request failed!'.format(request.method))
    elif request.method == 'DELETE':
        response = Utils.delete(url_endpoint, episode_payload,
                                cookies=Utils.get_tvtime_cookies())
        if not response.ok:
            return abort(502, '{} request failed!'.format(request.method))

    return Utils.ok_response()
