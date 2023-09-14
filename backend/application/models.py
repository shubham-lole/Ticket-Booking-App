from .database import db
from datetime import datetime

roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer(), db.ForeignKey("user.UserID")),
    db.Column("role_id", db.Integer(), db.ForeignKey("role.id")),
)


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model):
    __tablename__ = "user"
    UserID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100))
    Email = db.Column(db.String(100))
    Password = db.Column(db.String(100))
    IsAdmin = db.Column(db.Boolean, default=False)
    last_visited = db.Column(db.DateTime, default=datetime.utcnow)
    Roles = db.relationship(
        "Role", secondary="roles_users", backref=db.backref("users", lazy="subquery")
    )


show_theater_association = db.Table(
    "show_theater_association",
    db.Column("ShowID", db.Integer, db.ForeignKey("show.ShowID"), primary_key=True),
    db.Column(
        "TheaterID", db.Integer, db.ForeignKey("theater.TheaterID"), primary_key=True
    ),
)


class Show(db.Model):
    __tablename__ = "show"
    ShowID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100))
    Rating = db.Column(db.String(100))
    Tags = db.Column(db.String(100))
    TicketPrice = db.Column(db.Float)
    theaters = db.relationship(
        "Theater",
        secondary=show_theater_association,
        backref=db.backref("shows", lazy="subquery", overlaps="shows"),
    )
    timings = db.relationship("ShowTiming", backref="show", lazy="subquery")


class Theater(db.Model):
    __tablename__ = "theater"
    TheaterID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100))
    Place = db.Column(db.String(100))
    Capacity = db.Column(db.Integer)

    timings = db.relationship("ShowTiming", backref="theater", lazy="subquery")


class ShowTiming(db.Model):
    __tablename__ = "show_timing"
    TimingID = db.Column(db.Integer, primary_key=True)
    ShowID = db.Column(db.Integer, db.ForeignKey("show.ShowID"))
    TheaterID = db.Column(db.Integer, db.ForeignKey("theater.TheaterID"))
    Timing = db.Column(db.DateTime)


class Booking(db.Model):
    __tablename__ = "booking"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.UserID"), nullable=False)
    show_timing_id = db.Column(
        db.Integer, db.ForeignKey("show_timing.TimingID"), nullable=False
    )
    num_tickets = db.Column(db.Integer, nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
