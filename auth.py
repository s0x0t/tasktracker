import functools

from flask import (
    Blueprint,
    render_template, url_for, 
    request, session, redirect, abort, escape, g, jsonify, flash
    )

from werkzeug.security import (
    check_password_hash,
    generate_password_hash
    )

from .db import select_user, check_user

bp = Blueprint('auth', __name__, url_prefix='/auth')

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = select_user(user_id)

@bp.route("/login", methods=('GET', 'POST'))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        user, error = check_user(login, password)

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('tasks.open_tasks'))

        flash(error)

    return render_template("auth/login.html")

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
