from flask import Flask, jsonify

def create_app(): #config_filename):
    app = Flask(__name__)
    #app.config.from_pyfile(config_filename)
    
    @app.route('/')
    def hello_world():
        return 'Hello, World!'
        
    @app.route('/shorten', methods=['POST'])
    def shorten():
        return jsonify(statusCode=400, data=[]), 400
        
    return app