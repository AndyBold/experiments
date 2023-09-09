## main.py
from flask import Flask
from .routes import app

def run_server():
    """Run the Flask server."""
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    run_server()
