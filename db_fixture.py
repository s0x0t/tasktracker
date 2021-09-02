#!/usr/bin/env python3.6
# coding: utf-8

from sqlalchemy import create_engine
from db import meta, users, tasks
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


engine = create_engine('sqlite:///task_tracker.db', echo=True)
meta.drop_all(engine)
meta.create_all(engine)

conn = engine.connect()

def fill_db():
    conn.execute(users.insert(), [
        {'id': 1, 'login': 'admin', 'password': generate_password_hash('qwert123'), 'username': 'Администратор'},
        {'id': 2, 'login': 'vasya', 'password': generate_password_hash('vasya123'), 'username': 'Василий'},
        {'id': 3, 'login': 'petya', 'password': generate_password_hash('petya123'), 'username': 'Пётр'},
        {'id': 4, 'login': 'masha', 'password': generate_password_hash('masha123'), 'username': 'Мария'},
        {'id': 5, 'login': 'alisa', 'password': generate_password_hash('alisa123'), 'username': 'Алиса'},
    ])

    conn.execute(tasks.insert(), [
        {'id': 1, 'description': 'Задача № 1', 'executor_id': 1, 
                    'creation_date' : datetime.date(datetime(2021, 8, 25)), 
                    'start_date'    : datetime.date(datetime(2021, 8, 26)), 
                    'finish_date'   : datetime.date(datetime(2021, 8, 27)) 
                    },
        {'id': 2, 'description': 'Задача № 2', 'executor_id': 2, 
                    'creation_date' : datetime.date(datetime(2021, 8, 26)), 
                    'start_date'    : datetime.date(datetime(2021, 8, 27)), 
                    'finish_date'   : None 
                    },
        {'id': 3, 'description': 'Задача № 3', 'executor_id': 5, 
                    'creation_date' : datetime.date(datetime(2021, 8, 30)), 
                    'start_date'    : datetime.date(datetime(2021, 8, 30)), 
                    'finish_date'   : datetime.date(datetime(2021, 8, 30))
                    },
        {'id': 4, 'description': 'Задача № 4', 'executor_id': None, 
                    'creation_date' : datetime.date(datetime(2021, 8, 31)), 
                    'start_date'    : None, 
                    'finish_date'   : None
                    },
        {'id': 5, 'description': 'Задача № 5', 'executor_id': None, 
                    'creation_date' : datetime.date(datetime.now()), 
                    'start_date'    : None, 
                    'finish_date'   : None
                    },
    ])

if __name__ == '__main__':
    fill_db()
