import pytest
from flask import g, session
from clownbot.database.db import db
from clownbot.database.models import User


def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'username': 'a', 'password': 'a', 'email': 'a'}
    )
    assert 'http://localhost/auth/login' == response.headers['Location']

    with app.app_context():
        assert User.objects(username = 'a').first() is not None


@pytest.mark.parametrize(('username', 'email', 'password', 'message'), (
    ('', '', '', b'Username is required.'),
    ('a', '', '', b'Email is required.'),
    ('a', 'a', '', b'Password is required.'),
    ('testniqquh', 'testniqquh@testsite.dom', 'testpass', b'already registered'),
))
def test_register_validate_input(client, username, email, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'email': email, 'password': password}
    )
    print(response.data)
    assert message in response.data

def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    print(response.headers)
    assert response.headers['Location'] == 'http://localhost/'

    with client:
        client.get('/')

        assert g.user['username'] == 'testniqquh'


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'testpass', b'Incorrect username.'),
    ('testniqquh', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data

def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session
