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
    get_statistics,
    insert_new_task,
    update_start_task,
    update_finish_task,
    update_cancel_task,
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

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create_task():
    if request.method == 'POST':
        description = request.form['task_description']
        insert_new_task(description)
    username = g.user.username
    return render_template('tasks/new_task.html', username=username)

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

@bp.route('/start_task/<int:task_id>')
@login_required
def start_task(task_id):
    username = g.user.username
    executor_id = g.user.id
    update_start_task(task_id, executor_id)
    return redirect(url_for('tasks.my_tasks'))

@bp.route('/finish_task/<int:task_id>')
@login_required
def finish_task(task_id):
    username = g.user.username
    update_finish_task(task_id)
    return redirect(url_for('tasks.my_tasks'))

@bp.route('/cancel_task/<int:task_id>')
@login_required
def cancel_task(task_id):
    username = g.user.username
    update_cancel_task(task_id)
    return redirect(url_for('tasks.my_tasks'))