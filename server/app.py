from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods = ['GET', 'POST'])
def messages():
    message = Message.query.order_by(Message.created_at).all()
    if request.method == 'GET':
        return make_response(
            jsonify([msg.to_dict() for msg in message]),
            200,
        )
    
    elif request.method == 'POST':
        data = request.get_json()
        new_message = Message()

        for field in data:
            setattr(new_message, field, data[field])
        db.session.add(new_message)
        db.session.commit()
        return make_response(jsonify(new_message.to_dict()), 201)

@app.route('/messages/<int:id>', methods = ['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter(Message.id == id).first()
    if request.method == 'GET':
        return make_response(jsonify(message.to_dict()), 200)
    
    elif request.method == 'PATCH':
        data = request.get_json()
        for field in data:
            setattr(message, field, data[field])
        db.session.add(message)
        db.session.commit()
        return make_response(jsonify(message.to_dict()), 200)
    
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        return make_response(jsonify({'status': 'delete sucess'}), 200)

if __name__ == '__main__':
    app.run(port=5555)
