from flask import current_app as app
from flask import render_template, request
from .models import User, Booking, Show, Theater, ShowTiming
from .tasks import create_analytics
from datetime import datetime, timedelta
from .database import db
from application import tasks
from .cache import *


@cache.memoize()
def get_user(id=None, name=None):
    if id:
        user = User.query.get(id)
    else:
        user = User.query.filter_by(Name=name).first()
    return user


@cache.memoize()
def get_theaters():
    theaters = Theater.query.all()
    return theaters


@cache.memoize()
def get_theater(id=None, name=None):
    if name:
        theater = Theater.query.filter_by(Name=name).first()
    else:
        theater = Theater.query.get(id)
    return theater


@cache.memoize()
def get_shows():
    shows = Show.query.all()
    return shows


@cache.memoize()
def get_show(show_id):
    show = Show.query.get(show_id)
    return show


@cache.memoize()
def get_current_happening_shows():
    now = datetime.utcnow()
    shows = Show.query.join(Show.timings).filter(ShowTiming.Timing > now).all()
    return shows


@cache.memoize()
def get_all_bookings():
    bookings = Booking.query.all()
    return bookings


@cache.memoize()
def get_booking(user_id):
    booking = Booking.query.filter_by(user_id=user_id).all()
    return booking
