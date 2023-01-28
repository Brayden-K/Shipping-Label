from flask import render_template, jsonify, request, redirect, session, flash, url_for
from app import app
from app.decorators import login_required, admin_required
from app.errors import page_not_found
import time, os, glob, shutil

@app.route('/admin', methods=['GET', 'POST'])
@login_required
@admin_required
def admin():
	return render_template('admin/admin.html')