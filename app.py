from flask import Flask, render_template
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
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])