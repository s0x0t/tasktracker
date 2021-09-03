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

engine = create_engine('sqlite:///task_tracker.db', echo=True)
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
    # Column('creator_id', Integer),        # Было бы полезно, но не задано условями задачи
    # Column('executor_id', Integer, ForeignKey('users.id')),
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
                tasks.c.description, 
                tasks.c.creation_date,
                users.c.username
                ).select_from(tasks.outerjoin(users, tasks.c.executor_id == users.c.id)
                ).where(tasks.c.executor_id == user_id)
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

def get_statistics():
    with engine.connect() as conn:
        opened = conn.execute(select(func.count(tasks.c.id)).where(tasks.c.start_date == None)).fetchone()
        cancelled = conn.execute(select(func.count(tasks.c.id)).where(tasks.c.cancel_date != None)).fetchone()
        executing = conn.execute(select(func.count(tasks.c.id)).where(and_(
                tasks.c.start_date != None,
                tasks.c.finish_date == None
                ))).fetchone()
        median_execute_time = None
    parameter_list = dict()
    parameter_list['Открытых задач'] = opened[0]
    parameter_list['Выполняется задач'] = executing[0]
    parameter_list['Отменённых задач'] = cancelled[0]

    return parameter_list