from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from database import get_db_connection

events_bp = Blueprint('events', __name__, url_prefix='/events')

@events_bp.route('/')
def list_events():
    """Zeigt Events, bei denen der Benutzer Teilnehmer ist"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    events = conn.execute('''
        SELECT e.*
        FROM events e
        JOIN event_participants ep ON e.id = ep.event_id
        WHERE ep.user_id = ?
        ORDER BY e.created_at DESC
    ''', (session['user_id'],)).fetchall()
    conn.close()
    return render_template('events/list.html', events=events)

@events_bp.route('/new', methods=['GET', 'POST'])
def create_event():
    """Neues Event erstellen und den Ersteller als Teilnehmer hinzufügen"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        name = request.form['name']
        if not name.strip():
            flash('Bitte gib einen Namen ein!')
            return render_template('events/create.html')

        conn = get_db_connection()
        # Event erstellen
        cursor = conn.execute('INSERT INTO events (name, owner_id) VALUES (?, ?)', (name, session['user_id']))
        event_id = cursor.lastrowid

        # Ersteller als Teilnehmer hinzufügen
        conn.execute('INSERT INTO event_participants (event_id, user_id) VALUES (?, ?)', (event_id, session['user_id']))
        conn.commit()
        conn.close()

        flash('✅ Event wurde erstellt!')
        return redirect(url_for('events.list_events'))

    return render_template('events/create.html')

@events_bp.route('/<int:event_id>')
def show_event(event_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    event = conn.execute('SELECT * FROM events WHERE id = ?', (event_id,)).fetchone()

    if event is None:
        conn.close()
        return "Event nicht gefunden", 404

    users = conn.execute('''
        SELECT u.* FROM users u
        JOIN event_participants ep ON u.id = ep.user_id
        WHERE ep.event_id = ?
        ORDER BY u.username
    ''', (event_id,)).fetchall()

    expenses = conn.execute('''
        SELECT e.*, u.username AS payer_name
        FROM expenses e
        JOIN users u ON e.payer_id = u.id
        WHERE e.event_id = ?
        ORDER BY e.date DESC
    ''', (event_id,)).fetchall()

    conn.close()
    return render_template('events/show.html', event=event, users=users, expenses=expenses)


@events_bp.route('/<int:event_id>/add_participant', methods=['POST'])
def add_participant(event_id):
    """Fügt einen bestehenden Benutzer als Teilnehmer hinzu (per Username)"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    username = request.form['username'].strip()

    if not username:
        flash('Bitte gib einen Benutzernamen ein.')
        return redirect(url_for('events.show_event', event_id=event_id))

    conn = get_db_connection()
    user = conn.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()

    if not user:
        flash('Benutzer nicht gefunden.')
    else:
        # Prüfen ob schon Teilnehmer
        already = conn.execute('''
            SELECT 1 FROM event_participants WHERE event_id = ? AND user_id = ?
        ''', (event_id, user['id'])).fetchone()

        if already:
            flash('Benutzer ist bereits Teilnehmer.')
        else:
            conn.execute('INSERT INTO event_participants (event_id, user_id) VALUES (?, ?)', (event_id, user['id']))
            conn.commit()
            flash('Teilnehmer hinzugefügt!')

    conn.close()
    return redirect(url_for('events.show_event', event_id=event_id))

@events_bp.route('/<int:event_id>/add_expense', methods=['GET', 'POST'])
def add_expense(event_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    conn = get_db_connection()

    participants = conn.execute('''
        SELECT u.id, u.username FROM users u
        JOIN event_participants ep ON u.id = ep.user_id
        WHERE ep.event_id = ?
    ''', (event_id,)).fetchall()

    if request.method == 'POST':
        title = request.form['title']
        amount = float(request.form['amount'])
        payer_id = int(request.form['payer'])
        split_user_ids = request.form.getlist('split_users')

        if not title or not amount or not split_user_ids:
            flash('Bitte alle Felder ausfüllen.')
            return redirect(url_for('events.add_expense', event_id=event_id))

        cur = conn.execute(
            'INSERT INTO expenses (title, amount, payer_id, event_id) VALUES (?, ?, ?, ?)',
            (title, amount, payer_id, event_id)
        )
        expense_id = cur.lastrowid

        split_amount = round(amount / len(split_user_ids), 2)
        for user_id in split_user_ids:
            conn.execute('''
                INSERT INTO expense_participants (expense_id, user_id, amount_owed)
                VALUES (?, ?, ?)
            ''', (expense_id, user_id, split_amount))

        conn.commit()
        conn.close()
        flash('Ausgabe hinzugefügt!')
        return redirect(url_for('events.show_event', event_id=event_id))

    conn.close()
    return render_template('events/add_expense.html', event_id=event_id, participants=participants)



