from flask import render_template, jsonify, request, redirect, session, flash, url_for, send_from_directory, abort
from app import app
from app.decorators import login_required
from app.errors import page_not_found, webhook
import time, os, datetime
from discord_webhook import DiscordWebhook
from pprint import pprint

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'GET':
        user = app.db.GetUserByEmail(session['username'])
        tickets = app.db.GetTicketsById(user['id'])
        activeTickets = app.db.GetActiveTicketsById(user['id'])
        return render_template('dashboard.html', tickets=tickets, activeTickets=activeTickets)

    if 'createTicket' in request.form:
        data = request.form.to_dict()
        data['complete'] = 0
        data['progress'] = 0
        del data['createTicket']
        data['created'] = datetime.date.today()
        app.db.Insert('tickets', data)
        flash('Your ticket has been created successfully.')
        return redirect(url_for('dashboard'))