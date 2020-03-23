from clownbot import create_app


def test_config(monkeypatch):

    class Recorder(object):
        called = False

    def fake_init_db(app):
        Recorder.called = True

    monkeypatch.setattr('clownbot.database.db.db.init_app', fake_init_db)
    assert not create_app('development').testing
    assert create_app('testing').testing
    assert Recorder.called

def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!'
