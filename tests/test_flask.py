from project import app

def test_running():
    a = app.create_app()

    with a.test_client() as c:
        res = c.get('/')
        assert res.status_code == 200


def test_not_found():
    a = app.create_app()

    with a.test_client() as c:
        res = c.get('/dope')
        assert res.status_code == 404


def test_hello():
    a = app.create_app()

    with a.test_client() as c:
        res = c.get('/')
        assert b"Hello, World!" in res.data


def test_shorten():
    a = app.create_app()

    with a.test_client() as c:
        res = c.post('/shorten', json={'url': 'https://www.energyworx.com/', 'shortcode': 'ewx123'})
        assert res.status_code == 201

        content = res.get_json()
        assert content['shortcode'] == 'ewx123'


def test_shorten_random_url():
    a = app.create_app()

    with a.test_client() as c:
        import re

        res = c.post('/shorten', json={'url': 'https://www.energyworx.com/', 'shortcode': 'ewx123'})
        assert res.status_code == 201

        content = res.get_json()
        assert re.match(r"^[a-zA-Z0-9_]{6}$", content['shortcode'])


def test_shorten_no_url():
    a = app.create_app()

    with a.test_client() as c:
        res = c.post('/shorten', json={'shortcode': 'ewx123'})
        assert res.status_code == 400


def test_shorten_badcode():
    a = app.create_app()

    with a.test_client() as c:
        res = c.post('/shorten', json={'url': 'https://www.energyworx.com/', 'shortcode': 'eWx1235'})
        assert res.status_code == 412


def test_shorten_double_add():
    a = app.create_app()

    with a.test_client() as c:
        res = c.post('/shorten', json={'url': 'https://www.energyworx.com/', 'shortcode': 'ewx123'})
        assert res.status_code == 201

        content = res.get_json()
        assert content['shortcode'] == 'ewx123'

        res = c.post('/shorten', json={'url': 'https://www.energyworx.com/', 'shortcode': 'ewx123'})
        assert res.status_code == 409


def test_unshorten():
    from urllib.parse import urlparse

    a = app.create_app()

    with a.test_client() as c:
        res = c.post('/shorten', json={'url': 'https://www.energyworx.com/', 'shortcode': 'ewx123'})
        assert res.status_code == 201

        content = res.get_json()
        assert content['shortcode'] == 'ewx123'

        res = c.get('/ewx123')
        assert res.status_code == 302
        assert res.location == 'https://www.energyworx.com/'


def test_unshorten_invalid():
    a = app.create_app()

    with a.test_client() as c:
        res = c.get('/ewx123')
        assert res.status_code == 404


def test_unshorten_stats():
    a = app.create_app()

    with a.test_client() as c:
        res = c.post('/shorten', json={'url': 'https://www.energyworx.com/', 'shortcode': 'ewx123'})
        assert res.status_code == 201

        content = res.get_json()
        assert content['shortcode'] == 'ewx123'

        res = c.get('/ewx123/stats')
        assert res.status_code == 200

        content = res.get_json()
        assert content['redirectCount'] == 0

        # use it
        res = c.get('/ewx123')

        res = c.get('/ewx123/stats')
        assert res.status_code == 200

        content = res.get_json()
        assert content['redirectCount'] == 1

        # use twice
        res = c.get('/ewx123')
        res = c.get('/ewx123')

        res = c.get('/ewx123/stats')
        assert res.status_code == 200

        content = res.get_json()
        assert content['redirectCount'] == 3
