from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

load_dotenv()

from config import Config
from extensions import db, login_manager
from flask_migrate import Migrate
from models import JobApplication, User
from flask_login import login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home():
    applications = JobApplication.query.order_by(JobApplication.date_applied.desc()).all()
    return render_template("home.html", applications=applications)

@app.route("/register", methods=["GET", "POST"])
def register():
    if User.query.first():
        flash("Registration is closed.", "danger")
        return redirect(url_for("login"))

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash("Account created! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash("Logged in successfully!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password.", "danger")

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.", "success")
    return redirect(url_for("login"))

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