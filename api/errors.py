from werkzeug.exceptions import BadRequest, Unauthorized


def error_response(message=None):
    if message is not None:
        raise BadRequest(message)
    raise BadRequest()


def unauthorized_response():
    raise Unauthorized()
