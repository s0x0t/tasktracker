from sqlalchemy import (
    create_engine,
    MetaData, Table, Column, 
    Integer, String, 
    ForeignKey,
)

from sqlalchemy.sql import (
    select, bindparam
    )

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

def get_task_list():
    with engine.connect() as conn:
        request = select(tasks.c.description, users.c.username)\
            .select_from(tasks.outerjoin(users, tasks.c.executor_id == users.c.id))
        result = conn.execute(request)
        task_list = result.fetchall()
    return task_list
