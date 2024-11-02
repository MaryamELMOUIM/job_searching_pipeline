from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    company = db.Column(db.String(200))
    location = db.Column(db.String(100))
    description = db.Column(db.Text)
    url = db.Column(db.String(200), unique=True)
    date_posted = db.Column(db.DateTime)
    status = db.Column(db.String(50), default="Not Applied")
    interview_date = db.Column(db.Date)  # For interview scheduling
    interview_status = db.Column(db.String(50))  # e.g., "Passed" or "Failed"
