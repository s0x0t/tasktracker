from sqlalchemy import (
    create_engine,
    MetaData, Table, Column, 
    Integer, String, 
    ForeignKey, 
    func, and_
)

from sqlalchemy.sql import (
    select, bindparam
    )

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from datetime import datetime

engine = create_engine('sqlite:///task_tracker.db', echo=False)
meta = MetaData()

users = Table('users', meta,
    Column('id', Integer, primary_key=True),
    Column('login', String),
    Column('password', String),
    Column('username', String)
    )

tasks = Table('tasks', meta,
    Column('id', Integer, primary_key=True),
    Column('description', String),
    Column('executor_id', Integer),
    Column('creation_date', String),
    Column('start_date', String),
    Column('finish_date', String),
    Column('cancel_date', String)
    )

def select_user(id):
    with engine.connect() as conn:
        request = select(users).where(users.c.id == id)
        user = conn.execute(request).fetchone()
    return user

def check_user(login, password):
    with engine.connect() as conn:
        request = select(users).where(users.c.login == login)
        user = conn.execute(request).fetchone()

    error = None

    if user is None:
        error = "Incorrect username"
    elif not check_password_hash(user["password"], password):
        error = "Incorrect password"

    print (user, error)

    return user, error


def get_task_list(user_id=None):
    with engine.connect() as conn:
        request = select(
                tasks.c.id,
                tasks.c.description, 
                tasks.c.creation_date,
                users.c.username
                ).select_from(tasks.outerjoin(users, tasks.c.executor_id == users.c.id)
                ).where(and_(
                    tasks.c.executor_id == user_id,
                    tasks.c.finish_date == None,
                    tasks.c.cancel_date == None,
                    ))
        result = conn.execute(request)
        task_list = result.fetchall()
    return task_list

def get_all_tasks():
    with engine.connect() as conn:
        request = select(
                tasks.c.description, 
                tasks.c.creation_date,
                tasks.c.start_date,
                tasks.c.finish_date,
                tasks.c.cancel_date,
                users.c.username
                ).select_from(tasks.outerjoin(users, tasks.c.executor_id == users.c.id))
        result = conn.execute(request)
        task_list = result.fetchall()
    return task_list

def insert_new_task(description):
    with engine.connect() as conn:
        conn.execute(tasks.insert().values(description=description, creation_date=datetime.date(datetime.now())))
    return

def update_start_task(task_id, executor_id):
    with engine.connect() as conn:
        conn.execute(tasks.update().where(tasks.c.id == task_id).values(executor_id=executor_id, start_date=datetime.date(datetime.now())))
    return

def update_finish_task(task_id):
    with engine.connect() as conn:
        conn.execute(tasks.update().where(tasks.c.id == task_id).values(finish_date=datetime.date(datetime.now())))
    return

def update_cancel_task(task_id):
    with engine.connect() as conn:
        conn.execute(tasks.update().where(tasks.c.id == task_id).values(cancel_date=datetime.date(datetime.now())))
    return

def get_statistics():
    with engine.connect() as conn:
        opened = conn.execute(select(func.count(tasks.c.id)).where(tasks.c.executor_id == None)).fetchone()
        cancelled = conn.execute(select(func.count(tasks.c.id)).where(tasks.c.cancel_date != None)).fetchone()
        executing = conn.execute(select(func.count(tasks.c.id)).where(and_(
                tasks.c.start_date != None,
                tasks.c.finish_date == None,
                tasks.c.cancel_date == None,
                ))).fetchone()

        request = select(tasks.c.start_date, tasks.c.finish_date).where(and_(
            tasks.c.start_date != None,
            tasks.c.finish_date != None
            ))
        executed_tasks = conn.execute(request).fetchall()
    durations = list()
    for task in executed_tasks:
        duration = (str_to_date(task[1]) - str_to_date(task[0])).days
        durations.append(duration)
    average_execute_time = round(sum(durations)/len(durations), 2)

    parameter_list = dict()
    parameter_list['???????????????? ??????????'] = opened[0]
    parameter_list['?????????????????????? ??????????'] = executing[0]
    parameter_list['???????????????????? ??????????'] = cancelled[0]
    parameter_list['?????????????? ?????????? ???????????????????? ????????????, ????????'] = average_execute_time

    return parameter_list

def str_to_date(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%d')
    return date_object

def date_to_str(date_object):
    date_string = datetime.strftime(date_object, '%d.%m.%Y')
    return date_string

