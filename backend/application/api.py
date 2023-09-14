from flask_restful import Api, Resource
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity,
)
from flask import request
from application.models import (
    User,
    Theater,
    Show,
    Role,
    ShowTiming,
    Booking,
    show_theater_association,
)
from application.database import db
from passlib.hash import bcrypt
from flask import jsonify
from functools import wraps
from datetime import datetime
from flask import current_app as app
from flask import render_template
from time import perf_counter_ns
from .cache import cache

from .data_access import *


def create_admin_user():
    if not User.query.filter_by(Name="admin").first():
        admin_role = Role(name="admin", description="Administrator Role")
        db.session.add(admin_role)
        db.session.commit()
        password = "adminpassword"
        hashed_password = bcrypt.hash(password)
        admin_user = User(Name="admin", Password=hashed_password, IsAdmin=True)
        admin_user.Roles.append(admin_role)
        db.session.add(admin_user)
        db.session.commit()


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        start = perf_counter_ns()
        current_user = get_jwt_identity()
        user = User.query.filter_by(Name=current_user).first()
        end = perf_counter_ns()
        print("time taken", end - start)
        if user and user.IsAdmin:
            return fn(*args, **kwargs)
        else:
            return {"message": "Admin access required"}, 403

    return wrapper


def isShowFull(show_timing_id):
    show_timing = ShowTiming.query.get(show_timing_id)
    total_booked_tickets = (
        Booking.query.filter_by(show_timing_id=show_timing_id)
        .with_entities(db.func.sum(Booking.num_tickets))
        .scalar()
    )
    if total_booked_tickets is None:
        total_booked_tickets = 0

    available_seats = show_timing.theater.Capacity - total_booked_tickets
    if available_seats > 0:
        return False
    else:
        return True


# User Login resource
class UserLoginResource(Resource):
    def post(self):
        username = request.form.get("username", None)
        password = request.form.get("password", None)

        if not username or not password:
            return {"message": "Missing username or password"}, 400

        user = User.query.filter_by(Name=username).first()

        if not user:
            return {"message": "User not found"}, 404

        if not bcrypt.verify(password, user.Password):
            return {"message": "Invalid credentials"}, 401

        access_token = create_access_token(identity=username)
        user.last_visited = datetime.utcnow()
        db.session.commit()
        return {"access_token": access_token}, 200


# Admin Login resource
class AdminLoginResource(Resource):
    def post(self):
        username = request.form.get("username", None)
        password = request.form.get("password", None)

        if not username or not password:
            return {"message": "Missing username or password"}, 400

        admin = User.query.filter_by(Name=username).first()

        if not admin:
            return {"message": "User not found"}, 404

        if not bcrypt.verify(password, admin.Password):
            return {"message": "Invalid credentials"}, 401

        if not any(role.name == "admin" for role in admin.Roles):
            return {"message": "User is not an admin"}, 401

        access_token = create_access_token(identity=username)
        return {"access_token": access_token}, 200


# User Login resource
class UserRegisterationResource(Resource):
    def post(self):
        username = request.form.get("username", None)
        password = request.form.get("password", None)
        email = request.form.get("email", None)

        if not username or not password:
            return {"message": "Missing username or password"}, 400

        user = get_user(name=username)

        if user:
            return {"message": "User already exists"}, 400
        else:
            hashed_password = bcrypt.hash(password)
            user = User(Name=username, Password=hashed_password, Email=email)
            db.session.add(user)
            db.session.commit()
            cache.clear()
            return {"message": "User created successfully"}, 200


class TheaterResource(Resource):
    @jwt_required()
    @admin_required
    def post(self):
        data = request.get_json()
        name = data.get("name")
        place = data.get("place")
        capacity = data.get("capacity")

        if not all([name, place, capacity]):
            return {"message": "Please provide all required data."}, 400

        theater = get_theater(name=name)
        if theater:
            return {"message": "Theater already exists."}, 400

        try:
            theater = Theater(Name=name, Place=place, Capacity=capacity)
            db.session.add(theater)
            db.session.commit()
            cache.clear()
            return {
                "message": "Theater added successfully.",
                "theater_id": theater.TheaterID,
            }, 201
        except Exception as e:
            db.session.rollback()
            return {"message": "Failed to add the theater.", "error": str(e)}, 500

    def get(self):
        theaters = get_theaters()

        theaters_data = [
            {
                "TheaterID": theater.TheaterID,
                "Name": theater.Name,
                "Place": theater.Place,
                "Capacity": theater.Capacity,
            }
            for theater in theaters
        ]
        return {"theaters": theaters_data}, 200


