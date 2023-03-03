from flask import render_template, jsonify, request, redirect, session, flash, url_for
from app import app
from app.decorators import login_required, admin_required
from app.errors import page_not_found
import time

@app.route('/admin', methods=['GET', 'POST'])
@login_required
@admin_required
def admin():
	tickets = app.db.GetAllTickets()
	members = app.db.GetAllMembers()
	invoices = app.db.GetAllInvoices()
	return render_template('admin/adminhome.html', tickets=tickets, members=members, invoices=invoices)

@app.route('/admin/tickets')
def tickets():
	tickets = app.db.GetAllTickets()
	return render_template('admin/tickets.html', tickets=tickets)

@app.route('/admin/members')
def members():
	members = app.db.GetAllMembers()
	return render_template('admin/members.html', members=members)