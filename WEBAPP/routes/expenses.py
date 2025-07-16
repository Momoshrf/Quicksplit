from flask import Blueprint, render_template, session, redirect, url_for, request
from database import get_db_connection

expenses_bp = Blueprint('expenses', __name__, url_prefix='/expenses')

@expenses_bp.route('/<int:event_id>/summary')
def summary(event_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    conn = get_db_connection()

    # Teilnehmer des Events
    participants = conn.execute(
        'SELECT * FROM participants WHERE event_id = ?',
        (event_id,)
    ).fetchall()

    balances = {p['id']: 0.0 for p in participants}
    id_to_name = {p['id']: p['name'] for p in participants}

    # Nur unbezahlte Schulden berücksichtigen
    rows = conn.execute('''
        SELECT e.id AS expense_id, e.payer_id, ep.user_id, ep.amount_owed
        FROM expenses e
        JOIN expense_participants ep ON e.id = ep.expense_id
        WHERE e.event_id = ? AND ep.paid = 0
    ''', (event_id,)).fetchall()

    for row in rows:
        balances[row['payer_id']] -= row['amount_owed']
        balances[row['user_id']] += row['amount_owed']

    # Rückzahlungen berechnen
    debtors = sorted([(uid, amt) for uid, amt in balances.items() if amt > 0], key=lambda x: x[1])
    creditors = sorted([(uid, -amt) for uid, amt in balances.items() if amt < 0], key=lambda x: x[1])

    transactions = []
    i, j = 0, 0
    while i < len(debtors) and j < len(creditors):
        debtor_id, debt_amt = debtors[i]
        creditor_id, credit_amt = creditors[j]
        amount = min(debt_amt, credit_amt)

        transactions.append({
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

    # Detailausgaben + Beteiligte laden
    expense_rows = conn.execute('''
        SELECT e.id, e.title, e.amount, e.payer_id, p.name AS payer_name
        FROM expenses e
        JOIN participants p ON e.payer_id = p.id
        WHERE e.event_id = ?
    ''', (event_id,)).fetchall()

    all_expenses = []
    for exp in expense_rows:
        participants_split = conn.execute('''
            SELECT ep.user_id, ep.amount_owed, ep.paid, p.name
            FROM expense_participants ep
            JOIN participants p ON ep.user_id = p.id
            WHERE ep.expense_id = ?
        ''', (exp['id'],)).fetchall()

        all_expenses.append({
            'id': exp['id'],
            'title': exp['title'],
            'amount': exp['amount'],
            'payer_name': exp['payer_name'],
            'participants': participants_split
        })

    conn.close()

    return render_template(
        'events/summary.html',
        transactions=transactions,
        balances=balances,
        names=id_to_name,
        all_expenses=all_expenses,
        event_id=event_id
    )


@expenses_bp.route('/<int:expense_id>/toggle_paid/<int:user_id>', methods=['POST'])
def toggle_paid(expense_id, user_id):
    conn = get_db_connection()
    current = conn.execute(
        'SELECT paid FROM expense_participants WHERE expense_id = ? AND user_id = ?',
        (expense_id, user_id)
    ).fetchone()

    if current:
        new_status = 0 if current['paid'] else 1
        conn.execute(
            'UPDATE expense_participants SET paid = ? WHERE expense_id = ? AND user_id = ?',
            (new_status, expense_id, user_id)
        )
        conn.commit()

    referrer = request.referrer or url_for('events.list_events')
    conn.close()
    return redirect(referrer)
