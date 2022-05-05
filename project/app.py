import datetime
from flask import Flask, jsonify, request, redirect


class MyUrl:
    """wrapper for shortened urls that also tracks redirect count and last used time"""

    def __init__(self, code, link):
        self.code = code
        self.link = link
        self.created = datetime.datetime.now(datetime.timezone.utc)
        self.lastRedirect = self.created
        self.redirectCount = 0


    def touch(self):
        """use link"""
        self.lastRedirect = datetime.datetime.now(datetime.timezone.utc)
        self.redirectCount += 1
        return redirect(self.link, code=302)


    def stats(self):
        return jsonify(created=to_iso8601(self.created), lastRedirect=to_iso8601(self.lastRedirect), redirectCount=self.redirectCount), 200


def create_url(length=6):
    """randomize shortened url"""
    import string
    import random

    s = string.ascii_lowercase + string.ascii_uppercase + '_'

    return ''.join(random.choice(s) for i in range(length))


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
            return missing_field()

        link = content['url']

        if not 'shortcode' in content:
            code = create_url()
        else:
            code = content['shortcode']

        if code in urls:
            return code_used()
        elif not re.match(r"^[a-zA-Z0-9_]{6}$", code):
            return '', 412

        urls[code] = MyUrl(code, link)
        return jsonify(shortcode=code), 201


    @app.route('/', defaults={'u_path': ''})
    @app.route('/<path:u_path>')
    def unshorten(u_path):
        if u_path is None:
            return not_found()

        if '/' in u_path:
            u_path, rest = u_path.split('/', maxsplit=2)
            if rest == 'stats':
                return unshorten_stats(u_path)
            else:
                return not_found()

        if u_path not in urls:
            return not_found()

        return urls[u_path].touch()


    def unshorten_stats(code):
        if code not in urls:
            return not_found()

        return urls[code].stats()

    return app

# error handling

def missing_field():
    return '', 400


def not_found():
    return '', 404


def code_used():
    return '', 409


def code_bad():
    return '', 412

# utilities

def to_iso8601(time):
    """convert time to database friendly T Z format"""
    return time.replace(tzinfo=None).isoformat() + 'Z'
