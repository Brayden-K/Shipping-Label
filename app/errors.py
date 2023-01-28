from flask import render_template, redirect, url_for, session, flash
from app import app
from functools import wraps
import requests

from flask import render_template

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

def webhook(title, msg, type=False):
    settings = app.db.GetSettings()
    if settings['enableWebhooks']:
        match type:
            case 'contact':
                url = settings['contactWebhook']
            case 'ticket':
                url = settings['ticketWebhook']
            case 'project':
                url = settings['projectWebhook']
            case 'invoice':
                url = settings['invoiceWebhook']

        data = {
            "embeds": [{
                "title": title,
                "color": "14177041",
                "description": msg,
                "footer": {
                    "text": get_time(),
                }
            }]
        }
        r = requests.post(url, json=data)
    else:
        pass

def get_time():
    from datetime import datetime
    from pytz import timezone, utc
    # date_format='%m/%d/%Y %H:%M:%S:%Z'
    date_format='%m-%d-%Y %H:%M:%S'
    date = datetime.now(tz=utc)
    date = date.astimezone(timezone('US/Pacific'))
    pstDateTime=date.strftime('%Y/%m/%d %I:%M %p')
    return pstDateTime