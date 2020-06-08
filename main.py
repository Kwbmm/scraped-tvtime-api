from flask import Flask, jsonify, request
import Login
import Utils

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({})


@app.route('/login', methods=['POST'])
def login():
    if not Login.check_login_data(request.form):
        return jsonify({'status': 'KO', 'reason': 'Invalid POST data'})
    data = Login.do_login(request.form['username'], request.form['password'])
    if Utils.are_form_data_keys_valid(data, ['symfony', 'tvstRemember', 'user_id']) and \
            Utils.are_form_data_values_valid(data):
        data.update({'status': 'OK'})
        return jsonify(data)
    return jsonify({'status': 'KO', 'reason': 'Not logged in'})
