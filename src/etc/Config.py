import base64
import json

with open('config.json', 'r') as fp_config:
    config_data = json.load(fp_config)
    HEADERS = config_data['http_headers']
    SESSION_KEY = base64.b64decode(config_data['session_key'])
