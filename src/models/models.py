from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), default='Participant') # Admin, Organizer, Judge, Participant

class Contest(db.Model):
    __tablename__ = 'contests'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    theme = db.Column(db.Text)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='Upcoming') # Upcoming, Ongoing, Judging, Completed

class Submission(db.Model):
    """Lưu trữ tác phẩm dự thi và thông số máy phim (Metadata)"""
    __tablename__ = 'submissions'
    id = db.Column(db.Integer, primary_key=True)
    contest_id = db.Column(db.Integer, db.ForeignKey('contests.id'), nullable=False)
    participant_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Image Files
    image_url = db.Column(db.String(500), nullable=False)
    reference_url = db.Column(db.String(500)) # Ảnh cuộn phim/contact sheet (optional)
    
    # Analog Photography Metadata
    film_stock = db.Column(db.String(100))      # VD: Kodak Portra 400
    camera_body = db.Column(db.String(100))     # VD: Canon AE-1
    lens = db.Column(db.String(100))            # VD: Canon FD 50mm f/1.4
    iso = db.Column(db.Integer)                 # VD: 400
    film_format = db.Column(db.String(50))      # VD: 35mm, 120 (Medium Format)
    frame_number = db.Column(db.String(10))     # VD: 24A
    dev_lab = db.Column(db.String(100))         # Lab tráng rửa
    scan_specs = db.Column(db.String(100))      # Máy scan (VD: Noritsu, Frontier)
    
    # Status & AI Verification
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_ai_generated = db.Column(db.Boolean, default=False)  # AI flag
    status = db.Column(db.String(20), default='Pending')    # Pending, Verified, Rejected