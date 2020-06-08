from flask import Flask, jsonify, request
import Login

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
    data = Login.do_login(username, password)
    if data['symfony'] != '' and data['tvstRemember'] != '' and data['user_id'] != '':
        data.update({'status': 'OK'})
        return jsonify(data)
    return jsonify({'status': 'KO', 'reason': 'Not logged in'})
