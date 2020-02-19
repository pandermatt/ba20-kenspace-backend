from flask_httpauth import HTTPTokenAuth

from api.errors import unauthorized_response

token_auth = HTTPTokenAuth()


@token_auth.verify_token
def verify_token(token):
    return token == "hallo"


@token_auth.error_handler
def token_auth_error():
    return unauthorized_response()

# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxiii-application-programming-interfaces-apis
