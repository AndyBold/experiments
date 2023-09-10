from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    """User model."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __init__(self, username: str, password: str):
        self.username = username
        self.password_hash = generate_password_hash(password)

    def authenticate(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Environment(db.Model):
    """Environment model."""
    __tablename__ = 'environments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    status = db.Column(db.String(64), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    owner = db.relationship('User', backref=db.backref('environments', lazy=True))

    def __init__(self, name: str, status: str, owner: User):
        self.name = name
        self.status = status
        self.owner = owner

    def start(self):
        # Implement start environment logic here
        pass

    def stop(self):
        # Implement stop environment logic here
        pass

    def delete(self):
        # Implement delete environment logic here
        pass
