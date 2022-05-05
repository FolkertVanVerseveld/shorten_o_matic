from flask import Flask, jsonify, request

def create_app(): #config_filename):
    app = Flask(__name__)
    #app.config.from_pyfile(config_filename)

    urls = {}

    @app.route('/')
    def hello_world():
        return 'Hello, World!'

    @app.route('/shorten', methods=['POST'])
    def shorten():
        import re
        content = request.json

        if not 'url' in content:
            return '', 400

        link = content['url']

        if not 'shortcode' in content:
            code = 'abc123'
        else:
            code = content['shortcode']

        if code in urls:
            return '', 409
        elif not re.match(r"^[a-zA-Z0-9_]{6}$", code):
            return '', 412

        urls[link] = code
        return jsonify(statusCode=201, data={'shortcode': code}), 201

    return app
