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
    )

bp = Blueprint('tasks', __name__, url_prefix="/tasks")


@bp.route('/')
def index():
    return render_template('tasks/index.html')

@bp.route('/list')
def task_list():
    task_list = get_task_list()
    return render_template('tasks/task_list.html', task_list=task_list)

@bp.route('/create')
def create_task():
    return "create new task"

@bp.route('/id/')
def task():
    return redirect('/list')

@bp.route('/id/<int:id>')
def task_id(id):
    return f"task number {id} description"

@bp.route('/my')
def my_tasks():
    return "my tasks"

@bp.route('/archive')
def archive():
    return "task archive"

@bp.route('/stat')
def stat():
    return "task statistics"
