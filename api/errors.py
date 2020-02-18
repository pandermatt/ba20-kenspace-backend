from werkzeug.exceptions import BadRequest


def error_response(status_code, message=None):
    raise BadRequest(status_code)
