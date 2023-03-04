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
	orders = app.db.GetAllOrders()
	return render_template('admin/adminhome.html', tickets=tickets, members=members, invoices=invoices, orders=orders)

@app.route('/admin/tickets')
def tickets():
	tickets = app.db.GetAllTickets()
	return render_template('admin/tickets.html', tickets=tickets)

@app.route('/admin/members')
def members():
	members = app.db.GetAllMembers()
	return render_template('admin/members.html', members=members)

@app.route('/admin/orders')
def adminOrders():
	orders = app.db.GetAllOrders()
	return render_template('admin/orders.html', orders=orders)

@app.route('/admin/deleteAccount')
def adminDeleteAccount():
	if not request.args.get('id'):
		flash('No id specified.')
		return redirect(url_for('members'))

	app.db.DeleteAccountById(request.args.get('id'))
	flash('Account deleted.')
	return redirect(url_for('members'))

@app.route('/admin/banAccount')
def adminBanAccount():
	if not request.args.get('id'):
		flash('No id specified.')
		return redirect(url_for('members'))

	app.db.BanAccount(request.args.get('id'))
	flash('Account banned.')
	return redirect(url_for('members'))

@app.route('/admin/unbanAccount')
def adminUnbanAccount():
	if not request.args.get('id'):
		flash('No id specified.')
		return redirect(url_for('members'))

	app.db.UnbanAccount(request.args.get('id'))
	flash('Account unbanned.')
	return redirect(url_for('members'))