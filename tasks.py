from flask import (
    Blueprint,
    render_template, url_for, 
    request, session, redirect, abort, escape, g, jsonify
    )

from werkzeug.security import (
    check_password_hash,
    generate_password_hash
    )

from .db import (
    get_task_list,
    get_all_tasks,
    get_statistics
    )
from .auth import login_required

bp = Blueprint('tasks', __name__, url_prefix="/tasks")


@bp.route('/')
def index():
    return render_template('tasks/index.html')

@bp.route('/list')
@login_required
def open_tasks():
    username = g.user.username
    task_list = get_task_list()
    return render_template('tasks/open_tasks.html', task_list=task_list, username=username)

@bp.route('/create')
@login_required
def create_task():
    return "create new task"

@bp.route('/id/')
@login_required
def task():
    return redirect('/list')

@bp.route('/id/<int:id>')
@login_required
def task_id(id):
    return f"task number {id} description"

@bp.route('/my')
@login_required
def my_tasks():
    user_id = g.user.id
    username = g.user.username
    task_list = get_task_list(user_id)
    return render_template('tasks/my_tasks.html', task_list=task_list, username=username)

@bp.route('/archive')
@login_required
def archive():
    username = g.user.username
    task_list = get_all_tasks()
    return render_template('tasks/archive.html', task_list=task_list, username=username)

@bp.route('/stat')
@login_required
def stat():
    username = g.user.username
    parameter_list = get_statistics()
    return render_template('tasks/stat.html', parameter_list=parameter_list, username=username)
