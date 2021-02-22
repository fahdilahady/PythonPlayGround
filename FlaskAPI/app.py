from flask import Flask, request, abort
from flask_restful import Api, Resource

app = Flask(__name__)

api = Api(app)

class EchoReverse(Resource):
    def post(self, msg):
        if len(msg) > 20:
            abort(400, 'message length cannot exceed 20 chars')
        
        if not msg.isalnum():
            abort(400, 'message should contain only alphanumeric characters')

        return { "message": f"{msg[::-1]}" }


api.add_resource(EchoReverse, '/echo/<string:msg>')

if __name__ == '__main__':
    app.run()