from werkzeug.exceptions import BadRequest, Unauthorized, NotFound


def error_response(message=None):
    if message is not None:
        raise BadRequest(message)
    raise BadRequest()


def unauthorized_response():
    raise Unauthorized()


def not_found_response():
    raise NotFound()
