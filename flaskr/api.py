
import sys
import traceback


from flask import (
    Blueprint, request, Response, abort, current_app
)

from .db import get_db

bp = Blueprint('api', __name__)

@bp.route('/db.sql')
def print_dump():
    def generate(db_path):
        import sqlite3
        conn = sqlite3.connect(
            db_path,
            detect_types=sqlite3.PARSE_DECLTYPES
        )

        conn.row_factory = sqlite3.Row

        for line in conn.iterdump():
            yield "{}\n".format(line)

        return

    return current_app.response_class(generate(current_app.config['DATABASE']), mimetype="text/plain")



@bp.route("/api/set-counter", methods=['POST'])
def set_counter():
    if request.is_json:
        request_data = request.get_json()
        print(request_data)
        app_key = request_data['app_key']
        counter_key = request_data['counter_key']
        value = request_data['value']

        try:
            counter_id = get_counter_id_by_key(counter_key)
            current_app.logger.info(f'counter_id = {counter_id}')

            db = get_db()
            db.execute('''
                INSERT INTO counter_value_raw (counter_id, counter_value)
                VALUES (?, ?)
                ''', (counter_id, value))

            row_processed = process_minutes(counter_id)
            if row_processed > 0:
                row_processed = process_hours(counter_id)

                if row_processed > 0:
                    print('process counter_value_day')


            db.commit()
            return Response(status=201)
        except Exception as e:
            print("Oops!", e.__class__, "occurred.")
            print(sys.exc_info()[2])
            traceback.print_exc()
            abort(502)


def get_counter_id_by_key(counter_key):
    db = get_db()
    row = db.execute('''
    SELECT counter_id
    FROM counter
    WHERE enabled = true
    AND counter_key = ?
    ''', (counter_key,)).fetchone()

    counter_id = row[0]
    return counter_id


def process_minutes(counter_id):
    db = get_db()
    row = db.execute('''
        SELECT MIN(id)
        FROM counter_value_raw
        WHERE counter_id = ?
        GROUP BY STRFTIME('%Y-%m-%d %H:%M', created)
        ORDER BY id DESC
        LIMIT 1
    ''', (counter_id,)).fetchone()

    max_id = row[0]

    row = db.execute('''
    INSERT INTO counter_value_min (id, counter_id, created, counter_value)
    SELECT
        MAX(id),
        counter_id,
        STRFTIME('%Y-%m-%d %H:%M', created),
        AVG(counter_value)
    FROM counter_value_raw
    WHERE id < ?
        AND counter_id = ?
    GROUP BY STRFTIME('%Y-%m-%d %H:%M', created)
    ''', (max_id, counter_id))

    row_processed = row.rowcount
    if row_processed > 0:
        db.execute('''
        DELETE FROM counter_value_raw
        WHERE id < ?
            AND counter_id = ?
        ''', (max_id, counter_id))

    return row_processed


def process_hours(counter_id):
    db = get_db()
    row = db.execute('''
    SELECT MIN(id)
    FROM counter_value_min
    WHERE counter_id = ?
    GROUP BY STRFTIME('%Y-%m-%d %H', created)
    ORDER BY id DESC
    LIMIT 1
    ''', (counter_id,)).fetchone()

    max_id = row[0]

    row = db.execute('''
    SELECT MAX(id)
    FROM counter_value_hour
    WHERE counter_id = ?
    ''', (counter_id,))

    min_id = 0
    rs = row.fetchone()
    if rs is not None:
        min_id = rs[0]

    current_app.logger.info(f'process_hours: min_id = {min_id}')
    current_app.logger.info(f'process_hours: max_id = {max_id}')

    row = db.execute('''
    INSERT INTO counter_value_hour (id, counter_id, created, counter_value)
    SELECT
        MAX(id),
        counter_id,
        STRFTIME('%Y-%m-%d %H', created),
        SUM(counter_value) / 60
    FROM counter_value_min
    WHERE counter_id = ?
    AND id BETWEEN ? AND ?
    GROUP BY STRFTIME('%Y-%m-%d %H', created)
    ''', (counter_id, min_id + 1, max_id - 1))
    row_processed = row.rowcount

    return row_processed
