#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter11/bank.py
# A small library of database routines to power a payments application.

import os, pprint, sqlite3
from collections import namedtuple

def open_database(path='user.db'):
    new = not os.path.exists(path)
    db = sqlite3.connect(path)
    if new:
        c = db.cursor()
        c.execute('CREATE TABLE user (id INTEGER PRIMARY KEY,'
                  ' account TEXT, name TEXT, age INTEGER, memo TEXT)')
        add_data(db, 'TH', 'T.H.Liu', 25, 'hihi')
        add_data(db, 'Nick', 'Nick Liang', 26, 'I am a bitch!')
        add_data(db, 'TH2', 'T.H.Liu', 25, 'hihi2')
        db.commit()
    return db

def add_data(db, account, name, age, memo):
    db.cursor().execute('INSERT INTO user (account, name, age, memo)'
                        ' VALUES (?, ?, ?, ?)', (account, name, age, memo))

def get_data_of(db, search):
    c = db.cursor()
    if search:
        sql = 'SELECT * FROM user WHERE account LIKE("%' + search + '%") ORDER BY id'
        c.execute(sql)
    else:
        c.execute('SELECT * FROM user ORDER BY id')
    Row = namedtuple('Row', [tup[0] for tup in c.description])
    return [Row(*row) for row in c.fetchall()]

def get_data_count(db, search):
    c = db.cursor()
    if search:
        sql = 'SELECT count(*) AS count FROM user WHERE account LIKE("%' + search + '%")'
        c.execute(sql)
    else:
        c.execute('SELECT count(*) AS count FROM user')
    data = c.fetchone()
    return data

def get_user_data(db, data_id):
    c = db.cursor()
    c.execute('SELECT * FROM user WHERE id =?', (data_id,))
    data = c.fetchone()
    return data

def update_data(db, data_id, name, age, memo):
    db.cursor().execute('UPDATE user SET name=?, age=?, memo=?'
                        ' WHERE id=?', (name, age,memo, data_id))
def delete_data(db, data_id):
    db.cursor().execute('DELETE FROM user WHERE id =?', (data_id,))
    
if __name__ == '__main__':
    db = open_database()
    pprint.pprint(get_user_data(db, 'TH'))
