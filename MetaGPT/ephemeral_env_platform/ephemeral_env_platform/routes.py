## routes.py
from flask import Flask, request, jsonify, abort
from flask_security import Security, SQLAlchemySessionUserDatastore
from .models import User, Role, Project, Environment, db
from .azure_manager import AzureManager

app = Flask(__name__)
user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
security = Security(app, user_datastore)

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data:
        abort(400, description="No input data provided")
    user = User(username=data['username'], password=data['password'], email=data['email'], active=data['active'], roles=data['roles'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created'}), 200

@app.route('/projects', methods=['POST'])
def create_project():
    data = request.get_json()
    if not data:
        abort(400, description="No input data provided")
    user = User.query.get(data['user_id'])
    if not user:
        abort(400, description="User not found")
    project = Project(name=data['name'], description=data['description'], user=user)
    db.session.add(project)
    db.session.commit()
    return jsonify({'message': 'Project created'}), 200

@app.route('/environments', methods=['POST'])
def create_environment():
    data = request.get_json()
    if not data:
        abort(400, description="No input data provided")
    project = Project.query.get(data['project_id'])
    if not project:
        abort(400, description="Project not found")
    environment = Environment(name=data['name'], status='pending', project=project)
    db.session.add(environment)
    azure_manager = AzureManager()
    if not azure_manager.setup_environment(environment):
        db.session.rollback()
        abort(500, description="Failed to setup environment on Azure")
    db.session.commit()
    return jsonify({'message': 'Environment created'}), 200

@app.route('/environments/<int:id>', methods=['DELETE'])
def delete_environment(id):
    environment = Environment.query.get(id)
    if not environment:
        abort(400, description="Environment not found")
    azure_manager = AzureManager()
    if not azure_manager.destroy_environment(environment):
        abort(500, description="Failed to destroy environment on Azure")
    db.session.delete(environment)
    db.session.commit()
    return jsonify({'message': 'Environment deleted'}), 200
