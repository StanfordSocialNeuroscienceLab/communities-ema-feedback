import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash

from feedback.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        cursor = db.cursor(cursor_factory = RealDictCursor)
        error = None



        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        else:
            cursor.execute(
                'SELECT id FROM participant WHERE username = %s', (username,))
            if cursor.rowcount != 0:
                error = f'Participant {username} is already registered.'

        if error is None:
            form = request.form
            insert_command = 'INSERT INTO participant (%s) VALUES (%s)' % (
                    ", ".join(form.keys()),
                    ', '.join(['%s'] * len(form)))
            print(insert_command)
            values = []
            for k, v in form.items():
                if k == 'password':
                    values.append(generate_password_hash(v))
                else:
                    values.append(v)
            cursor.execute(
                insert_command,
                values
                )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        cursor = db.cursor(cursor_factory = RealDictCursor)
        error = None
        cursor.execute(
            'SELECT * FROM participant WHERE username = %s', (username,)
        )

        if cursor.rowcount == 0:
            error = 'Unknown participant.'
        else:
            participant = cursor.fetchall()[0]
            if not check_password_hash(participant['password'], password):
                error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['participant_id'] = participant['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    participant_id = session.get('participant_id')
    g.participant = None

    if participant_id is not None:
        cursor = get_db().cursor(cursor_factory = RealDictCursor)
        cursor.execute(
            'SELECT * FROM participant WHERE id = %s', (participant_id,)
        )
        if cursor.rowcount > 0:
            g.participant = cursor.fetchone()
        else:
            session.clear()



@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.participant is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
