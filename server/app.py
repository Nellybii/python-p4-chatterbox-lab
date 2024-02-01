from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Message  # Assuming 'Message' is your SQLAlchemy model

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json_encoder.compact = False  # Fixed typo: it should be `app.json_encoder` instead of `app.json`

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)

class Messages(Resource):

    def get(self):
        response_dict_list = [n.to_dict() for n in Message.query.all()]
        response = make_response(
            jsonify(response_dict_list),
            200,
        )
        return response

    def post(self):
        new_record = Message(
            body=request.form['body'],
            username=request.form['username'],
            updated_at=request.form['updated_at'],
        )

        db.session.add(new_record)
        db.session.commit()

        response_dict = new_record.to_dict()

        response = make_response(
            jsonify(response_dict),
            201,
        )

        return response

api.add_resource(Messages, '/messages')  

class MessageByID(Resource):

    def get(self, id):

        response_dict = Newsletter.query.filter_by(id=id).first().to_dict()

        response = make_response(
            jsonify(response_dict),
            200,
        )

        return response

api.add_resource(MessageByID, '/messages/<int:id>')

if __name__ == '__main__':
    app.run(port=5555)
