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
