from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

load_dotenv()

from config import Config
from extensions import db
from flask_migrate import Migrate
from models import JobApplication

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

@app.route("/")
def home():
    applications = JobApplication.query.order_by(JobApplication.date_applied.desc()).all()
    return render_template("home.html", applications=applications)

@app.route("/add", methods=["GET", "POST"])
def add_application():
    if request.method == "POST":
        new_app = JobApplication(
            company=request.form["company"],
            role=request.form["role"],
            status=request.form["status"],
            date_applied=request.form["date_applied"],
            notes=request.form.get("notes"),
            job_url=request.form.get("job_url")
        )
        db.session.add(new_app)
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("add_application.html")

@app.route("/edit/<int:app_id>", methods=["GET", "POST"])
def edit_application(app_id):
    application = JobApplication.query.get_or_404(app_id)

    if request.method == "POST":
        application.company = request.form["company"]
        application.role = request.form["role"]
        application.status = request.form["status"]
        application.date_applied = request.form["date_applied"]
        application.notes = request.form.get("notes")
        application.job_url = request.form.get("job_url")

        db.session.commit()
        flash("Application updated successfully!", "success")
        return redirect(url_for("home"))

    return render_template("edit_application.html", application=application)

@app.route("/delete/<int:app_id>", methods=["POST"])
def delete_application(app_id):
    application = JobApplication.query.get_or_404(app_id)
    db.session.delete(application)
    db.session.commit()
    flash("Application deleted.", "success")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])