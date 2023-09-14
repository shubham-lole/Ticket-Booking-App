from flask import current_app as app
from flask import render_template, request
from .models import User, Booking, Show, Theater, ShowTiming
from .tasks import create_analytics
from datetime import datetime, timedelta
from .database import db
from application import tasks
from flask import render_template, redirect, url_for
from flask_mail import Message
from .mail import mail
from .tasks import send_analytics

@app.route("/")
def index():
    return render_template("home.html")


@app.route("/api/update_last_visited")
def update_last_visited():
    user = request.args.get("user")
    user = User.query.filter_by(Name=user).first()
    user.last_visited = datetime.utcnow()
    db.session.commit()
    return "success", 200

@app.route("/test_anaytics/<user_id>")
def test(user_id):
    data = create_analytics(user_id)
    return render_template("analytics.html", data=data)

@app.route("/test_reminder/<user_id>")
def test_reminder(user_id):
    user = User.query.filter_by(UserID=user_id).first()
    return render_template("reminder.html", user=user)