from flask import Flask, request
from flask_cors import CORS
from flask_restx import Api, Resource, fields
from werkzeug.utils import escape

from api import cached_response
from api.auth import token_auth
from config import config

app = Flask(__name__)
CORS(
    app,
    resources={
        "/auth/": {"origins": ["http://localhost:8080"]},
        "/queries/*": {"origins": ["http://localhost:8080"]},
        "/facet/*": {"origins": ["http://localhost:8080"]},
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
facet = api.namespace('facet', description='Generate facet')
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
            request.args.get('deletedWords')
        )


@facet.route('/')
class FacetList(Resource):
    @token_auth.login_required
    def get(self):
        """Get all Facet"""
        return cached_response.generate_facet(
            escape(request.args.get('uuid'))
        )


@auth.route('/')
class AuthHandler(Resource):
    @token_auth.login_required
    def get(self):
        """Check Authentication"""
        return 'successful'


if __name__ == '__main__':
    app.run(threaded=False, processes=config.get_env("PROCESSES_NUMBER"), debug=False)
