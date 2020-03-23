import pytest, re
from clownbot.database.db import db
from clownbot.database.models import Post


def test_index(client, auth, app):
    response = client.get('/')
    assert b"Log In" in response.data
    assert b"Register" in response.data

    auth.login()
    response = client.get('/')
    assert b'Log Out' in response.data
    assert b'hello helloo' in response.data
    assert b'by testniqquh on' in response.data
    assert b'Tafadhali Kaka' in response.data
    with app.app_context():
        post = Post.objects(title='hello helloo').first()
        assert b'href="/'+ str(post.id).encode() + b'/update"' in response.data

@pytest.mark.parametrize('path', (
    '/create',
    '/1/update',
    '/1/delete',
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers['Location'] == 'http://localhost/auth/login'

def test_author_required(app, client, auth):
    # change the post author to another user
    with app.app_context():
        post = Post.objects(title='hello helloo').first()
        assert post is not None
    auth.login(username='champ', password='sampion')
    # current user can't modify other user's post
    assert client.post(f'/{post.id}/update').status_code == 403
    assert client.post(f'/{post.id}/delete').status_code == 403
    # current user doesn't see edit link
    assert b'href="/'+ str(post.id).encode() + b'/update"' not in client.get('/').data


@pytest.mark.parametrize('path', (
    '/666f6f2d6261722d71757578/update',
    '/666f6f2d6261722d71757578/delete',
))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404

def test_create(client, auth, app):
    auth.login()
    assert client.get('/create').status_code == 200
    client.post('/create', data={'title': 'created', 'body': 'I am creating youuu'})

    with app.app_context():
        post = Post.objects(title='created').first()
        assert post

def test_update(client, auth, app):
    auth.login()

    with app.app_context():
        post = Post.objects(title='hello helloo').first()

        assert client.get(f'/{post.id}/update').status_code == 200
        client.post(f'/{post.id}/update', data={'title': 'updated', 'body': ''})

        post2 = Post.objects(id=post.id).first()
        assert post2['title'] == 'updated'


@pytest.mark.parametrize('path', ('/create',))
def test_create_validate(client, auth, path):
    auth.login()
    response = client.post(path, data={'title': '', 'body': ''})
    assert b'Title is required.' in response.data

def test_update_validate(client, auth, app):
    auth.login()

    with app.app_context():
        post = Post.objects(title='hello helloo').first()

    response = client.post(f'{post.id}/update', data={'title': '', 'body': ''})
    assert b'Title is required.' in response.data

def test_delete(client, auth, app, blog_id):
    auth.login()
    response = client.post(f'/{blog_id}/delete')
    assert response.headers['Location'] == 'http://localhost/'

    with app.app_context():
        post = Post.objects(id=blog_id).first()
        assert post is None
