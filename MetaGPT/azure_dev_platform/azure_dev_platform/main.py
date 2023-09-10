from flask import Flask
from models import db
from routes import app

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    return app

if __name__ == "__main__":
    app = create_app('default')
    app.run(host='0.0.0.0', port=5000)
