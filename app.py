import traceback

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restx import Api, Resource, fields
from werkzeug.utils import escape

from api import cached_response
from api.auth import token_auth
from config import config
from util.logger import log

app = Flask(__name__)
CORS(
    app,
    resources={
        "/auth/": {"origins": ["http://localhost:8080", "http://pandermatt.ch"]},
        "/queries/*": {"origins": ["http://localhost:8080", "http://pandermatt.ch"]},
    }
)
authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
}

api = Api(app, version='0.0.1', title='KenSpace API',
          description='API for KenSpace',
          security='Bearer Auth',
          authorizations=authorizations
          )

queries = api.namespace('queries', description='Query operations')
auth = api.namespace('auth', description='Authentication')

uuid = api.model('UUID', {
    'uuid': fields.String(readOnly=True, description='unique identifier'),
})


@queries.route('/')
class QueryList(Resource):
    @token_auth.login_required
    def get(self):
        """Get all Queries Result"""
        return cached_response.generate_queries(
            escape(request.args.get('uuid')),
            request.args.get('deletedWords'),
            request.headers.get('Authorization')
        )


@auth.route('/')
class AuthHandler(Resource):
    @token_auth.login_required
    def get(self):
        """Check Authentication"""
        return 'successful'


@app.after_request
def after_request(response):
    log.info('%s %s %s %s %s', request.remote_addr, request.method, request.scheme, request.full_path, response.status)
    return response


@app.errorhandler(Exception)
def exceptions(e):
    tb = traceback.format_exc()
    log.error('%s %s %s %s 5xx INTERNAL SERVER ERROR\n%s', request.remote_addr, request.method, request.scheme,
              request.full_path, tb)
    return e.status_code


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


if __name__ == '__main__':
    app.run(threaded=False, processes=config.get_env("PROCESSES_NUMBER"), debug=False)
