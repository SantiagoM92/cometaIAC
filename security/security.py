from functools import wraps
from flask import request, jsonify

from config import Config


def require_apikey(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        api_key = Config.API_KEY
        if request.headers.get('X-API-KEY') and request.headers['X-API-KEY'] == api_key:
            return view_function(*args, **kwargs)
        else:
            return jsonify({"error": "API key is invalid or missing"}), 401

    return decorated_function
