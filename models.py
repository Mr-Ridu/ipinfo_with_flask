from app import db
from datetime import datetime

class VisitorIP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(100), unique=True, nullable=False)
    visit_time = db.Column(db.DateTime, default=datetime.utcnow)
    visit_count = db.Column(db.Integer, default=1)

    def increment_visit_count(self):
        self.visit_count += 1
        db.session.commit()
