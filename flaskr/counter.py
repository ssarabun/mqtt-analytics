from flask import (
    Blueprint, request, session, render_template, redirect, url_for
)

from datetime import (datetime, timedelta, timezone)

from .db import get_db
from .plot import data_to_chart

bp = Blueprint('counter', __name__)

@bp.route("/counters", methods=['GET'])
def counters():
    if request.method == 'GET':
        rows = get_counters()
        return render_template('counters.html', rows=rows)


@bp.route("/counter/<key>", methods=['GET'])
def counter(key):
    print(f'key={key}')

    start_date = None
    end_date = None

    if 'end_date' in session:
        end_date = session['end_date']
    else:
        end_date = datetime.now().replace(second=0, microsecond=0)
        session['end_date'] = end_date

    if 'start_date' in session:
        start_date = session['start_date']

    min = request.args.get('min', None)
    hour = request.args.get('h', None)
    day = request.args.get('d', None)
    month = request.args.get('m', None)
    year = request.args.get('y', None)

    if min is not None:
        start_date = end_date - timedelta(minutes=int(min))
        session['start_date'] = start_date
    elif hour is not None:
        start_date = end_date - timedelta(hours=int(hour))
        session['start_date'] = start_date
    elif day is not None:
        start_date = end_date - timedelta(days=int(day))
        session['start_date'] = start_date
    elif month is not None:
        start_date = end_date - timedelta(days=(int(month) * 30))
        session['start_date'] = start_date
    elif year is not None:
        start_date = end_date - timedelta(days=(int(year) * 365))
        session['start_date'] = start_date

    if start_date is None:
        start_date = end_date - timedelta(days=365)

    before_min = request.args.get('bmin', None)
    before_hour = request.args.get('bh', None)
    before_day = request.args.get('bd', None)
    before_month = request.args.get('bm', None)
    before_year = request.args.get('by', None)

    if before_min is not None:
        start_date = start_date - timedelta(minutes=int(before_min))
        session['start_date'] = start_date

        end_date = end_date - timedelta(minutes=int(before_min))
        session['end_date'] = end_date
    elif before_hour is not None:
        start_date = start_date - timedelta(hours=int(before_hour))
        session['start_date'] = start_date

        end_date = end_date - timedelta(hours=int(before_hour))
        session['end_date'] = end_date
    elif before_day is not None:
        start_date = start_date - timedelta(days=int(before_day))
        session['start_date'] = start_date

        end_date = end_date - timedelta(days=int(before_day))
        session['end_date'] = end_date
    elif before_month is not None:
        start_date = start_date - timedelta(days=(int(before_month) * 30))
        session['start_date'] = start_date

        end_date = end_date - timedelta(days=(int(before_month) * 30))
        session['end_date'] = end_date

    after_min = request.args.get('amin', None)
    after_hour = request.args.get('ah', None)
    after_day = request.args.get('ad', None)
    after_month = request.args.get('am', None)
    after_year = request.args.get('ay', None)

    d = datetime.now().replace(second=0, microsecond=0)
    if after_min is not None:
        start_date = start_date + timedelta(minutes=int(after_min))
        end_date = end_date + timedelta(minutes=int(after_min))

        if end_date.replace(tzinfo=timezone.utc) > d.replace(tzinfo=timezone.utc):
            delta = end_date - start_date
            end_date = d
            start_date = end_date - delta

        session['start_date'] = start_date
        session['end_date'] = end_date
    elif after_hour is not None:
        start_date = start_date + timedelta(hours=int(after_hour))
        end_date = end_date + timedelta(hours=int(after_hour))

        if end_date.replace(tzinfo=timezone.utc) > d.replace(tzinfo=timezone.utc):
            delta = end_date - start_date
            end_date = d
            start_date = end_date - delta

        session['start_date'] = start_date
        session['end_date'] = end_date
    elif after_day is not None:
        start_date = start_date + timedelta(days=int(after_day))
        end_date = end_date + timedelta(days=int(after_day))

        print(d.replace(tzinfo=timezone.utc).tzname())
        print(end_date.replace(tzinfo=timezone.utc).tzname())
        if end_date.replace(tzinfo=timezone.utc) > d.replace(tzinfo=timezone.utc):
            delta = end_date - start_date
            end_date = d
            start_date = end_date - delta

        session['start_date'] = start_date
        session['end_date'] = end_date
    elif after_month is not None:
        start_date = start_date + timedelta(days=(int(after_month) * 30))
        end_date = end_date + timedelta(days=(int(after_month) * 30))

        if end_date.replace(tzinfo=timezone.utc) > d.replace(tzinfo=timezone.utc):
            delta = end_date - start_date
            end_date = d
            start_date = end_date - delta

        session['start_date'] = start_date
        session['end_date'] = end_date

    print(start_date.strftime('%Y-%m-%d %H:%M:%S'))
    print(end_date.strftime('%Y-%m-%d %H:%M:%S'))

    td = end_date - start_date
    print(f'td = {td}')
    print(f'td.days = {td.days}')
    print(f'td.seconds = {td.seconds}')

    db = get_db()
    if request.method == 'GET':
        counter = db.execute('SELECT * FROM counter WHERE counter_key = ?', (key,)).fetchone()

        int_str = None
        counter_data = None
        if td.days == 0 and td.seconds <= 57600:
            int_str = 'min'
            counter_data = db.execute('''
                SELECT
                    created,
                    counter_value
                FROM counter_value_min
                WHERE counter_id = ?
                AND created BETWEEN ? AND ?
                ORDER BY id
            ''', (counter['counter_id'], start_date, end_date)
            ).fetchall()
        elif td.days >= 1:
            int_str = 'hour'
            counter_data = db.execute('''
                SELECT
                    created,
                    counter_value
                FROM counter_value_hour
                WHERE counter_id = ?
                AND created BETWEEN ? AND ?
                ORDER BY id
            ''', (counter['counter_id'], start_date, end_date)
            ).fetchall()
        else:
            int_str = 'day'
            counter_data = db.execute('''
                SELECT
                    created,
                    counter_value
                FROM counter_value_day
                WHERE counter_id = ?
                AND created BETWEEN ? AND ?
                ORDER BY id
            ''', (counter['counter_id'], start_date, end_date)
            ).fetchall()

        print(f'counter_data.len={len(counter_data)}')

        db.commit()

        label = "{} {} - {} ({})".format(counter['counter_key'], start_date.strftime('%Y-%m-%d %H:%M:%S'), end_date.strftime('%Y-%m-%d %H:%M:%S'), (end_date - start_date))

        return render_template('counter.html', item=counter, chart=data_to_chart(label, counter_data, int_str))


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
