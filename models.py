from extensions import db
from datetime import date

class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Applied")
    date_applied = db.Column(db.Date, nullable=False, default=date.today)
    notes = db.Column(db.Text, nullable=True)
    job_url = db.Column(db.String(300), nullable=True)

    def __repr__(self):
        return f"<JobApplication {self.company} - {self.role}>"