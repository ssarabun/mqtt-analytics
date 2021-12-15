from flask import (
    Blueprint, request, render_template, redirect, url_for
)

from .db import get_db

bp = Blueprint('counter', __name__)

@bp.route("/counters", methods=['GET'])
def counters():
    if request.method == 'GET':
        rows = get_counters()
        return render_template('counters.html', rows=rows)


@bp.route("/counter/<id>", methods=['GET', 'POST'])
def counter(id):
    print(f'id={id}')
    db = get_db()
    if request.method == 'GET':
        row = db.execute('SELECT * FROM counter WHERE counter_key = ?', (id))
        db.commit()
        return render_template('counter.html', row=row)
    elif request.method == 'POST':
        delete(id)
        return redirect(url_for('counter.counters'))


@bp.route("/edit-counter/<id>", methods=['GET', 'POST'])
def edit_counter(id):
    db = get_db()
    if request.method == 'GET':
        row = get_counter_by_id(id)
        return render_template('edit-counter.html', row=row)
    elif request.method == 'POST':
        delete(id)
        return redirect(url_for('counter.counters'))

@bp.route("/delete-counter/<id>", methods=['GET'])
def delete_counter(id):
    delete(id)
    return redirect(url_for('counter.counters'))


@bp.route("/save-counter", methods=['POST'])
def save_counter():
    if request.method == 'POST':
        counter_id = request.form.get('counter_id')
        print(f'counter_id = {counter_id}')
        counter_key = request.form['counter_key']
        print(f'counter_key = {counter_key}')
        interval = request.form['interval']
        multiplicator = request.form['multiplicator']
        unit = request.form['unit']
        delta = request.form.get('delta')
        if delta is None:
            delta = False
        else:
            delta = True

        enabled = request.form.get('enabled')
        if enabled is None:
            enabled = False
        else:
            enabled = True

        if counter_id is None:
            create(counter_key, interval, multiplicator, unit, delta, enabled)
        else:
            print('Update....')
            update(counter_id, counter_key, interval, multiplicator, unit, delta, enabled)
        return redirect(url_for('counter.counters'))
    else:
        print('#########################')


def create(counter_key, interval, multiplicator, unit, delta, enabled):
    db = get_db()
    db.execute('''
    INSERT INTO counter (counter_key, interval, multiplicator, unit, delta, enabled)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (counter_key, interval, multiplicator, unit, delta, enabled))
    db.commit()


def update(id, counter_key, interval, multiplicator, unit, delta, enabled):
    db = get_db()
    db.execute('''
    UPDATE counter
    SET
    counter_key = ?,
    interval = ?,
    multiplicator = ?,
    unit = ?,
    delta = ?,
    enabled = ?
    WHERE counter_id = ?
    ''', (counter_key, interval, multiplicator, unit, delta, enabled, id))
    db.commit()


def get_counter_by_id(id):
    db = get_db()
    row = db.execute('''
    SELECT counter_id, counter_key, interval, multiplicator, unit, delta, enabled
    FROM counter
    WHERE counter_id = ?
    ''', (id)).fetchone()
    return row

def get_counters():
    db = get_db()
    rows = db.execute('''
    SELECT counter_id, counter_key, interval, multiplicator, unit, delta, enabled
    FROM counter
    ORDER BY counter_key
    ''')
    return rows


def delete(id):
    db = get_db()
    db.execute('DELETE FROM counter WHERE counter_id = ?', (id))
    db.commit()
