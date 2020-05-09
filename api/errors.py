from werkzeug.exceptions import BadRequest, Unauthorized, NotFound

from util.logger import log


def error_response(message=None):
    log.error(f'BadRequest')
    if message is not None:
        log.error(f'with: {message}')
        raise BadRequest(message)
    raise BadRequest()


def unauthorized_response():
    log.error(f'Unauthorized')
    raise Unauthorized()


def not_found_response():
    log.error(f'NotFound')
    raise NotFound()
