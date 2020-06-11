from flask import Flask, jsonify, request, session

import Config
import Login
import Shows
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
