from flask import Flask
from flask_cors import CORS
from flask_restx import Api, Resource

from api.auth import token_auth
from api.cached_response import generate_queries, generate_facet

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


@queries.route('/')
class QueryList(Resource):
    @token_auth.login_required
    def get(self):
        """Get all Queries Result"""
        return generate_queries()


facet = api.namespace('facet', description='Generate facet')


@facet.route('/')
class FacetList(Resource):
    @token_auth.login_required
    def get(self):
        """Get all Facet"""
        return generate_facet()


auth = api.namespace('auth', description='Authentication')


@auth.route('/')
class AuthHandler(Resource):
    @token_auth.login_required
    def get(self):
        """Check Authentication"""
        return 'successful'


if __name__ == '__main__':
    app.run(threaded=False, processes=3,debug=False)
