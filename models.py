"""
Database models for the SafeLink Protection Cleaner application
"""
import datetime
from app import db

class EmailList(db.Model):
    """Model for uploaded email lists"""
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_count = db.Column(db.Integer, nullable=False)
    cleaned_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    processed = db.Column(db.Boolean, default=False)
    processing_time = db.Column(db.Float, default=0.0)
    
    # Relationships
    emails = db.relationship('Email', backref='email_list', lazy=True, cascade="all, delete-orphan")
    security_stats = db.relationship('SecurityStats', backref='email_list', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<EmailList {self.filename}>"

class Email(db.Model):
    """Model for individual email addresses"""
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255), nullable=False)
    domain = db.Column(db.String(255), nullable=False)
    valid = db.Column(db.Boolean, default=True)
    removed = db.Column(db.Boolean, default=False)
    reason = db.Column(db.String(255))
    security_system = db.Column(db.String(255))
    list_id = db.Column(db.Integer, db.ForeignKey('email_list.id'), nullable=False)
    
    def __repr__(self):
        return f"<Email {self.address}>"

class SecurityStats(db.Model):
    """Model for security system detection statistics"""
    id = db.Column(db.Integer, primary_key=True)
    security_system = db.Column(db.String(255), nullable=False)
    count = db.Column(db.Integer, default=0)
    list_id = db.Column(db.Integer, db.ForeignKey('email_list.id'), nullable=False)
    
    def __repr__(self):
        return f"<SecurityStats {self.security_system}: {self.count}>"

class ProcessingJob(db.Model):
    """Model for background processing jobs"""
    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey('email_list.id'), nullable=False)
    status = db.Column(db.String(50), default='queued')  # queued, processing, completed, failed
    progress = db.Column(db.Integer, default=0)
    started_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    error = db.Column(db.Text)
    
    def __repr__(self):
        return f"<ProcessingJob {self.id} - {self.status}>"
