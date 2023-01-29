from flask import render_template, jsonify, request, redirect, session, flash, url_for, send_from_directory, abort
from app import app
from app.decorators import login_required
from app.errors import page_not_found, webhook
import time, os
from discord_webhook import DiscordWebhook
from pprint import pprint

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')