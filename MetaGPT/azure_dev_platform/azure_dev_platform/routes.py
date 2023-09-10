from flask import Flask, request, jsonify
from models import db, User, Environment
from config import config

app = Flask(__name__)
app.config.from_object(config['default'])
db.init_app(app)

@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400
    user = User(username, password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created'}), 200

@app.route('/user/authenticate', methods=['POST'])
def authenticate_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if not user or not user.authenticate(password):
        return jsonify({'message': 'Invalid username or password'}), 400
    return jsonify({'message': 'User authenticated'}), 200

@app.route('/environment', methods=['POST'])
def create_environment():
    data = request.get_json()
    name = data.get('name')
    status = data.get('status')
    owner_username = data.get('owner')
    owner = User.query.filter_by(username=owner_username).first()
    if not owner:
        return jsonify({'message': 'Invalid owner'}), 400
    environment = Environment(name, status, owner)
    db.session.add(environment)
    db.session.commit()
    return jsonify({'message': 'Environment created'}), 200

@app.route('/environment', methods=['PUT'])
def update_environment():
    data = request.get_json()
    name = data.get('name')
    action = data.get('action')
    environment = Environment.query.filter_by(name=name).first()
    if not environment:
        return jsonify({'message': 'Invalid environment'}), 400
    if action == 'start':
        environment.start()
    elif action == 'stop':
        environment.stop()
    elif action == 'delete':
        environment.delete()
        db.session.delete(environment)
    else:
        return jsonify({'message': 'Invalid action'}), 400
    db.session.commit()
    return jsonify({'message': 'Environment updated'}), 200
