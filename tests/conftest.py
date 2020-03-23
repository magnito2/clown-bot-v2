import os
import tempfile

import pytest
from clownbot import create_app
from clownbot.database.db import db
from clownbot.database.models import User, Post

from werkzeug.security import generate_password_hash
from mongoengine import connect

@pytest.fixture
def app():

    app = create_app('testing')

    with app.app_context():

        user = User(
            username='testniqquh',
            email='testniqquh@testsite.dom',
            password=generate_password_hash('testpass')
        ).save()
        user2 = User(
            username='champ',
            email='champ@test.dev',
            password=generate_password_hash('sampion')
        ).save()

        post = Post(
            title='hello helloo',
            body='I really think I still messed up, I can never be perfect',
            author=user
        ).save()
        post2 = Post(
            title='Nataka kuongea na riddy',
            body='Tafadhali Kaka, kwangu hii ni wrong number',
            author=user2
        ).save()

    yield app

    db_c = connect('test_clownbot')
    db_c.drop_database('test_clownbot') #see how to improve on this one

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='testniqquh', password='testpass'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)

@pytest.fixture
def blog_id(app):
    with app.app_context():
        post = Post.objects(title='hello helloo').first()
    return post.id
