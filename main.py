from flask import Flask, jsonify, request, session

import Login
import Shows

app = Flask(__name__)
app.secret_key = '<super secret key>'


@app.route('/')
def index():
    return jsonify({})


@app.route('/login', methods=['POST'])
def login():
    session.pop('username', None)
    if not Login.check_login_data(request.form):
        return jsonify({'status': 'KO', 'reason': 'Invalid POST data'})
    if Login.do_login(request.form['username'], request.form['password']):
        return jsonify({'status': 'OK'})
    return jsonify({'status': 'KO', 'reason': 'Not logged in'})


@app.route('/shows')
def shows():
    if 'username' not in session:
        return jsonify({'status': 'KO', 'reason': 'Not logged in'})
    data = Shows.get_shows()
    return jsonify(data)
