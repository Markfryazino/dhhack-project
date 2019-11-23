from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from json import dumps
from flask_jsonpify import jsonify
from datetime import datetime
from hashlib import md5
from os import urandom
import werkzeug
from prod import pipeline, production

docs_c, wordset_c, full_c, docs_t, wordset_t, full_t, texts, fulls, sets, model, tfidf, fnames = pipeline()

# Initialize flask app and api
app = Flask(__name__)
api = Api(app)

file_index = 0


class AnalyzeFile(Resource):
    def post(self):
        global file_index
        args = file_parser.parse_args()
        file = args['file']
        print(file)
        text = file.read().decode('utf-8')
        text = text.replace('\n', '<br>')
        file_index += 1
        a = production(text, model, sets, fnames, tfidf, 1)
        print(a)
        return jsonify({'data': a})


file_parser = reqparse.RequestParser()
file_parser.add_argument(
    'file',
    type=werkzeug.datastructures.FileStorage,
    location='files')


api.add_resource(AnalyzeFile, '/api/analyze_file')

if __name__ == '__main__':
    app.run(port=1337)
