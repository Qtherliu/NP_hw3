#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter11/app_improved.py
# A payments application with basic security improvements added.

import DB, uuid
from flask import (Flask, abort, flash, get_flashed_messages,
                   redirect, render_template, request, session, url_for)

app = Flask(__name__)
app.secret_key = 'saiGeij8AiS2ahleahMo5dahveixuV3J'

@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    if request.method == 'POST':
        if (username, password) in [('TH', 'TH'), ('TH2', 'TH')]:
            session['username'] = username
            session['csrf_token'] = uuid.uuid4().hex
            return redirect(url_for('index'))
    return render_template('login.html', username=username)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/', methods=['GET'])
def index():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    db = DB.open_database()
    search = request.args.get('search')
    if search:
        search = search.strip()
    else:
        search = None
    userProfile = DB.get_data_of(db, search)
    count = DB.get_data_count(db, search)
    return render_template('index.html', userProfile=userProfile, username=username, count=count,
                           flash_messages=get_flashed_messages())

@app.route('/create', methods=['GET', 'POST'])
def create():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    account = request.form.get('account', '').strip()
    name = request.form.get('name', '').strip()
    age = request.form.get('age', '').strip()
    memo = request.form.get('memo', '').strip()
    complaint = None
    if request.method == 'POST':
        if account and name and age and age.isdigit() and memo:
            db = DB.open_database()
            DB.add_data(db, account, name, age, memo)
            db.commit()
            flash('Create successful')
            return redirect(url_for('index'))
        complaint = ('Age must be an integer' if not age.isdigit()
                     else 'Please fill in all the fields')
    else:
        complaint='Please fill in all the fields'
    return render_template('create.html', complaint=complaint, account=account,
                           name=name, age=age, memo=memo)

@app.route('/edit/<data_id>', methods=['GET', 'POST'])
def edit(data_id):
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))    
    db = DB.open_database()
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        age = request.form.get('age', '').strip()
        memo = request.form.get('memo', '').strip()
        complaint = None
        if name and age and age.isdigit() and memo:            
            DB.update_data(db, data_id, name, age, memo)
            db.commit()
            flash('Edit successful')
            return redirect(url_for('index'))
        complaint = ('Age must be an integer' if not age.isdigit()
                     else 'Please fill in all the fields')
    else:
        complaint = 'Please fill in all the fields'
        user = DB.get_user_data(db, data_id)
        if user == None:
            complaint = 'No such person'
        else:
            account = user[1]
            name = user[2]
            age = user[3]
            memo = user[4]
    return render_template('edit.html', complaint=complaint, data_id=data_id, account=account,
                           name=name, age=age, memo=memo)

@app.route('/delete/<data_id>', methods=['GET'])
def delete(data_id):
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    db = DB.open_database()
    DB.delete_data(db, data_id)
    db.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.debug = True
    app.run()
