## models.py
from datetime import datetime
from flask_security import UserMixin, RoleMixin
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from .config import Config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(Config)

# Define association table for many-to-many relationship between User and Role
user_roles = Table('user_roles', db.Model.metadata,
    Column('user_id', Integer(), ForeignKey('user.id')),
    Column('role_id', Integer(), ForeignKey('role.id'))
)

class Role(db.Model, RoleMixin):
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))

class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    password = Column(String(128))
    email = Column(String(120), index=True, unique=True)
    active = Column(Boolean())
    roles = relationship('Role', secondary=user_roles, backref=db.backref('users', lazy='dynamic'))
    projects = relationship('Project', backref='user', lazy='dynamic')

class Project(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(64), index=True, unique=True)
    description = Column(String(255))
    created_at = Column(DateTime, index=True, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('user.id'))
    environments = relationship('Environment', backref='project', lazy='dynamic')

class Environment(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(64), index=True)
    status = Column(String(64))
    created_at = Column(DateTime, index=True, default=datetime.utcnow)
    destroyed_at = Column(DateTime, index=True)
    project_id = Column(Integer, ForeignKey('project.id'))
