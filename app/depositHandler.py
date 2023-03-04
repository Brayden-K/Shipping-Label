from flask import render_template, jsonify, request, redirect, session, flash, url_for, send_from_directory, abort
from app import app
from app.decorators import login_required
from app.errors import page_not_found
import time, os
from pprint import pprint
from app.coinbase import Coinbase

@app.route('/deposit', methods=["GET","POST"])
@login_required
def deposit():
    amount = request.form.get('amount')
    if not amount:
        flash('Amount is required to deposit.')
        return redirect(url_for('index'))

    settings = app.db.GetSettings()

    CB = Coinbase(
        key=settings['coinbaseKey'],
        signingSecret=settings['coinbaseSigningSecret'],
        )
    
    product = {
        'name': f"{settings['siteName']} - Deposit",
        'description': f'Deposit ${amount} for your {settings["siteName"]} account.',
        'price': f'{amount}',
        'successUrl':request.host_url,
        'cancelUrl':request.host_url,
        'metadata': {
            'email': session['username'],
            'amount': amount
        }
    }
    
    checkout = CB.createInvoice(product)
    return redirect(checkout)

@app.route('/coinbaseWebhook', methods=['POST'])
def coinbaseWebhook():
    settings = app.db.GetSettings()
    client = Coinbase.Client(api_key=settings['coinbaseKey'])
    WEBHOOK_SECRET = settings['coinbaseSigningSecret']
    request_data = request.data.decode('utf-8')
    request_sig = request.headers.get('X-CC-Webhook-Signature', None)

    try:
        # signature verification and event object construction
        event = Webhook.construct_event(request_data, request_sig, WEBHOOK_SECRET)
    except Exception as e:
        return str(e), 400

    if event.type == 'charge:confirmed':
        user = app.db.GetUserByEmail(event['data']['metadata']['email'])
        amount = event['data']['metadata']['amount']
        data = {
            'ownerId': user['id'],
            'invoiceId': event['id'],
            'email': event['data']['metadata']['email'],
            'amount': event['data']['payments'][0]['net']['crypto']['amount'],
            'currency': event['data']['payments'][0]['net']['crypto']['currency'],
            'paid': True
        }
        app.db.Insert('invoices', data)
        app.db.AddBalanceToUser(user['email'], amount)
    return 'success', 200

@app.route('/success')
def successPage():
    return render_template('success.html')