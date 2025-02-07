import os
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Add routes here :
    @app.route('/')
    def menu():
        return '<h1>Axolotl Menu</h1>'
    
    return app
