from flask import Flask
from flask_cors import CORS
from flask_restx import Api, Resource, fields

from api.auth import token_auth

app = Flask(__name__)
CORS(
    app,
    resources={
        "/auth/": {"origins": ["http://localhost:8080"]},
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

todo = api.model('Todo', {
    'id': fields.Integer(readOnly=True, description='The task unique identifier'),
    'task': fields.String(required=True, description='The task details')
})


@queries.route('/')
class TodoList(Resource):
    @token_auth.login_required
    def get(self):
        """List all tasks"""
        return {"hoi": 1}

    @token_auth.login_required
    @queries.expect(todo)
    def post(self):
        """Create a new task"""
        return api.payload, 201


@queries.route('/<int:id>')
@queries.response(404, 'Todo not found')
@queries.param('id', 'The task identifier')
class Todo(Resource):
    @token_auth.login_required
    def get(self, id):
        """Fetch a given resource"""
        return {"id": id}

    @token_auth.login_required
    @queries.response(204, 'Todo deleted')
    def delete(self, id):
        return '', 204

    @token_auth.login_required
    @queries.expect(todo)
    def put(self, id):
        return api.payload


auth = api.namespace('auth', description='Authentication')


@auth.route('/')
class AuthHandler(Resource):
    @token_auth.login_required
    def get(self):
        """Check Authentication"""
        return 'successful'


if __name__ == '__main__':
    app.run(debug=False)
