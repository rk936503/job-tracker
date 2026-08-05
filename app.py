from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

from config import Config  # noqa: E402
from extensions import db, login_manager  # noqa: E402
from flask_migrate import Migrate     # noqa: E402
from models import JobApplication, User   # noqa: E402
from flask_login import login_user, logout_user, login_required  # noqa: E402


def create_app(config_overrides=None):
    app = Flask(__name__)
    app.config.from_object(Config)

    if config_overrides:
        app.config.update(config_overrides)

    db.init_app(app)
    Migrate(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    @app.route("/")
    @login_required
    def home():
        applications = JobApplication.query.order_by(JobApplication.date_applied.desc()).all()
        return render_template("home.html", applications=applications)

    @app.route("/add", methods=["GET", "POST"])
    @login_required
    def add_application():
        if request.method == "POST":
            new_app = JobApplication(
                company=request.form["company"],
                role=request.form["role"],
                status=request.form["status"],
                date_applied=datetime.strptime(request.form["date_applied"], "%Y-%m-%d").date(),
                notes=request.form.get("notes"),
                job_url=request.form.get("job_url")
            )
            db.session.add(new_app)
            db.session.commit()
            return redirect(url_for("home"))
        return render_template("add_application.html")

    @app.route("/edit/<int:app_id>", methods=["GET", "POST"])
    @login_required
    def edit_application(app_id):
        application = JobApplication.query.get_or_404(app_id)
        if request.method == "POST":
            application.company = request.form["company"]
            application.role = request.form["role"]
            application.status = request.form["status"]
            application.date_applied = datetime.strptime(request.form["date_applied"], "%Y-%m-%d").date()
            application.notes = request.form.get("notes")
            application.job_url = request.form.get("job_url")
            db.session.commit()
            flash("Application updated successfully!", "success")
            return redirect(url_for("home"))
        return render_template("edit_application.html", application=application)

    @app.route("/delete/<int:app_id>", methods=["POST"])
    @login_required
    def delete_application(app_id):
        application = JobApplication.query.get_or_404(app_id)
        db.session.delete(application)
        db.session.commit()
        flash("Application deleted.", "success")
        return redirect(url_for("home"))

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if User.query.first():
            flash("Registration is closed.", "danger")
            return redirect(url_for("login"))
        if request.method == "POST":
            user = User(username=request.form["username"])
            user.set_password(request.form["password"])
            db.session.add(user)
            db.session.commit()
            flash("Account created! Please log in.", "success")
            return redirect(url_for("login"))
        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            user = User.query.filter_by(username=request.form["username"]).first()
            if user and user.check_password(request.form["password"]):
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

    @app.route("/dashboard")
    @login_required
    def dashboard():
        statuses = ["Applied", "Interview", "Offer", "Rejected"]
        status_counts = {
            status: JobApplication.query.filter_by(status=status).count()
            for status in statuses
        }
        total = JobApplication.query.count()
        return render_template("dashboard.html", status_counts=status_counts, total=total)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