class EditTheaterResource(Resource):
    @jwt_required()
    @admin_required
    def put(self, theater_id):
        name = request.json.get("theaterName", None)
        capacity = request.json.get("capacity", None)

        if not name:
            return {"message": "Please provide all required data."}, 400

        theater = get_theater(id=theater_id)
        if not theater:
            return {"message": "Theater not found."}, 404

        try:
            theater.Name = name
            theater.Capacity = capacity
            db.session.commit()
            cache.clear()
            return {"message": "Theater updated successfully."}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Failed to update the theater.", "error": str(e)}, 500

    @jwt_required()
    @admin_required
    def delete(self, theater_id):
        theater = get_theater(id=theater_id)
        if not theater:
            return {"message": "Theater not found."}, 404

        try:
            shows = ShowTiming.query.filter_by(TheaterID=theater_id).all()
            ShowTiming.query.filter_by(TheaterID=theater_id).delete()
            for show in shows:
                Booking.query.filter_by(show_timing_id=show.TimingID).delete()
            db.session.delete(theater)
            db.session.commit()
            cache.clear()
            return {"message": "Theater deleted successfully."}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Failed to delete the theater.", "error": str(e)}, 500


class ShowResource(Resource):
    @jwt_required()
    @admin_required
    def post(self):
        data = request.get_json()
        name = data.get("name")
        rating = data.get("ratings")
        tags = data.get("tags")
        ticket_price = data.get("ticket_price")
        theaters_data = data.get("theaters")

        if not all([name, ticket_price, theaters_data]):
            return {"message": "Please provide all required data."}, 400

        try:
            show = Show(Name=name, Rating=rating, Tags=tags, TicketPrice=ticket_price)
            db.session.add(show)
            db.session.flush()

            for theater_data in data["theaters"]:
                theater_data["timing"] = datetime.strptime(
                    theater_data["timing"], "%Y-%m-%d %H:%M:%S"
                )

            for theater_data in theaters_data:
                theater_id = theater_data.get("theater_id")
                timing = theater_data.get("timing")

                if not theater_id or not timing:
                    continue

                theater = get_theater(id=theater_id)
                if not theater:
                    continue

                new_timing = timing
                existing_timings = ShowTiming.query.filter_by(
                    TheaterID=theater_id
                ).all()
                for existing_timing in existing_timings:
                    print(existing_timing.Timing)
                    if existing_timing.Timing == new_timing:
                        return {
                            "message": "Show timing conflicts with an existing show timing."
                        }, 409

                show_timing = ShowTiming(
                    ShowID=show.ShowID, TheaterID=theater_id, Timing=timing
                )
                db.session.add(show_timing)
                show.theaters.append(theater)

            db.session.commit()
            cache.clear()
            return {
                "message": "Show added to theaters successfully.",
                "show_id": show.ShowID,
            }, 201
        except Exception as e:
            db.session.rollback()
            return {
                "message": "Failed to add the show to theaters.",
                "error": str(e),
            }, 500

    def get(self):
        current = request.args.get("current")
        now = datetime.now()
        if current == "0":
            shows = Show.query.all()
        else:
            shows = Show.query.join(Show.timings).filter(ShowTiming.Timing > now).all()
        shows_data = [
            {
                "ShowID": show.ShowID,
                "Name": show.Name,
                "Rating": show.Rating,
                "Tags": show.Tags,
                "TicketPrice": show.TicketPrice,
                "Theaters": [
                    {
                        "TheaterID": theater.TheaterID,
                        "Name": theater.Name,
                        "Place": theater.Place,
                    }
                    for theater in show.theaters
                ],
                "Timings": [
                    {
                        "TimingID": timing.TimingID,
                        "Timing": timing.Timing.strftime("%Y-%m-%d %H:%M:%S"),
                        "TheaterID": timing.TheaterID,
                        "show_id": timing.ShowID,
                        "isShowFull": isShowFull(timing.TimingID),
                    }
                    for timing in show.timings
                ],
            }
            for show in shows
        ]
        return {"shows": shows_data}, 200


class EditShowResource(Resource):
    @jwt_required()
    @admin_required
    def put(self, show_id):
        data = request.get_json()
        print(data)
        name = data.get("showName")
        rating = data.get("showRating")
        tags = data.get("tags")
        ticket_price = data.get("ticketPrice")

        if not all([name, ticket_price]):
            return {"message": "Please provide all required data."}, 400

        show = get_show(show_id=show_id)
        if not show:
            return {"message": "Show not found."}, 404

        try:
            show.Name = name
            show.Rating = rating
            show.Tags = tags
            show.TicketPrice = ticket_price
            db.session.commit()
            cache.clear()
            return {"message": "Show updated successfully."}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Failed to update the show.", "error": str(e)}, 500

    @jwt_required()
    @admin_required
    def delete(self, show_id):
        show = get_show(show_id=show_id)
        if not show:
            return {"message": "Show not found."}, 404

        try:
            show_timing = ShowTiming.query.filter_by(ShowID=show_id).first()
            ShowTiming.query.filter_by(ShowID=show_id).delete()
            Booking.query.filter_by(show_timing_id=show_timing.TimingID).delete()
            db.session.delete(show)
            db.session.commit()
            cache.clear()
            return {"message": "Show deleted successfully."}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Failed to delete the show.", "error": str(e)}, 500


