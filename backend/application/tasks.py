from .models import User, Show, Theater, ShowTiming, Booking
from datetime import datetime, timedelta
import os
import matplotlib.pyplot as plt
import matplotlib
from application.workers import celery
from celery.schedules import crontab
from flask_mail import Message, Mail
from .mail import mail
from flask import current_app as app


matplotlib.use("agg")
from flask import url_for, render_template


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute="*", hour="*"),
                             reminder_email.s(), name="reminder")
    sender.add_periodic_task(
        crontab(day_of_month="1", minute=0, hour=0), send_analytics.s(), name="anaytics report"
    )


@celery.task()
def send_analytics():
    users = User.query.all()
    
    for user in users:
        email = user.Email
        subject = "Analytics Report"
        data = create_analytics(user.UserID)
        message = render_template("analytics.html", data=data)
        if send_email(email, subject, message):
            print("Reminder email sent to:", email)
    return "success", 200


def verify_activity(user_id):
    user = User.query.filter_by(UserID=user_id).first()
    booking_dates = Booking.query.filter_by(user_id=user_id).all()
    if not booking_dates:
        return True
    booking_date = max(booking_dates, key=lambda x: x.booking_date).booking_date
    today = datetime.utcnow()
    yesterday = today - timedelta(days=1)
    if not (yesterday < booking_date) or user.last_visited < yesterday:
        return True
    return False


def send_email(email, subject, body):
    msg = Message(subject=subject, recipients=[email], html=body)
    #msg.body = body

    try:
        with app.app_context():
            mail.send(msg)
        return True
    except Exception as e:
        print("Error sending email:")
        return False


@celery.task()
def reminder_email():
    users = User.query.all()
    for user in users:
        if verify_activity(user.UserID):
            # email = user.Email
            email = "shyamfrozenfood@gmail.com"
            subject = "Reminder: We are missing you"
            message = render_template("reminder.html", user=user)
            if send_email(email, subject, message):
                print("Reminder email sent to:", email)
        else:
            # Don't send email
            pass


def get_bookings_for_previous_month(user_id):
    today = datetime.today()
    first_day_of_current_month = today.replace(day=1)
    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
    first_day_of_previous_month = last_day_of_previous_month.replace(day=1)
    all_bookings = Booking.query.filter_by(user_id=user_id).all()
    bookings = []
    for booking in all_bookings:
        show_timing = ShowTiming.query.filter_by(
            TimingID=booking.show_timing_id
        ).first()
        if (
            show_timing.Timing >= first_day_of_previous_month
            and show_timing.Timing <= last_day_of_previous_month
        ):
            bookings.append(booking)
    print("Bookings : ", bookings)
    return bookings


@celery.task()
def create_analytics(user_id):
    user = User.query.filter_by(UserID=user_id).first()

    bookings = get_bookings_for_previous_month(user.UserID)

    total_tickets = 0
    total_amount = 0
    show_ids = []
    for booking in bookings:
        show_timing = ShowTiming.query.filter_by(
            TimingID=booking.show_timing_id
        ).first()
        show_ids.append(show_timing.ShowID)
        show = Show.query.filter_by(ShowID=show_timing.ShowID).first()
        total_tickets += booking.num_tickets
        total_amount += booking.num_tickets * show.TicketPrice
    shows = Show.query.filter(Show.ShowID.in_(show_ids)).all()
    show_names = [show.Name for show in shows]
    theater_ids = [theater.TheaterID for show in shows for theater in show.theaters]
    theaters = Theater.query.filter(Theater.TheaterID.in_(theater_ids)).all()
    theater_names = [theater.Name for theater in theaters]

    analytics = {
        "user": user.Name,
        "total_tickets": total_tickets,
        "total_amount": total_amount,
        "show_names": show_names,
        "theater_names": theater_names,
    }

    create_plots(analytics)

    return analytics


def create_plots(analytics, output_folder="static/plots"):
    user_folder = os.path.join(output_folder, analytics["user"])
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    plt.figure()
    plt.bar(
        ["Total Tickets", "Total Amount"],
        [analytics["total_tickets"], analytics["total_amount"]],
    )
    plt.xlabel("Metrics")
    plt.ylabel("Values")
    plt.title("Total Tickets vs. Total Amount")
    plt.savefig(os.path.join(user_folder, "total_tickets_vs_total_amount.png"))
    plt.close()

    plt.figure()
    plt.bar(
        ["Number of Shows", "Number of Theaters"],
        [len(analytics["show_names"]), len(analytics["theater_names"])],
    )
    plt.xlabel("Metrics")
    plt.ylabel("Counts")
    plt.title("Number of Shows vs. Number of Theaters")
    plt.savefig(os.path.join(user_folder, "num_shows_vs_num_theaters.png"))
    plt.close()

    plot_paths = {
        "total_tickets_vs_total_amount": "plots/total_tickets_vs_total_amount.png",
        "num_shows_vs_num_theaters": "plots/num_shows_vs_num_theaters.png",
    }

    return plot_paths
