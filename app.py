import http
import traceback
from datetime import datetime

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restx import Api, Resource, fields
from werkzeug.datastructures import FileStorage
from werkzeug.utils import escape

from api import cached_response
from api.auth import token_auth
from config import config
from file_io.feedback_writer import save_feedback
from file_io.file_upload import handle_file_upload
from util.logger import log

app = Flask(__name__)
CORS(
    app,
    resources={
        "/auth/": {"origins": ["http://localhost:8080", "https://pandermatt.ch", "https://kenspace.ch"]},
        "/queries/*": {"origins": ["http://localhost:8080", "https://pandermatt.ch", "https://kenspace.ch"]},
        "/feedback/*": {"origins": ["http://localhost:8080", "https://pandermatt.ch", "https://kenspace.ch"]},
        "/upload/*": {"origins": ["http://localhost:8080", "https://pandermatt.ch", "https://kenspace.ch"]},
    }
)
authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
}

swagger_ui_enabled = '/'
if config.get_env('PRODUCTION') == 'Y':
    swagger_ui_enabled = False

api = Api(app, version='0.1.0', title='KenSpace API',
          description='API for KenSpace',
          security='Bearer Auth',
          authorizations=authorizations,
          doc=swagger_ui_enabled
          )

queries = api.namespace('queries', description='Query operations')
auth = api.namespace('auth', description='Authentication')
feedback = api.namespace('feedback', description='Submit Feedback')
upload = api.namespace('upload', description='Upload Data')

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
            request.headers.get('Authorization'),
            request.args.get('settings')
        )


@auth.route('/')
class AuthHandler(Resource):
    @token_auth.login_required
    def get(self):
        """Check Authentication"""
        return 'successful'


@feedback.route('/')
class FeedbackHandler(Resource):
    @token_auth.login_required
    def post(self):
        """Submit feedback"""
        save_feedback(
            request.headers.get('Authorization'),
            request.args.get('uuid'),
            request.args.get('isHelpful'),
            request.args.get('movieTitle'),
            request.args.get('search'),
            request.args.get('facet'),
            request.args.get('delete'),
            request.args.get('similarClusterActive'),
            request.args.get('resultCount'),
            datetime.now()
        )
        return '', http.HTTPStatus.NO_CONTENT


upload_parser = api.parser()
upload_parser.add_argument('file', location='files',
                           type=FileStorage, required=True)


@upload.route('/')
@upload.expect(upload_parser)
class Upload(Resource):
    @token_auth.login_required
    def post(self):
        response = handle_file_upload(request.files['file'])
        return response, 201


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
