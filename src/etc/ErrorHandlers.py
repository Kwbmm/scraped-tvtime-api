from typing import Any

from flask import jsonify


def ko_error(error) -> Any:
    return jsonify({'status': 'KO', 'reason': '{} - {}'.format(error.code, error.description)}), error.code
