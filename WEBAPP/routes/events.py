from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from database import get_db_connection

events_bp = Blueprint('events', __name__, url_prefix='/events')


@events_bp.route('/')
def list_events():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    events = conn.execute(
        'SELECT * FROM events WHERE owner_id = ? ORDER BY created_at DESC',
        (session['user_id'],)
    ).fetchall()
    conn.close()

    return render_template('events/list.html', events=events)


@events_bp.route('/new', methods=['GET', 'POST'])
def create_event():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        name = request.form['name'].strip()
        if not name:
            flash('Bitte gib einen Namen ein!')
            return render_template('events/create.html')

        conn = get_db_connection()

        # Event erstellen
        cursor = conn.execute(
            'INSERT INTO events (name, owner_id) VALUES (?, ?)',
            (name, session['user_id'])
        )
        event_id = cursor.lastrowid

        
        user = conn.execute('SELECT username FROM users WHERE id = ?', (session['user_id'],)).fetchone()
        if user:
            conn.execute(
                'INSERT INTO participants (name, event_id) VALUES (?, ?)',
                (user['username'], event_id)
            )

        conn.commit()
        conn.close()

        flash('Event wurde erstellt!')
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

    
    participants = conn.execute('''
        SELECT * FROM participants WHERE event_id = ? ORDER BY name
    ''', (event_id,)).fetchall()

    # Ausgaben + Zahlername (aus participants!)
    expenses = conn.execute('''
        SELECT e.*, p.name AS payer_name
        FROM expenses e
        JOIN participants p ON e.payer_id = p.id
        WHERE e.event_id = ?
        ORDER BY e.date DESC
    ''', (event_id,)).fetchall()

    
    balances = {p['id']: 0.0 for p in participants}
    id_to_name = {p['id']: p['name'] for p in participants}

    rows = conn.execute('''
        SELECT e.id AS expense_id, e.payer_id, ep.user_id, ep.amount_owed
        FROM expenses e
        JOIN expense_participants ep ON e.id = ep.expense_id
        WHERE e.event_id = ? AND ep.paid = 0
    ''', (event_id,)).fetchall()

    for row in rows:
        balances[row['payer_id']] -= row['amount_owed']
        balances[row['user_id']] += row['amount_owed']

    debtors = sorted([(uid, amt) for uid, amt in balances.items() if amt > 0], key=lambda x: x[1])
    creditors = sorted([(uid, -amt) for uid, amt in balances.items() if amt < 0], key=lambda x: x[1])

    summary = []
    i, j = 0, 0
    while i < len(debtors) and j < len(creditors):
        debtor_id, debt_amt = debtors[i]
        creditor_id, credit_amt = creditors[j]
        amount = min(debt_amt, credit_amt)

        summary.append({
            'from': id_to_name[debtor_id],
            'to': id_to_name[creditor_id],
            'amount': round(amount, 2)
        })

        debtors[i] = (debtor_id, debt_amt - amount)
        creditors[j] = (creditor_id, credit_amt - amount)

        if debtors[i][1] == 0:
            i += 1
        if creditors[j][1] == 0:
            j += 1

    conn.close()

    return render_template(
        'events/show.html',
        event=event,
        participants=participants,
        expenses=expenses,
        summary=summary
    )


@events_bp.route('/<int:event_id>/add_participant', methods=['POST'])
def add_participant(event_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    name = request.form['name'].strip()

    if not name:
        flash('Bitte gib einen Teilnehmernamen ein.')
        return redirect(url_for('events.show_event', event_id=event_id))

    conn = get_db_connection()

    # Check for duplicates
    existing = conn.execute(
        'SELECT 1 FROM participants WHERE event_id = ? AND name = ?',
        (event_id, name)
    ).fetchone()

    if existing:
        flash('Teilnehmer ist bereits hinzugefügt.')
    else:
        conn.execute(
            'INSERT INTO participants (name, event_id) VALUES (?, ?)',
            (name, event_id)
        )
        conn.commit()
        flash('Teilnehmer hinzugefügt!')

    conn.close()
    return redirect(url_for('events.show_event', event_id=event_id))


@events_bp.route('/<int:event_id>/add_expense', methods=['GET', 'POST'])
def add_expense(event_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    conn = get_db_connection()

    participants = conn.execute(
        'SELECT * FROM participants WHERE event_id = ? ORDER BY name',
        (event_id,)
    ).fetchall()

    if request.method == 'POST':
        title = request.form['title'].strip()
        amount = float(request.form['amount'])
        payer_id = int(request.form['payer'])
        split_ids = request.form.getlist('split_users')

        if not title or not amount or not split_ids:
            flash('Bitte alle Felder korrekt ausfüllen.')
            return redirect(url_for('events.add_expense', event_id=event_id))

        cur = conn.execute(
            'INSERT INTO expenses (title, amount, payer_id, event_id) VALUES (?, ?, ?, ?)',
            (title, amount, payer_id, event_id)
        )
        expense_id = cur.lastrowid

        split_amount = round(amount / len(split_ids), 2)

        for participant_id in split_ids:
            conn.execute(
                'INSERT INTO expense_participants (expense_id, user_id, amount_owed, paid) VALUES (?, ?, ?, ?)',
                (expense_id, participant_id, split_amount, 0)
            )

        conn.commit()
        conn.close()
        flash('Ausgabe wurde hinzugefügt!')
        return redirect(url_for('events.show_event', event_id=event_id))

    conn.close()
    return render_template('events/add_expense.html', event_id=event_id, participants=participants)
