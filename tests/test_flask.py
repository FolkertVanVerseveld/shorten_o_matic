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