from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from .auth import login_required
from .database.models import Post, User

bp = Blueprint('blog', __name__)

def get_post(id, check_author=True):
    post = Post.objects(id=id).first()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))
    if check_author and post.author.id != g.user['id']:
        abort(403)

    return post

@bp.route('/')
def index():
    posts = []
    for post in Post.objects:
        p = {
            'id' : str(post.id),
            'title' : post.title,
            'body'  : post.body,
            'author_id' : post.author.id,
            'username' : post.author.username,
            'created' : post.created
            }
        posts.append(p)

    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            Post(
                title=title,
                body=body,
                author=g.user
            ).save()

            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

@bp.route('/<string:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            post.update(
                title=title,
                body=body
            )

            return redirect(url_for('blog.index'))
    p = {
        'id' : str(post.id),
        'title' : post.title,
        'body'  : post.body,
        'author_id' : post.author.id,
        'created' : post.created
        }

    return render_template('blog/update.html', post=p)

@bp.route('/<string:id>/delete', methods=('POST',))
@login_required
def delete(id):
    post = get_post(id)

    Post.objects(id=id).first().delete()
    return redirect(url_for('blog.index'))