class BookingResource(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        user = data.get("user")
        show_timing_id = data.get("show_timing_id")
        num_tickets = data.get("num_tickets")
        theaterId = data.get("theaterId")

        user_id = get_user(name=user).UserID

        if not all([user_id, show_timing_id, num_tickets]):
            return {"message": "Please provide all required data."}, 400

        try:
            show_timing = ShowTiming.query.get(show_timing_id)
            if not show_timing:
                return {"message": "Invalid show timing ID."}, 404

            if show_timing.Timing < datetime.utcnow():
                return {
                    "message": "The show has already taken place. Cannot book tickets for past shows."
                }, 400

            total_booked_tickets = (
                Booking.query.filter_by(show_timing_id=show_timing_id)
                .with_entities(db.func.sum(Booking.num_tickets))
                .scalar()
            )
            if total_booked_tickets is None:
                total_booked_tickets = 0

            available_seats = show_timing.theater.Capacity - total_booked_tickets
            if int(num_tickets) > available_seats:
                return {
                    "message": f"Not enough seats available. Only {available_seats} seats left for this show timing."
                }, 400

            booking = Booking(
                user_id=user_id, show_timing_id=show_timing_id, num_tickets=num_tickets
            )
            db.session.add(booking)
            db.session.commit()
            cache.clear()
            return {
                "message": "Booking created successfully.",
                "booking_id": booking.id,
            }, 201
        except Exception as e:
            db.session.rollback()
            return {"message": "Failed to create booking.", "error": str(e)}, 500

    @jwt_required()
    def get(self):
        user = request.args.get("user")

        user_id = get_user(name=user).UserID

        if not user:
            return {"message": "User is required."}, 400

        bookings = get_booking(user_id)
        if user == "admin":
            bookings = get_all_bookings()
        if not bookings:
            return {"message": "No bookings found for the given user."}, 404

        booking_info_list = []

        for booking in bookings:
            show_timing = ShowTiming.query.filter_by(
                TimingID=booking.show_timing_id
            ).first()
            theater_id = show_timing.TheaterID
            show_id = show_timing.ShowID
            show = get_show(show_id)
            show_name = show.Name
            theater_name = get_theater(id=theater_id).Name
            booking_info = {
                "BookingID": booking.id,
                "ShowName": show_name,
                "ShowDate": show_timing.Timing.strftime("%Y-%m-%d"),
                "ShowTiming": show_timing.Timing.strftime("%H:%M:%S"),
                "TheaterName": theater_name,
                "NumTickets": booking.num_tickets,
                "BookingDate": booking.booking_date.strftime("%Y-%m-%d"),
            }

            booking_info_list.append(booking_info)

        return {"bookings": booking_info_list}, 200


class TheaterSearchResource(Resource):
    def get(self):
        location_preference = request.args.get("location")
        if not location_preference:
            return {"message": "Location preference is required."}, 400

        theaters = Theater.query.filter(
            Theater.Place.ilike(f"%{location_preference}%")
        ).all()
        if not theaters:
            return {
                "message": "No theaters found for the given location preference."
            }, 404

        theaters_data = [
            {
                "TheaterID": theater.TheaterID,
                "Name": theater.Name,
                "Place": theater.Place,
                "Capacity": theater.Capacity,
            }
            for theater in theaters
        ]
        return {"theaters": theaters_data}, 200


class ShowSearchResource(Resource):
    def get(self):
        tags = request.args.get("tags")
        rating = request.args.get("rating")
        print("tags and ratings", tags, rating)

        query = Show.query.join(ShowTiming).join(Theater)

        if tags:
            query = query.filter(Show.Tags.ilike(f"%{tags}%"))

        if rating:
            query = query.filter(Show.Rating == rating)

        shows = query.all()

        if tags is None and rating is None:
            shows = Show.query.all()

        if not shows:
            return {"message": "No movies found for the given criteria."}, 404

        for show in shows:
            print(show.Name, show.Rating, show.Tags)

        shows_data = [
            {
                "ShowID": show.ShowID,
                "Name": show.Name,
                "Rating": show.Rating,
                "Tags": show.Tags,
                "TicketPrice": show.TicketPrice,
            }
            for show in shows
        ]
        return {"shows": shows_data}, 200


import os
from flask import Flask, send_from_directory
from flask_restful import Resource
import pandas as pd


class ExportResource(Resource):
    @jwt_required()
    @admin_required
    def get(self, theater_id):
        theater = get_theater(id=theater_id)
        shows = get_shows()
        show_name= []
        show_rating = []
        show_tags = []
        for show in shows:
            show_name.append(show.Name)
            show_rating.append(show.Rating)
            show_tags.append(show.Tags)
        theater_data = {
            "name": theater.Name,
            "place": theater.Place,
            "capacity": theater.Capacity,
            "show_name": show_name,
            "show_rating": show_rating,
            "show_tags": show_tags
        }
        data = pd.DataFrame(theater_data)

        export_folder = os.path.join(app.static_folder, "exports")
        os.makedirs(export_folder, exist_ok=True)
        csv_path = os.path.join(export_folder, "theater_data.csv")
        data.to_csv(csv_path, index=False)

        return send_from_directory(
            directory=export_folder,
            path="theater_data.csv",
            as_attachment=True,
            mimetype="text/csv",
        )


from .tasks import (
    create_analytics,
    create_plots,
    verify_activity,
    reminder_email,
    get_bookings_for_previous_month,
)
