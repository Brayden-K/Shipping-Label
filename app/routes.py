from flask import render_template, jsonify, request, redirect, session, flash, url_for, send_from_directory, abort
from app import app
from app.decorators import login_required
from app.errors import page_not_found, webhook
import time, os
from pprint import pprint

@app.route('/')
def index():
    return render_template('index.html')