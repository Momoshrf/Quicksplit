from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        # Check if username already exists
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        
        if user:
            flash(' Der Benutzername ist bereits vergeben.')
            conn.close()
            return redirect(url_for('auth.register'))

        hashed_password = generate_password_hash(password)
        conn.execute(
            'INSERT INTO users (username, password) VALUES (?, ?)',
            (username, hashed_password)
        )
        conn.commit()
        conn.close()

        flash(' Registrierung erfolgreich! Bitte einloggen.')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['username']
            flash(' Erfolgreich eingeloggt!')
            return redirect(url_for('index'))
        else:
            flash('Benutzername oder Passwort ist falsch.')

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Erfolgreich ausgeloggt.')
    return redirect(url_for('auth.login'))
