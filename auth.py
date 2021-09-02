from flask import (
    Blueprint,
    render_template, url_for, 
    request, session, redirect, abort, escape, g, jsonify
    )

from werkzeug.security import (
    check_password_hash,
    generate_password_hash
    )


bp = Blueprint('auth', __name__, url_prefix="/auth")


@bp.route('/login', methods=('GET', 'POST'))
def login():
    return "login page"

@bp.route('/logout')
def logout():
    return "logout page or logout POST command"
